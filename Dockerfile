FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Bu bot portsiz ishlaydi
CMD ["python", "telegram_music_bot.py"]
