import os
import sys
import glob
import random
import shutil
from mutagen.id3 import ID3, TALB
import yt_dlp as youtube_dl

def process_audio(path):
    mp3_files = glob.glob(os.path.join(path, "*.mp3"))
    if not mp3_files:
        return
    
    aFile = mp3_files[0]
    tags = ID3(aFile)
    filename = os.path.basename(aFile)
    
    try:
        Name = filename.split("-")[1].replace(".mp3", "").strip()
        id_tag = "YDown | " + Name + str(random.randint(1, 99))
    except Exception:
        id_tag = "YDown | " + filename.replace(".mp3", "") + str(random.randint(1, 99))
        
    tags.add(TALB(encoding=3, text=id_tag))
    tags.save()
    
    dest_dir = "/storage/emulated/0/PMusic3/"
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(aFile, os.path.join(dest_dir, filename))

def process_video(path):
    video_files = glob.glob(os.path.join(path, "*.mp4")) + glob.glob(os.path.join(path, "*.mkv"))
    if not video_files:
        return
    
    vFile = video_files[0]
    filename = os.path.basename(vFile)
    
    dest_dir = "/storage/emulated/0/Download/YDown/"
    os.makedirs(dest_dir, exist_ok=True)
    shutil.move(vFile, os.path.join(dest_dir, filename))

def main():
    base_path = "/storage/emulated/0/PMusic3/.tmp/"
    path = base_path
    i = 0
    
    # Find a unique temporary directory path
    while os.path.isdir(path):
        i += 1
        path = f"/storage/emulated/0/PMusic3/.tmp{i}/"
        
    try:
        # Get link from command line argument or user prompt
        if len(sys.argv) > 1:
            link = sys.argv[1]
        else:
            print("Insert the YouTube link:")
            link = input("--> ").strip()
            
        # Get media type choice (Audio or Video)
        if len(sys.argv) > 2:
            choice = sys.argv[2].lower()
        else:
            print("\nSelect Download Type:")
            print("[1] Audio (MP3 320kbps + Album Art)")
            print("[2] Video (MP4 Best Quality)")
            choice_input = input("--> ").strip()
            choice = "v" if choice_input == "2" or choice_input.startswith("v") else "a"

        # Configure yt-dlp options based on choice
        if choice in ['v', 'video']:
            print("\n[+] Preparing Video Download...")
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'postprocessors': [{'key': 'FFmpegMetadata'}],
            }
            is_video = True
        else:
            print("\n[+] Preparing Audio Download...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'writethumbnail': True,
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
                    {'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegMetadata'},
                ],
            }
            is_video = False

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            
        # Post-processing and moving file to appropriate directory
        if is_video:
            process_video(path)
            print("\n[✔] Video saved to: /storage/emulated/0/Download/YDown/")
        else:
            process_audio(path)
            print("\n[✔] Audio saved to: /storage/emulated/0/PMusic3/")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("[+] 0 : EXIT\n[+] 1 : RETRY")
        try:
            c = int(input("--> "))
            if c == 0:
                sys.exit()
            else:
                main()
        except ValueError:
            sys.exit()
            
    finally:
        # Clean up temp folder safely
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=True)

if __name__ == "__main__":
    main()
