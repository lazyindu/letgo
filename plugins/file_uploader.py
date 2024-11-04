from helper.utils import progress_for_pyrogram
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery)
import os
import time
from config import *
import aiohttp
import asyncio
import uuid
from aiohttp import FormData
from helper.txt import lazyvars

      
@Client.on_callback_query(filters.regex("skiprename"))
async def skiprename(bot, update: CallbackQuery):
    try:
        file = update.message.reply_to_message
        # file_name = file.document.file_name if file.document else "Unnamed_file.mkv"
        # Check for the file type and get the file_name accordingly
        media = getattr(file, file.media.value, None)  # This will work for document, video, and audio
        file_name = media.file_name if media and hasattr(media, "file_name") else "Unnamed_file.mkv"
        lazy_filename = file_name.replace("_", " ")

        # Derive extension or set a default one
        # if "." in file_name:
        #     extn = file_name.rsplit('.', 1)[-1]
        # else:
        #     extn = "mkv"  # Default extension
        # new_name = file_name.rsplit('.', 1)[0] + "." + extn

        # Show server upload options without renaming
        buttons = [
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

        await update.message.edit_text(
            f"<b>Select the server to upload</b>\n<blockquote>📂 <b>File Name</b> :- <code>{lazy_filename}</code></blockquote>",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as lazyee :
        print(lazyee)

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update: CallbackQuery):
    try:
        user_id = update.message.chat.id
        date = update.message.date
        await update.message.delete()
        await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",
                                        reply_to_message_id=update.message.reply_to_message.id,
                                        reply_markup=ForceReply(True))

    except Exception as lazye:
        print(lazye)

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update: CallbackQuery):
    # Run each upload task independently
    asyncio.create_task(process_upload(bot, update))


async def process_upload(bot, update):
    type = update.data.split("_")[1]

    # setting up dynamic template for all server // Your Father @LazyDeveloper !
    if type == "streamtape":
        displaylazyserver = "🚀 StreamTape"
        displaylazyserver2 = "🚀 StreamTape"
    elif type == "streamwish":
        displaylazyserver = "☢ StreamWish"
        displaylazyserver2 = "☢ StreamWish"
    elif type == "vidhide":
        displaylazyserver = "🍟 VidHide"
        displaylazyserver2 = "🍟 VidHide"
    elif type == "playerx":
        displaylazyserver = "▶ Playerx"
        displaylazyserver2 = "▶ Playerx"
    elif type == "allserver":
        displaylazyserver = (
                            "<blockquote>    1) 🚀 StreamTape    </blockquote>\n"
                            "<blockquote>    2) ☢ StreamWish    </blockquote>\n"
                            "<blockquote>    3) 🍟 VidHide    </blockquote>\n"
                            "<blockquote>    4) ▶ PlayerX   </blockquote>"
                            )
            
        displaylazyserver2 = " '🚀 StreamTape' + '☢ StreamWish' + '🍟 VidHide' + '▶ PLayerX' "

    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    print(f'New FileNAme in process upload => {new_filename}')
    # Generate a unique directory and path for each file // Your father @LazyDeveloperr
    unique_id = str(uuid.uuid4())
    download_dir = f"downloads/{unique_id}"
    os.makedirs(download_dir, exist_ok=True)

    file_path = os.path.join(download_dir, new_filename)
    file = update.message.reply_to_message

    ms = await update.message.edit(f"<spoiler><b>⚙ Preparing to upload on {displaylazyserver}</b>\n\n<blockquote>📂 {new_filename} </blockquote></spoiler>",
                                   disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML)
    c_time = time.time()

    # Download the file
    try:
        path = await bot.download_media(
            message=file,
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=(
                f"<blockquote><b> {displaylazyserver2} </b></blockquote>\n<blockquote><b>📂 File Name:</b> {new_filename} </blockquote>\n", ms, c_time)
        )
    except Exception as e:
        await ms.edit(f"Download failed: {e}")
        return

    # Begin uploading to the specified server
    if type == "streamtape":
        await upload_to_streamtape(bot, update, path, displaylazyserver2, ms, new_filename)
    elif type == "streamwish":
        await upload_to_streamwish(bot, update, path, displaylazyserver2, ms, new_filename)
    elif type == "vidhide":
        await upload_to_vidhide(bot, update, path, displaylazyserver2, ms, new_filename)
    elif type == "playerx":
        await upload_to_playerx(bot, update, path, displaylazyserver2, ms, new_filename)
    elif type == "allserver":
        await upload_to_allserver(bot, update, path, displaylazyserver2, ms, new_filename)

    # Clean up the downloaded file after processing
    if os.path.exists(path):
        os.remove(path)


async def upload_to_streamtape(bot, update, path, server_name, ms, new_filename):
    data = update  # update is query here
    tempfilename = new_filename
    the_media = path

    lzm = await data.message.edit(
        text=f"<blockquote><b>{server_name}</b></blockquote>\n\n<b>Trying to upload file on StreamTape server !\n\n⏳ Please wait...</b>",
        parse_mode=enums.ParseMode.HTML
    )
    async with aiohttp.ClientSession() as session:
        try:
            Main_API = "https://api.streamtape.com/file/ul?login={}&key={}"
            hit_api = await session.get(Main_API.format(STREAMTAPE_API_USERNAME, STREAMTAPE_API_PASS))
            json_data = await hit_api.json()
            print(json_data)
            temp_api = json_data["result"]["url"]
            print(temp_api)
            files = {'file1': open(the_media, 'rb')}
            response = await session.post(temp_api, data=files)
            data_f = await response.json(content_type=None)
            status = data_f["status"]
            download_link = data_f["result"]["url"]
            # filename = the_media.split("/")[-1].replace("_", " ")

            await lzm.delete()
            if not int(status) == 200:
                await data.message.reply_to_message.reply_text(
                    "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request!", parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True)
                return
            else:
                await data.message.reply_to_message.reply_text(
                    f"<spoiler><blockquote><b> {server_name} </b></blockquote>\n<b>Uploaded on StreamTape server</b> ❤\n<blockquote><b>📂File Name:</b> {tempfilename} </blockquote></spoiler>",
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton(
                                "🚀 Upload Done", callback_data="uploaddone")]
                        ]
                    )
                )
                forwarded_msg = await data.message.reply_to_message.forward(LOG_CHANNEL)
                await bot.send_message(chat_id=LOG_CHANNEL,
                                       text=f"#STREAMTAPE_UPLOAD:\n\n[{data.from_user.first_name}](tg://user?id={data.from_user.id}) Uploaded to Streamtape !!\n\n**URL:** {download_link}",
                                       reply_to_message_id=forwarded_msg.id, parse_mode=enums.ParseMode.MARKDOWN,
                                       disable_web_page_preview=True)
        except Exception as lazy_err:
            print(
                f'❌ Something went wrong while uploading file to streamtape server : {lazy_err} ')


async def upload_to_streamwish(bot, update, path, server_name, ms, new_filename):
    data = update  # update is query here
    tempfilename = new_filename
    the_media = path

    lzm = await data.message.edit(
        text=f"<blockquote><b> {server_name} </b></blockquote>\n\n<b>Trying to upload file on StreamWish server !\n\n⏳ Please wait...</b>",
        parse_mode=enums.ParseMode.HTML
    )
    async with aiohttp.ClientSession() as session:
        try:
            # Get Streamwish upload URL
            Main_API = f"https://api.streamwish.com/api/upload/server?key={STREAMWISH_API_KEY}"
            async with session.get(Main_API) as hit_api:
                json_data = await hit_api.json()
                temp_api = json_data.get("result")
            # File upload preparation
            # filename = the_media.split("/")[-1].replace("_", " ")
            headers = {"Accept": "application/json"}
            files = {
                'file': open(the_media, 'rb'),
                'key': STREAMWISH_API_KEY,
                'html_redirect': '1'
            }
            async with session.post(temp_api, data=files, headers=headers) as upload_response:
                if upload_response.status != 200:
                    await data.message.reply_to_message.reply_text(
                        "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request!",
                        parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                    )
                    return

                # Extract download link
                # response_text = await upload_response.text()
                # file_code = re.search(r'<textarea name="fn">(.+?)</textarea>', response_text)
                # if file_code:
                #     file_id = file_code.group(1)
                #     watch_link = await generate_streamwish_watch_link(file_id)
                #     download_link = await generate_streamwish_download_link(session, file_id)
                # Clean up and respond
                # os.remove(the_media)

                await lzm.delete(True)
                await data.message.reply_to_message.reply_text(
                    f"<spoiler><blockquote><b> {server_name} </b></blockquote>\n<b>Uploaded on StreamWish server</b> ❤\n<blockquote><b>📂File Name:</b> {tempfilename} </blockquote></spoiler>",
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "☢ Upload Done", callback_data="uploaddone")]
                    ])
                )
                # Log the upload event
                forwarded_msg = await data.message.reply_to_message.forward(LOG_CHANNEL)
                await bot.send_message(
                    chat_id=LOG_CHANNEL,
                    text=f"#STREAMWISH_UPLOAD:\n\n[{data.from_user.first_name}](tg://user?id={data.from_user.id}) Uploaded to Streamwish !!",
                    reply_to_message_id=forwarded_msg.id,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
        except Exception as lazy_err:
            print(
                f"❌ Something went wrong while uploading file to streamwish server: {lazy_err}")


async def upload_to_vidhide(bot, update, path, server_name, ms, new_filename):
    data = update  # update is query here
    tempfilename = new_filename
    the_media = path

    lzm = await data.message.edit(
        text=f"<blockquote><b>{server_name} </b></blockquote>\n\n<b>Trying to upload file on VidHide server !\n\n⏳ Please wait...</b>",
        parse_mode=enums.ParseMode.HTML
    )

    async with aiohttp.ClientSession() as session:
        try:
            # Get VIDHIDE upload URL
            Main_API = f"https://vidhideapi.com/api/upload/server?key={VIDHIDE_API_KEY}"
            async with session.get(Main_API) as hit_api:
                json_data = await hit_api.json()
                temp_api = json_data.get("result")

            # File upload preparation
            # filename = the_media.split("/")[-1].replace("_", " ")
            headers = {"Accept": "application/json"}
            files = {
                'file': open(the_media, 'rb'),
                'key': VIDHIDE_API_KEY,
                'html_redirect': '1'
            }

            async with session.post(temp_api, data=files, headers=headers) as upload_response:
                if upload_response.status != 200:
                    await data.message.reply_to_message.reply_text(
                        "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request!",
                        parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                    )
                    return

                # Extract download link - i'm not deleting this - bcouse i know u r noob 😂 [ ur father on tg @LazyDeveloper ]

                # response_text = await upload_response.text()
                # file_code = re.search(r'<textarea name="fn">(.+?)</textarea>', response_text)
                # if file_code:
                #     file_id = file_code.group(1)
                #     # watch_link = await generate_streamwish_watch_link(file_id)
                #     download_link = await generate_vidhide_download_link(session, file_id)

                # Clean up and respond
                # os.remove(the_media)
                await lzm.delete()
                await data.message.reply_to_message.reply_text(
                    f"<spoiler><blockquote><b> {server_name} </b></blockquote>\n<b>Uploaded on VidHide server</b> ❤\n<blockquote><b>📂File Name:</b> {tempfilename} </blockquote></spoiler>",
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "🍟 Upload Done", callback_data="uploaddone")]
                    ])
                )

                # Log the upload event
                forwarded_msg = await data.message.reply_to_message.forward(LOG_CHANNEL)
                await bot.send_message(
                    chat_id=LOG_CHANNEL,
                    text=f"#VidHIDE_UPLOAD:\n\n[{data.from_user.first_name}](tg://user?id={data.from_user.id}) Uploaded to vidhide !!",
                    reply_to_message_id=forwarded_msg.id,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
        except Exception as lazy:
            print(
                f"❌ Something went wrong while uploading file to vidhide: {lazy}")


async def upload_to_playerx(bot, update, path, server_name, ms, new_filename):
    data = update  # update is query here
    tempfilename = new_filename
    the_media = path

    lzm = await data.message.edit(
        text=f"<blockquote><b> {server_name} </b></blockquote>\n\n<b>Trying to upload file on Playerx server !\n\n⏳ Please wait...</b>",
        parse_mode=enums.ParseMode.HTML
    )

    # Prepare FormData with file for upload
    lazydeveloper_datas = FormData()
    lazydeveloper_datas.add_field('files[]', open(
        the_media, 'rb'), filename=tempfilename)
    lazydeveloper_datas.add_field('api_key', PLAYERX_API_KEY)
    lazydeveloper_datas.add_field('action', 'upload_video')
    # This should be '0' or '1' depending on your preference
    lazydeveloper_datas.add_field('raw', '1')

    async with aiohttp.ClientSession() as session:
        try:
            server_lazy_url = "https://www.playerx.stream/api.php"
            async with session.post(server_lazy_url, data=lazydeveloper_datas) as response:
                response_data = await response.json()
                print(response_data)
                if response_data.get('status') != 'success':
                    await data.message.reply_to_message.reply_text(
                        "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request => Playerx!",
                        parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                    )
                    return

                await lzm.delete(True)
                await data.message.reply_to_message.reply_text(
                    f"<spoiler><blockquote><b> {server_name} </b></blockquote>\n<b>Uploaded on Playerx server</b> ❤\n<blockquote><b>📂File Name:</b> {tempfilename} </blockquote></spoiler>",
                    parse_mode=enums.ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "▶ Upload Done", callback_data="uploaddone")]
                    ])
                )

                # Log the upload event
                forwarded_msg = await data.message.reply_to_message.forward(LOG_CHANNEL)
                await bot.send_message(
                    chat_id=LOG_CHANNEL,
                    text=f"#PLAYERX_UPLOAD:\n\n[{data.from_user.first_name}](tg://user?id={data.from_user.id}) Uploaded to Playerx !!",
                    reply_to_message_id=forwarded_msg.id,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
        except Exception as e:
            print(
                f"something went wrong while uploading file to Playerx : {e}")


async def upload_to_allserver(bot, update, path, server_name, ms, new_filename):
    data = update  # update is query here
    tempfilename = new_filename
    the_media = path

    lzm = await data.message.edit(
        text=(
            f"<blockquote><b>{server_name} </b></blockquote>\n\n"
            "<b>Trying to upload file on Streamtape, Streamwish, Vidhide and PlayerX server!\n\n⏳ Please wait...</b>"
        ),
        parse_mode=enums.ParseMode.HTML
    )
    async with aiohttp.ClientSession() as session:
        # initiating upload on streamtape
        lazy_ms = await lzm.edit(
            text=(
                "<b>[ 🚀 StreamTape</b> => <i>⚙ Processing...</i>\n"
                "<b>[ ☢ StreamWish</b> => <i>💤 in queue...</i>\n"
                "<b>[ 🍟 VidHide </b> =>>>> <i>💤 in queue...</i>\n"
                "<b>[ ▶ PlayerX </b> =>>>> <i>💤 in queue...</i>\n\n"
                f"<blockquote><b>📂File Name</b>: {tempfilename}</blockquote>"),
            parse_mode=enums.ParseMode.HTML
        )
        Main_API = "https://api.streamtape.com/file/ul?login={}&key={}"
        hit_api = await session.get(Main_API.format(STREAMTAPE_API_USERNAME, STREAMTAPE_API_PASS))
        json_data = await hit_api.json()
        temp_api = json_data["result"]["url"]
        files = {'file1': open(the_media, 'rb')}
        async with session.post(temp_api, data=files) as streamtape_response:
            if streamtape_response.status != 200:
                await data.message.reply_to_message.reply_text(
                    "Something Went Wrong!\n\n**Error:** Server Didn't Accept request => streamtape!",
                    parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                )
                return
        #  ./uploaded on streamtape ✅

         # initiating upload on Streamwish
        lazy_mt = await lazy_ms.edit(
            text=(
                "<b>[ 🚀 StreamTape</b> => <i>✅ Upload Done</i>\n"
                "<b>[ ☢ StreamWish</b> => <i>⚙ Processing...</i>\n"
                "<b>[ 🍟 VidHide </b> =>>>> <i>💤 in queue...</i>\n"
                "<b>[ ▶ PlayerX </b> =>>>> <i>💤 in queue...</i>\n\n"
                f"<blockquote><b>📂File Name</b>: {tempfilename}</blockquote>"
            ),
            parse_mode=enums.ParseMode.HTML
        )

        # Get Streamwish upload URL
        Main_API = f"https://api.streamwish.com/api/upload/server?key={STREAMWISH_API_KEY}"
        async with session.get(Main_API) as hit_api:
            json_data = await hit_api.json()
            temp_api = json_data.get("result")

         # File upload preparation
        # filename = the_media.split("/")[-1].replace("_", " ")
        headers = {"Accept": "application/json"}
        files = {
            'file': open(the_media, 'rb'),
            'key': STREAMWISH_API_KEY,
            'html_redirect': '1'
        }

        async with session.post(temp_api, data=files, headers=headers) as streamwish_response:
            if streamwish_response.status != 200:
                await data.message.reply_to_message.reply_text(
                    "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request => Streamwish!",
                    parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                )
                return
        # ./ uploaded on Streamwish ✅

        # initiating upload on Vidhide
        lazy_mu = await lazy_mt.edit(
            text=(
                "<b>[ 🚀 StreamTape</b> => <i>✅ Upload Done</i>\n"
                "<b>[ ☢ StreamWish</b> => <i>✅ Upload Done</i>\n"
                "<b>[ 🍟 VidHide </b> =>>>> <i>⚙ Processing...</i>\n"
                "<b>[ ▶ PlayerX </b> =>>>> <i>💤 in queue...</i>\n\n"
                f"<blockquote><b>📂File Name</b>: {tempfilename}</blockquote>"
            ),
            parse_mode=enums.ParseMode.HTML
        )

        # Get VIDHIDE upload URL
        Main_API = f"https://vidhideapi.com/api/upload/server?key={VIDHIDE_API_KEY}"
        async with session.get(Main_API) as hit_api:
            json_data = await hit_api.json()
            temp_api = json_data.get("result")

            # File upload preparation
        # filename = the_media.split("/")[-1].replace("_", " ")
        headers = {"Accept": "application/json"}
        files = {
            'file': open(the_media, 'rb'),
            'key': VIDHIDE_API_KEY,
            'html_redirect': '1'
        }

        async with session.post(temp_api, data=files, headers=headers) as vidhide_response:
            if vidhide_response.status != 200:
                await data.message.reply_to_message.reply_text(
                    "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request => vidhide !",
                    parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                )
                return
        #  uploaded on vidhide ✅ [ its 30th October - Night 02:49'am = working late night ! #LazyDeveloperr 🥱]

        # initiating upload on PlayerX
        lazy_mv = await lazy_mu.edit(
            text=(
                "<b>[ 🚀 StreamTape</b> => <i>✅ Upload Done</i>\n"
                "<b>[ ☢ StreamWish</b> => <i>✅ Upload Done</i>\n"
                "<b>[ 🍟 VidHide </b> =>>>> <i>✅ Upload Done</i>\n"
                "<b>[ ▶ PlayerX </b> =>>>> <i>⚙ Processing...</i>\n\n"
                f"<blockquote><b>📂File Name</b>: {tempfilename}</blockquote>"
            ),
            parse_mode=enums.ParseMode.HTML
        )
        # ./ uploaded on Vidhide

        # Prepare FormData with file for upload
        lazydeveloper_datas = FormData()
        lazydeveloper_datas.add_field('files[]', open(
            the_media, 'rb'), filename=tempfilename)
        lazydeveloper_datas.add_field('api_key', PLAYERX_API_KEY)
        lazydeveloper_datas.add_field('action', 'upload_video')
        # This should be '0' or '1' depending on your preference
        lazydeveloper_datas.add_field('raw', '1')

        # File upload preparation

        server_lazy_url = "https://www.playerx.stream/api.php"
        async with session.post(server_lazy_url, data=lazydeveloper_datas) as lazy_response:
            response_data = await lazy_response.json()
            print(response_data)
            if response_data.get('status') != 'success':
                await data.message.reply_to_message.reply_text(
                    "Something Went Wrong!\n\n**Error:** Server Didn't Accept My Request => PlayerX !",
                    parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True
                )
                return
        #  uploaded on PLayerx
        await lazy_mv.edit(
            text=(
                "<spoiler>"
                "<b>[ 🚀 StreamTape</b> => <i>✅ Upload Done</i>\n"
                "<b>[ ☢ StreamWish</b> => <i>✅ Upload Done</i>\n"
                "<b>[ 🍟 VidHide </b> =>>>> <i>✅ Upload Done</i>\n"
                "<b>[ ▶ PlayerX </b> =>>>> <i>✅ Upload Done</i>\n\n"
                f"<blockquote><b>📂File Name</b>: {tempfilename}</blockquote></spoiler>"
            ),
            parse_mode=enums.ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(
                            "🔥 Upload Done ", callback_data="uploaddone")]
                    ])
            )
        # Log the upload event
        forwarded_msg = await data.message.reply_to_message.forward(LOG_CHANNEL)
        await bot.send_message(
            chat_id=LOG_CHANNEL,
            text=f"<blockquote>#{server_name}</blockquote> <a href='tg://user?id={data.from_user.id}'>{data.from_user.first_name}</a> Uploaded to Playerx !!",
            reply_to_message_id=forwarded_msg.id,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )


@Client.on_callback_query()
async def lazycall(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=f"👋 Hello {query.from_user.mention} \n\nI am an Advance server uploader BOT with custom filename support.\n\n<blockquote>Send me any video or document !</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                InlineKeyboardButton('⚡️ About', callback_data='about'),
                InlineKeyboardButton('🤕 Help', callback_data='help')
                ],
                [
                InlineKeyboardButton("🦋 About Developer 🦋", callback_data='dev')
                ]
                ]),
                parse_mode=enums.ParseMode.HTML
        )
    
    elif data == "help":
        await query.message.edit_text(
            text=lazyvars.HELP_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton("👑 Contact Admin 👑", url="https://t.me/zonflix")
               ],[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    
    elif data == "about":
        await query.message.edit_text(
            text=lazyvars.ABOUT_TXT.format(client.mention),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup( [[
               InlineKeyboardButton("👑 Contact Admin 👑", url="https://t.me/zonflix")
               ],[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    
    elif data == "dev":
        await query.message.edit_text(
            text=lazyvars.DEV_TXT,
            reply_markup=InlineKeyboardMarkup( [[
               #⚠️ don't change source code & source link ⚠️ #
               InlineKeyboardButton("🦋 Contact Developer 🦋", url="https://t.me/LazyDeveloperr")
               ],[
               InlineKeyboardButton("🔒 𝙲𝙻𝙾𝚂𝙴", callback_data = "close"),
               InlineKeyboardButton("◀️ 𝙱𝙰𝙲𝙺", callback_data = "start")
               ]]
            )
        )
    
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()
    
    elif data == "uploaddone":
        await query.message.delete() 

    elif data == "selectserver":
        await query.answer("🥱 Please select your desired server from below to upload", show_alert=True)
    
    elif data == "cancel":
        try:
            await query.message.delete()
        except:
            return
    
    elif data == "pages":
        await query.answer("This is page button 😅", show_alert=True)
