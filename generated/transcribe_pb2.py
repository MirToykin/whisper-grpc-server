# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: transcribe.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'transcribe.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10transcribe.proto\"F\n\x15TranscribePathRequest\x12\x11\n\tfile_path\x18\x01 \x01(\t\x12\x11\n\x04lang\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x07\n\x05_lang\"I\n\x17TranscribeBinaryRequest\x12\x12\n\naudio_data\x18\x01 \x01(\x0c\x12\x11\n\x04lang\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x07\n\x05_lang\"%\n\x15TranscriptionResponse\x12\x0c\n\x04text\x18\x01 \x01(\t2\xa2\x01\n\x14TranscriptionService\x12\x42\n\x10TranscribeByPath\x12\x16.TranscribePathRequest\x1a\x16.TranscriptionResponse\x12\x46\n\x12TranscribeByBinary\x12\x18.TranscribeBinaryRequest\x1a\x16.TranscriptionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transcribe_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRANSCRIBEPATHREQUEST']._serialized_start=20
  _globals['_TRANSCRIBEPATHREQUEST']._serialized_end=90
  _globals['_TRANSCRIBEBINARYREQUEST']._serialized_start=92
  _globals['_TRANSCRIBEBINARYREQUEST']._serialized_end=165
  _globals['_TRANSCRIPTIONRESPONSE']._serialized_start=167
  _globals['_TRANSCRIPTIONRESPONSE']._serialized_end=204
  _globals['_TRANSCRIPTIONSERVICE']._serialized_start=207
  _globals['_TRANSCRIPTIONSERVICE']._serialized_end=369
# @@protoc_insertion_point(module_scope)
