FROM python:3.11-slim

# Install system dependencies
RUN apt update && apt install -y \
    curl \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install yt-dlp and Flask
RUN pip install --no-cache-dir flask yt-dlp

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
