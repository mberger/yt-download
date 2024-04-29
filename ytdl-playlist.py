from pytube import Playlist, YouTube
from tqdm import tqdm
import os
import shutil

def on_progress(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    bytes_downloaded = filesize - bytes_remaining
    pbar.update(bytes_downloaded - pbar.n)

pbar = None  # Initialize pbar globally

def download_video(url, output_path='./', video_quality='720p', video_only=False):
    global pbar  # Use global pbar
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        if video_only:
            video = yt.streams.filter(only_audio=True).first()
            if video:
                print("Downloading audio...")
                pbar = tqdm(total=video.filesize, unit='B', unit_scale=True, desc=video.title)
                audio_path = video.download(output_path, filename='temp_audio')
                pbar.close()
                print("Audio download successful.")
                return audio_path
            else:
                print("No audio stream found.")
                return None
        else:
            if video_quality == '1080p':
                video_stream = yt.streams.filter(res='1080p', file_extension='mp4', progressive=True).first()
                audio_stream = yt.streams.filter(only_audio=True).first()
                if video_stream and audio_stream:
                    print("Downloading...")
                    pbar = tqdm(total=video_stream.filesize, unit='B', unit_scale=True, desc=video_stream.title)
                    video_path = video_stream.download(output_path, filename='temp_video')
                    pbar.close()
                    print("Video download successful.")
                    return video_path, audio_stream.download(output_path, filename='temp_audio')
                else:
                    print("No suitable video/audio streams found.")
                    return None, None
            else:
                video = yt.streams.filter(res=video_quality, file_extension='mp4', progressive=True).first()
                if video:
                    print("Downloading...")
                    pbar = tqdm(total=video.filesize, unit='B', unit_scale=True, desc=video.title)
                    video_path = video.download(output_path, filename='temp')
                    pbar.close()
                    print("Download successful.")
                    return video_path
                else:
                    print("No suitable video found.")
                    return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def merge_video_audio(video_path, audio_path, output_path):
    try:
        print("Merging video and audio...")
        if isinstance(video_path, tuple):  # If video_path is a tuple, it means both video and audio were downloaded separately
            video_path, audio_path = video_path  # Extracting video and audio paths
        video_file = os.path.join(output_path, 'temp_video.mp4')
        audio_file = os.path.join(output_path, 'temp_audio.mp4')
        output_file = os.path.join(output_path, 'output.mp4')
        shutil.move(video_path, video_file)
        shutil.move(audio_path, audio_file)
        os.system(f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -strict experimental "{output_file}"')
        os.remove(video_file)
        os.remove(audio_file)
        print("Merge successful.")
        return output_file
    except Exception as e:
        print(f"An error occurred during merge: {e}")
        return None

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    if "playlist?list=" not in playlist_url:
        print("Invalid playlist URL. Please provide a valid YouTube playlist URL.")
    else:
        download_type = input("Enter 'v' to download video, 'a' to download audio only: ")
        if download_type.lower() == 'v':
            video_quality = input("Enter '720p' or '1080p' for video quality: ")
            if video_quality.lower() == '720p' or video_quality.lower() == '1080p':
                playlist = Playlist(playlist_url)
                for video_url in playlist.video_urls:
                    download_result = download_video(video_url, video_quality=video_quality)
                    if download_result:
                        if isinstance(download_result, tuple):
                            video_path, audio_path = download_result
                            if audio_path:
                                final_file = os.path.join(os.getcwd(), f'{YouTube(video_url).title}.mp4')
                                merge_video_audio(video_path, audio_path, os.path.dirname(final_file))
                                print(f"Video downloaded successfully as {final_file}")
                            else:
                                final_file = os.path.join(os.getcwd(), f'{YouTube(video_url).title}.mp4')
                                shutil.move(video_path, final_file)
                                print(f"Video downloaded successfully as {final_file}")
                        else:
                            final_file = os.path.join(os.getcwd(), f'{YouTube(video_url).title}.mp4')
                            shutil.move(download_result, final_file)
                            print(f"Video downloaded successfully as {final_file}")
            else:
                print("Invalid video quality.")
        elif download_type.lower() == 'a':
            playlist = Playlist(playlist_url)
            for video_url in playlist.video_urls:
                audio_path = download_video(video_url, video_only=True)
                if audio_path:
                    final_file = os.path.join(os.getcwd(), f'{YouTube(video_url).title}.mp3')
                    shutil.move(audio_path, final_file)
                    print(f"Audio downloaded successfully as {final_file}")
        else:
            print("Invalid choice.")
