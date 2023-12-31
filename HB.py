import asyncio
from datetime import datetime
from pyromodz import Client, filters

# Configuration
API_ID = 14604313  # Replace with your API ID
API_HASH = "a8ee65e5057b3f05cf9f28b71667203a"  # Replace with your API hash
TOKEN = "6155002509:AAFsGEZh95aE6Jag-n2o7l6rwuDMvf4SiWg"
bots = []  # List to store cloned bot instances

app = Client("main_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    current_time = datetime.now().strftime("%H:%M:%S")
    await message.reply_text(f"Welcome, {message.from_user.mention}! It's currently {current_time}.")

@app.on_message(filters.command("clone"))
async def clone(client, message):
    
        bot_token = message.text.split(" ")[1].strip()

        cloned_bot = Client("cloned_bot" + str(len(bots)), api_id=API_ID, api_hash=API_HASH, bot_token=bot_token)
        bots.append(cloned_bot)

        try:
            await cloned_bot.run()
            await message.reply_text("Bot cloned successfully!")
        except Exception as e:
            await message.reply_text("Error cloning bot: " + str(e))

@app.on_message(filters.command("clones"))
async def get_clones(client, message):
    await message.reply_text(f"Total cloned bots: {len(bots)}")

async def main():
    await app.run()
    await idle()
    await asyncio.gather(*[bot.run() for bot in bots])

if __name__ == "__main__":
    asyncio.run(main())
