FROM python:3.11-slim

RUN apt update && apt install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask yt-dlp

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
