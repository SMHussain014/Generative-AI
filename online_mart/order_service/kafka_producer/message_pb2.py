# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rmessage.proto\"\x83\x02\n\x05Order\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x17\n\nproduct_id\x18\x02 \x01(\x05H\x01\x88\x01\x01\x12\x14\n\x07user_id\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x15\n\x08quantity\x18\x04 \x01(\x05H\x03\x88\x01\x01\x12\x13\n\x06\x61mount\x18\x05 \x01(\x02H\x04\x88\x01\x01\x12\x13\n\x06status\x18\x06 \x01(\tH\x05\x88\x01\x01\x12&\n\toperation\x18\x07 \x01(\x0e\x32\x0e.OperationTypeH\x06\x88\x01\x01\x42\x05\n\x03_idB\r\n\x0b_product_idB\n\n\x08_user_idB\x0b\n\t_quantityB\t\n\x07_amountB\t\n\x07_statusB\x0c\n\n_operation*3\n\rOperationType\x12\n\n\x06\x43REATE\x10\x00\x12\n\n\x06UPDATE\x10\x01\x12\n\n\x06\x44\x45LETE\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'message_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OPERATIONTYPE._serialized_start=279
  _OPERATIONTYPE._serialized_end=330
  _ORDER._serialized_start=18
  _ORDER._serialized_end=277
# @@protoc_insertion_point(module_scope)
