import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
DB_USER: str = os.getenv("DB_USER", "")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
DB_NAME: str = os.getenv("DB_NAME", "vpnbot")

KEY_BULGARIA: str = os.getenv("KEY_BULGARIA", "")
KEY_GEORGIA: str = os.getenv("KEY_GEORGIA", "")

SUPPORT_BOT_URL: str = os.getenv("SUPPORT_BOT_URL", "https://t.me/karasiqsupport_bot")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не вказано у файлі .env")

if not DB_USER or not DB_PASSWORD:
    raise ValueError("DB_USER та DB_PASSWORD не вказано у файлі .env")
