FROM python:3.11-slim

WORKDIR /app

# Fayllarni ish papkasiga nusxalash
COPY . .

# Python kutubxonalarini o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# ffmpeg o‘rnatish (audio uchun)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Botni ishga tushirish
CMD ["python", "telegram_music_bot.py"]
