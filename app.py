import streamlit as st
import ollama as ol
import os
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

MODEL = os.getenv("MODEL")

# ---------------------------
# Text To Speech
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

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask your HR question:")

# Submit button
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

        # Voice output
        speak(response)

        # Save history
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))

# Chat History
st.subheader("📜 Chat History")

for sender, msg in st.session_state.history:
    st.write(f"**{sender}:** {msg}")
