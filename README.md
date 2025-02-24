# yt-download

Python script the download individual YouTube Videos.


ytdl2.py is the main script moving forward.




1. **Make sure you have** `ffmpeg` installed. Run:

   ```javascript
   nginxCopyEditffmpeg -version
   
   ```

   If not installed, install it using:
   * Mac/Linux: `brew install ffmpeg`
   * Windows: Download from [ffmpeg.org](https://ffmpeg.org/)
2. **Ensure** `yt-dlp` is up to date:

   ```javascript
   cssCopyEditpip install --upgrade yt-dlp
   
   ```

This should allow you to download videos with both video and audio intact! 🚀


Update Feb 16, 2025


Added ytdl-AS.py, this script is optimized for Apple Silicone.


This version **forces 1080p download** and **ensures Apple Silicon optimizations**.


## **🔑 What’s New on Feb 24, 2025?**

✅ **Creates a unique folder for each video** inside `./downloads/VideoTitle/` \n ✅**Handles special characters** in video titles to prevent file system errors \n ✅**Stores both the original and converted files in the same folder** \n ✅**Keeps everything neatly organized** 🎯



## **🔥 How This Ensures 1080p and Maximum Speed**

✅ **Forces** `yt-dlp`to download at least 1080p \n ✅**Uses Apple Silicon (**`h264_videotoolbox`) for ultra-fast conversion \n ✅**Applies** `-vf scale=1920:1080`to enforce 1080p resolution \n ✅**Increases bitrate to** `8000k`for better quality \n ✅**Uses** `-threads 0` to enable multi-threading


**Uses** `h264_videotoolbox`for ultra-fast H.264 encoding \n ✅**Avoids unnecessary re-encoding when possible** \n ✅**Optimizes** `yt-dlp` to download the fastest compatible format

✅ **Force** `yt-dlp`to download at least 1080p \n ✅**Ensure** `ffmpeg` upscales (if needed) while using Apple’s VideoToolbox (`h264_videotoolbox`) \n ✅**Set proper bitrates to maintain quality**




Update Feb 15, 2025

### **Key Fixes & Improvements:**

✅ **Ensures Video + Audio are merged correctly** using `bestvideo+bestaudio/best`. \n ✅**Forces final output format to MP4** using `merge_output_format`. \n ✅**Uses yt-dlp's built-in FFmpeg postprocessor**instead of manually converting. \n ✅**Creates the output folder if it doesn't exist** (`os.makedirs`). \n ✅**Fixes progress bar handling issues** (previous version had issues with global `pbar` use).

✅**Removes the progress bar issue** \n ✅**Fixes the** `NoneType`error \n ✅**Ensures proper video+audio merging using yt-dlp's built-in processing**

✅ **Forces H.264 video encoding** \n ✅**Forces AAC audio encoding** \n ✅**Ensures proper MP4 formatting**





These python scripts will download either single videos or all videos in a playlist.


Individual Video

```python
python ytdl.py
```


Playlist

```python
python ytdl-playist.py
```


Note: there is a problem with these if they are age protected. You will get an error.


For the ytdl2.py file, you will also need to install ffmpeg.


```bash
brew install ffmpeg
```


