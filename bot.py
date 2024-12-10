import telebot
import requests
import os

# Replace with your bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

# Replace with your file upload server endpoint
UPLOAD_URL = 'https://your-server.com/upload'

@bot.message_handler(content_types=['document', 'photo', 'video'])
def handle_file(message):
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = "photo.jpg"
    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name or "video.mp4"

    # Get the file URL from Telegram
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
    file_data = requests.get(file_url).content

    # Upload the file to your server
    response = requests.post(UPLOAD_URL, files={'file': (file_name, file_data)})

    # Respond with the download link
    if response.status_code == 200:
        public_link = response.json().get('link', 'Error generating link')
        bot.reply_to(message, f"File uploaded! Download link: {public_link}")
    else:
        bot.reply_to(message, "Failed to upload file. Try again.")

# Start the bot
bot.polling()