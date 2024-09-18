from Helper.config import Config

import subprocess

def play_audio(filename):
    try:
        mpv_path = Config.MVP_PATH
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen([mpv_path, "--no-terminal", filename], startupinfo=startupinfo)

    except Exception as e:
        print(f"Exception: {e}")
            