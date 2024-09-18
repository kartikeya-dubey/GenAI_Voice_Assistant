# main.py (python example)
import json
import os
from dotenv import load_dotenv
from Helper.config import Config

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()

# Path to the audio file
AUDIO_FILE = Config.OUTPUT_AUDIO_TSS

def convertSTT(AUDIO_FILE):
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=Config.DEEPGRAM_API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        # STEP 4: Print the response
        json_response = response.to_json(indent=4)
        # Parse the JSON response
        data = json.loads(json_response)
        #print(data)

        # Extract the "transcript" value
        transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]

        # Print the extracted transcript
        #print(transcript)
        return transcript


    except Exception as e:
        print(f"Exception: {e}")


#if __name__ == "__main__": convertSTT(AUDIO_FILE)
