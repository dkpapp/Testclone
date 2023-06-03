import re
from pyrogram import Client, filters
import yt_dlp as yt
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

def download_video(url):

    ydl_opts = {

        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',

        'outtmpl': '%(title)s.%(ext)s',

    }

    with yt.YoutubeDL(ydl_opts) as ydl:

        info_dict = ydl.extract_info(url, download=False)

        video_title = info_dict.get('title', 'video')

        video_ext = info_dict.get('ext', 'mp4')

        out_file = f'{video_title}.{video_ext}'

        ydl_opts['outtmpl'] = out_file

        ydl.download([url])

        return out_file

def send_video_to_telegram(chat_id, video_path):

    app.send_video(chat_id=chat_id, video=video_path)

# ...

@app.on_message(filters.regex(url_pattern))

def handle_url(client, message):

    text = message.text

    # Extract URL from the message using regex

    match = re.search(url_pattern, text)

    if match:

        url = match.group(0)

        video_path = download_video(url)

        send_video_to_telegram(message.chat.id, video_path)

        os.remove(video_path)  # Optionally, delete the video file after sending

    else:

        message.reply_text('Invalid URL!')

def main():

    # Start the Pyrogram client

    app.run()

if __name__ == '__main__':

    main()

        




        
        
         
    


