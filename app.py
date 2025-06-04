import streamlit as st
import os
from transcription import get_youtube_id_pytube, get_transcript, save_transcript_to_file
from summary import create_summary_file

# Page config
st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="▶️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match the design
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 600px;
    }

    .stApp > header {
        background-color: transparent;
    }

    .stApp {
        background-color: #f5f5f5;
    }

    .main-container {
        background-color: white;
        padding: 3rem 2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin: 1rem 0;
    }

    .header-section {
        text-align: center;
        margin-bottom: 3rem;
    }

    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 1rem;
    }

    .youtube-icon {
        background-color: #ff0000;
        color: white;
        padding: 8px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
    }

    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #000;
        margin: 0;
    }

    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-top: 8px;
    }

    .section-label {
        font-size: 20px;
        font-weight: 600;
        color: #000;
        margin-bottom: 8px;
    }

    .section-description {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 16px;
    }

    .stTextInput > div > div > input {
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 16px;
        font-size: 15px;
    }

    .stTextInput > div > div > input:focus {
        background-color: white;
        border-color: #3b82f6;
        box-shadow: none;
    }

    .stButton > button {
        background-color: #000;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 16px 24px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        margin: 4px 0;
    }

    .stButton > button:hover {
        background-color: #1f2937;
        border: none;
        color: white;
    }

    .result-container {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px;
        margin-top: 2rem;
    }

    .result-title {
        font-size: 18px;
        font-weight: 600;
        color: #000;
        margin-bottom: 16px;
    }

    .error-container {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 24px;
        margin-top: 2rem;
    }

    .error-title {
        font-size: 18px;
        font-weight: 600;
        color: #dc2626;
        margin-bottom: 16px;
    }

    .error-content {
        color: #dc2626;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Main app
def main():
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="header-section">
            <div class="logo-container">
                <span class="youtube-icon">▶</span>
                <h1 class="main-title">YouTube Summarizer</h1>
            </div>
            <p class="subtitle">Get transcriptions and summaries from any YouTube video</p>
        </div>
    """, unsafe_allow_html=True)

    # URL input section
    st.markdown('<p class="section-label">Enter YouTube URL</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-description">Paste a YouTube video link to get started</p>', unsafe_allow_html=True)

    url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        transcript_btn = st.button("Get Transcription", key="transcript")

    with col2:
        summary_btn = st.button("Get Summary", key="summary")

    # Processing
    if transcript_btn or summary_btn:
        if not url:
            st.markdown("""
            <div class="error-container">
                <p class="error-title">Error</p>
                <p class="error-content">Please enter a YouTube URL</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            video_id = get_youtube_id_pytube(url)
            if not video_id:
                st.markdown("""
                <div class="error-container">
                    <p class="error-title">Error</p>
                    <p class="error-content">Please enter a valid YouTube URL</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                if transcript_btn:
                    with st.spinner("Getting transcription..."):
                        transcript = get_transcript(video_id)
                        if transcript:
                            # Save transcript to file
                            save_transcript_to_file(transcript)

                            # Display transcript from file
                            try:
                                with open('transcription.txt', 'r', encoding='utf-8') as f:
                                    transcript_text = f.read()
                                    
                                st.text_area("", value=transcript_text, height=300, label_visibility="collapsed")

                            except FileNotFoundError:
                                st.markdown("""
                                <div class="error-container">
                                    <p class="error-title">Error</p>
                                    <p class="error-content">Transcription file not found.</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="error-container">
                                <p class="error-title">Error</p>
                                <p class="error-content">Could not get transcription. Video may not have captions available.</p>
                            </div>
                            """, unsafe_allow_html=True)

                elif summary_btn:
                    with st.spinner("Generating summary..."):
                        transcript = get_transcript(video_id)
                        if transcript:
                            # Save transcript to file
                            save_transcript_to_file(transcript)

                            # Create summary file
                            if create_summary_file():
                                # Read summary from file
                                try:
                                    with open('summary.txt', 'r', encoding='utf-8') as summary_file:
                                        summary = summary_file.read()

                                    st.markdown(summary)

                                except FileNotFoundError:
                                    st.markdown("""
                                    <div class="error-container">
                                        <p class="error-title">Error</p>
                                        <p class="error-content">Summary file not found.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="error-container">
                                    <p class="error-title">Error</p>
                                    <p class="error-content">Could not generate summary.</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="error-container">
                                <p class="error-title">Error</p>
                                <p class="error-content">Could not get transcription to summarize. Video may not have captions available.</p>
                            </div>
                            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()