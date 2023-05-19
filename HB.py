import os
import time
from telegram import InputFile
from telegram.ext import Updater, CommandHandler
from pytube import YouTube, Playlist
from pytube.cli import on_progress

# Enable logging
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define your Telegram bot token
TOKEN = '6291981656:AAF86nMi_WL9uWrAqgGGW9rlxLgy2BMnlRY'

# Define PRO_USERS and AUTH_USERS
PRO_USERS = [2067727305]  # Telegram user IDs of PRO users
AUTH_USERS = [2067727305]  # Telegram user IDs of AUTH users

# Define the time gap for AUTH_USERS
TIME_GAP_AUTH = 30 * 60  # 30 minutes in seconds

# Define the owner ID for broadcasting messages
OWNER = 2067727305  # Telegram user ID of the OWNER

# Store the download queue
download_queue = []

# Store the download progress
download_progress = {}


def start(update, context):
    """Send a welcome message when the command /start is issued."""
    update.message.reply_text('Welcome to YouTube Downloader Bot!\n'
                              'Please send me a YouTube video URL or playlist URL to download.')
    # Add the user to AUTH_USERS if not already present
    user_id = update.message.from_user.id
    if user_id not in AUTH_USERS:
        AUTH_USERS.append(user_id)


def on_progress_callback(stream, chunk, file_handle, bytes_remaining):
    """Update the download progress for a specific stream."""
    total_bytes = stream.filesize
    bytes_downloaded = total_bytes - bytes_remaining
    progress = (bytes_downloaded / total_bytes) * 100
    speed = stream.get_framerate() * (bytes_downloaded / (time.time() - download_progress[stream.url]['start_time']))
    eta = (bytes_remaining / speed) if speed > 0 else 0

    download_progress[stream.url].update({
        'bytes_downloaded': bytes_downloaded,
        'progress': progress,
        'speed': speed,
        'eta': eta
    })

    # Update the status in the download queue
    if stream.url in download_queue[0]['status']:
        download_queue[0]['status'][stream.url] = f"{stream.default_filename}: {progress:.2f}%"

    # Print the progress
    print(f"\r{stream.default_filename}: {progress:.2f}%", end="")


def process_next_in_queue():
    """Process the next video in the download queue."""
    if download_queue:
        item = download_queue[0]
        if item['type'] == 'video':
            download_video(item['url'], item['update'], item['context'])
        elif item['type'] == 'playlist':
            download_playlist(item['url'], item['update'], item['context'])
        download_queue.pop(0)


def download_video(url, update, context):
    """Download a single YouTube video."""
    try:
        yt = YouTube(url, on_progress_callback=on_progress_callback)
        video = yt.streams.get_highest_resolution()

        update.message.reply_text('Adding video to download queue...')

        # Store the initial progress information
        download_progress[video.url] = {
            'bytes_downloaded': 0,
            'progress': 0,
            'speed': 0,
            'eta': 0,
            'start_time': time.time()
        }

        # Add the video to the download queue
        item = {
            'url': url,
            'update': update,
            'context': context,
            'type': 'video',
            'status': {video.url: ""}
        }
        download_queue.append(item)
        position = len(download_queue)
        update.message.reply_text(f'Your video is in position {position} in the download queue.')
        if position == 1:
            process_next_in_queue()  # Start processing the first item in the queue

    except Exception as e:
        update.message.reply_text('An error occurred while adding the video to the download queue.')

def download_playlist(url, update, context):
    """Download a YouTube playlist."""
    try:
        playlist = Playlist(url)
        playlist.populate_video_urls()
        num_videos = len(playlist.video_urls)
        update.message.reply_text(f'Adding playlist to download queue with {num_videos} videos...')
        # Add each video in the playlist to the download queue
        for i, video_url in enumerate(playlist.video_urls):
            item = {
                'url': video_url,
                'update': update,
                'context': context,
                'type': 'video',
                'status': {video_url: ""}
            }
            download_queue.append(item)
            position = len(download_queue) - num_videos + 1
            update.message.reply_text(f'Your playlist is in position {position} in the download queue.')

            if position == 1:
                process_next_in_queue()  # Start processing the first item in the queue

    except Exception as e:
        update.message.reply_text('An error occurred while adding the playlist to the download queue.')


def upload_video(video_path, update, context):
    """Upload a video file to Telegram with progress bar."""
    chat_id = update.effective_chat.id
    # Get the file size
    file_size = os.path.getsize(video_path)

    # Start uploading with progress bar
    with open(video_path, 'rb') as video_file:
        context.bot.send_chat_action(chat_id=chat_id, action="upload_video")
        message = context.bot.send_video(
            chat_id=chat_id,
            video=InputFile(video_file),
            caption="Uploading video...",
            progress=progress_callback,
            progress_args=(file_size,),
        )

        # Delete the video file from the download directory
        os.remove(video_path)

        # Wait for the upload to finish
        message.wait()

        # Send upload complete message
        context.bot.send_message(chat_id=chat_id, text="Video upload complete!")

def progress_callback(current, total, update, context):
    """Update the upload progress in the message."""
    chat_id = update.effective_chat.id
    # Calculate the progress percentage
    progress = current / total * 100

    # Update the progress bar message
    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=update.message.message_id,
        text=f"Uploading video...\n"
             f"Progress: {progress:.2f}%"
    )

    # Update the progress bar in the console
    print(f"\rUploading video... Progress: {progress:.2f}%", end="")


def main():
    """Start the bot."""
    updater = Updater(TOKEN, update_queue=None)
    dp = Updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    # Remove the following lines as add_to_queue command is no longer needed
    # dp.add_handler(CommandHandler("download_video", download_video))
    # dp.add_handler(CommandHandler("download_playlist", download_playlist))
    # dp.add_handler(CommandHandler("add_to_queue", add_to_queue))
    # Start the bot
    updater.start_polling()
    logger.info("Bot started.")
    updater.idle()


if __name__ == '__main__':
    main()
