# YouTube Downloader

A versatile application for fetching available formats and downloading videos and audio from YouTube and other supported platforms. This project offers both a user-friendly web interface built with React and a robust Flask API backend, alongside a powerful command-line interface (CLI) tool for direct use.

## Features
-   **Comprehensive Format Listing:** Easily retrieve and display all available video and audio formats for any given YouTube URL.
-   **Organized Format Presentation:** Formats are categorized into "Video + Audio", "Video Only", and "Audio Only" for clarity.
-   **Detailed Format Information:** Each format includes details such as Format ID, File Extension, Video Codec, Audio Codec, Height, FPS, estimated File Size (MB), Bitrate (Kbps), and additional notes.
-   **Flexible Download Options:** Users can select specific format IDs or combinations of video and audio format IDs for tailored downloads, or simply choose the "best" available quality.
-   **Subtitle Download Support:** Automatically download available subtitles in English and Indonesian (SRT format) along with the video.
-   **Web-Based Interface (Frontend):**
    -   Intuitive React application for pasting URLs, viewing formats, and initiating downloads.
    -   Live video preview directly within the application.
    -   Dynamic selection of desired formats using radio buttons.
-   **RESTful API (Backend):**
    -   Flask-based API to handle format fetching and video download requests.
    -   Configurable Cross-Origin Resource Sharing (CORS) for frontend integration.
    -   Health check endpoint (`/health`) to monitor service status.
    -   Temporary file serving: Downloaded files are served and automatically removed from the server.
-   **Command-Line Interface (CLI):**
    -   A standalone Python script for quick and efficient video/audio downloads directly from the terminal.
    -   Presents formats in a readable tabular format using `tabulate`.
-   **Dockerized Deployment:** Includes Dockerfile and Docker Compose configuration for easy setup and deployment of the backend service.

## Prerequisites
To run this project, you will need:

### For the Backend (Python & Docker)
-   **Python 3.8+**: For running the Python scripts directly.
-   **pip**: Python package installer.
-   **ffmpeg**: A cross-platform solution to record, convert and stream audio and video. Required by `yt-dlp` for merging streams, audio extraction, etc.
    -   On Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y ffmpeg`
    -   On macOS (with Homebrew): `brew install ffmpeg`
    -   On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
-   **Docker & Docker Compose**: For containerized deployment of the backend.

### For the Frontend (Node.js)
-   **Node.js 18+**: JavaScript runtime environment.
-   **npm** or **yarn**: Package managers for Node.js.

## Installation

You can install and run the project using Docker Compose for the backend, or run the backend and frontend separately.

### 1. Clone the Repository

```bash
git clone https://github.com/galang006/youtube_download.git
cd youtube_download
```

### 2. Docker Compose (Recommended for Backend)

This is the easiest way to get the backend API running.

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Build and start the Docker containers:
    ```bash
    docker compose up --build -d
    ```
    The `-d` flag runs the services in detached mode. The backend API will be available at `http://localhost:8000`.

### 3. Manual Installation (Backend API)

If you prefer to run the Flask backend directly:

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ensure `ffmpeg` is installed on your system (see [Prerequisites](#prerequisites)).
4.  Run the Flask application using Gunicorn (recommended for production) or the Flask development server:
    ```bash
    # For production/stable local setup
    gunicorn 'app:app' --bind 0.0.0.0:8000

    # For development (with auto-reload if files change)
    # Set the FLASK_APP environment variable if using 'flask run'
    # export FLASK_APP=app.py # Linux/macOS
    # $env:FLASK_APP="app.py" # Windows PowerShell
    # flask run --host=0.0.0.0 --port=8000
    ```
    The backend API will be available at `http://localhost:8000`.

### 4. Manual Installation (Frontend)

To run the React frontend locally:

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install Node.js dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```
3.  **Important Note for Local Development:**
    If you are running the backend locally (e.g., via Docker Compose or manual Flask setup on `http://localhost:8000`) and want the frontend to connect to your local backend, you will need to **edit `frontend/src/App.jsx`** and change all occurrences of `${API_BASE}` to `http://localhost:8000`.

4.  Start the development server:
    ```bash
    npm run dev
    # or
    yarn dev
    ```
    The frontend application will typically open in your browser at `http://localhost:5173` (or a similar address provided by Vite).

## Usage

### Web Interface

1.  Ensure both the [Backend API](#2-docker-compose-recommended-for-backend) (or [3.-manual-installation-backend-api]) and [Frontend](#4-manual-installation-frontend) are running. Remember to adjust the frontend's API URL if running both locally.
2.  Open your web browser and go to the frontend URL (e.g., `http://localhost:5173`).
3.  Paste a YouTube video URL into the input field.
4.  Click "Show Formats". The application will fetch and display all available video and audio formats.
5.  Select your desired format(s) using the radio buttons. You can choose:
    -   A combined "Video + Audio" format.
    -   A "Video Only" format, which can be combined with an "Audio Only" format (the backend will merge them).
    -   An "Audio Only" format.
6.  Click "Download Selected Format". The download will start automatically, and the file will be removed from the server after delivery.

### Command-Line Interface (CLI)

1.  Ensure you have `yt-dlp` and `tabulate` installed in your Python environment. If not, you can install them via `pip`:
    ```bash
    pip install yt-dlp tabulate
    ```
2.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
3.  Run the CLI script:
    ```bash
    python main.py
    ```
4.  Follow the prompts:
    -   Enter the YouTube video URL.
    -   The script will list all available formats in a table.
    -   Enter the desired `format id` (e.g., `best`, `bestvideo+bestaudio`, `137+251` for specific formats). If left blank, it defaults to `best`.
5.  The video/audio will be downloaded to the `./downloads` directory.

### API Endpoints (for developers)

The backend API exposes the following endpoints:

-   **GET `/health`**:
    -   **Description**: Checks the health and status of the API.
    -   **Response**: `{"status": "ok", "time": "..."}`
-   **GET `/formats?url=<youtube_url>`**:
    -   **Description**: Retrieves a list of available formats for the specified YouTube URL.
    -   **Query Parameter**: `url` (string, required) - The YouTube video URL.
    -   **Response**: JSON object containing `title` and `formats` (categorized into `audio_video`, `video_only`, `audio_only`).
-   **POST `/download`**:
    -   **Description**: Initiates the download of a video/audio from the specified URL in the chosen format.
    -   **Request Body**: JSON object `{ "url": "string", "format": "string", "subtitles": boolean (optional, default: true) }`
        -   `url`: The YouTube video URL (required).
        -   `format`: The desired `yt-dlp` format string (e.g., "best", "bestvideo+bestaudio", "137+251", or a single format ID like "251"). Defaults to "best".
        -   `subtitles`: Whether to download subtitles.
    -   **Response**: JSON object containing `message`, `files` (list of downloaded filenames), and `download_base` (base path for file access).
-   **GET `/file/<path:filename>`**:
    -   **Description**: Serves a downloaded file and removes it after being sent.
    -   **Path Parameter**: `filename` (string, required) - The name of the file to be downloaded.
    -   **Behavior**: The file is served as an attachment and then deleted from the server.

## Code Structure

The project is organized into two main components: `backend` (Python Flask API & CLI) and `frontend` (React web application).

```
.
├── backend/
│   ├── .dockerignore                 # Specifies files/folders to ignore when building Docker image
│   ├── .gitignore                    # Git ignore rules for the backend
│   ├── app.py                        # Flask API: handles format listing, downloads, and file serving
│   ├── compose.yaml                  # Docker Compose configuration for the backend service
│   ├── Dockerfile                    # Docker build instructions for the Flask app
│   ├── main.py                       # Standalone Command-Line Interface (CLI) for downloads
│   ├── README.Docker.md              # Docker specific usage instructions
│   ├── requirements.txt              # Python dependencies for the backend
│   └── downloads/                    # Directory for temporary downloaded files (created at runtime)
├── frontend/
│   ├── public/                       # Static assets for the frontend (e.g., vite.svg)
│   ├── src/                          # Source code for the React application
│   │   ├── App.css                   # CSS for the main App component
│   │   ├── App.jsx                   # Main React component, handles UI logic and API calls
│   │   ├── index.css                 # Global CSS (includes TailwindCSS directives)
│   │   └── main.jsx                  # Entry point for the React application
│   ├── .gitignore                    # Git ignore rules for the frontend
│   ├── eslint.config.js              # ESLint configuration
│   ├── index.html                    # Main HTML file for the React app
│   ├── package.json                  # Frontend dependencies and scripts (Node.js/React)
│   ├── postcss.config.js             # PostCSS configuration (used by TailwindCSS)
│   ├── README.md                     # Frontend specific README (Vite+React boilerplate)
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   └── vite.config.js                # Vite build configuration
└── README.md (this file)
```