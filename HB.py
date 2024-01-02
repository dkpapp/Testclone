import asyncio
import math
import os
import time
import json
from datetime import datetime
from pyrogram import Client, filters, idle
import logging
from umongo import Instance, Document, fields
import motor
import shutil
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("Botlog.txt", mode="w"),
        logging.StreamHandler(),
    ],
    datefmt="%d/%b/%Y | %H:%M:%S %p",
)
logging.getLogger("pyromodz").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logit = logger.info
# Configuration
API_ID = 14604313  # Replace with your API ID
API_HASH = "a8ee65e5057b3f05cf9f28b71667203a"  # Replace with your API hash
TOKEN = "1612398731:AAH6nKToUUeO9DHsKXFsvRnAn6dFJJ3sQtM"
bots = []  # List to store cloned bot instances
class Translation:
    STATUS_TXT = """<b>᚛› 𝚃𝙾𝚃𝙰𝙻 𝙵𝙸𝙻𝙴𝚂: <code>{}</code></b>
<b>᚛› 𝚃𝙾𝚃𝙰𝙻 𝚄𝚂𝙴𝚁𝚂: <code>{}</code></b>
<b>᚛› 𝚃𝙾𝚃𝙰𝙻 𝙲𝙷𝙰𝚃𝚂: <code>{}</code></b>
<b>᚛› 𝚄𝚂𝙴𝙳 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝙱</b>
<b>᚛› 𝙵𝚁𝙴𝙴 𝚂𝚃𝙾𝚁𝙰𝙶𝙴: <code>{}</code> 𝙼𝙱</b>"""

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
  if not size:
    return ""
  power = 2**10
  n = 0
  Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
  while size > power:
    size /= power
    n += 1
  return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'
def get_size(size):
      units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
      size = float(size)
      i = 0
      while size >= 1024.0 and i < len(units):
          i += 1
          size /= 1024.0
      return "%.2f %s" % (size, units[i])

app = Client("main_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    current_time = datetime.now().strftime("%H:%M:%S")
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    await message.reply_text(f"Welcome, {message.from_user.mention}! It's currently {current_time}.")

@app.on_message(filters.command("clone"))
async def clone(client, message):
    
        bot_token = message.text.split(" ")[1].strip()

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

@app.on_message(filters.command("mongo"))
async def start(client, message):
     dburl = message.text.split(" ")[1]
     dbname = message.text.split(" ")[2]
     COLLECTION_NAME = message.text.split(" ")[3]
     rju = await message.reply('<b>Processing🔰...</b>')
     try:
        mongo = motor.motor_asyncio.AsyncIOMotorClient(dburl)
        db = mongo[dbname]
        col = db.users
        grp = db.groups
        sizes = await db.command("dbstats")['dataSize']
     except Exception as e:
           await rju.edit(f"Error **{e}**")
     instance = Instance.from_db(db)
     @instance.register
     class Media(Document):
          file_id = fields.StrField(attribute='_id')
          file_ref = fields.StrField(allow_none=True)
          file_name = fields.StrField(required=True)
          file_size = fields.IntField(required=True)
          file_type = fields.StrField(allow_none=True)
          mime_type = fields.StrField(allow_none=True)
          caption = fields.StrField(allow_none=True)
          class Meta:
              collection_name = COLLECTION_NAME
     files = await Media.count_documents()
     size = get_size(sizes)
     free = 536870912 - size
     free = get_size(free)
     total_users = await col.count_documents({})
     totl_chats = await grp.count_documents({})
     await rju.edit(Translation.STATUS_TXT.format(files, total_users, totl_chats, size, free))

async def main():
    
    await app.start()
    logit("Hello Master Dhruv 🥳")
    await idle()
    await asyncio.gather(*[bot.run() for bot in bots])
    
if __name__ == "__main__":
    asyncio.run(main())
