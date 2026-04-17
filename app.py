import streamlit as st
import whisper
from moviepy import VideoFileClip
from transformers import pipeline
import os

st.title("🎓 Lecture Video → Notes AI")

uploaded_file = st.file_uploader("Upload Lecture Video", type=["mp4", "mov", "avi"])

if uploaded_file:
    # Save video
    with open("video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded!")

    # Extract audio
    st.write("🔊 Extracting audio...")
    video = VideoFileClip("video.mp4")

    audio_path = "audio.mp3"   # ✅ add this line

    audio = video.audio
    audio.write_audiofile(audio_path)

    audio.close()
    video.close()

    # Speech to text
    st.write("🧠 Converting speech to text...")
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path, task="translate")
    text = result["text"]

    # Summarization
    st.write("✍️ Generating summary...")
    summarizer = pipeline("text-generation", model="google/flan-t5-base")

    # Split long text
    max_chunk = 1000
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]

    final_summary = ""
    for chunk in chunks:
        prompt = "Summarize this lecture into clear notes:\n" + chunk
        summary = summarizer(prompt, max_length=200)[0]['generated_text']
        final_summary += summary + " "

    # Output
    st.subheader("📄 Transcript")
    st.write(text)

    st.subheader("✨ Notes")
    st.write(final_summary)

    # Cleanup
    import time

# Wait and safely delete
time.sleep(2)

try:
    os.remove("video.mp4")
except:
    pass

try:
    os.remove("audio.mp3")
except:
    pass