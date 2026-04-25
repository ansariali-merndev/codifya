from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_URI = getenv("DB_URI")
GMAIL_PASS = getenv("GMAIL_PASS")
GMAIL_USER = getenv("GMAIL_USER")
