import streamlit as st
import ollama as ol
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
load_dotenv()

MODEL = os.getenv("MODEL")

engine = pyttsx3.init()

# Voice input function
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

# Voice output function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.set_page_config(page_title="HR Chatbot", layout="centered")

st.title("🤖 HR Policy Q&A Chatbot")

mode = st.radio("Choose Mode:", ["Text", "Voice"])

# Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# TEXT MODE
if mode == "Text":
    user_input = st.text_input("Ask your HR question:")

    if st.button("Submit") and user_input:
        with st.spinner("Thinking..."):
            st.write("You:", user_input)
            ollama = ol.chat(
                model=MODEL,
                messages=[{"role": "system", "content": "Answer HR questions."},
                          {"role": "user", "content": user_input}],
                stream=True,
                think=True
            )
            response = ""
            for chunk in ollama:
                response += chunk['message']['content']
            st.write("Bot:", response)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))

# VOICE MODE
elif mode == "Voice":
    if st.button("Speak"):
        user_input = voice_input()
        st.write("You said:", user_input)
        ollama = ol.chat(
            model=MODEL,
            messages=[{"role": "system", "content": "Answer HR questions."},
                          {"role": "user", "content": user_input}],
            stream=True,
            think=True
        )
        response = ""
        for chunk in ollama:
            response += chunk['message']['content']
        st.write("Bot:", response)

        speak(response)

        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Bot", response))
# Display chat history
st.subheader("Chat History")
for sender, msg in st.session_state.history:
    st.write(f"**{sender}:** {msg}")