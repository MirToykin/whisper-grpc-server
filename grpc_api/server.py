import logging
import os
import sys

import grpc
from concurrent import futures

import settings
from grpc_api.api import TranscriptionServiceServicer
from generated import transcribe_pb2 as transcribe_pb2
from generated import transcribe_pb2_grpc as transcribe_pb2_grpc
from grpc_reflection.v1alpha import reflection

from service.transcriber.vosk.transcriber import VoskTranscriber

logging.basicConfig(level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        transcriber = VoskTranscriber(models_data=settings.get_models_data())
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
        logger.info(f"gRPC server is running on port {port}...")
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info(f"server stopped")
    except Exception as e:
        logger.error(f"failed to run server: {str(e)}")
        sys.exit(1)
