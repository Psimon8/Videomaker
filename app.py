import streamlit as st
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip
import os

# Create a Streamlit app
st.title("Text to Video Generator")
st.write("Enter your text and create a video")

# Input text
text = st.text_area("Enter the script here")

# Upload background media
background_option = st.selectbox("Choose background type", ["Image", "Video"])
background_file = st.file_uploader(f"Upload a {background_option}", type=["jpg", "jpeg", "png", "mp4"])

# Button to generate video
if st.button("Generate Video"):
    if text and background_file:
        try:
            # Text-to-speech conversion
            tts = gTTS(text, lang='en')
            audio_path = "temp_audio.mp3"
            tts.save(audio_path)
            
            audio_clip = AudioFileClip(audio_path)
            
            # Create video
            if background_option == "Image":
                image_path = "temp_image.jpg"
                with open(image_path, "wb") as f:
                    f.write(background_file.getvalue())
                
                image_clip = ImageClip(image_path).set_duration(audio_clip.duration)
                image_clip = image_clip.set_audio(audio_clip)
                
                final_clip = image_clip
                
            else:
                video_path = "temp_video.mp4"
                with open(video_path, "wb") as f:
                    f.write(background_file.getvalue())
                
                video_clip = VideoFileClip(video_path).subclip(0, audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                final_clip = video_clip
            
            final_clip.write_videofile("output_video.mp4", codec='libx264', fps=24)
            
            # Display video
            st.video("output_video.mp4")
            
            # Clean up temporary files
            os.remove(audio_path)
            if background_option == "Image":
                os.remove(image_path)
            else:
                os.remove(video_path)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide both text and background media")
