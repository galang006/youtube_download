# YouTube Video Downloader

A command-line tool for downloading YouTube videos and playlists using `yt-dlp` and displaying available formats in a tabular format.  Supports subtitle downloads and various video/audio formats.

## Features

- Downloads YouTube videos in various formats (including best quality, specific resolutions, and custom format specifications).
- Downloads YouTube playlists.
- Lists available video and audio formats with detailed information (codec, resolution, bitrate, etc.) before download.
- Includes subtitle downloads (Indonesian and English).
- Uses `yt-dlp` for robust and efficient downloads.
- Creates a dedicated "downloads" directory for storing downloaded files.
- Handles errors gracefully and provides informative error messages.


## Prerequisites

- Python 3.7 or higher.
- `yt-dlp`
- `tabulate`


## Installation

1. **Clone the repository:** 
2. **Install dependencies:** Open your terminal or command prompt and navigate to the project directory. Then, run:
   ```bash
   pip install yt-dlp
   pip install tabulate
   ```
   

## Usage

1. **Run the script:** Execute the `main.py` script from your terminal:
   ```bash
   python main.py
   ```
2. **Enter the YouTube URL:** The script will prompt you to enter the URL of the YouTube video you want to download.
3. **View Available Formats:** The script will then display a table listing all available formats. Carefully examine the table to choose a suitable format.    
4. **Specify the Format (Optional):** Enter the desired format ID or specification from the table (e.g., 'best', 'bestvideo+bestaudio', a specific format ID like '137+251').  Press Enter without input to use 'best' as default.
5. **Download:** The script will download the video to the `./downloads` directory.


## Code Structure

The project consists of a single Python file:

- **`main.py`:** This file contains all the code for downloading YouTube videos and playlists.  The main functions are:
    - `download_youtube_video(url, output_path, format)`: Downloads a single YouTube video.
    - `list_formats(url)`: Lists available formats for a given YouTube URL.
    - `download_playlist(playlist_url, output_path)`: Downloads a YouTube playlist.

- **`.gitignore`:** This file specifies files and directories to exclude from version control (e.g., `downloads` directory to avoid committing downloaded files, `cookies.txt` which might contain sensitive information).


**Important Notes:**

* **Error Handling:** The script includes basic error handling to catch and report exceptions during the download process.
* **Format Selection:** Understanding the format codes provided by `yt-dlp` is crucial for selecting the desired video and audio quality. Refer to `yt-dlp`'s documentation for details.
* **Output Path:** Downloaded videos are saved in a `downloads` folder created in the script's directory.
* **Legal Considerations:** Always respect copyright laws and only download videos you have permission to access.


This documentation provides a comprehensive guide to using the YouTube video downloader.  Remember to install the required libraries before running the script.
