from typing import Callable

from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from service.transcriber.abstract_classes import Transcriber


class TranscriptionServiceServicer(transcribe_pb2_grpc.TranscriptionServiceServicer):

    def __init__(self, ru_transcriber: Transcriber, default_transcriber: Transcriber):
        self._ru_transcriber = ru_transcriber
        self._default_transcriber = default_transcriber

    def TranscribeByPath(self, request, context):
        lang = request.lang
        transcriber = self._get_transcriber(lang)
        text = transcriber.transcribe_by_path(path=request.file_path, lang=lang)
        return transcribe_pb2.TranscriptionResponse(text=text)

    def TranscribeByBinary(self, request, context):
        lang = request.lang
        transcriber = self._get_transcriber(lang)
        text = transcriber.transcribe_by_binary(audio_data=request.audio_data, lang=lang)
        return transcribe_pb2.TranscriptionResponse(text=text)

    def _get_transcriber(self, lang: str) -> Transcriber:
        if lang == "ru":
            return self._ru_transcriber
        else:
            return self._default_transcriber
    