import re
from pyrogram import Client, filters
import yt_dlp as yt

# Telegram Bot Token
API_ID = 14604313
API_HASH = 'a8ee65e5057b3f05cf9f28b71667203a'
BOT_TOKEN = '6150084524:AAHutAX3WQjZxQVOxI4vCdlR4tzyRIotMt8'

# Initialize the Pyrogram client
app = Client("YouDl", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# URL regex pattern
url_pattern = r'(https?://[^\s]+)'

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
    }
    with yt.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def send_video_to_telegram(chat_id):
    app.send_video(chat_id=chat_id, video='video.mp4')

@app.on_message(filters.regex(url_pattern))
def handle_url(client, message):
    text = message.text

    # Extract URL from the message using regex
    match = re.search(url_pattern, text)
    if match:
        url = match.group(0)
        download_video(url)
        send_video_to_telegram(message.chat.id)
    else:
        message.reply_text('Invalid URL!')

def main():
    # Start the Pyrogram client
    app.run()

if __name__ == '__main__':
    main()
