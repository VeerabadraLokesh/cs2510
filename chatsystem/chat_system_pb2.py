# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat_system.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63hat_system.proto\x12\nchatsystem\"\x18\n\x06Status\x12\x0e\n\x06status\x18\x01 \x01(\x08\"\x19\n\x05Group\x12\x10\n\x08group_id\x18\x01 \x01(\t\"/\n\x0cGroupDetails\x12\x10\n\x08group_id\x18\x01 \x01(\t\x12\r\n\x05users\x18\x02 \x03(\t\"\x17\n\x04User\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"e\n\x07Message\x12\x10\n\x08group_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x15\n\rcreation_time\x18\x03 \x01(\x04\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x12\n\nmessage_id\x18\x05 \x01(\t2\xf1\x01\n\nChatServer\x12\x31\n\x07GetUser\x12\x10.chatsystem.User\x1a\x12.chatsystem.Status\"\x00\x12;\n\x08GetGroup\x12\x11.chatsystem.Group\x1a\x18.chatsystem.GroupDetails\"\x00\x30\x01\x12\x39\n\x0bGetMessages\x12\x11.chatsystem.Group\x1a\x13.chatsystem.Message\"\x00\x30\x01\x12\x38\n\x0bPostMessage\x12\x13.chatsystem.Message\x1a\x12.chatsystem.Status\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_system_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STATUS._serialized_start=33
  _STATUS._serialized_end=57
  _GROUP._serialized_start=59
  _GROUP._serialized_end=84
  _GROUPDETAILS._serialized_start=86
  _GROUPDETAILS._serialized_end=133
  _USER._serialized_start=135
  _USER._serialized_end=158
  _MESSAGE._serialized_start=160
  _MESSAGE._serialized_end=261
  _CHATSERVER._serialized_start=264
  _CHATSERVER._serialized_end=505
# @@protoc_insertion_point(module_scope)
