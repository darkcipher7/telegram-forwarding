import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaDocument
from dotenv import load_dotenv
from flask import Flask

# === Load .env variables ===
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
source_channel = int(os.getenv("SOURCE_CHANNEL_ID"))
destination_channel = int(os.getenv("DESTINATION_CHANNEL_ID"))
session_name = os.getenv("SESSION_NAME")  # e.g., "session_name" (no .session)

client = TelegramClient(session_name, api_id, api_hash)

# === Flask server (to keep service alive) ===
app = Flask(__name__)

@app.route('/')
def home():
    return 'OK'  # Keep this lightweight for uptime pings

# === Telegram event handler ===
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    message = event.message
    if message.media and isinstance(message.media, MessageMediaDocument):
        try:
            await client.forward_messages(destination_channel, message.id, message.peer_id)
            print(f"📤 Forwarded media message ID {message.id}", flush=True)
        except FloodWaitError as e:
            print(f"⏳ Sleeping {e.seconds}s due to rate limit...", flush=True)
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ Error forwarding message ID {message.id}: {e}", flush=True)

# === Start both Flask + Telegram bot together ===
async def main():
    await client.start()
    print("✅ Logged in successfully", flush=True)
    print("🤖 Waiting for new media...", flush=True)
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.create_task(main())
    app.run(host='0.0.0.0', port=1000)
