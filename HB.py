import re
import time
import math
from pyrogram import Client, filters
import yt_dlp as yt
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Telegram Bot Token
API_ID = 14604313
API_HASH = 'a8ee65e5057b3f05cf9f28b71667203a'
BOT_TOKEN = '6150084524:AAHutAX3WQjZxQVOxI4vCdlR4tzyRIotMt8'

# Initialize the Pyrogram client
app = Client("YouDl", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# URL regex pattern
url_pattern = r'(https?://[^\s]+)'

# ...

def progress_for_pyrogram(current, total, bot, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
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
#...
def download_video(url, message):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [lambda d: progress_for_pyrogram(d['downloaded_bytes'], d['total_bytes'], None, 'Downloading', message, time.time())]
    }
    with yt.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'video')
        video_ext = info_dict.get('ext', 'mp4')
        out_file = f'{video_title}.{video_ext}'
        ydl_opts['outtmpl'] = out_file
        ydl.download([url])
        return out_file

def send_video_to_telegram(chat_id, video_path, message):
    app.send_video(chat_id=chat_id, video=video_path, progress=progress_for_pyrogram, progress_args=(message, time.time()))
    os.remove(video_path)

# ...





        
             

        
# ...

@app.on_callback_query()
def handle_callback_query(client, query):
    query.answer()
    url = query.message.text
    video_path = download_video(url, query.message)
    send_video_to_telegram(query.message.chat.id, video_path, query.message)
# ...

@app.on_message(filters.regex(url_pattern))
def handle_url(client, message):
    text = message.text

    # Extract URL from the message using regex
    match = re.search(url_pattern, text)
    if match:
        url = match.group(0)

    else:
        message.reply_text('Invalid URL!')

def main():
    # Start the Pyrogram client
    app.run()

if __name__ == '__main__':
    main()
