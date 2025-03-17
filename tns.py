import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import MessageEntityCustomEmoji

# Configure logging (only logs errors to reduce RAM usage)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Load API credentials from environment variables
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

# Ensure credentials are set
if not api_id or not api_hash:
    raise ValueError("Missing API credentials. Set TELEGRAM_API_ID and TELEGRAM_API_HASH as environment variables.")

api_id = int(api_id)  # Convert API ID to integer

# Source & Target Channels (Script 3)
source_channel_script3 = [-1002168406093]  # Replace with actual source channel(s)
target_channels_script3 = [-1002133004108]  # Replace with actual target channels

# Premium emoji ID provided by the user
premium_emoji_id = 5370909405975953360  

# Initialize Telegram client
client = TelegramClient('script3_session', api_id, api_hash, flood_sleep_threshold=10)

@client.on(events.NewMessage(chats=source_channel_script3))
async def forward_messages(event):
    """Forward messages only to Script 3's assigned target channels."""
    msg = event.message
    text = msg.raw_text or ""
    media = msg.media if msg.media else None
    entities = msg.entities  # Preserve formatting
    buttons = msg.reply_markup  # Preserve buttons

    tasks = []
    for channel_id in target_channels_script3:
        tasks.append(send_message(channel_id, text, media, entities, buttons))

    await asyncio.gather(*tasks)

async def send_message(channel_id, text, media, entities, buttons):
    """Send messages while keeping formatting, media, and buttons intact, followed by a custom message with a premium emoji."""
    try:
        # Forward the original message
        sent_message = await client.send_message(
            entity=channel_id,
            message=text,
            file=media if media else None,
            link_preview=True,
            buttons=buttons,
            formatting_entities=entities
        )

        # Custom message with the premium emoji
        custom_message =  "REGISTER HERE :-http://in-rkwg.com/#/register?invitationCode=4G19522240 ⚡️"
        premium_entities = [MessageEntityCustomEmoji(offset=0, length=1, document_id=premium_emoji_id)]

        # Send the follow-up message with the premium emoji
        await client.send_message(channel_id, f"⭐{custom_message}", formatting_entities=premium_entities, reply_to=sent_message.id)

    except ChatAdminRequiredError:
        logger.error(f"Bot is not an admin in {channel_id}")
    except Exception as e:
        logger.error(f"Failed to send message to {channel_id}: {e}")

async def main():
    """Start the Telegram client."""
    print("Script 3 Forwarder is running...")
    await client.start()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
