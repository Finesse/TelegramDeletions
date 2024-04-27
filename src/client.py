from telethon import TelegramClient
from config import dataDirectory, telegramAppId, telegramAppHash

def make_client() -> TelegramClient:
    return TelegramClient(f'{dataDirectory}/telegram', telegramAppId, telegramAppHash)
