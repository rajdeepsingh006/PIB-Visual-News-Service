# 🎬 PressPlay AI: Text-to-Video Generator

<div align="center">
  </div>

**PressPlay AI** is a Python application that automatically converts any text script into a downloadable `.mp4` video, complete with multilingual audio, dynamic background images, and synchronized text overlays.

This project was built to solve the challenge of making dense, text-based information (like government press releases) more accessible and engaging for a modern, multilingual audience.

## 🎯 About The Project

Government communications, like those from the Press Information Bureau (PIB), are often dense, text-heavy, and published in limited languages. This creates a huge accessibility barrier for a mobile-first, multilingual population that prefers video content.

> This tool empowers a user to paste **any** script, upload a few background images, select a language, and generate a dynamic, shareable video in minutes.

This repository contains two versions of the project:

* **`app.py` (Main Project):** A full-stack Streamlit application that generates a real, downloadable `.mp4` file.
* **`index.html` (Prototype):** A polished, multi-page HTML/JS/Tailwind prototype that *simulates* the video in-browser and provides a real `.mp3` audio download.

## ✨ Key Features (Streamlit App)

* **Multi-Page UI:** A clean, professional interface built with Streamlit, featuring Home, Create Video, and How-To pages.
* **Multilingual Audio:** Uses Google's TTS (`gTTS`) to generate audio in 13+ languages (Hindi, Tamil, Bengali, etc.).
* **Custom Image Backgrounds:** Upload your own set of images to be used as backgrounds for the video scenes.
* **Real Video Generation:** Uses `MoviePy` to programmatically create a high-quality `.mp4` file.
* **Dynamic Scenes:** Automatically creates text overlays, smooth **crossfade transitions**, and a "Ken Burns" (slow zoom) effect for each scene.
* **Downloadable Output:** A working `st.download_button` appears so you can save the final `final_pib_video.mp4` file.

## 🛠️ Technology Stack

* **Core:** Python
* **Web App / UI:** Streamlit
* **Video Assembly:** `MoviePy`
* **Audio Generation:** `gTTS` (Google Text-to-Speech)
* **Image Processing:** `OpenCV`, `Pillow`
