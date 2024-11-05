import os
import time
from urllib.parse import urlparse

import requests
import soundfile as sf


def is_wav_file(file_path: str):
    file_info = sf.info(file_path)
    return file_info.format.lower() == "wav"


def get_wav_path(path: str) -> str:
    data, samplerate = sf.read(path)
    wav_path = get_temp_file_name()
    sf.write(wav_path, data, samplerate, format="WAV", subtype="PCM_16")
    return wav_path


def get_temp_file_name(base_name: str = "temp_audio", ext: str = ".wav") -> str:
    timestamp = time.time()
    timestamp = str(timestamp).replace(".", "_")
    return f"{base_name}_{timestamp}{ext}"


def download_audio(url, save_path):
    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, "wb") as file:
        file.write(response.content)


def is_url(path):
    parsed = urlparse(path)
    return bool(parsed.scheme and parsed.netloc)


def get_file_extension_from_url(url):
    path = urlparse(url).path
    return os.path.splitext(path)[1]
