import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect():
    DATABASE_URL = os.environ['DATABASE_URL']
    connection = psycopg2.connect(DATABASE_URL)
    return connection
