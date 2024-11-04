### Generate GRPC code
```python -m grpc_tools.protoc -Iproto --python_out=generated --grpc_python_out=generated proto/transcribe.proto```

Then you need to change ```import transcribe_pb2 as transcribe__pb2```  
with ```from generated import transcribe_pb2 as transcribe__pb2```
