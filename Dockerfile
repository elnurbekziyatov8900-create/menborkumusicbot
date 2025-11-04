# Python 3.13 bazaviy imidjidan foydalanamiz
FROM python:3.13-slim

# Ishchi papkani yaratamiz
WORKDIR /app

# Fayllarni konteyner ichiga nusxalaymiz
COPY . /app

# Kerakli kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir python-telegram-bot==21.4 yt-dlp python-dotenv requests pyopenssl

# Asosiy faylni ishga tushirish
CMD ["python", "telegram_music_bot.py"]
