import os
from dotenv import load_dotenv


load_dotenv()

CURRENCIES_DB_PATH = os.getenv("CURRENCIES_DB_PATH")
EXCHANGE_RATES_DB_PATH = os.getenv("EXCHANGE_RATES_DB_PATH")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
FILE_LOG = os.getenv("FILE_LOG")