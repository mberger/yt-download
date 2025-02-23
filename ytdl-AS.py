from yt_dlp import YoutubeDL
import os
import subprocess

def download_video(url, output_path='./downloads/', audio_only=False):
    try:
        os.makedirs(output_path, exist_ok=True)  # Ensure output directory exists

        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'noplaylist': True,  # Prevent downloading entire playlists
            'merge_output_format': 'mp4',
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]',  # Force 1080p max
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
            'concurrent_fragments': 10,  # Increase parallel connections
        }

        if audio_only:
            ydl_opts['format'] = 'bestaudio[ext=m4a]/best'
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
        
        with YoutubeDL(ydl_opts) as ydl:
            print("Downloading...")
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise ValueError("Failed to retrieve video information.")
            
            filename = ydl.prepare_filename(info)
            print(f"Download successful: {filename}")
            return filename
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_premiere_pro_compatible(input_file):
    try:
        output_file = os.path.splitext(input_file)[0] + "_1080p.mp4"

        # Use Apple Silicon's VideoToolbox hardware acceleration
        cmd = [
            "ffmpeg", "-y", "-i", input_file, 
            "-vf", "scale=1920:1080",  # Force 1080p resolution
            "-c:v", "h264_videotoolbox", "-b:v", "8000k",  # Use Apple's VideoToolbox with 8Mbps bitrate
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", 
            "-threads", "0", output_file
        ]
        subprocess.run(cmd, check=True)
        print(f"Conversion successful: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion error: {e}")
        return None

if __name__ == "__main__":
    video_url = input("Enter the YouTube URL: ")
    download_type = input("Enter 'v' to download video, 'a' to download audio only: ")

    if download_type.lower() == 'v':
        download_result = download_video(video_url)
        if download_result:
            converted_file = convert_to_premiere_pro_compatible(download_result)
            if converted_file:
                print(f"Video ready for Premiere Pro: {converted_file}")
    elif download_type.lower() == 'a':
        audio_path = download_video(video_url, audio_only=True)
        if audio_path:
            print(f"Audio downloaded successfully: {audio_path}")
    else:
        print("Invalid choice.")
