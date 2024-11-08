### Generate GRPC code
```python -m grpc_tools.protoc -Iproto --python_out=generated --grpc_python_out=generated proto/transcribe.proto```

Then you need to change ```import transcribe_pb2 as transcribe__pb2```  
with ```from generated import transcribe_pb2 as transcribe__pb2```

### Build/push/run image example
Build: ```docker build -t mirtoykin/python-grpc-stt:latest .```   
Login: ```docker login```   
Push: ```docker push mirtoykin/python-grpc-stt:latest```  
Run: ```docker run --name transcriber --env-file /opt/transcriber/.env -v /opt/transcriber/vosk:/root/.cache/vosk -p 50052:50051 mirtoykin/python-grpc-stt:latest```

### Environment
* SERVER_PORT - port to run gRPC server on
* WHISPER_MODEL_TYPE - type of Whisper model (```tiny```, ```base```, ```small```, ```medium``` or ```large```)
* VOSK_MODEL_PATH - path to Vosk model to use