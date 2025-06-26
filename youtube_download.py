import yt_dlp
from tabulate import tabulate
import os

def download_youtube_video(url, output_path, format='best'):
    ydl_opts = {
        #'format': 'best[ext=mp4]',  # Download best mp4 format
        #'format': 'best[height=1080]',  # Download best mp4 format
        #'format': 'best[height<=720]',  # Download best mp4 format
        #'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'format': f'{format}',
        'merge_output_format': 'mp4',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': True,   
    }
   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Download completed successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")


def list_formats(url):
    with yt_dlp.YoutubeDL({'quiet': True,}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "Unknown Title")
        os.system("cls")
        print(f"\n📺 Judul Video: {title}\n")
        print("📝 Daftar Format:")
        print("-" * 60)

        headers = ["Format ID", "Ext", "Video Codec", "Audio Codec", "Height", "FPS", "File Size (MB)", "Bitrate (Mbps)" ,"Note"]
        table_audio, table_video, table_all = [], [], []

        for f in info['formats']:
            vcodec = str(f.get('vcodec')).lower()
            acodec = str(f.get('acodec')).lower()

            # Skip jika tidak ada audio maupun video
            if vcodec == 'none' and acodec == 'none':
                continue
            
            size_bytes = f.get("filesize")                 # bisa None
            size_mb    = "-" if size_bytes is None else f"{size_bytes/1_048_576:,.2f}"

            br_kbps = f.get("tbr")
            br_display = "-" if br_kbps is None else f"{br_kbps:.0f}" 

            row = [
                f.get('format_id'),
                f.get('ext'),
                '-' if vcodec == 'none' else f.get('vcodec'),
                '-' if acodec == 'none' else f.get('acodec'),
                f.get('height', '-'),
                f.get('fps', '-'),
                size_mb,
                br_kbps,
                f.get('format_note', '-'),
                
            ]

            if vcodec == 'none':
                table_audio.append(row)
            elif acodec == 'none':
                table_video.append(row)
            else:
                table_all.append(row)

        if table_all:
            print("\n📼 Video + Audio Formats:")
            print(tabulate(table_all, headers=headers, tablefmt="grid"))
        if table_video:
            print("\n🎥 Video Only Formats:")
            print(tabulate(table_video, headers=headers, tablefmt="grid"))
        if table_audio:
            print("\n🎵 Audio Only Formats:")
            print(tabulate(table_audio, headers=headers, tablefmt="grid"))

# def download_audio_only(url, output_path="./downloads"):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': f'{output_path}/%(title)s.%(ext)s',
#     }
    
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             ydl.download([url])
#             print("Audio download completed successfully!")
#         except Exception as e:
#             print(f"Error occurred: {e}")

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

if __name__ == "__main__":
    otput_path = "./downloads"
    os.makedirs(otput_path, exist_ok=True)
    os.system("cls")
    video_url = input("Enter YouTube video URL: ")
    
    list_formats(video_url)
    format = input("Enter the format you want to download (e.g., best, bestvideo[ext=mp4]+bestaudio[ext=m4a], format id ,video format id + audio format id): ")
    if not format:
        format = 'best'
    download_youtube_video(video_url, otput_path, format=format)
