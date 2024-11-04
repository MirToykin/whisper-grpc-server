from grpc_api.server import serve
from service.transcriber.transcriber import WhisperTranscriber
from settings import WhisperModels


def start_grpc_server():
    transcriber = WhisperTranscriber(WhisperModels.BASE)
    serve(transcriber)


if __name__ == "__main__":
    start_grpc_server()
