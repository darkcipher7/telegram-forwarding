import asyncio
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread

# === Telegram API credentials ===
api_id = 29291225
api_hash = '2d38616fcd9fad440261b9a155350a7b'

# === Channel Information ===
source_channel = -1002860581357  # 🔁 Replace this
target_channel = -1002819316162  # 🔁 Replace this

client = TelegramClient('session', api_id, api_hash)

# === Flask App for Keep-Alive ===
app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Telegram Forwarder is running!'

@app.route('/health')
def health():
    return '✅ OK', 200

# === Start Flask in Background ===
def run_flask():
    app.run(host='0.0.0.0', port=10000)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.message.media:
        try:
            await client.forward_messages(target_channel, event.message)
            print(f"✅ Forwarded message ID: {event.message.id}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    await client.start()
    print("🚀 Bot started and listening...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(main())
