import yt_dlp
"""

Must install ffmpeg on system: 
 Instructions: https://phoenixnap.com/kb/ffmpeg-windows    

 binaries location: https://www.gyan.dev/ffmpeg/builds/

"""
def yt_dlp_download_youtube_playlist(playlist_url, download_folder, type="audio", resolution = None):
    ydl_opts_audio = {
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' # Best quality
    name_ext = "_full_resolution"
    # resolution decided by user
    # ex: 360, 480, 720, 1080
    # Other options that can replae height
    #   [filesize<=50M] -- by filesize
    #   [fps<=30] -- by frames per second
    #   [vbr<=800]  -- video bitrate of 800 kpbs
    #   [vcodec=avc1.42E01E]  -- video codec of H.264 
    if resolution is not None:
        format = f'bestvideo[ext=mp4][height<={resolution}]+bestaudio[ext=m4a]/mp4' 
        name_ext = f"_{resolution}"
        
    ydl_opts_video = {
        'outtmpl': f'{download_folder}/%(title)s.%(ext)s{name_ext}',
        'format': format, 
        'merge_output_format': 'mp4',  # Ensure final format is MP4
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'  # Final conversion to MP4 if necessary
        }]
    }
    
    if type=="audio":
        ydl_opts = ydl_opts_audio
    else: 
        ydl_opts = ydl_opts_video
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])
        
def download_audio_only():
   
    single_video_or_playlist_url = "https://www.youtube.com/watch?v=97uVDPOibYw"
  
    download_folder = r"C:\Users\nagub\Music\Bhavesh_Music"
 
    #set type="audio" for mp3 download
    yt_dlp_download_youtube_playlist(single_video_or_playlist_url, download_folder, type="audio")
 
def download_video_only():
    single_video_or_playlist_url = "https://www.youtube.com/watch?v=97uVDPOibYw"
  
    download_folder = r"C:\Users\nagub\Music\Bhavesh_Music"
 
    #  set type="video". Optionally set resolution to 240, 360, 720, or 1080 or any other. If you don't set, it will download at highest
    yt_dlp_download_youtube_playlist(single_video_or_playlist_url, download_folder, type="video", resolution="240")
    
# Example usage
if __name__ == "__main__":
    download_audio_only()
    download_video_only()
    
    
  

