import streamlit as st
import re
from gtts import gTTS
import io
import os
from moviepy.editor import *
import math

# --- Page Configuration ---
st.set_page_config(
    page_title="PressPlay AI",
    page_icon="🎬",
    layout="wide"
)

# --- Language Dictionary ---
LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Bengali (বাংলা)": "bn",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te",
    "Kannada (ಕನ್ನಡ)": "kn",
    "Gujarati (ગુજરાતી)": "gu",
    "Marathi ( मराठी)": "mr",
    "Malayalam (മലയാളം)": "ml",
    "Punjabi (ਪੰਜਾਬੀ)": "pa",
    "Urdu (اردو)": "ur",
    "Odia (ଓଡ଼IA)": "or",
}

# --- Helper Functions ---
def parse_text_to_sentences(text):
    """Splits text into sentences."""
    text = re.sub(r'(\.+|!|\?)(\s|(?=[\r\n]{2,}))', r'\1|', text)
    text = re.sub(r'(\r\n|\n){2,}', '|', text)
    sentences = text.split('|')
    return [s.strip() for s in sentences if s.strip()]

def cleanup_files(paths):
    """Removes temporary files."""
    for path in paths:
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                st.warning(f"Could not delete temp file: {path} ({e})")

def save_uploaded_files(uploaded_files):
    """Saves uploaded files to temp paths and returns the paths."""
    temp_paths = []
    for i, file in enumerate(uploaded_files):
        # Use a consistent naming convention
        path = f"temp_upload_{i}.jpg" 
        try:
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            temp_paths.append(path)
        except Exception as e:
            st.error(f"Error saving uploaded file: {e}")
    return temp_paths

# --- Page Functions ---

def show_home_page():
    """Displays the Home Page content."""
    st.markdown(
        """
        <div style="position: relative; border-radius: 1rem; overflow: hidden; background-image: linear-gradient(to right, #3b82f6, #8b5cf6); padding: 3rem 5rem; text-align: center; color: white; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);">
            <h1 style="font-size: 3.75rem; font-weight: 800; margin-bottom: 1rem;">
                Bring Information to Life
            </h1>
            <p style="font-size: 1.5rem; color: #dbeafe; margin-bottom: 2rem; max-width: 48rem; margin-left: auto; margin-right: auto;">
                Automatically convert static PIB press releases into dynamic, multilingual videos in seconds.
            </p>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.subheader("Project Features")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="background-color: #1f2937; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.75rem;">🌍</span> Multilingual Voices
                </h3>
                <p style="color: #9ca3af;">
                    Select from 13+ languages, including Hindi, Tamil, Bengali, and more, using Google's TTS engine.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="background-color: #1f2937; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.75rem;">🖼️</span> Custom Backgrounds
                </h3>
                <p style="color: #9ca3af;">
                    Upload your own background images. The app will automatically cycle through them with smooth crossfade transitions.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div style="background-color: #1f2937; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                <h3 style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <span style="font-size: 1.5rem; margin-right: 0.75rem;">📥</span> Downloadable Video
                </h3>
                <p style="color: #9ca3af;">
                    Generate and download a real, high-quality MP4 video file, complete with audio and text overlays.
                </p>
            </div>
            """, unsafe_allow_html=True
        )

def show_create_page():
    """Displays the main Video Generation Page."""
    st.title("🎬 Create Your Video")
    
    col1, col2 = st.columns([0.4, 0.6]) # Left column 40%, Right 60%
    
    with col1:
        st.subheader("1. Configuration")
        
        with st.container(border=True, height=650):
            # Language Selection
            selected_language_name = st.selectbox(
                "Select Language",
                options=list(LANGUAGES.keys())
            )
            lang_code = LANGUAGES[selected_language_name]
            
            # Image Upload
            uploaded_files = st.file_uploader(
                "Select Background Images",
                accept_multiple_files=True,
                type=["jpg", "jpeg", "png"]
            )
            
            # Text Input
            script_text = st.text_area(
                "Paste Press Release Text",
                height=250,
                value="The Union Cabinet, chaired by the Prime Minister, has approved a landmark scheme. This initiative aims to empower millions. The government has allocated a significant budget for this purpose. Online registration portals will be launched next month."
            )
            
            generate_button = st.button("Generate Full Video", type="primary", use_container_width=True)

    with col2:
        st.subheader("2. Generated Video")
        video_placeholder = st.empty()
        video_placeholder.info("Your generated video and download link will appear here.")

    # --- Generation Logic ---
    if generate_button:
        # --- 1. Validate Inputs ---
        if not script_text.strip():
            st.error("Please enter some text in the text area.")
        elif not uploaded_files:
            st.error("Please upload at least one background image.")
        else:
            temp_files = [] # To store paths for cleanup
            video_path = "final_pib_video.mp4"
            
            try:
                # --- 2. Save Uploaded Images ---
                with st.spinner("Step 1/4: Loading images..."):
                    temp_image_paths = save_uploaded_files(uploaded_files)
                    if not temp_image_paths:
                        st.error("Could not save uploaded images. Please try again.")
                        st.stop()
                    temp_files.extend(temp_image_paths)

                # --- 3. Generate Audio ---
                with st.spinner(f"Step 2/4: Generating '{selected_language_name}' audio..."):
                    sentences = parse_text_to_sentences(script_text)
                    if not sentences:
                        st.error("No sentences found in text. Cannot proceed.")
                        st.stop()
                    
                    full_text_for_audio = " ".join(sentences)
                    tts = gTTS(text=full_text_for_audio, lang=lang_code, slow=False)
                    
                    audio_bytes_io = io.BytesIO()
                    tts.write_to_fp(audio_bytes_io)
                    audio_bytes_io.seek(0)
                    
                    audio_path = "temp_audio.mp3"
                    temp_files.append(audio_path)
                    with open(audio_path, 'wb') as f:
                        f.write(audio_bytes_io.read())
                    
                    # Display audio immediately
                    st.toast("Audio generated successfully!")
                    col1.audio(audio_bytes_io, format='audio/mp3')

                # --- 4. Create Video Scenes ---
                with st.spinner("Step 3/4: Creating video scenes... (This is the longest step)"):
                    audio_clip = AudioFileClip(audio_path)
                    # Estimate duration per scene.
                    scene_duration = audio_clip.duration / len(sentences)
                    
                    video_clips = []
                    crossfade_duration = 0.5 # 0.5 second crossfade
                    
                    for i, sentence in enumerate(sentences):
                        # Cycle through the uploaded images
                        img_path = temp_image_paths[i % len(temp_image_paths)]
                        
                        # Create ImageClip
                        img_clip = ImageClip(img_path, plugin="pillow").set_duration(scene_duration).resize(height=720)
                        # Resize to a standard 16:9 width based on the 720 height
                        img_clip = img_clip.fx(vfx.crop, width=1280, height=720, x_center=img_clip.w/2, y_center=img_clip.h/2)

                        # Add Ken Burns effect (slow zoom-in)
                        img_clip_zoomed = img_clip.fx(vfx.resize, 1.1) # Zoom to 110%
                        img_clip = CompositeVideoClip([img_clip_zoomed.set_position(("center", "center"))], size=(1280, 720))
                        
                        # Create TextClip
                        txt_clip = TextClip(
                            sentence,
                            font='Arial-Bold',
                            fontsize=36,
                            color='white',
                            bg_color='rgba(0, 0, 0, 0.6)',
                            size=(1200, None), # 1200px width, auto-height
                            method='caption'
                        ).set_duration(scene_duration).set_position(('center', 0.8), relative=True)
                        
                        # Compose the scene
                        scene = CompositeVideoClip([img_clip, txt_clip])
                        
                        # Add crossfade
                        if video_clips: # Add fade-in only from the second clip onwards
                            scene = scene.fx(vfx.fadein, crossfade_duration)

                        video_clips.append(scene)

                # --- 5. Assemble Final Video ---
                with st.spinner("Step 4/4: Assembling final video..."):
                    # The crossfade effect is handled by overlapping clips
                    final_video = concatenate_videoclips(video_clips, method="compose", padding=-crossfade_duration)
                    final_video = final_video.set_audio(audio_clip)
                    
                    temp_files.append(video_path)
                    
                    final_video.write_videofile(
                        video_path,
                        codec="libx264",
                        audio_codec="aac",
                        temp_audiofile='temp-audio.m4a', 
                        remove_temp=True,
                        fps=24
                    )
                    
                    audio_clip.close()
                    final_video.close()
                    
                    # Display the final video
                    video_file = open(video_path, 'rb')
                    video_bytes = video_file.read()
                    video_placeholder.video(video_bytes)
                    
                    # Add the download button
                    video_placeholder.download_button(
                        label="Download Generated Video (.mp4)",
                        data=video_bytes,
                        file_name="pib_generated_video.mp4",
                        mime="video/mp4"
                    )
                    st.success("Generation Complete!")

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                if "ImageMagick" in str(e):
                     st.error("This error often means ImageMagick is not installed on your system. Please see the 'How It Works' page for setup instructions.")
            
            finally:
                # Clean up all temporary files
                cleanup_files(temp_files)
                if os.path.exists("temp-audio.m4a"):
                    os.remove("temp-audio.m4a")

def show_how_it_works_page():
    """Displays the 'How It Works' Page."""
    st.title("💡 How It Works")
    
    st.markdown("""
    This application is a powerful prototype that combines several Python libraries to create a video from text. Here's a breakdown of the process and the tools used.
    """)
    
    st.subheader("The Generation Pipeline")
    st.markdown("""
    When you click "Generate Full Video", the following steps happen:

    1.  **Image Loading:** The images you uploaded are saved to temporary files on the server.
    2.  **Sentence Parsing:** Your script is split into individual sentences. This will determine the "scenes" of your video.
    3.  **Audio Generation:** The *entire* script is sent to the Google Text-to-Speech (`gTTS`) API, which returns a single `.mp3` file of the full audio in the language you selected.
    4.  **Scene Creation:** The app divides the total audio duration by the number of sentences to get an "average duration" for each scene.
    5.  **Video Assembly:** The app loops through each sentence and:
        * Takes one of your uploaded images.
        * Applies a slow "Ken Burns" (zoom) effect.
        * Overlays the sentence text on top with a semi-transparent background.
        * Sets the scene's duration to the "average duration" calculated in Step 4.
    6.  **Final Render:** All the individual scenes are stitched together with a smooth crossfade using `MoviePy`. The full `.mp3` audio is attached, and the final `.mp4` video is created.
    7.  **Display & Download:** The final video is displayed on the page, and a download button appears.
    """)
    
    st.subheader("Key Technologies Used")
    st.markdown("""
    * **Streamlit:** For creating this entire interactive web application.
    * **gTTS (Google Text-to-Speech):** For generating the multilingual audio.
    * **Pillow (PIL):** For reading and handling the uploaded images.
    * **OpenCV (cv2):** Used by `MoviePy` as a backend for reading and writing video frames.
    * **MoviePy:** The core engine for all video editing. It programmatically creates text overlays, composites scenes, adds crossfades, and renders the final MP4 file.
    """)
    
    st.warning("""
    **Important Setup Requirement: ImageMagick**

    `MoviePy`'s `TextClip` function (which creates the text overlays) **requires** a separate program called **ImageMagick** to be installed on the computer running this app.

    If you see an error related to "ImageMagick" or "policy.xml", it means this program is not installed. You must download and install it from the [official ImageMagick website](https://imagemagick.org/script/download.php).
    """)

def show_about_page():
    """Displays the 'About' Page."""
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    This project, "PressPlay AI," is a proof-of-concept designed to tackle a major challenge in public communication: **information accessibility**.
    
    Government bodies like the Press Information Bureau (PIB) release critical information as text-heavy articles. This format creates a barrier for citizens who speak one of India's 13+ regional languages, as well as for those who prefer more engaging video content.
    
    The full-scale version of this project would use a more sophisticated AI pipeline:
    
    * **Web Scraping** to automatically fetch press releases.
    * **AI Summarization** (Hugging Face Transformers) to create a concise script.
    * **High-Quality Neural TTS** (like AI4Bharat's models) for more natural voices.
    * **AI Image Generation** (Stable Diffusion) to create relevant visuals for each sentence.
    * **Asynchronous Task Queues** (Celery & Redis) to handle long video renders without making the user wait.
    
    This Streamlit prototype simulates the core user experience and proves that the video assembly portion is feasible using Python.
    """)

# --- Main App Logic (Navigation) ---

def main():
    # Sidebar Navigation
    st.sidebar.title("PressPlay AI")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Create Video", "How It Works", "About"],
        label_visibility="hidden"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("© 2024. This is a prototype project.")
    
    # Page Routing
    if page == "Home":
        show_home_page()
    elif page == "Create Video":
        show_create_page()
    elif page == "How It Works":
        show_how_it_works_page()
    elif page == "About":
        show_about_page()

if __name__ == "__main__":
    main()
