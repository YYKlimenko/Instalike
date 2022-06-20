import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_LOGIN = os.getenv('DATABASE_LOGIN')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
