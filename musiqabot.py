import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

BOT_TOKEN = "7780144299:AAEiGYayucjHGXMCxN0FPwDgjz7A-mTprko"

# Matndan mp3 yuklash
def download_audio(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

# Videoni yuklash
def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'video.%(ext)s',
        'quiet': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Videodan mp3 chiqarish
def extract_audio():
    subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "-y", "audio.mp3"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Xabarlarni qabul qilish
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Eski fayllarni o‘chiramiz
    for f in ["video.mp4", "audio.mp3", "music.mp3"]:
        if os.path.exists(f):
            os.remove(f)

    if "youtu" in text or "tiktok" in text or "instagram" in text:
        await update.message.reply_text("⏬ Videoni yuklab olyapman...")
        try:
            download_video(text)
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open("video.mp4", 'rb'))

            await update.message.reply_text("🎧 Audio chiqarilmoqda...")
            extract_audio()
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open("audio.mp3", 'rb'))
        except Exception as e:
            await update.message.reply_text(f"❌ Xatolik: {e}")
    else:
        await update.message.reply_text("🔍 Musiqa qidirilmoqda...")
        try:
            download_audio(text)
            await update.message.reply_text("✅ Musiqa topildi. Yuborilmoqda...")
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open("music.mp3", 'rb'))
        except Exception as e:
            await update.message.reply_text(f"❌ Xatolik: {e}")

# Botni ishga tushirish
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
