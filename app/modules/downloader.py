import yt_dlp
import os
import re
import time
import subprocess
from PIL import Image

# Limit to 5 concurrent downloads


def clear_downloads():
    """Clears files in the downloads folder."""
    for file in os.listdir('downloads'):
        delete_file(f"downloads/{file}")

def crop_to_square(image_path, out_path):
    """Crops an image to a square format."""
    with Image.open(image_path) as img:
        width, height = img.size
        new_size = min(width, height)
        left = (width - new_size) / 2
        top = (height - new_size) / 2
        right = (width + new_size) / 2
        bottom = (height + new_size) / 2
        img = img.crop((left, top, right, bottom))
        img.save(out_path)

def sanitize_filename(text: str):
    """Sanitizes filenames by removing invalid characters."""
    return re.sub(r'[\\/:"*?<>|]+', '', text).replace(' ', '_')

def get_video_formats(url: str, domain: str):
    """Retrieves available video resolutions."""
    ydl_opts = {'quiet': True}
    # if domain.startswith("you"):
    #     ydl_opts['cookiefile'] = '/cookies/youtube.txt'
    # elif domain == 'instagram.com':
    #     ydl_opts['cookiefile'] = '/cookies/insta.txt'
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return [
            {
                'format_id': fmt['format_id'],
                'resolution': fmt.get('resolution', 'N/A'),
                'ext': fmt['ext']
            } for fmt in info_dict.get('formats', [])
        ]

def get_domain(url: str):
    """Extracts domain name from URL."""
    match = re.match(r'^(https?:\/\/)?(www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$', url)
    return match.group(3) if match else None

def delete_file(f_path):
    """Attempts to delete a file."""
    try:
        os.remove(f_path)
    except:
        time.sleep(5)

def download_audio(video_url, output_path, thumb):
    """Downloads audio with metadata and thumbnail."""
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
                {'key': 'FFmpegMetadata'},
                {'key': 'EmbedThumbnail'}
            ],
            'outtmpl': output_path[:-4],
            'writethumbnail': True,
            # 'cookiefile': 'cookies/youtube.txt'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        # audio_thumb = f"{thumb[:-4]}_audio.jpg"
        # try:
        #     crop_to_square(thumb, audio_thumb)
        # except:
        #     pass
        # delete_file(audio_thumb)
    except Exception as e:
        print(f"Audio download failed: {e}")

def download_video(url, output_path="downloads/%(title)s.%(ext)s",):
    """Downloads video with user-selected format."""

    ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': output_path
        }
    try:
        
        # if domain == "instagram.com":
        #     ydl_opts['cookiefile'] = 'cookies/insta.txt'
        # elif domain.startswith("youtu"):
        #     ydl_opts['cookiefile'] = 'cookies/youtube.txt'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Video download failed: {e}")

def download_image(url, output_path, domain):
    """Downloads an image from Instagram, Twitter, or X."""
    
    try:
        if domain in ["instagram.com", "twitter.com", "x.com"]:
            output_path = output_path.replace("mp4", "jpg")
            command = [
                "gallery-dl", "--config", "gallery-dl.conf",
                "--filename", output_path.replace("downloads/", ""),
                "--directory", "downloads/", url
            ]
            subprocess.run(command)
    except Exception as e:
        print(f"Image download failed: {e}")
    delete_file(output_path)

