### Generate GRPC code
```python -m grpc_tools.protoc -Iproto --python_out=generated --grpc_python_out=generated proto/transcribe.proto```

Then you need to change ```import transcribe_pb2 as transcribe__pb2```  
with ```from generated import transcribe_pb2 as transcribe__pb2``` in ```generated/transcribe_pb2_grpc.py```

### Build/push/run image example
Build: ```docker build -t mirtoykin/python-grpc-stt:latest .```   
Login: ```docker login```   
Push: ```docker push mirtoykin/python-grpc-stt:latest```  
Run: ```docker run --name transcriber --env-file /opt/transcriber/.env -v /opt/transcriber/vosk:/root/.cache/vosk -p 50052:50051 mirtoykin/python-grpc-stt:latest```  
Mount the directory with models on the host to the directory specified in the MODELS_PATH environment variable

### Environment
* SERVER_PORT - port to run gRPC server on
* MODELS_PATH - path to the directory with recognition models
* MODELS - information about models and languages in the following format: lang1:model1|lang2:model2|lang3:model3 (e.g. ru:vosk-model-small-ru-0.22|en:vosk-model-small-en-us-0.15)
* LOG_LEVEL - level of logging (CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET)