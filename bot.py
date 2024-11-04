import logging
import logging.config

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
from pyrogram import  __version__
from pyrogram.raw.all import layer
import glob


from aiohttp import web
from plugins.web_support import web_server

import asyncio
from pyrogram import idle
from plugins import Lazydeveloper
from config import *
import importlib
import sys
from pathlib import Path

ppath = "plugins/*.py"
files = glob.glob(ppath)
PORT = "8080"
Lazydeveloper.start()
loop = asyncio.get_event_loop()

async def Lazy_start():
    print('\n')
    print('🍟 Initalizing Server Bot ')
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Lazy Imported => " + plugin_name)
    if not os.path.isdir(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    bot_info = await Lazydeveloper.get_me()
    Lazydeveloper.username = bot_info.username
    
    me = await Lazydeveloper.get_me()

    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(Lazy_start())
        logging.info('-----------------------🧐 Service running in Lazy Mode 😴-----------------------')
        logging.info('-----------------------🍟 Code Updated to run parallel 🍟-----------------------')
    except KeyboardInterrupt:
        logging.info('-----------------------😜 Service Stopped Sweetheart 😝-----------------------')
