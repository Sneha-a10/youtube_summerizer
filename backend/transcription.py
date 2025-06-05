import os
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import time
import traceback

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_youtube_id_pytube(url):
    """
    Extracts the YouTube video ID using the pytube library.
    """
    try:
        video_id = extract.video_id(url)
        return video_id
    except Exception as e:
        logging.error(f"Error extracting ID with pytube: {e}")
        print(f"Error extracting ID with pytube: {e}")
        return None

def get_transcript(url, max_retries=3, initial_delay=1, filename='transcription.txt'):
    """
    Fetches the transcript for a given video ID with retry logic.
    Saves the transcript to a file if it doesn't already exist.
    """
    if os.path.exists(filename):
        print(f"{filename} already exists. Skipping transcript retrieval.")
        return None 

    video_id = get_youtube_id_pytube(url)
    for attempt in range(max_retries):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            save_transcript_to_file(transcript, filename)  # Save the transcript here
            return transcript
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed to get transcript for video ID {video_id}: {e}")
            print(f"Attempt {attempt + 1} failed to get transcript for video ID {video_id}: {e}")
            if attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt)
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"Max retries reached. Could not retrieve transcript.\n{traceback.format_exc()}")
                print("Could not retrieve transcript after multiple retries.")
                return None
    return None

def save_transcript_to_file(transcript, filename='transcription.txt'):
    """
    Saves the transcript to a file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            text = ' '.join(entry['text'] for entry in transcript)
            f.write(text)
        print(f"Transcript saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving transcript to {filename}: {e}")
        print(f"Error saving transcript to {filename}: {e}")

def main():
    url = 'https://youtu.be/LI57EB_T38c?si=o3tQVSdDKPhY18WP'
    video_id = get_youtube_id_pytube(url)
    if video_id:
        print(f"URL: {url} -> Video ID: {video_id}")
        transcript = get_transcript(video_id)
        if transcript:
            pass
        else:
            print("Could not retrieve transcript. Skipping summarization.")
    else:
        print(f"Could not extract video ID from URL: {url}")

if __name__ == "__main__":
    main()




