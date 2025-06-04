# YouTube Summarizer

## Overview

This project provides a way to automatically generate summaries of YouTube videos by extracting the transcript and using the OpenAI API to create a concise summary.

## Features

- Extracts YouTube video ID from a given URL.
- Fetches the transcript of a YouTube video.
- Saves the transcript to a text file.
- Uses the OpenAI API to summarize the transcript.
- Saves the summary to a text file.
- Includes error logging and retry mechanisms for robustness.

## Setup

1.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your OpenAI API key:**

    -   Create a `.env` file in the project directory.
    -   Add your OpenAI API key to the `.env` file:

        ```
        OPENAI_API_KEY=YOUR_API_KEY
        ```

## Usage

1.  **Run the `Transcription.py` script to extract the transcript:**

    ```bash
    python Transcription.py
    ```

    This will save the transcript to `transcription.txt`.

2.  **Run the `summary.py` script to generate the summary:**

    ```bash
    python summary.py
    ```

    This will read the transcript from `transcription.txt`, generate a summary using the OpenAI API, and save the summary to `summary.txt`.

3. **Run the Application**

    ```bash
     streamlit run app.py 
    ```

The app will run on http://127.0.0.1:5000 by default.
## Error Handling

The scripts include error logging to `error.log`. If any errors occur during the execution, they will be logged in this file. The `Transcription.py` script also includes a retry mechanism for fetching the transcript from YouTube.


