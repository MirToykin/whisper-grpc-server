from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from service.transcriber.abstract_classes import Transcriber


class TranscriptionServiceServicer(transcribe_pb2_grpc.TranscriptionServiceServicer):

    def __init__(self, transcriber: Transcriber):
        self._transcriber = transcriber

    def TranscribeByPath(self, request, context):
        text = self._transcriber.transcribe_by_path(path=request.file_path, lang=request.lang)
        return transcribe_pb2.TranscriptionResponse(text=text)

    def TranscribeByBinary(self, request, context):
        text = self._transcriber.transcribe_by_binary(audio_data=request.audio_data, lang=request.lang)
        return transcribe_pb2.TranscriptionResponse(text=text)
