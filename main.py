import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from flask import Flask
import threading

# Load environment variables
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
source_channel = int(os.getenv("SOURCE_CHANNEL_ID"))
destination_channel = int(os.getenv("DESTINATION_CHANNEL_ID"))

# Initialize Telegram client with bot token
client = TelegramClient("session_name", api_id, api_hash)

# Flask web server to keep Render alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram media-forwarder bot is running."

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Start Flask in a background thread
threading.Thread(target=run_flask).start()

# Async function to handle media forwarding
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.media and (isinstance(event.media, MessageMediaPhoto) or isinstance(event.media, MessageMediaDocument)):
        try:
            await client.send_file(destination_channel, event.media)
            print(f"📤 Forwarded media message ID {event.id}")
        except Exception as e:
            print(f"❌ Failed to forward message ID {event.id}: {e}")

async def main():
    await client.start(bot_token=bot_token)
    print("✅ Bot started and listening...")
    await client.run_until_disconnected()

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
