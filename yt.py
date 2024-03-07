import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube

# Telegram Bot token and YouTube API credentials
TELEGRAM_TOKEN = '7152551098:AAE3yVc80slmtsW4m7-CxxM5VZdOl1VRUbg'
YOUTUBE_API_KEY = 'AIzaSyAFNSws_6PxBPr1vbK1QKHwFW_bVXHfZ9o'

# Initialize Telegram bot
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! Send me a file and I'll upload it to YouTube.")

# Define the handler for file uploads
def handle_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)

    # Download the file to Heroku server's download folder
    file_path = f'/app/{file_id}.mp4'  # Adjust the path as per Heroku environment
    file.download(file_path)

    # Upload the file to YouTube
    youtube = YouTube(YOUTUBE_API_KEY)
    video = youtube.upload(file_path, title='Uploaded from Telegram')

    # Send the YouTube link to the user
    update.message.reply_text(f"File uploaded to YouTube: {video.watch_url}")

# Add command and message handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

# Start the bot
updater.start_polling()
updater.idle()
