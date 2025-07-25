import os
from dotenv import load_dotenv


load_dotenv()

DB_PATH = os.getenv("DB_PATH")
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
FILE_LOG = os.getenv("FILE_LOG")