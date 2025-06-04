from openai import OpenAI
import dotenv
import os

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
            # Use the initialized client to create the chat completion
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

def main():
    try:
        with open('transcription.txt', 'r') as file:
            text = file.read()
        
        if not text:
            print("The file is empty.")
            return
        
        summary = summarize_text_from_input(text)
        print("Summary: ", summary)
    
    except FileNotFoundError:
        print("Error: transcription.txt not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

