from yt_dlp import YoutubeDL
from tqdm import tqdm
import os
import shutil

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
        }
        if video_only:
            ydl_opts['format'] = 'bestaudio'
        else:
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=mp4]/best[ext=mp4]'
            ydl_opts['noplaylist'] = True  # Prevent downloading playlists
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading...")
            pbar = tqdm(unit='B', unit_scale=True, desc="Downloading")
            ydl.download([url])
            pbar.close()
            print("Download successful.")
            return os.path.join(output_path, '%(title)s.%(ext)s')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def merge_video_audio(video_path, audio_path, output_path):
    try:
        print("Merging video and audio...")
        output_file = os.path.join(output_path, 'output.mp4')
        os.system(f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "{output_file}"')
        print("Merge successful.")
        return output_file
    except Exception as e:
        print(f"An error occurred during merge: {e}")
        return None

if __name__ == "__main__":
    video_url = input("Enter the YouTube URL: ")
    download_type = input("Enter 'v' to download video, 'a' to download audio only: ")
    if download_type.lower() == 'v':
        download_result = download_video(video_url)
        if download_result:
            final_file = download_result.replace('temp.', '')  # Remove 'temp' prefix
            final_file = os.path.join(os.getcwd(), 'downloads', final_file)
            print(f"Video downloaded successfully as {final_file}")
    elif download_type.lower() == 'a':
        audio_path = download_video(video_url, video_only=True)
        if audio_path:
            final_file = audio_path.replace('temp.', '')  # Remove 'temp' prefix
            final_file = os.path.join(os.getcwd(), 'downloads', final_file)
            print(f"Audio downloaded successfully as {final_file}")
    else:
        print("Invalid choice.")
