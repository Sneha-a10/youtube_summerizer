from openai import OpenAI
import os
from transcription import get_transcript

# import dotenv

# dotenv.load_dotenv()    
# openaikey = os.getenv('OPENAI_API_KEY')
# if not openaikey:
#     raise ValueError("OPENAI_API_KEY environment variable is not set.")
# client = OpenAI(api_key=openaikey)  



def summarize_text_from_input(text):
        system_prompt = "I would like for you to assume the role of a teacher"
        user_prompt = f"""Generate a concise summary of the text below.
        Text: {text}

        Add a title to the summary.

        Make sure your summary has useful and true information about the main points of the topic.
        Begin with a short introduction explaining the topic. If you can, use bullet points to list important details,
        and finish your summary with a concluding sentence"""

        print('summarizing ... ')
        try:
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt}
                ],
                max_tokens=4096,
                temperature=1
            )
            summary = response.choices[0].message.content
            return summary
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Error during summarization."
        
def create_summary_file(url, transcript_filename='transcription.txt', summary_filename='summary.txt',):
    """
    Reads the transcript from a file, generates a summary, and saves it to another file.
    """
    if os.path.exists(summary_filename):
        print(f"{summary_filename} already exists. Skipping summarization.")
        return True

    try:
        get_transcript(url)
        with open(transcript_filename, 'r', encoding='utf-8') as file:
            text = file.read()

        if not text:
            print("The transcription file is empty.")
            return False

        summary = summarize_text_from_input(text)

        with open(summary_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(summary)

        print(f"Summary saved to {summary_filename}")
        return True

    except FileNotFoundError:
        print(f"Error: {transcript_filename} not found.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def main():
    create_summary_file()

if __name__ == "__main__":
    main()

