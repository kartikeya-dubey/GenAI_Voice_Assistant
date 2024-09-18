
#App.py with Streamlit working GUI for recording voice

import streamlit as st
from pvrecorder import PvRecorder
from config import Config
import wave
import struct
from playAudio import play_audio

class Recorder:
    def __init__(self, device_index=-1, frame_length=512):
        self.device_index = device_index
        self.frame_length = frame_length
        self.audio = []
        self.path = Config.INPUT_AUDIO_STT
        self.recorder = PvRecorder(device_index=self.device_index, frame_length=self.frame_length)
        self.isSaved = False

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
            isSaved = st.write(f"Recording saved to {self.path}")

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
st.title("Voice Recorder")

if st.sidebar.button("Start Recording"):
    st.session_state.recorder = Recorder(device_index=-1, frame_length=512)  # Initialize recorder
    start_recording()

if st.sidebar.button("Stop Recording"):
    stop_recording()
    st.session_state.recorder.delete_recorder()  # Delete recorder after stopping recording