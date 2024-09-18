
#Original Chatbot

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from TTS import convertTTS
from STT import convertSTT
import streamlit as st
import os
import time
import threading  # Import the threading module
import playAudio


# Load environment values
load_dotenv()

os.environ["HF_HOME"] = "E:/Cache"  # Set the path to your desired cache directory
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # LangSmith: automatically trace for all codes executed
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")  # To store monitoring results of chatbot calls for analysis via LangSmith

gKey = os.getenv("GROQ_API_KEY")
if gKey is None:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

gModel = os.getenv("MODEL_NAME")
if gModel is None:
    raise ValueError("MODEL_NAME is not set in the .env file.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def typewriter_effect(text, placeholder):
    for i in range(len(text) + 1):
        placeholder.write(text[:i])
        time.sleep(0.05)

def play_audio(filename):
    playAudio.play_audio(filename)

def main():
    with st.sidebar:
        st.header("GROQ chatbot with Listen feature :books:")
        st.subheader("Developed by Kartikeya Dubey")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/kartikeyadubey/)")
        st.markdown("[GitHub](https://github.com/kartikeya-dubey)")

    askText = st.chat_input("Ask me something?")

    tts_dummy = convertTTS(askText)
    print(tts_dummy)
    transcribedQuery = convertSTT(tts_dummy)
    print(transcribedQuery)

    if askText:
        chat = ChatGroq(temperature=0, groq_api_key=gKey, model_name=gModel)

        system = "You are a helpful assistant. You give short and precise answers to human queries."
        human = "{query}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

        chain = prompt | chat

        response = chain.invoke({"query": askText})

        ttsFile = convertTTS(response.content)
        print("ttsFile: ",ttsFile)

        st.session_state.chat_history.append({"role": "human", "content": askText})
        st.session_state.chat_history.append({"role": "ai", "content": response.content})

        # Store the response content in the session state
        st.session_state.response_content = response.content

        # Launch the audio file in a separate thread
        audio_thread = threading.Thread(target=play_audio, args=(ttsFile,))
        audio_thread.start()

    # Display chat messages in a conversation chain format
    for idx, chat_message in enumerate(st.session_state.chat_history):
        if chat_message["role"] == "human":
            st.write(f"User: {chat_message['content']}")
        else:
            if idx == len(st.session_state.chat_history) - 1 and askText:
                # Last AI message with typewriter effect
                placeholder = st.empty()
                typewriter_effect(f"AI: {chat_message['content']}", placeholder)
            else:
                st.write(f"AI: {chat_message['content']}")

if __name__ == '__main__':
    main()
