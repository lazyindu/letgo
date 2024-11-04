import logging
import logging.config
from pyrogram import Client 
from config import API_ID, API_HASH, BOT_TOKEN

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Lazydeveloperr(Client):

    def __init__(self):
        super().__init__(
            name="serveruploader",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def stop(self, *args):
      await super().stop()      
      logging.info("Bot Stopped 🙄 - \nContact @LazyDeveloper on telegram for any query")
        
Lazydeveloper = Lazydeveloperr()
