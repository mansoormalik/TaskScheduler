# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: masterslave.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='masterslave.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x11masterslave.proto\"\x1e\n\x0bJoinRequest\x12\x0f\n\x07slaveid\x18\x01 \x01(\t\"\x0e\n\x0cJoinResponse\"#\n\x10HeartbeatRequest\x12\x0f\n\x07slaveid\x18\x01 \x01(\t\"\x13\n\x11HeartbeatResponse\"\x1e\n\x0bTaskRequest\x12\x0f\n\x07slaveid\x18\x01 \x01(\t\"3\n\x0cTaskResponse\x12\x10\n\x08taskname\x18\x01 \x01(\t\x12\x11\n\tsleeptime\x18\x02 \x01(\x05\"2\n\rStatusRequest\x12\x0f\n\x07slaveid\x18\x01 \x01(\t\x12\x10\n\x08taskname\x18\x02 \x01(\t\"\x10\n\x0eStatusResponse\">\n\x19\x41\x66terMasterFailureRequest\x12\x0f\n\x07slaveid\x18\x01 \x01(\t\x12\x10\n\x08taskname\x18\x02 \x01(\t\"\x1c\n\x1a\x41\x66terMasterFailureResponse\"\x14\n\x12\x41\x63knowledgeRequest\"\x15\n\x13\x41\x63knowledgeResponse2\xcd\x02\n\rTaskScheduler\x12%\n\x04Join\x12\x0c.JoinRequest\x1a\r.JoinResponse\"\x00\x12\x34\n\tHeartbeat\x12\x11.HeartbeatRequest\x1a\x12.HeartbeatResponse\"\x00\x12%\n\x04Task\x12\x0c.TaskRequest\x1a\r.TaskResponse\"\x00\x12+\n\x06Status\x12\x0e.StatusRequest\x1a\x0f.StatusResponse\"\x00\x12O\n\x12\x41\x66terMasterFailure\x12\x1a.AfterMasterFailureRequest\x1a\x1b.AfterMasterFailureResponse\"\x00\x12:\n\x0b\x41\x63knowledge\x12\x13.AcknowledgeRequest\x1a\x14.AcknowledgeResponse\"\x00\x62\x06proto3')
)




_JOINREQUEST = _descriptor.Descriptor(
  name='JoinRequest',
  full_name='JoinRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slaveid', full_name='JoinRequest.slaveid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=51,
)


_JOINRESPONSE = _descriptor.Descriptor(
  name='JoinResponse',
  full_name='JoinResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=67,
)


_HEARTBEATREQUEST = _descriptor.Descriptor(
  name='HeartbeatRequest',
  full_name='HeartbeatRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slaveid', full_name='HeartbeatRequest.slaveid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=104,
)


_HEARTBEATRESPONSE = _descriptor.Descriptor(
  name='HeartbeatResponse',
  full_name='HeartbeatResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=125,
)


_TASKREQUEST = _descriptor.Descriptor(
  name='TaskRequest',
  full_name='TaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slaveid', full_name='TaskRequest.slaveid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=127,
  serialized_end=157,
)


_TASKRESPONSE = _descriptor.Descriptor(
  name='TaskResponse',
  full_name='TaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='taskname', full_name='TaskResponse.taskname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sleeptime', full_name='TaskResponse.sleeptime', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=210,
)


_STATUSREQUEST = _descriptor.Descriptor(
  name='StatusRequest',
  full_name='StatusRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slaveid', full_name='StatusRequest.slaveid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='taskname', full_name='StatusRequest.taskname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=212,
  serialized_end=262,
)


_STATUSRESPONSE = _descriptor.Descriptor(
  name='StatusResponse',
  full_name='StatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=280,
)


_AFTERMASTERFAILUREREQUEST = _descriptor.Descriptor(
  name='AfterMasterFailureRequest',
  full_name='AfterMasterFailureRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='slaveid', full_name='AfterMasterFailureRequest.slaveid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='taskname', full_name='AfterMasterFailureRequest.taskname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=282,
  serialized_end=344,
)


_AFTERMASTERFAILURERESPONSE = _descriptor.Descriptor(
  name='AfterMasterFailureResponse',
  full_name='AfterMasterFailureResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=346,
  serialized_end=374,
)


_ACKNOWLEDGEREQUEST = _descriptor.Descriptor(
  name='AcknowledgeRequest',
  full_name='AcknowledgeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=376,
  serialized_end=396,
)


_ACKNOWLEDGERESPONSE = _descriptor.Descriptor(
  name='AcknowledgeResponse',
  full_name='AcknowledgeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=398,
  serialized_end=419,
)

DESCRIPTOR.message_types_by_name['JoinRequest'] = _JOINREQUEST
DESCRIPTOR.message_types_by_name['JoinResponse'] = _JOINRESPONSE
DESCRIPTOR.message_types_by_name['HeartbeatRequest'] = _HEARTBEATREQUEST
DESCRIPTOR.message_types_by_name['HeartbeatResponse'] = _HEARTBEATRESPONSE
DESCRIPTOR.message_types_by_name['TaskRequest'] = _TASKREQUEST
DESCRIPTOR.message_types_by_name['TaskResponse'] = _TASKRESPONSE
DESCRIPTOR.message_types_by_name['StatusRequest'] = _STATUSREQUEST
DESCRIPTOR.message_types_by_name['StatusResponse'] = _STATUSRESPONSE
DESCRIPTOR.message_types_by_name['AfterMasterFailureRequest'] = _AFTERMASTERFAILUREREQUEST
DESCRIPTOR.message_types_by_name['AfterMasterFailureResponse'] = _AFTERMASTERFAILURERESPONSE
DESCRIPTOR.message_types_by_name['AcknowledgeRequest'] = _ACKNOWLEDGEREQUEST
DESCRIPTOR.message_types_by_name['AcknowledgeResponse'] = _ACKNOWLEDGERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

JoinRequest = _reflection.GeneratedProtocolMessageType('JoinRequest', (_message.Message,), dict(
  DESCRIPTOR = _JOINREQUEST,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:JoinRequest)
  ))
_sym_db.RegisterMessage(JoinRequest)

JoinResponse = _reflection.GeneratedProtocolMessageType('JoinResponse', (_message.Message,), dict(
  DESCRIPTOR = _JOINRESPONSE,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:JoinResponse)
  ))
_sym_db.RegisterMessage(JoinResponse)

HeartbeatRequest = _reflection.GeneratedProtocolMessageType('HeartbeatRequest', (_message.Message,), dict(
  DESCRIPTOR = _HEARTBEATREQUEST,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:HeartbeatRequest)
  ))
_sym_db.RegisterMessage(HeartbeatRequest)

HeartbeatResponse = _reflection.GeneratedProtocolMessageType('HeartbeatResponse', (_message.Message,), dict(
  DESCRIPTOR = _HEARTBEATRESPONSE,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:HeartbeatResponse)
  ))
_sym_db.RegisterMessage(HeartbeatResponse)

TaskRequest = _reflection.GeneratedProtocolMessageType('TaskRequest', (_message.Message,), dict(
  DESCRIPTOR = _TASKREQUEST,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:TaskRequest)
  ))
_sym_db.RegisterMessage(TaskRequest)

TaskResponse = _reflection.GeneratedProtocolMessageType('TaskResponse', (_message.Message,), dict(
  DESCRIPTOR = _TASKRESPONSE,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:TaskResponse)
  ))
_sym_db.RegisterMessage(TaskResponse)

StatusRequest = _reflection.GeneratedProtocolMessageType('StatusRequest', (_message.Message,), dict(
  DESCRIPTOR = _STATUSREQUEST,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:StatusRequest)
  ))
_sym_db.RegisterMessage(StatusRequest)

StatusResponse = _reflection.GeneratedProtocolMessageType('StatusResponse', (_message.Message,), dict(
  DESCRIPTOR = _STATUSRESPONSE,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:StatusResponse)
  ))
_sym_db.RegisterMessage(StatusResponse)

AfterMasterFailureRequest = _reflection.GeneratedProtocolMessageType('AfterMasterFailureRequest', (_message.Message,), dict(
  DESCRIPTOR = _AFTERMASTERFAILUREREQUEST,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:AfterMasterFailureRequest)
  ))
_sym_db.RegisterMessage(AfterMasterFailureRequest)

AfterMasterFailureResponse = _reflection.GeneratedProtocolMessageType('AfterMasterFailureResponse', (_message.Message,), dict(
  DESCRIPTOR = _AFTERMASTERFAILURERESPONSE,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:AfterMasterFailureResponse)
  ))
_sym_db.RegisterMessage(AfterMasterFailureResponse)

AcknowledgeRequest = _reflection.GeneratedProtocolMessageType('AcknowledgeRequest', (_message.Message,), dict(
  DESCRIPTOR = _ACKNOWLEDGEREQUEST,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:AcknowledgeRequest)
  ))
_sym_db.RegisterMessage(AcknowledgeRequest)

AcknowledgeResponse = _reflection.GeneratedProtocolMessageType('AcknowledgeResponse', (_message.Message,), dict(
  DESCRIPTOR = _ACKNOWLEDGERESPONSE,
  __module__ = 'masterslave_pb2'
  # @@protoc_insertion_point(class_scope:AcknowledgeResponse)
  ))
_sym_db.RegisterMessage(AcknowledgeResponse)



_TASKSCHEDULER = _descriptor.ServiceDescriptor(
  name='TaskScheduler',
  full_name='TaskScheduler',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=422,
  serialized_end=755,
  methods=[
  _descriptor.MethodDescriptor(
    name='Join',
    full_name='TaskScheduler.Join',
    index=0,
    containing_service=None,
    input_type=_JOINREQUEST,
    output_type=_JOINRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Heartbeat',
    full_name='TaskScheduler.Heartbeat',
    index=1,
    containing_service=None,
    input_type=_HEARTBEATREQUEST,
    output_type=_HEARTBEATRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Task',
    full_name='TaskScheduler.Task',
    index=2,
    containing_service=None,
    input_type=_TASKREQUEST,
    output_type=_TASKRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Status',
    full_name='TaskScheduler.Status',
    index=3,
    containing_service=None,
    input_type=_STATUSREQUEST,
    output_type=_STATUSRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AfterMasterFailure',
    full_name='TaskScheduler.AfterMasterFailure',
    index=4,
    containing_service=None,
    input_type=_AFTERMASTERFAILUREREQUEST,
    output_type=_AFTERMASTERFAILURERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Acknowledge',
    full_name='TaskScheduler.Acknowledge',
    index=5,
    containing_service=None,
    input_type=_ACKNOWLEDGEREQUEST,
    output_type=_ACKNOWLEDGERESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASKSCHEDULER)

DESCRIPTOR.services_by_name['TaskScheduler'] = _TASKSCHEDULER

# @@protoc_insertion_point(module_scope)
