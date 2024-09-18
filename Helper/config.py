import os
from dotenv import load_dotenv

class Config:

    #Project details
    LANGCHAIN_TRACING_V2_STATUS = "true"
    LANGCHAIN_PROJECT = "AI Voice Assistant"
    CACHE_LOCATION = "E:/Cache"


    # Model selection
    TRANSCRIPTION_MODEL = 'groq'  # Options: 'openai', 'groq', 'deepgram', 'fastwhisperapi' 'local'
    RESPONSE_MODEL = 'groq'       # Options: 'openai', 'groq', 'ollama', 'local'
    TTS_MODEL = 'deepgram'        # Options: 'openai', 'deepgram', 'elevenlabs', 'local', 'melotts'
    
    #GROQ Model
    MODEL_NAME="llama-3.1-8b-instant"
    CONVERSATIONAL_MEMORY_LENGTH = 10

    # API keys and paths
    LANGCHAIN_API_KEY = "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"
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

    #Groq response - TTS output file
    OUTPUT_AUDIO_TSS = "Helper\TTSAudio\ottsOutput.wav"

    #Recorder - STT input file
    INPUT_AUDIO_STT = "Helper\STTAudio\inputAudioSTT.wav"

    #Audio Player App- MVP.exe
    MVP_PATH = r"C:\Users\hp\Downloads\mpv-x86_64-v3-20240609-git-d2bd77a\mpv.exe"

    