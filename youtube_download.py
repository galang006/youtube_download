import yt_dlp

def download_youtube_video(url, output_path="./downloads"):
    ydl_opts = {
        #'format': 'best[ext=mp4]',  # Download best mp4 format
        #'format': 'best[height=1080]',  # Download best mp4 format
        'format': 'best[height<=720]',  # Download best mp4 format
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("Download completed successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

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
    video_url = "https://www.youtube.com/watch?v=NJlUbuW54TA"
    
    # Download video
    download_youtube_video(video_url)
    
    # # Download audio only
    # download_audio_only(video_url)