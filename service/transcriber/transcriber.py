import os

import whisper
from whisper import Whisper

from service.transcriber.abstract_classes import Transcriber
from settings import WhisperModels


class WhisperTranscriber(Transcriber):
    _instance = None
    _model: Whisper = None

    def __new__(cls, model_type: WhisperModels):
        if cls._instance is None:
            cls._instance: WhisperTranscriber = super(WhisperTranscriber, cls).__new__(cls)
            cls._instance._model = whisper.load_model(model_type.value)
        return cls._instance

    def transcribe_by_path(self, path: str, lang: str = None) -> str:
        result = self._model.transcribe(path, language=lang)
        return result["text"]

    def transcribe_by_binary(self, audio_data: bytes, lang: str = None) -> str:
        temp_file_path = "temp_audio.wav"
        with open(temp_file_path, "wb") as f:
            f.write(audio_data)
        try:
            result = self._model.transcribe(temp_file_path, language=lang)
            return result['text']
        finally:
            os.remove(temp_file_path)


