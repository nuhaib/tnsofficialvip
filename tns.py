import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageEntityCustomEmoji

# Load API credentials from environment variables
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Initialize Telegram client
client = TelegramClient('emoji_session', api_id, api_hash)

async def get_premium_emoji_id():
    """Fetch the premium emoji IDs from recent messages."""
    await client.start()
    chat = "me"  # Fetch messages from your own Telegram saved messages
    messages = await client.get_messages(chat, limit=10)  # Fetch last 10 messages

    for msg in messages:
        if msg.entities:
            for entity in msg.entities:
                if isinstance(entity, MessageEntityCustomEmoji):
                    print(f"Premium Emoji ID: {entity.document_id}")

    await client.disconnect()

with client:
    client.loop.run_until_complete(get_premium_emoji_id())
