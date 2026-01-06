from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/resolve")
def resolve():
    yt_url = request.args.get("yt")
    if not yt_url:
        return jsonify({"error": "missing yt parameter"}), 400

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "bestaudio/best",
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)

            return jsonify({
                "title": info.get("title"),
                "duration": info.get("duration"),
                "audio_url": info.get("url"),
                "codec": info.get("acodec")
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def health():
    return "yt-dlp resolver OK"
