from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_id_pytube(url):
    """
    Extracts the YouTube video ID using the pytube library.
    """
    try:
        video_id = extract.video_id(url)
        return video_id
    except Exception as e:
        print(f"Error extracting ID with pytube: {e}")
        return None


url = 'https://youtu.be/LI57EB_T38c?si=o3tQVSdDKPhY18WP'
video_id = get_youtube_id_pytube(url)
if video_id:
    print(f"URL: {url} -> Video ID: {video_id}")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    with open('transcription.txt', 'w', encoding='utf-8') as f:
        for entry in transcript:
            f.write(entry['text'] + '\n')
            
    print("Transcript saved to transcription.txt")
else:
    print(f"Could not extract video ID from URL: {url}")




