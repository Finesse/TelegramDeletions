# (in venv): python3 src/list_dialogs.py

import asyncio
from client import makeClient
from telethon.tl.custom import Dialog

async def main():
    client = makeClient()
    async with client:
        async for dialog in client.iter_dialogs(100):
            dialog: Dialog
            print(dialog.name)
            print('\tId:', dialog.id)
            print('\tInput entity:', dialog.input_entity)

if __name__ == '__main__':
    asyncio.run(main())
