# (in venv): python3 src/get_deleted.py

import asyncio
from telethon.tl.types import InputChannel, PeerChannel, Channel
from telethon.tl.custom import AdminLogEvent
import time
from client import makeClient

GROUP_CHAT_ID = -1001693102452 # Чат Tinkoff CTF

async def main():
    client = makeClient()
    async with client:
        group = await client.get_entity(PeerChannel(GROUP_CHAT_ID))

        #messages = client.get_admin_log(group)

        file1 = open('data/dump.json', 'w')
        c = 0
        m = 0
        async for event in client.iter_admin_log(group):
            event: AdminLogEvent
            if event.deleted_message:
                print('Dumping message', c, '(', event.old.id, event.old.date, ')')
                file1.write(event.old.to_json() + ',')
                c += 1
                if event.old.media:
                    m += 1
                    #print(event.old.media.to_dict()['Document']['id'])
                    await client.download_media(event.old.media, 'data/' + str(event.old.id))
                    print(' Dumped media', m)
                await asyncio.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(main())
