# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: products.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eproducts.proto\"\xd7\x02\n\x07Product\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x11\n\x04name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x18\n\x0b\x64\x65scription\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x12\n\x05price\x18\x04 \x01(\x02H\x03\x88\x01\x01\x12\x13\n\x06\x65xpiry\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x12\n\x05\x62rand\x18\x06 \x01(\tH\x05\x88\x01\x01\x12\x13\n\x06weight\x18\x07 \x01(\x02H\x06\x88\x01\x01\x12\x15\n\x08\x63\x61tegory\x18\x08 \x01(\tH\x07\x88\x01\x01\x12\x10\n\x03sku\x18\t \x01(\tH\x08\x88\x01\x01\x12&\n\toperation\x18\n \x01(\x0e\x32\x0e.OperationTypeH\t\x88\x01\x01\x42\x05\n\x03_idB\x07\n\x05_nameB\x0e\n\x0c_descriptionB\x08\n\x06_priceB\t\n\x07_expiryB\x08\n\x06_brandB\t\n\x07_weightB\x0b\n\t_categoryB\x06\n\x04_skuB\x0c\n\n_operation*3\n\rOperationType\x12\n\n\x06\x43REATE\x10\x00\x12\n\n\x06UPDATE\x10\x01\x12\n\n\x06\x44\x45LETE\x10\x02\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'products_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OPERATIONTYPE._serialized_start=364
  _OPERATIONTYPE._serialized_end=415
  _PRODUCT._serialized_start=19
  _PRODUCT._serialized_end=362
# @@protoc_insertion_point(module_scope)
