# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages_robocup_ssl_geometry_legacy.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import messages_robocup_ssl_geometry_pb2 as messages__robocup__ssl__geometry__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*messages_robocup_ssl_geometry_legacy.proto\x12\x1aRoboCup2014Legacy.Geometry\x1a#messages_robocup_ssl_geometry.proto\"\x8a\x03\n\x15SSL_GeometryFieldSize\x12\x12\n\nline_width\x18\x01 \x02(\x05\x12\x14\n\x0c\x66ield_length\x18\x02 \x02(\x05\x12\x13\n\x0b\x66ield_width\x18\x03 \x02(\x05\x12\x16\n\x0e\x62oundary_width\x18\x04 \x02(\x05\x12\x15\n\rreferee_width\x18\x05 \x02(\x05\x12\x12\n\ngoal_width\x18\x06 \x02(\x05\x12\x12\n\ngoal_depth\x18\x07 \x02(\x05\x12\x17\n\x0fgoal_wall_width\x18\x08 \x02(\x05\x12\x1c\n\x14\x63\x65nter_circle_radius\x18\t \x02(\x05\x12\x16\n\x0e\x64\x65\x66\x65nse_radius\x18\n \x02(\x05\x12\x17\n\x0f\x64\x65\x66\x65nse_stretch\x18\x0b \x02(\x05\x12#\n\x1b\x66ree_kick_from_defense_dist\x18\x0c \x02(\x05\x12)\n!penalty_spot_from_field_line_dist\x18\r \x02(\x05\x12#\n\x1bpenalty_line_from_spot_dist\x18\x0e \x02(\x05\"\x83\x01\n\x10SSL_GeometryData\x12@\n\x05\x66ield\x18\x01 \x02(\x0b\x32\x31.RoboCup2014Legacy.Geometry.SSL_GeometryFieldSize\x12-\n\x05\x63\x61lib\x18\x02 \x03(\x0b\x32\x1e.SSL_GeometryCameraCalibration')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_robocup_ssl_geometry_legacy_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SSL_GEOMETRYFIELDSIZE']._serialized_start=112
  _globals['_SSL_GEOMETRYFIELDSIZE']._serialized_end=506
  _globals['_SSL_GEOMETRYDATA']._serialized_start=509
  _globals['_SSL_GEOMETRYDATA']._serialized_end=640
# @@protoc_insertion_point(module_scope)
