import yt_dlp as yt
import re
import time
import math
from pyrogram import Client, filters
import os
import asyncio
from yt_dlp import DownloadError
import threading
from pyrogram.errors import MessageNotModified, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
from pytube import Playlist
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


# Telegram Bot Token
API_ID = 14604313
API_HASH = 'a8ee65e5057b3f05cf9f28b71667203a'
BOT_TOKEN = '6291981656:AAF86nMi_WL9uWrAqgGGW9rlxLgy2BMnlRY'

# Initialize the Pyrogram client
app = Client("YouDl", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# URL regex pattern
url_pattern = r'(https?://[^\s]+)'

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

async def Mdata01(download_directory):
          width = 0
          height = 0
          duration = 0
          metadata = extractMetadata(createParser(download_directory))
          if metadata is not None:
              if metadata.has("duration"):
                  duration = metadata.get('duration').seconds
              if metadata.has("width"):
                  width = metadata.get("width")
              if metadata.has("height"):
                  height = metadata.get("height")
          return width, height, duration
          
          
async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)

@app.on_message(filters.regex(url_pattern))
async def download_video(bot, message):
     link = message.text  
     boa = await message.reply_text("**DOWNLOADING**")
     if 'playlist' in link:
            pyt = Playlist(link)
            for video in pyt.videos:
                  try:
                      phd = video.streams.get_by_resolution(resolution ='360p')
                      wide = phd.download()
                  except:
                        phd = video.streams.get_highest_resolution()
                        wide = phd.download()
                  width, height, duration = await Mdata01(wide)
                  await  bot.send_video(
                            chat_id = message.chat.id, 
                            supports_streaming=True,
                            duration=duration,
                            width=width,
                            height=height,
                            caption=(f"⭕️ PLAYLIST : "+ pyt.title + "\n📥 DOWNLOADED " + "\n✅ JOIN @HKBOTZ" ),
                            video = wide,
                           # progress=progress_for_pyrogram,
                           # progress_args=(bot, "UPLOADING", boa, cp_time)
                  )
                  os.remove(wide)
            await boa.delete()   
     else:  
            ydl_opts = {
                #'format': 'bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480]',
                "format": "best",
                "addmetadata": True,
                "key": "FFmpegMetadata",
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
                "ignoreerrors": True,
                "usenetrc": True,
                "cookiefile": "cookies.txt",
                "allow_multiple_video_streams": True,
                "allow_multiple_audio_streams": True,
                "noprogress": True,
                "allow_playlist_files": True,
                "overwrites": True,
                # "outtmpl": "%(id)s.mp4",
                "logtostderr": False,
                #"quiet": True,
                # outtmpl: '%(title)s.%(ext)s',
                # 'progress_hooks': [lambda d: progress_for_pyrogram(
                "progress_hooks": [lambda d: download_progress_hook(d, boa, bot)]
            }
            with yt.YoutubeDL(ydl_opts) as ydl:
               try:
                  ytdl_data = ydl.extract_info(link, download=False)
                  await run_async(ydl.download, [link])
               except DownloadError as d:
                  await boa.edit(f"Sorry, an error {d} occurred")
                  return
            for file in os.listdir('.'):
              if file.endswith(".mp4") or file.endswith(".mkv"):
                    width, height, duration = await Mdata01(file)
                    await boa.reply_video(
                        f"{file}",
                        supports_streaming=True,        
                       # width=852,
                        #height=480,
                        duration=duration,
                        width=width,
                        height=height,
                        caption="The content you requested has been successfully downloaded!",
                        reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                      InlineKeyboardButton("• Owner •", url="https://t.me/dhruvprajapati2"),
                                   ],
                               ],
                        ),
                    )
                    os.remove(f"{file}")
                    break
             else:
                 continue
            await boa.delete()
    
def main():
    # Start the Pyrogram client
    app.run()

if __name__ == '__main__':
    main()
