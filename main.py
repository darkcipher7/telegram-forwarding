import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest, ForwardMessagesRequest
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
source_channel = int(os.getenv("SOURCE_CHANNEL_ID"))
destination_channel = int(os.getenv("DESTINATION_CHANNEL_ID"))

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    print("🤖 Bot started successfully.")

    history = await client(GetHistoryRequest(
        peer=source_channel,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    messages = history.messages
    for message in reversed(messages):
        if message.media:
            await client(ForwardMessagesRequest(
                from_peer=source_channel,
                id=[message.id],
                to_peer=destination_channel
            ))
            print(f"📤 Forwarded media message ID {message.id}")
        await asyncio.sleep(1)

    print("✅ Finished forwarding.")

if __name__ == '__main__':
    asyncio.run(main())
