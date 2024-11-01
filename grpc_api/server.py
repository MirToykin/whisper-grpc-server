import os

import grpc
from concurrent import futures

from grpc_api.api import TranscriptionServiceServicer
from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from grpc_reflection.v1alpha import reflection
from service.transcriber.abstract_classes import Transcriber


def serve(transcriber: Transcriber):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transcribe_pb2_grpc.add_TranscriptionServiceServicer_to_server(
        TranscriptionServiceServicer(transcriber=transcriber), server
    )

    # Enable reflection
    SERVICE_NAMES = (
        transcribe_pb2.DESCRIPTOR.services_by_name['TranscriptionService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    port = os.getenv("SERVER_PORT", "50051")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"gRPC server is running on port {port}...")
    server.wait_for_termination()
