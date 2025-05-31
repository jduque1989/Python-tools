import yt_dlp


def download_video(url):
    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",  # Best quality video + audio
            "outtmpl": "%(title)s.%(ext)s",  # Save as video title
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed!")
    except Exception as e:
        print(f"Error downloading video: {str(e)}")


if __name__ == "__main__":
    url = input("Enter YouTube video URL: ")
    download_video(url)
