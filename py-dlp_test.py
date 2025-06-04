import yt_dlp

def test_youtube_url_yt_dlp(url):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'N/A')
            video_views = info_dict.get('view_count', 'N/A')

            print(f"URL: {url}")
            print(f"Title: {video_title}")
            print(f"Views: {video_views}")
            print("This URL is likely recognized by yt-dlp.")
        return True
    except Exception as e:
        print(f"Error for URL: {url}")
        print(f"yt-dlp did NOT recognize this URL. Error: {e}")
        return False

print("problem: ")
# --- Test with your problematic URL ---
test_youtube_url_yt_dlp('https://youtu.be/bzwD7vfQJCA?si=UA-oXg6ctxAHf2xE')

print("-" * 30)

print("good: ")
# --- Test with a known good YouTube URL ---
test_youtube_url_yt_dlp('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

print("-" * 30)

print("short: ")
# Example: A short tutorial video
test_youtube_url_yt_dlp('https://youtu.be/dQw4w9WgXcQ')