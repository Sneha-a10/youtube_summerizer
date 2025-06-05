from openai import OpenAI

# import dotenv
# import os

# dotenv.load_dotenv()    
# openaikey = os.getenv('OPENAI_API_KEY')
# if not openaikey:
#     raise ValueError("OPENAI_API_KEY environment variable is not set.")
# client = OpenAI(api_key=openaikey) 



def load_transcript(filename='transcription.txt'):
    """Loads the transcript from a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            transcript = f.read()
        return transcript
    except FileNotFoundError:
        return None

def chat_with_transcript(user_question):
    """
    Enables chatting with the video transcript using OpenAI.
    """

    transcript_text = load_transcript()

    if not transcript_text:
         return "Error: Could not load transcript from file."

    system_prompt = """You are a helpful assistant that answers questions about a YouTube video.
    You are given the transcript of the video, and your task is to answer the user's question taking reference from the information in the transcript. Be concise and to the point. Give then information strictly from the transcript."""

    user_prompt = f"""
    User Question: {user_question}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1024,
            temperature=0.5,
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(f"OpenAI API error: {e}")  
        return f"Error: An error occurred during the chat: {e}"


def main():
    prompt = "What is the first step to being a good communicator?"
    answer = chat_with_transcript(prompt)
    print(f"User Question: {prompt}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
