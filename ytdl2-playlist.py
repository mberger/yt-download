from yt_dlp import YoutubeDL
from tqdm import tqdm
import os

def on_progress(d):
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            pbar.total = d['total_bytes']
            pbar.update(d['downloaded_bytes'] - pbar.n)
        else:
            pbar.update()

def download_playlist(playlist_url, output_path='./downloads/', video_only=False):
    global pbar
    try:
        ydl_opts = {
            'progress_hooks': [on_progress],
            'outtmpl': os.path.join(output_path, '%(playlist_title)s', '%(title)s.%(ext)s'),  # Store in subdirectories named after playlist title
        }
        if video_only:
            ydl_opts['format'] = 'bestaudio'
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]'
            ydl_opts['noplaylist'] = False  # Allow downloading playlists
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading playlist...")
            pbar = tqdm(unit='B', unit_scale=True, desc="Downloading")
            ydl.download([playlist_url])
            pbar.close()
            print("Download successful.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    download_type = input("Enter 'v' to download videos, 'a' to download audio only: ")
    if download_type.lower() == 'v':
        download_playlist(playlist_url)
    elif download_type.lower() == 'a':
        download_playlist(playlist_url, video_only=True)
    else:
        print("Invalid choice.")
