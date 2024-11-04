### Generate GRPC code
```python -m grpc_tools.protoc -Iproto --python_out=generated --grpc_python_out=generated proto/transcribe.proto```

Then you need to change ```import transcribe_pb2 as transcribe__pb2```  
with ```from generated import transcribe_pb2 as transcribe__pb2```

### Build/push/run image example
Build: ```docker build -t mirtoykin/python-whisper:tiny .```   
Login: ```docker login```   
Push: ```docker push mirtoykin/python-whisper:tiny```  
Run: ```docker run -p 50052:50051 mirtoykin/python-whisper:tiny```