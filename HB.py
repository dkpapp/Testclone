import asyncio
from datetime import datetime
from pyrogram import Client, filters

# Configuration
API_ID = 1234567  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API hash

bots = []  # List to store cloned bot instances

app = Client("main_bot", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.reply_text(f"Welcome, {message.from_user.mention}! It's currently {current_time}.")

@app.on_message(filters.command("clone", reply_to_message=True))
async def clone(client, message):
    if message.reply_to_message.text.startswith("Bot Token: "):
        bot_token = message.reply_to_message.text.split(":", 1)[1].strip()

        cloned_bot = Client("cloned_bot" + str(len(bots)), api_id=API_ID, api_hash=API_HASH, bot_token=bot_token)
        bots.append(cloned_bot)

        try:
            await cloned_bot.start()
            await message.reply_text("Bot cloned successfully!")
        except Exception as e:
            await message.reply_text("Error cloning bot: " + str(e))

@app.on_message(filters.command("clones"))
async def get_clones(client, message):
    await message.reply_text(f"Total cloned bots: {len(bots)}")

async def main():
    await app.start()
    await asyncio.gather(*[bot.run() for bot in bots])

if __name__ == "__main__":
    asyncio.run(main())
