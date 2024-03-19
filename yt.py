import os
import re
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize the bot
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a YouTube link followed by a rename command to download the video with a custom name.\n\nExample:\nhttps://www.youtube.com/watch?v=VIDEO_ID /rename CustomName")

# Define the download handler
def download(update, context):
    message_text = update.message.text
    
    # Extracting URL and rename command from the message text
    match = re.match(r'(https?://[^\s]+) /rename (.+)', message_text)
    if not match:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a YouTube link followed by a /rename command with a custom name.")
        return
    
    url = match.group(1)
    custom_name = match.group(2)
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_url = info_dict.get('url', None)
        filename = f"{video_title}.mp4"
        ydl.download([url])
    
    # Custom renaming
    filename = f"{custom_name}.mp4"
    os.rename(f"{video_title}.mp4", filename)
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Downloading {video_title}...")

    # Upload the downloaded video file
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(filename, 'rb'), caption=f"Here is your video: {custom_name}")

# Handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

download_handler = MessageHandler(Filters.text & ~Filters.command, download)
dispatcher.add_handler(download_handler)

# Start polling
updater.start_polling()
updater.idle()