# (in venv): python3 src/watch_deletions.py

import os
import asyncio
from telethon import events
from telethon.tl import types, custom
from client import makeClient

messagesDirectory = 'data/messages'

chatsToWatch = [
    1000000000
]
chatToOutput = types.InputPeerChannel(channel_id=2000000000, access_hash=29075892034895839)

client = makeClient()

@client.on(events.NewMessage(chats=chatsToWatch))
async def handleNewMessage(event: events.NewMessage.Event):
    print('New message', event)
    message: custom.Message = event.message
    messageDirectory = messagesDirectory + '/' + str(message.id)
    os.makedirs(messageDirectory, exist_ok=True)

    with open(messageDirectory + '/event.txt', 'w') as file:
        file.write(str(event))
    with open(messageDirectory + '/message.txt', 'w') as file:
        file.write(message.message or '')

    if message.media is not None:
        await client.download_media(message.media, messageDirectory + '/media')

@client.on(events.MessageDeleted()) # Can't filter by chats here
async def handleMessageDeleted(event: events.MessageDeleted.Event):
    print('Message deleted', event)

    # Waiting for the media, attached to the deleted message, to download just in case
    await asyncio.sleep(10)

    for messageId in event.deleted_ids:
        messageDirectory = messagesDirectory + '/' + str(messageId)
        if not os.path.exists(messageDirectory):
            print('Message ' + str(messageId) + ' was not saved')
            continue

        with open(messageDirectory + '/message.txt', 'r') as file:
            message = file.read()

        await client.send_message(chatToOutput, 'Message #' + str(messageId) + ':\n\n' + message)
        print('Reported message ' + str(messageId))

        for filename in os.listdir(messageDirectory):
            if filename.startswith('media'):
                mediaPath = messageDirectory + '/' + filename
                await client.send_message(chatToOutput, 'An attachment to the message ' + str(messageId), file=mediaPath)
                print('Reported the media of the message ' + str(messageId))
                break

client.start()
client.run_until_disconnected()
