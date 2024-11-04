from pyrogram import Client, filters, enums
# from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
       new_name = message.text 
       await message.delete() 
       msg = await client.get_messages(message.chat.id, reply_message.id)
       file = msg.reply_to_message
       media = getattr(file, file.media.value)
       await reply_message.delete()
       if not "." in new_name:
          if "." in media.file_name:
              extn = media.file_name.rsplit('.', 1)[-1]
          else:
              extn = "mkv"
          new_name = new_name + "." + extn

       button = [
            [
               InlineKeyboardButton("🔥 Upload to All Server 🔥",callback_data = "upload_allserver")
            ],
            [
               InlineKeyboardButton("👇 Below Are Seperate Servers 👇",callback_data = "selectserver")
            ],
            [
               InlineKeyboardButton("🚀 StreamTape",callback_data = "upload_streamtape"),
               InlineKeyboardButton("☢ StreamWish",callback_data = "upload_streamwish")
            ],
            [
               InlineKeyboardButton("▶ PlayerX",callback_data = "upload_playerx"),
               InlineKeyboardButton("🍟 VidHide",callback_data = "upload_vidhide")
            ],
            [
               InlineKeyboardButton("❌ Cancel upload 🗑",callback_data = "cancel")
            ]

           ]

       await message.reply_text(
          f"<b>Select the server to upload</b>\n<blockquote>📂 <b>File Name</b> :- <code>{new_name}</code></blockquote>",
          reply_to_message_id=file.id,
          reply_markup=InlineKeyboardMarkup(button), parse_mode=enums.ParseMode.HTML)
