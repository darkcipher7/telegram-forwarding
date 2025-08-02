import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
source_channel_id = int(os.getenv("SOURCE_CHANNEL_ID"))
destination_channel_id = int(os.getenv("DESTINATION_CHANNEL_ID"))

client = TelegramClient("bot", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    if event.media:
        await client.send_message(destination_channel_id, event.message)
        print(f"📤 Forwarded media message ID {event.id}")

async def main():
    await client.start(bot_token=bot_token)
    print("✅ Bot started and listening...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
