import yt_dlp
from tabulate import tabulate
import os
def download_youtube_video(url, output_path="./downloads", format='best'):
    ydl_opts = {
        #'format': 'best[ext=mp4]',  # Download best mp4 format
        #'format': 'best[height=1080]',  # Download best mp4 format
        #'format': 'best[height<=720]',  # Download best mp4 format
        #'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'format': f'{format}',
        'merge_output_format': 'mp4',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Download completed successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")


def list_formats(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "Unknown Title")
        print(f"\n📺 Judul Video: {title}\n")
        print("📝 Daftar Format:")
        print("-" * 60)
        table = []
        for f in info['formats']:
            table.append([
                f.get('format_id'),
                f.get('ext'),
                f.get('vcodec', '-') if f.get('vcodec') != 'none' else '-',
                f.get('acodec', '-') if f.get('acodec') != 'none' else '-',
                f.get('height', '-'),
                f.get('fps', '-'),
                f.get('format_note', '-'),
            ])

        headers = ["Format ID", "Ext", "Video Codec", "Audio Codec", "Height", "FPS", "Note"]
        print(tabulate(table, headers=headers, tablefmt="grid"))

def download_audio_only(url, output_path="./downloads"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Audio download completed successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

def download_playlist(playlist_url, output_path="./downloads"):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': f'{output_path}/%(playlist_index)s - %(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([playlist_url])
            print("Playlist download completed successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

# Usage examples
if __name__ == "__main__":
    os.system("cls")
    video_url = input("Enter YouTube video URL: ")
    
    list_formats(video_url)
    format = input("Enter the format you want to download (e.g., best, bestvideo[ext=mp4]+bestaudio[ext=m4a], number+number (video format + audio format)): ")
    if not format:
        format = 'best'
    download_youtube_video(video_url, format=format)
