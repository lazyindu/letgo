import math
import aiohttp
from pyrogram import Client, filters, enums
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *
import asyncio
from helper.utils import initate_lazy_verification
user_files_data = {}
files_per_page = 10

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    _, offset = query.data.split("_")

    try:
        offset = int(offset)
    except:
        offset = 0
   
    chat_id = query.from_user.id    

    files, n_offset, total = await get_api_results(chat_id,  offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return

    # btn = [
    #     [
    #         InlineKeyboardButton(text=f"{file['title']}", url=file['link']),  # Use bracket notation
    #         InlineKeyboardButton(text=f"{file['file_code']}", callback_data='showdetails'),
    #     ]
    #     for file in files
    # ]
    display_text= ''
    for file in files:
        display_text += (
            f"<blockquote>"
            f"• <a href='{file['link']}'>{file['title']}</a> \n"
            f"<b>C🛞DE</b> : <code>{file['file_code']}</code>\n"
            f"</blockquote>"
            f"⍟───────────────────"
            
        )

    btn = []

    if 0 < offset <= int(MAX_BTN):
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - int(MAX_BTN)
    

    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⋞ ʙᴀᴄᴋ", callback_data=f"next_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
             InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data=f"next_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⋞ ʙᴀᴄᴋ", callback_data=f"next_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
                InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data=f"next_{n_offset}")
            ],
        )
    try:
        await query.edit_message_text(
            text=f"<blockquote>☢ Here are your Streamwish files.</blockquote>\n{display_text}",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_message(filters.command("load_all_streamws_file"))
async def load_all_streamws_file(client, message):
    user_id = message.from_user.id
    if not await initate_lazy_verification(client, message):
        return
        
    async with aiohttp.ClientSession() as session:
        list_api = f"https://api.streamwish.com/api/file/list?key={STREAMWISH_API_KEY}"
        try:
            async with session.get(list_api) as response:
                if response.status == 200:
                    json_data = await response.json()
                    files_data = json_data.get("result", {}).get("files", [])
                    user_files_data[user_id] = files_data

                    if files_data:
                        await display_files(message, user_id, offset=0)  # Display page 1
                    else:
                        await message.reply_text("No files found.")
                else:
                    await message.reply_text(f"Failed to load files. Status: {response.status}")
        except Exception as e:
            await message.reply_text(f"An error occurred: {str(e)}")

async def display_files(message, user_id, offset):
    files, offset, total_results = await get_api_results(message.chat.id , offset=0, filter=True)
    # btn = [
    #     [
    #         InlineKeyboardButton(text=f"{file['title']}", url=file['link']),  # Use bracket notation
    #         InlineKeyboardButton(text=f"{file['file_code']}", callback_data='showdetails'),
    #     ]
    #     for file in files
    #     ]
    display_text= ''
    for file in files:
        display_text += (
            f"<blockquote>"
            f"• <a href='{file['link']}'>{file['title']}</a> \n"
            f"<b>C🛞DE </b> : <code>{file['file_code']}</code>\n"
            f"</blockquote>"
            f"⍟───────────────────"
            
        )
    btn = []
    if offset != "":
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{math.ceil(int(total_results) / int(MAX_BTN))}", callback_data="pages"),
             InlineKeyboardButton(text="ɴᴇxᴛ ⋟", callback_data=f"next_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
        )
    # Send the initial message to be edited on pagination
    await message.reply_text(f"<blockquote>☢ Here are your Streamwish files.</blockquote>\n{display_text}", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True)

async def get_api_results(chat_id,  max_results=MAX_BTN, offset=0, filter=False):
    """For given query return (results, next_offset)"""
    user_id = chat_id
    files_data = user_files_data.get(user_id, [])
    total_results = len(files_data) 
    next_offset = offset + max_results

    # Slice the files list according to the offset and max_results
    files = files_data[offset:offset + max_results]
    if next_offset > total_results:
        next_offset = ''
    
    return files, next_offset, total_results
