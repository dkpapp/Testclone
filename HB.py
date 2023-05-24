import os
import subprocess
from urllib.parse import urlparse
from telegram.ext import Updater, MessageHandler, Filters

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a URL and I'll download it for you.")

def download_file(update, context):
    url = update.message.text
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    context.user_data['filename'] = filename

    context.bot.send_message(chat_id=update.effective_chat.id, text="Downloading...")

    subprocess.Popen(['yt-dlp', '-o', filename, url], stdout=subprocess.PIPE)

def check_progress(context):
    chat_id = context.job.context
    filename = context.user_data['filename']

    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        context.bot.send_message(chat_id=chat_id, text=f"Uploading... ({file_size} bytes)")

        context.bot.send_document(chat_id=chat_id, document=open(filename, 'rb'))
        os.remove(filename)

        context.bot.send_message(chat_id=chat_id, text="Upload complete!")
        context.job.schedule_removal()

def main():
    # Set up the Telegram bot
    updater = Updater(token='6150084524:AAHutAX3WQjZxQVOxI4vCdlR4tzyRIotMt8')
    dispatcher = updater.dispatcher

    # Define handlers
    start_handler = MessageHandler(Filters.command & Filters.regex('^/start$'), start)
    download_handler = MessageHandler(Filters.text & ~Filters.command, download_file)

    # Add handlers to the dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(download_handler)

    # Start the bot
    updater.start_polling()

    # Set up the progress check job
    job_queue = updater.job_queue
    job_queue.run_repeating(check_progress, interval=5, context=2067727305)

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
