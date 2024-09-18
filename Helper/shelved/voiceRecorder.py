
#Simple voice recording program from PvRecorder

from pvrecorder import PvRecorder
from Helper.config import Config
import wave
import struct

devices = PvRecorder.get_available_devices()

for device in devices:
    print(device, end="\n")

recorder = PvRecorder(device_index=-1, frame_length=512)
audio = []

path = Config.INPUT_AUDIO_STT

try:
    recorder.start()

    while True:
        frame = recorder.read() 
        audio.extend(frame)

#KeyboardInterrupt means ctrl+c to end voice recording
except KeyboardInterrupt:
    recorder.stop()
    with wave.open(path, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
finally:
    recorder.delete()
