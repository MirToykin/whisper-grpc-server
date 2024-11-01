import os

import grpc
from concurrent import futures
from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from grpc_reflection.v1alpha import reflection
import whisper

# Load Whisper model
model = whisper.load_model("tiny")  # Use the model of your choice


class TranscriptionServiceServicer(transcribe_pb2_grpc.TranscriptionServiceServicer):
    def TranscribeByPath(self, request, context):
        result = model.transcribe(request.file_path, language="ru")
        return transcribe_pb2.TranscriptionResponse(text=result['text'])

    def TranscribeByBinary(self, request, context):
        temp_file_path = "temp_audio.wav"
        with open(temp_file_path, "wb") as f:
            f.write(request.audio_data)
        try:
            result = model.transcribe(temp_file_path)
            return transcribe_pb2.TranscriptionResponse(text=result['text'])
        finally:
            os.remove(temp_file_path)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transcribe_pb2_grpc.add_TranscriptionServiceServicer_to_server(
        TranscriptionServiceServicer(), server
    )

    # Enable reflection
    SERVICE_NAMES = (
        transcribe_pb2.DESCRIPTOR.services_by_name['TranscriptionService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
