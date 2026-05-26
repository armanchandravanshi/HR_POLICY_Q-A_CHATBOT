import streamlit as st
import ollama as ol
import os
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS

load_dotenv()

MODEL = os.getenv("MODEL")

# ---------------------------
# Voice input function
# ---------------------------
def voice_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return "Sorry, could not understand audio"


# ---------------------------
# Voice output function
# ---------------------------
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")

    audio_file = open("response.mp3", "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3")


# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(
    page_title="HR Chatbot",
    layout="centered"
)

st.title("🤖 HR Policy Q&A Chatbot")

mode = st.radio("Choose Mode:", ["Text", "Voice"])

# ---------------------------
# Session State
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------
# TEXT MODE
# ---------------------------
if mode == "Text":

    user_input = st.text_input("Ask your HR question:")

    if st.button("Submit") and user_input:

        with st.spinner("Thinking..."):

            st.write("### You:")
            st.write(user_input)

            ollama_response = ol.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Answer HR questions."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            response = ollama_response["message"]["content"]

            st.write("### Bot:")
            st.write(response)

            speak(response)

            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("Bot", response))


# ---------------------------
# VOICE MODE
# ---------------------------
elif mode == "Voice":

    if st.button("Speak"):

        user_input = voice_input()

        st.write("### You said:")
        st.write(user_input)

        with st.spinner("Thinking..."):

            ollama_response = ol.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Answer HR questions."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )

            response = ollama_response["message"]["content"]

            st.write("### Bot:")
            st.write(response)

            speak(response)

            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("Bot", response))


# ---------------------------
# Chat History
# ---------------------------
st.subheader("📜 Chat History")

for sender, msg in st.session_state.history:
    st.write(f"**{sender}:** {msg}")
