from os import environ, path

from pyrogram import Client

if path.exists("config.env"):
    print("Config File Exists.")
    from dotenv import load_dotenv

    load_dotenv("config.env")

TGAPI = int(environ["TGAPI"])
HASH = environ["HASH"]
BOT_TOKEN = environ["BOT_TOKEN"]
API = environ["API"]
CHANNEL = int(environ["CHANNEL"])

plugins = dict(root="bot/plugins")
bot = Client(
    "TelegramBot",
    api_id=TGAPI,
    api_hash=HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins,
)
