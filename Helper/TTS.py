import os
import Helper.config as config
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv()

#text = "Hi, This is sample text for TTS service"

filename = config.Config.OUTPUT_AUDIO_TSS

def convertTTS(text):

    SPEAK_OPTIONS = {"text": text}
    
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=config.Config.DEEPGRAM_API_KEY)
        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-orion-en",
            encoding="linear16",
            container="wav"
        )
        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        return filename

    except Exception as e:
        print(f"Exception in TTS: {e}")

#if __name__ == "__main__": convertTTS(text)