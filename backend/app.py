import os
from flask import Flask, request, jsonify, send_from_directory, abort
from datetime import datetime
from yt_dlp import YoutubeDL
from flask_cors import CORS
import os

app = Flask(__name__)
FRONTEND_URL = os.getenv("FRONTEND_URL")  # fallback to allow all
CORS(app, origins=[FRONTEND_URL, "https://youtube-download-9qlxn0q56.vercel.app", "youtube-download-galang-satriamahesa-putra-dewas-projects.vercel.app"])

DOWNLOAD_DIR = "./downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

cookies_content = os.getenv("YTDLP_COOKIES")
if cookies_content:
    with open("cookies.txt", "w") as f:
        f.write(cookies_content)

def classify_format(fmt):
    vcodec = (fmt.get("vcodec") or "").lower()
    acodec = (fmt.get("acodec") or "").lower()
    if vcodec == "none":
        return "audio_only"
    if acodec == "none":
        return "video_only"
    return "audio_video"

def size_mb(fmt):
    size = fmt.get("filesize") or fmt.get("filesize_approx")
    return None if size is None else round(size / 1_048_576, 2)

@app.get("/health")
def health():
    return jsonify(status="ok", time=datetime.utcnow().isoformat() + "Z")

@app.get("/formats")
def list_formats():
    url = request.args.get("url")
    if not url:
        return jsonify(error="Missing 'url' query parameter"), 400

    opts = {
        "quiet": True,
        'cookiefile': "cookies.txt",
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info.get("title", "Unknown Title")
    grouped = {"audio_video": [], "video_only": [], "audio_only": []}

    for f in info.get("formats", []):
        vcodec = str(f.get("vcodec")).lower()
        acodec = str(f.get("acodec")).lower()
        if vcodec == "none" and acodec == "none":
            continue

        entry = {
            "format_id": f.get("format_id"),
            "ext": f.get("ext"),
            "vcodec": "-" if vcodec == "none" else f.get("vcodec"),
            "acodec": "-" if acodec == "none" else f.get("acodec"),
            "height": f.get("height"),
            "fps": f.get("fps"),
            "size_mb": size_mb(f),
            "tbr_kbps": f.get("tbr"),
            "note": f.get("format_note"),
        }
        grouped[classify_format(f)].append(entry)

    return jsonify(title=title, formats=grouped)

@app.post("/download")
def download_video():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    fmt = data.get("format", "best")  # e.g., "best", "bestvideo+bestaudio", or a format_id
    with_subs = bool(data.get("subtitles", True))  

    if not url:
        return jsonify(error="Missing 'url' in JSON body"), 400

    saved_files = []

    def hook(d):
        # When a file finishes, yt-dlp passes the final name in d["filename"]
        if d.get("status") == "finished" and d.get("filename"):
            saved_files.append(os.path.basename(d["filename"]))

    outtmpl = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "quiet": True,
        "progress_hooks": [hook],
        'cookiefile': "cookies.txt",
        "cache_dir": "/app/downloads/.yt-dlp-cache", 
    }
    if with_subs:
        ydl_opts.update(
            {
                "writesubtitles": True,
                "subtitleslangs": ["id", "en"],
                "subtitlesformat": "srt",
            }
        )

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(
        message="Download completed",
        files=saved_files,  
        download_base="/file", 
    )

@app.get("/file/<path:filename>")
def get_file(filename):
    path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(path):
        abort(404, description="File not found")
    try:
        response = send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)
        os.remove(path)
        return response
    except Exception as e:
        abort(500, description=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  
    app.run(host="0.0.0.0", port=port)