import os
import logging

import wave
import json
from typing import List

from vosk import Model, KaldiRecognizer

from service.transcriber.abstract_classes import Transcriber
from service.transcriber.vosk.helpers import is_wav_file, get_wav_path, get_temp_file_name, is_url_path, download_audio, \
    get_file_extension_from_url
from settings import ModelData

logger = logging.getLogger(__name__)


class VoskTranscriber(Transcriber):
    _instance = None
    _models: dict[str, Model] = None

    def __new__(cls, models_data: List[ModelData]):
        if len(models_data) == 0:
            raise Exception("VoskTranscriber: models data is not provided")

        if cls._instance is None:
            cls._instance: VoskTranscriber = super(VoskTranscriber, cls).__new__(cls)
            cls._instance._load_models(models_data=models_data)

        return cls._instance

    def _load_models(self, models_data: List[ModelData]):
        models = {}
        for m in models_data:
            lang = m.get("lang")
            model = m.get("model")

            if not (lang and model):
                logger.warning(f"Invalid model data, lang: {lang}, model: {model}")

            models[lang] = Model(model_path=model, lang=lang)

        if not models:
            raise Exception("failed to load Vosk models")

        logger.debug(f"Loaded Vosk models: {models}")
        self._models = models

    def transcribe_by_path(self, path: str, lang: str = None) -> str:
        is_url = is_url_path(path)
        if is_url:
            local_path = get_temp_file_name(base_name="source", ext=get_file_extension_from_url(path))
            download_audio(path, local_path)
            path = local_path

        if not is_wav_file(path):
            path = get_wav_path(path)

        transcription = self._handle_wave_file(path=path, model=self._get_model_by_lang(lang))
        os.remove(path)
        if is_url:
            os.remove(local_path)

        return transcription

    def transcribe_by_binary(self, audio_data: bytes, lang: str = None) -> str:
        temp_file_path = get_temp_file_name()
        with open(temp_file_path, "wb") as f:
            f.write(audio_data)
        try:
            return self._handle_wave_file(path=temp_file_path, model=self._get_model_by_lang(lang))
        finally:
            os.remove(temp_file_path)

    def _get_model_by_lang(self, lang: str | None) -> Model:
        if not lang:
            lang = "default"

        model = self._models.get(lang, None)
        if not Model:
            raise Exception(f'model for language "{lang}" not found')

        return model

    def _handle_wave_file(self, path: str, model: Model) -> str:
        with wave.open(path, "rb") as wf:
            ch_count = wf.getnchannels() != 1
            samp_width = wf.getsampwidth() != 2
            compression_type = wf.getcomptype()
            if ch_count or samp_width or compression_type != "NONE":
                print(
                    f"ERROR: Converted file must be WAV format mono PCM. "
                    f"Channels: {ch_count}, sample width: {samp_width}, compression: {compression_type}")
                return ""

            recognizer = KaldiRecognizer(model, wf.getframerate())
            data = wf.readframes(wf.getnframes())

            # Run transcription
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                transcription = json.loads(result).get("text", "")
            else:
                final_result = recognizer.FinalResult()
                transcription = json.loads(final_result).get("text", "")

            return transcription
