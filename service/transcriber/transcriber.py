import os

import whisper

from service.transcriber.abstract_classes import Transcriber
from settings import WhisperModels


class WhisperTranscriber(Transcriber):
    _instance = None
    _model: WhisperModels = None

    def __new__(cls, model_type: WhisperModels):
        if cls._instance is None:
            cls._instance: WhisperTranscriber = super(WhisperTranscriber, cls).__new__(cls)
            cls._instance._model = whisper.load_model(model_type.value)
        return cls._instance

    def transcribe_by_path(self, path: str) -> str:
        result = self._model.transcribe(path)
        return result["text"]

    def transcribe_by_binary(self, audio_data: bytes) -> str:
        temp_file_path = "temp_audio.wav"
        with open(temp_file_path, "wb") as f:
            f.write(audio_data)
        try:
            result = self._model.transcribe(temp_file_path)
            return result['text']
        finally:
            os.remove(temp_file_path)


