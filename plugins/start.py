from asyncio import sleep
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram.errors import FloodWait
import humanize
from config import START_PIC, FLOOD, ADMIN 
from helper.utils import initate_lazy_verification



@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user           
    txt=f"👋 Hello {user.mention} \n\nI am an Advance server uploader BOT with custom filename support.\n\n<blockquote>Send me any video or document !</blockquote>"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton('⚡️ About', callback_data='about'),
        InlineKeyboardButton('🤕 Help', callback_data='help')
        ],
        [
        InlineKeyboardButton("🐱‍👤 About Developer 🐱‍👤", callback_data='dev')
        ]
        ])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button, parse_mode=enums.ParseMode.HTML)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)
    
@Client.on_message(filters.command('logs') & filters.user(ADMIN))
async def log_file(client, message):
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply_text(f"Error:\n`{e}`")

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    try:
        if not await initate_lazy_verification(client, message):
            return
        file = getattr(message, message.media.value)
        filename = file.file_name
        lazy_filename = filename.replace("_", " ")

        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        try:
            text = f"""**Do u really want to upload this file.... **\n\n**File Name** :- `{lazy_filename}`\n\n**File Size** :- `{filesize}`"""
            buttons = [[ 
                        InlineKeyboardButton("📃 Rename", callback_data="rename"),
                        InlineKeyboardButton("🚀 Skip Rename ", callback_data="skiprename")
                        ],
                    [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
            await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
            await sleep(FLOOD)
        except FloodWait as e:
            await sleep(e.value)
            text = f"""**Do u really want to upload this file.... **\n\n**File Name** :- `{lazy_filename}`\n\n**File Size** :- `{filesize}`"""
            buttons = [[ 
                        InlineKeyboardButton("📃 Rename", callback_data="rename"),
                        InlineKeyboardButton("🚀 Skip Rename ", callback_data="skiprename")
                        ],
                        [ InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="cancel") ]]
            await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
            # InlineKeyboardButton("🚀 Skip Rename ", callback_data="skiprename")
    except Exception as lazyerror:
        print(lazyerror)

