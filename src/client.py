from telethon import TelegramClient

# Get your own api_id and
# api_hash from https://my.telegram.org, under API Development. Or from https://tjhorner.dev/webogram/#/login
API_ID = 1000000
API_HASH = 'abababababababababababababababab'

def makeClient() -> TelegramClient:
    return TelegramClient('data/telegram', API_ID, API_HASH)
