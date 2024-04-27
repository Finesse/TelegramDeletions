# (in venv): python3 src/watch_deletions.py

import os
import asyncio
from telethon import events
from telethon.tl import types, custom
from client import make_client
from util import get_message_id, get_deleted_message_ids

messagesDirectory = 'data/messages'

chatsToWatch = [
    1000000000
]
chatToOutput = types.InputPeerChannel(channel_id=2000000000, access_hash=29075892034895839)

client = make_client()

@client.on(events.NewMessage(chats=chatsToWatch))
async def handle_new_message(event: events.NewMessage.Event):
    print('New message', event)
    message: custom.Message = event.message
    messageId = get_message_id(message)
    messageDirectory = f'{messagesDirectory}/{messageId}'
    os.makedirs(messageDirectory, exist_ok=True)

    with open(f'{messageDirectory}/event.txt', 'w') as file:
        file.write(str(event))
    with open(f'{messageDirectory}/message.txt', 'w') as file:
        file.write(message.message or '')

    if message.media is not None:
        await client.download_media(message.media, f'{messageDirectory}/media')

@client.on(events.MessageDeleted()) # Can't filter by chats here
async def handle_message_deleted(event: events.MessageDeleted.Event):
    print('Message deleted', event)

    # Waiting for the media, attached to the deleted message, to download just in case
    await asyncio.sleep(10)

    for messageId in get_deleted_message_ids(event):
        messageDirectory = f'{messagesDirectory}/{messageId}'
        if not os.path.exists(messageDirectory):
            print(f'Deleted message {messageId} was not saved. Most likely it is not from a watched chat.')
            continue

        with open(f'{messageDirectory}/message.txt', 'r') as file:
            message = file.read()

        await client.send_message(chatToOutput, f'Message #{messageId}:\n\n{message}')
        print(f'Posted the message {messageId} to the output chat')

        for filename in os.listdir(messageDirectory):
            if filename.startswith('media'):
                mediaPath = messageDirectory + '/' + filename
                await client.send_message(chatToOutput, f'An attachment to the message {messageId}', file=mediaPath)
                print(f'Posted the media of the message {messageId} to the output chat')
                break

client.start()
print('Ready')
client.run_until_disconnected()
