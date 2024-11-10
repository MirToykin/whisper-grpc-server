import logging
from functools import wraps

from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from service.transcriber.abstract_classes import Transcriber
from service.transcriber.errors import TranscriptionError

logger = logging.getLogger(__name__)

def _handle_transcription_exceptions(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except TranscriptionError as e:
            return transcribe_pb2.TranscriptionResponse(status=False, error_code=e.error_code, error_description=str(e))
        except Exception as e:
            return transcribe_pb2.TranscriptionResponse(status=False, error_code=500, error_description=str(e))

    return wrapper


class TranscriptionServiceServicer(transcribe_pb2_grpc.TranscriptionServiceServicer):

    def __init__(self, transcriber: Transcriber):
        self._transcriber = transcriber

    @_handle_transcription_exceptions
    def TranscribeByPath(self, request, context):
        lang = request.lang
        path = request.file_path
        logger.debug(f"VoskTranscriber: trying lang: {lang}, path: {path}")
        text = self._transcriber.transcribe_by_path(path=path, lang=lang)
        logger.debug(f"TranscribeByPath result: {text}")
        return transcribe_pb2.TranscriptionResponse(text=text, status=True)

    @_handle_transcription_exceptions
    def TranscribeByBinary(self, request, context):
        lang = request.lang
        audio_data = request.audio_data
        logger.debug(f"VoskTranscriber: trying lang: {lang}, bytes length: {len(audio_data)}")
        text = self._transcriber.transcribe_by_binary(audio_data=audio_data, lang=lang)
        logger.debug(f"TranscribeByBinary result: {text}")
        return transcribe_pb2.TranscriptionResponse(text=text, status=True)

    def GetAvailableLanguages(self, request, context):
        return transcribe_pb2.AvailableLanguagesResponse(languages=self._transcriber.get_available_languages())
