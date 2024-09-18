#Streamlit GUI for recording voice and hearing response

import streamlit as st
from pvrecorder import PvRecorder
#from config import Config
from Helper.playAudio import play_audio
from Helper.STT import convertSTT
from Helper.TTS import convertTTS
from Helper.config import Config
import wave
import struct
#from playAudio import play_audio
#from STT import convertSTT
#from TTS import convertTTS
#from config import Config

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import time
import threading

# Load environment values
load_dotenv()

gKey = Config.GROQ_API_KEY
if gKey is None:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

gModel = Config.MODEL_NAME
if gModel is None:
    raise ValueError("MODEL_NAME is not set in the .env file.")

class Recorder:

    def __init__(self, device_index=-1, frame_length=512):
        self.device_index = device_index
        self.frame_length = frame_length
        self.audio = []
        self.path = Config.INPUT_AUDIO_STT
        self.recorder = PvRecorder(device_index=self.device_index, frame_length=self.frame_length)
        self.isSaved = False

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # number of previous messages the chatbot will remember during the conversation
    conversational_memory_length = Config.CONVERSATIONAL_MEMORY_LENGTH
    chatbot_memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    def typewriter_effect(text):
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05)

    def play_audio(filename):
        play_audio(filename)



    def chatGroq(user_query):
        
        with st.status("Querrying the LLM..."):
            #askText = st.chat_input("Ask me something?")
            askText = user_query

            if askText:
                chatLLM = ChatGroq(temperature=0, groq_api_key=gKey, model_name=gModel)

                # Construct a prompt template using various components
                system = "You are a helpful assistant. You respond to human queries keeping it short and precise. You do not apologise or tell confidence level"
                human = "{query}"
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system),  # This is the persistent system prompt that is always included at the start of the chat
                        ('ai', "Hi, I am your AI Assistant. Please press the voice recording buttons to ask me something!"),
                        ("human", human),    # This template is where the user's current input will be injected into the prompt.
                        MessagesPlaceholder(variable_name="chat_history")  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.
                    ]
                )

                # Create a conversation chain using the LangChain LLM (Language Learning Model)
                chat = prompt | chatLLM
                

                # Invoke the chat chain with the input
                st.session_state.chat_history.append({"role": "human", "content": askText})
                response = chat.invoke({"query": askText, "chat_history": st.session_state.chat_history})
                print(st.session_state.chat_history)
                #print("Chatbot:", response, end="\n")

                #Call Deepgram TTS service
                #ttsFile = TTS.convertTTS(response.content)
                ttsFile = convertTTS(response.content)

                st.session_state.chat_history.append({"role": "ai", "content": response.content})

                # Store the response content in the session state
                st.session_state.response_content = response.content

                #Launch the audio file in a separate thread
                audio_thread = threading.Thread(target=play_audio, args=(ttsFile,))
                audio_thread.start()

        # Display chat messages in a conversation chain format
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                mssg = message["content"]
                if message['role'] == 'User':
                    st.write(mssg)
                else:
                    if message == st.session_state.chat_history[-1]: # Check if it's the last AI message
                        st.write_stream((Recorder.typewriter_effect(mssg)))
                    else:
                        st.write(mssg)


    def start_rec(self):
        try:
            self.recorder.start()
            st.session_state.recording = True
            st.write("Recording started...")

            while st.session_state.recording:
                frame = self.recorder.read()
                self.audio.extend(frame)
        except Exception as e:
            self.stop_rec()
            raise e

    def stop_rec(self):
        self.recorder.stop()
        with wave.open(self.path, 'w') as f:
            f.setparams((1, 2, 16000, 0, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(self.audio), *self.audio))
            #isSaved = st.write(f"Recording saved to {self.path}")

    def delete_recorder(self):
        self.recorder.delete()

# Initialize Streamlit session state
if "recorder" not in st.session_state:
    st.session_state.recorder = Recorder(device_index=-1, frame_length=512)
    st.session_state.recording = False

def start_recording():
    if not st.session_state.recording:
        try:
            st.session_state.recorder.start_rec()
        except Exception as e:
            st.write(f"An error occurred: {e}")

def stop_recording():
    if st.session_state.recording:
        st.session_state.recording = False
        try:
            st.session_state.recorder.stop_rec()
        except Exception as e:
            st.write(f"An error occurred: {e}")

# Streamlit interface
st.title("AI Voice Assistant :male-office-worker:")

with st.sidebar:
    st.header("Voice Assistant using GROQ and DeepGram :speaker:")
    st.subheader("Developed by Kartikeya Dubey")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/kartikeyadubey/)")
    st.markdown("[GitHub](https://github.com/kartikeya-dubey)")

if st.sidebar.button("Start Recording"):
    st.session_state.recorder = Recorder(device_index=-1, frame_length=512)  # Initialize recorder
    start_recording()

if st.sidebar.button("Stop Recording"):
    stop_recording()
    st.session_state.recorder.delete_recorder()  # Delete recorder after stopping recording
    path = Config.INPUT_AUDIO_STT

    transcript = convertSTT(path)

    st.chat_input(f"You asked: {transcript}")

    Recorder.chatGroq(transcript)