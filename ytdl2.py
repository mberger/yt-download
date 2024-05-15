from yt_dlp import YoutubeDL
from tqdm import tqdm
import os
import shutil
import subprocess


def on_progress(d):
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            pbar.total = d['total_bytes']
            pbar.update(d['downloaded_bytes'] - pbar.n)
        else:
            pbar.update()

def download_video(url, output_path='./downloads/', video_only=False):
    global pbar  # Use global pbar
    try:
        ydl_opts = {
            'progress_hooks': [on_progress],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Use video title as filename
            'ignoreerrors': True  # Ignore errors to prevent halting on unavailable formats
        }
        if video_only:
            ydl_opts['format'] = 'bestaudio'
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]'
            ydl_opts['noplaylist'] = True  # Prevent downloading playlists
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading...")
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            pbar = tqdm(unit='B', unit_scale=True, desc="Downloading")
            ydl.download([url])
            pbar.close()
            print("Download successful, please wait...")
            return filename
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

import os

def convert_to_mp4(input_file, output_path):
    try:
        output_file = os.path.join(output_path, 'output.mp4')
        os.system(f'ffmpeg -i "{input_file}" -c:v libx264 -crf 23 -c:a aac -strict experimental "{output_file}"')
        print("Conversion successful.")
        return output_file
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None

if __name__ == "__main__":
    video_url = input("Enter the YouTube URL: ")
    download_type = input("Enter 'v' to download video, 'a' to download audio only: ")
    if download_type.lower() == 'v':
        download_result = download_video(video_url)
        if download_result:
            mp4_file = convert_to_mp4(download_result, os.getcwd())  # Convert to MP4
            if mp4_file:
                os.remove(download_result)  # Remove original file
                shutil.move(mp4_file, download_result)  # Replace original file with MP4 version
                print(f"Video downloaded successfully as {download_result}")
    elif download_type.lower() == 'a':
        audio_path = download_video(video_url, video_only=True)
        if audio_path:
            print(f"Audio downloaded successfully as {audio_path}")
    else:
        print("Invalid choice.")
