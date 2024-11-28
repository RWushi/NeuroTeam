from dotenv import load_dotenv
import os
from fastapi import FastAPI
from openai import AsyncOpenAI
import asyncpg

load_dotenv()

app = FastAPI()

client_oai = AsyncOpenAI(api_key=os.getenv('OPENAI_KEY'))

access_token = os.getenv('ACCESS_TOKEN')
instagram_id = os.getenv('INSTAGRAM_ID')
url = f"https://graph.facebook.com/v21.0/{instagram_id}/messages"

DATABASE_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'port': os.getenv("DB_PORT")}

class DB:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(**DATABASE_CONFIG)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()
