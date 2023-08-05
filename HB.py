import re
import time
import math
from pyrogram import Client, filters
import yt_dlp as yt
from yt_dlp.utils import DownloadError
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import asyncio
import threading
from pyrogram.errors import MessageNotModified, FloodWait


# Telegram Bot Token
API_ID = 14604313
API_HASH = 'a8ee65e5057b3f05cf9f28b71667203a'
BOT_TOKEN = '6150084524:AAHutAX3WQjZxQVOxI4vCdlR4tzyRIotMt8'

# Initialize the Pyrogram client
app = Client("YouDl", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# URL regex pattern
url_pattern = r'(https?://[^\s]+)'

# ...
'''
def progress_for_pyrogram(current, total, bot, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        if total != 0:
            percentage = current * 100 / total
        else:
            percentage = 0
      #  percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n**Percentage:** {2}%\n".format(
            ''.join(["▣" for _ in range(math.floor(percentage / 10))]),
            ''.join(["□" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2)
        )

        tmp = progress + "**• Completed :** {0}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n**• Size :** {1}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n**• Speed :** {2}/s\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n**• ETA :** {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            message.edit_text(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                ),
                parse_mode="markdown"
            )
        except:
            pass

# ... 
def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

#...

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]
'''
def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def edit_msg(client, message, to_edit):
    try:
        client.loop.create_task(message.edit(to_edit))
    except FloodWait as e:
        client.loop.create_task(asyncio.sleep(e.value))
    except MessageNotModified:
        pass
    except TypeError:
        pass


def download_progress_hook(d, message, client):
    if d['status'] == 'downloading':
        current = d.get("_downloaded_bytes_str") or humanbytes(int(d.get("downloaded_bytes", 1)))
        total = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str")
        file_name = d.get("filename")
        eta = d.get('_eta_str', "N/A")
        percent = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        to_edit = f"📥 <b>Downloading!</b>\n\n<b>Name :</b> <code>{file_name}</code>\n<b>Size :</b> <code>{total}</code>\n<b>Speed :</b> <code>{speed}</code>\n<b>ETA :</b> <code>{eta}</code>\n\n<b>Percentage: </b> <code>{current}</code> from <code>{total} (__{percent}__)</code>"
        threading.Thread(target=edit_msg, args=(client, message, to_edit)).start()
#...
async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)

def download_video(c, m):
    ydl_opts = {
        "format": 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
       # outtmpl: '%(title)s.%(ext)s',
       # 'progress_hooks': [lambda d: progress_for_pyrogram(
        "progress_hooks": [lambda d: download_progress_hook(d, m, c)   
        
    }
    with yt.YoutubeDL(ydl_opts) as ydl:
       # info_dict = ydl.extract_info(url, download=False)
       # video_title = info_dict.get('title', None)
       # video_ext = info_dict.get('ext', None)
       # out_file = f'{video_title}.{video_ext}'
       # ydl_opts['outtmpl'] = out_file
       # ydl.download([url])
       # return 
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_ext = info_dict.get('ext', None)
        out_file = f'{video_title}.{video_ext}'
        return out_file

def send_video_to_telegram(chat_id, video_path, message):
    app.send_video(chat_id=chat_id, video=video_path, progress=progress_for_pyrogram, progress_args=(message, time.time()))
   # os.remove(video_path)

# ...





        
             

        
# ...



    
    
# ...

@app.on_message(filters.regex(url_pattern))
def handle_url(client, message):
    text = message.text

    # Extract URL from the message using regex
    match = re.search(url_pattern, text)
    if match:
        url = match.group(0)
        video_path = download_video(url, message)
        send_video_to_telegram(message.chat.id, video_path, message)
        os.remove(video_path)
    else:
        message.reply_text('Invalid URL!')

def main():
    # Start the Pyrogram client
    app.run()

if __name__ == '__main__':
    main()
