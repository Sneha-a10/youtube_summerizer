import streamlit as st
import os
from backend.transcription import get_youtube_id_pytube, get_transcript, save_transcript_to_file
from backend.summary import create_summary_file
from cleanup import cleanup_files  # Import the cleanup function

# Function to load local CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page config
st.set_page_config(
    page_title="YouTube Summarizer",
    page_icon="▶️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load CSS file
local_css("style.css")

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

    # Cleanup files when a new URL is entered
    if url:
        files_to_delete = ['summary.txt', 'transcription.txt']
        cleanup_files(files_to_delete)

    # Buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        transcript_btn = st.button("Get Transcription", key="transcript")

    with col2:
        chat_btn = st.button("Chat with Video", key="chat")

    with col3:
        summary_btn = st.button("Get Summary", key="summary")

    # Processing
    if transcript_btn or summary_btn or chat_btn:
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
                        if os.path.exists('transcription.txt'):
                            try:
                                with open('transcription.txt', 'r', encoding='utf-8') as f:
                                    transcript_text = f.read()
                                st.text_area("", value=transcript_text, height=300, label_visibility="collapsed")

                                # Add download button for transcription
                                with open('transcription.txt', 'r', encoding='utf-8') as f:
                                    st.download_button(
                                        label="Download Transcription",
                                        data=f,
                                        file_name="transcription.txt",
                                        mime="text/plain",
                                    )
                            except FileNotFoundError:
                                st.markdown("""
                                <div class="error-container">
                                    <p class="error-title">Error</p>
                                    <p class="error-content">Transcription file not found.</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            transcript = get_transcript(url)
                            if transcript:
                                try:
                                    with open('transcription.txt', 'r', encoding='utf-8') as f:
                                        transcript_text = f.read()
                                    st.text_area("", value=transcript_text, height=300, label_visibility="collapsed")

                                    # Add download button for transcription
                                    with open('transcription.txt', 'r', encoding='utf-8') as f:
                                        st.download_button(
                                            label="Download Transcription",
                                            data=f,
                                            file_name="transcription.txt",
                                            mime="text/plain",
                                        )
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

                if chat_btn:
                    st.write("Chat functionality will be implemented here.")

                elif summary_btn:
                    with st.spinner("Generating summary..."):
                        if os.path.exists('summary.txt'):
                            try:
                                with open('summary.txt', 'r', encoding='utf-8') as summary_file:
                                    summary = summary_file.read()
                                st.markdown(summary)

                                # Add download button for summary
                                with open('summary.txt', 'r', encoding='utf-8') as f:
                                    st.download_button(
                                        label="Download Summary",
                                        data=f,
                                        file_name="summary.txt",
                                        mime="text/plain",
                                    )
                            except FileNotFoundError:
                                st.markdown("""
                                <div class="error-container">
                                    <p class="error-title">Error</p>
                                    <p class="error-content">Summary file not found.</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            if create_summary_file(url):
                                try:
                                    with open('summary.txt', 'r', encoding='utf-8') as summary_file:
                                        summary = summary_file.read()
                                    st.markdown(summary)

                                    # Add download button for summary
                                    with open('summary.txt', 'r', encoding='utf-8') as f:
                                        st.download_button(
                                            label="Download Summary",
                                            data=f,
                                            file_name="summary.txt",
                                            mime="text/plain",
                                        )
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

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()