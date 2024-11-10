import logging

from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from service.transcriber.abstract_classes import Transcriber

logger = logging.getLogger(__name__)


class TranscriptionServiceServicer(transcribe_pb2_grpc.TranscriptionServiceServicer):

    def __init__(self, transcriber: Transcriber):
        self._transcriber = transcriber

    def TranscribeByPath(self, request, context):
        lang = request.lang
        path = request.file_path
        logger.debug(f"VoskTranscriber: trying lang: {lang}, path: {path}")
        text = self._transcriber.transcribe_by_path(path=path, lang=lang)
        logger.debug(f"TranscribeByPath result: {text}")
        return transcribe_pb2.TranscriptionResponse(text=text)

    def TranscribeByBinary(self, request, context):
        lang = request.lang
        audio_data = request.audio_data
        logger.debug(f"VoskTranscriber: trying lang: {lang}, bytes length: {len(audio_data)}")
        text = self._transcriber.transcribe_by_binary(audio_data=audio_data, lang=lang)
        logger.debug(f"TranscribeByBinary result: {text}")
        return transcribe_pb2.TranscriptionResponse(text=text)

    def GetAvailableLanguages(self, request, context):
        return transcribe_pb2.AvailableLanguagesResponse(languages=self._transcriber.get_available_languages())
