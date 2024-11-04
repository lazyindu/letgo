import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "")

API_HASH = os.environ.get("API_HASH", "")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

DB_NAME = os.environ.get("DB_NAME","")     

DB_URL = os.environ.get("DB_URL","")
 
FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]

PORT = os.environ.get("PORT", "8080")

MAX_BTN = int(os.environ.get('MAX_BTN', '5'))
PLAYERX_API_KEY = os.environ.get("PLAYERX_API_KEY")
STREAMWISH_API_KEY = os.environ.get("STREAMWISH_API_KEY")
VIDHIDE_API_KEY = os.environ.get("VIDHIDE_API_KEY")
STREAMWISH_WATCH_URL = os.environ.get("STREAMWISH_WATCH_URL","hlswish.com") #input only FQDN without https:// ✅
STREAMTAPE_API_PASS = os.environ.get("STREAMTAPE_API_PASS")
STREAMTAPE_API_USERNAME = os.environ.get("STREAMTAPE_API_USERNAME")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))
DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "./downloads")