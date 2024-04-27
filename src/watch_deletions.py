import os
import asyncio
import json
from telethon import events
from telethon.tl import types, custom
from client import make_client
from util import get_message_id, get_deleted_message_ids, name_peer
from config import dataDirectory, chatsToWatch, chatToOutput

messagesDirectory = dataDirectory/'messages'
client = make_client()

@client.on(events.NewMessage(chats=chatsToWatch))
async def handle_new_message(event: events.NewMessage.Event):
    print('New message', event)
    message: custom.Message = event.message
    messageId = get_message_id(message)
    messageDirectory = messagesDirectory / messageId
    os.makedirs(messageDirectory, exist_ok=True)

    with (messageDirectory/'event.txt').open('w') as file:
        file.write(str(event))
    with (messageDirectory/'message.json').open('w') as file:
        json.dump({
            'localId': message.id,
            'chatName': name_peer(message.peer_id),
            'fromName': name_peer(message.from_id),
            'message': message.message or '',
        }, file, ensure_ascii=False)

    if message.media is not None:
        await client.download_media(message.media, str(messageDirectory/'media'))

@client.on(events.MessageDeleted()) # Can't filter by chats here
async def handle_message_deleted(event: events.MessageDeleted.Event):
    print('Message deleted', event)

    # Waiting for the media, attached to the deleted message, to download just in case
    await asyncio.sleep(10)

    for messageId in get_deleted_message_ids(event):
        messageDirectory = messagesDirectory/messageId
        if not os.path.exists(messageDirectory):
            print(f'Deleted message {messageId} was not saved. Most likely it is not from a watched chat.')
            continue

        with (messageDirectory/'message.json').open('r') as file:
            message = json.load(file)

        await client.send_message(
            chatToOutput,
            f'Message #{message['localId']} in {message['chatName']} from {message['fromName']}:\n\n{message['message']}',
        )
        print(f'Posted the message {messageId} to the output chat')

        for mediaPath in messageDirectory.glob('media*'):
            await client.send_message(
                chatToOutput,
                f'The attachment to the message #{message['localId']}',
                file=str(mediaPath),
            )
            print(f'Posted the media of the message {messageId} to the output chat')
            break

client.start()
print(f'Watching chats {', '.join(map(str, chatsToWatch))}')
print(f'Deleted messages will be posted to {chatToOutput}')
client.run_until_disconnected()
