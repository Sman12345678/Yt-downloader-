from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    # Set up the download options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save video in the downloads folder
    }
    
    try:
        # Create the download folder if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        
        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_filename = f"{video_title}.mp4"  # assuming .mp4 format
            
            # Provide the download link to the user
            message = f'Video "{video_title}" downloaded successfully! Click below to download it to your device.'
            download_link = f"/downloads/{video_filename}"
        
    except Exception as e:
        message = f'Error: {str(e)}'
        download_link = None

    return render_template('index.html', message=message, download_link=download_link)

@app.route('/downloads/<filename>')
def download_file(filename):
    # Send the file from the 'downloads' folder to the user
    return send_from_directory('downloads', filename)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3000)
