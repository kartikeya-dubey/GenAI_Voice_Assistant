#from .config import Config
from config import Config

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

from dotenv import load_dotenv
from TTS import convertTTS
import streamlit as st
import time
import threading  # Import the threading module

from playAudio import play_audio

#import TTS, STT, playAudio

# Load environment values
load_dotenv()

gKey = Config.GROQ_API_KEY
if gKey is None:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

gModel = Config.MODEL_NAME
if gModel is None:
    raise ValueError("MODEL_NAME is not set in the .env file.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# number of previous messages the chatbot will remember during the conversation
conversational_memory_length = Config.CONVERSATIONAL_MEMORY_LENGTH
chatbot_memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

def typewriter_effect(text, placeholder):
    for i in range(len(text) + 1):
        placeholder.write(text[:i])
        time.sleep(0.05)

def play_audio(filename):
    play_audio(filename)

#def main():
def chatGroq(user_query):
    with st.sidebar:
        st.header("GROQ chatbot with Speak feature :books:")
        st.subheader("Developed by Kartikeya Dubey")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/kartikeyadubey/)")
        st.markdown("[GitHub](https://github.com/kartikeya-dubey)")

    #askText = st.chat_input("Ask me something?")
    askText = user_query

    if askText:
        chatLLM = ChatGroq(temperature=0, groq_api_key=gKey, model_name=gModel)

        # Construct a prompt template using various components
        system = "You are a helpful assistant. You give short and precise answers to human queries."
        human = "{query}"
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),  # This is the persistent system prompt that is always included at the start of the chat
                ("human", human),    # This template is where the user's current input will be injected into the prompt.
                MessagesPlaceholder(variable_name="chat_history")  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.
            ]
        )

        # Create a conversation chain using the LangChain LLM (Language Learning Model)
        chat = prompt | chatLLM

        # Invoke the chat chain with the input
        st.session_state.chat_history.append({"role": "human", "content": askText})
        response = chat.invoke({"query": askText, "chat_history": st.session_state.chat_history})
        print("Chatbot:", response, end="\n")

        #Call Deepgram TTS service
        #ttsFile = TTS.convertTTS(response.content)
        # print("ttsFile:", ttsFile)

        st.session_state.chat_history.append({"role": "ai", "content": response.content})

        # Store the response content in the session state
        st.session_state.response_content = response.content

        #Launch the audio file in a separate thread
        #audio_thread = threading.Thread(target=play_audio, args=(ttsFile,))
        #audio_thread.start()

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
    chatGroq("What is the color of white rose?")
