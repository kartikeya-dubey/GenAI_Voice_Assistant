from pvrecorder import PvRecorder
from config import Config
import wave
import struct

class Recorder:
    def __init__(self, device_index=-1, frame_length=512):
        self.recorder = PvRecorder(device_index=device_index, frame_length=frame_length)
        self.audio = []
        self.path = Config.INPUT_AUDIO_STT

    def start_rec(self):
        try:
            self.recorder.start()
            print("Recording started...")

            while True:
                frame = self.recorder.read()
                self.audio.extend(frame)
        except KeyboardInterrupt:
            print("Recording stopped by user.")
            self.stop_rec()
        except Exception as e:
            self.recorder.stop()
            self.recorder.delete()
            raise e

    def stop_rec(self):
        self.recorder.stop()
        with wave.open(self.path, 'w') as f:
            f.setparams((1, 2, 16000, 0, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(self.audio), *self.audio))
        print(f"Recording saved to {self.path}")
        self.recorder.delete()

if __name__ == "__main__":

    recorder = Recorder(device_index=-1, frame_length=512)
    
    try:
        recorder.start_rec()
    except Exception as e:
        print(f"An error occurred: {e}")
