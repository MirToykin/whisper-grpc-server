import os

import wave
import json
from vosk import Model, KaldiRecognizer

from service.transcriber.abstract_classes import Transcriber
from service.transcriber.vosk.helpers import is_wav_file, get_wav_path, get_temp_file_name, is_url_path, download_audio, \
    get_file_extension_from_url


class VoskTranscriber(Transcriber):
    _instance = None
    _model: Model = None

    def __new__(cls, model_path: str):
        if cls._instance is None:
            cls._instance: VoskTranscriber = super(VoskTranscriber, cls).__new__(cls)
            cls._instance._model = Model(model_path=model_path, lang="ru")
        return cls._instance

    def transcribe_by_path(self, path: str, lang: str = None) -> str:
        is_url = is_url_path(path)
        if is_url:
            local_path = get_temp_file_name(base_name="source", ext=get_file_extension_from_url(path))
            download_audio(path, local_path)
            path = local_path

        if not is_wav_file(path):
            path = get_wav_path(path)

        transcription = self._handle_wave_file(path)
        os.remove(path)
        if is_url:
            os.remove(local_path)

        return transcription

    def transcribe_by_binary(self, audio_data: bytes, lang: str = None) -> str:
        temp_file_path = get_temp_file_name()
        with open(temp_file_path, "wb") as f:
            f.write(audio_data)
        try:
            return self._handle_wave_file(temp_file_path)
        finally:
            os.remove(temp_file_path)

    def _handle_wave_file(self, path: str) -> str:
        with wave.open(path, "rb") as wf:
            ch_count = wf.getnchannels() != 1
            samp_width = wf.getsampwidth() != 2
            compression_type = wf.getcomptype()
            if ch_count or samp_width or compression_type != "NONE":
                print(
                    f"ERROR: Converted file must be WAV format mono PCM. "
                    f"Channels: {ch_count}, sample width: {samp_width}, compression: {compression_type}")
                return ""

            recognizer = KaldiRecognizer(self._model, wf.getframerate())
            data = wf.readframes(wf.getnframes())

            # Run transcription
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                transcription = json.loads(result).get("text", "")
            else:
                final_result = recognizer.FinalResult()
                transcription = json.loads(final_result).get("text", "")

            return transcription

    @staticmethod
    def new(model_path):
        return VoskTranscriber(model_path=model_path)
