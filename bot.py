import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("TOKEN не найден")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("Ищу... 🎧")

    try:
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            video = info['entries'][0]

            title = video['title']
            url = video['webpage_url']

        await update.message.reply_text(f"🎵 {title}\n{url}")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Ошибка 😢")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()