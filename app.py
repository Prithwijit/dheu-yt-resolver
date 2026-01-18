from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

YTDLP_CMD = [
    "yt-dlp",
    "-f", "ba/b",
    "-g",
    "--cookies", "cookies.txt",
    "--js-runtimes", "node"
]


@app.route("/")
def health():
    return "YT Resolver OK"

@app.route("/resolve")
def resolve():
    yt_url = request.args.get("yt")
    if not yt_url:
        return jsonify({"error": "missing yt parameter"}), 400

    cmd = YTDLP_CMD + [yt_url]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "yt-dlp timeout"}), 504

    if proc.returncode != 0:
        return jsonify({
            "error": "yt-dlp failed",
            "details": proc.stderr.strip()
        }), 500

    lines = [l.strip() for l in proc.stdout.splitlines() if l.startswith("http")]
    if not lines:
        return jsonify({"error": "no stream url found"}), 500

    return jsonify({
        "status": "ok",
        "stream_url": lines[0]
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port, debug=False)
