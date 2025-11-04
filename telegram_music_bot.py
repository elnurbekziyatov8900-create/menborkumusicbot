import asyncio
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import yt_dlp
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# .env faylni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! .env faylni to‘g‘ri to‘ldiring.")

MAX_TELEGRAM_BYTES = 50 * 1024 * 1024  # 50MB limit

YTDL_OPTS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'outtmpl': '%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    # SSL muammosi uchun legacy server connect
    'legacy_server_connect': True
}

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! YouTube, TikTok yoki Instagram link yuboring. 🎵")

# Help komandasi
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Foydalanish: YouTube, TikTok yoki Instagram link yuboring.")

# Linkni qayta ishlash
async def process_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    msg = await update.message.reply_text("🎧 Musiqa yuklanmoqda...")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = Path(tmpdir)
            ydl_opts = YTDL_OPTS.copy()
            ydl_opts['outtmpl'] = str(cwd / '%(id)s.%(ext)s')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                mp3_files = list(cwd.glob('*.mp3'))
                if not mp3_files:
                    await msg.edit_text('❌ Xatolik: mp3 fayl topilmadi.')
                    return

                mp3_path = mp3_files[0]
                size = mp3_path.stat().st_size
                if size > MAX_TELEGRAM_BYTES:
                    await msg.edit_text(f"❌ Fayl juda katta ({size/1024/1024:.1f} MB). Telegram limiti 50MB.")
                    return

                title = info.get('title') or mp3_path.stem
                await msg.edit_text('Fayl yuborilmoqda 🎧')
                await context.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=InputFile(mp3_path),
                    title=title,
                    performer=info.get('uploader')
                )
                await msg.delete()

    except yt_dlp.utils.DownloadError as e:
        await msg.edit_text('❌ Yuklab olishda xatolik: ' + str(e))
    except Exception as e:
        await msg.edit_text('⚠️ Nomaʼlum xatolik yuz berdi: ' + str(e))

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_link))

    print('🎧 Telegram Music Bot ishga tushdi...')
    
    # asyncio loop bilan ishlash (Conflict xatolarini oldini oladi)
    try:
        app.run_polling()
    except Exception as e:
        print('❌ Botni ishga tushirishda xatolik:', e)

if __name__ == '__main__':
    main()
