import yt_dlp
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Function to download video using yt-dlp with cookies
def download_video(url):
    # Get the cookies file path from the environment variable
    cookies_file_path = os.getenv('YT_COOKIE_PATH')
    
    if not cookies_file_path:
        print("Error: Cookies file path is not set.")
        return
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookies': cookies_file_path  # Use cookies for authentication
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the video download
@app.route('/download', methods=['POST'])
def handle_download():
    video_url = request.form['url']
    download_video(video_url)
    return f"Downloading video from {video_url}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
