from typing import List, Optional
from telethon import events
from telethon.tl import types, custom

def get_message_id(message: custom.Message) -> str:
    return get_raw_message_id(
        # Channel message ids are scoped to the channels, so we need to prefix them
        message.peer_id.channel_id if type(message.peer_id) == types.PeerChannel else None,
        message.id
    )

def get_deleted_message_ids(event: events.MessageDeleted.Event) -> List[str]:
    # Channel message ids are scoped to the channels, so we need to prefix them
    channelId = (
        event.original_update.channel_id
        if type(event.original_update) == types.UpdateDeleteChannelMessages else
        None
    )
    return [get_raw_message_id(channelId, messageId) for messageId in event.deleted_ids]

def get_raw_message_id(channelId: Optional[int], messageId: int) -> str:
    return f'{messageId}' if channelId is None else f'{channelId}_{messageId}'
