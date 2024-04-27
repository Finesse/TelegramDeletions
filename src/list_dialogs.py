# (in venv): python3 src/list_dialogs.py

import asyncio
from client import make_client
from telethon.tl.custom import Dialog

async def main():
    client = make_client()
    async with client:
        async for dialog in client.iter_dialogs(100):
            dialog: Dialog
            print(dialog.name)
            print('\tChat id:', dialog.id)
            print('\tInput entity:', dialog.input_entity)

if __name__ == '__main__':
    asyncio.run(main())
