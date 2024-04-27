import os
from dotenv import load_dotenv
from telethon.tl import types

load_dotenv()

telegramAppId = int(os.environ.get('TELEGRAM_APP_ID'))
telegramAppHash = os.environ.get('TELEGRAM_APP_HASH')
dataDirectory = os.environ.get('APP_DATA_DIRECTORY') or 'data'
chatsToWatch = [int(idStr) for idStr in os.environ['APP_CHATS_TO_WATCH'].split(',')]
chatToOutput = eval(f'types.{os.environ['APP_CHAT_TO_OUTPUT']}')

print(f'Storing data at {os.path.abspath(dataDirectory)}')
