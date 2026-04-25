from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_URI = getenv("DB_URI")