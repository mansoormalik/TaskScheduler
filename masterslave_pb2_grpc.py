# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import masterslave_pb2 as masterslave__pb2


class TaskSchedulerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Task = channel.unary_unary(
        '/TaskScheduler/Task',
        request_serializer=masterslave__pb2.TaskRequest.SerializeToString,
        response_deserializer=masterslave__pb2.TaskResponse.FromString,
        )
    self.Status = channel.unary_unary(
        '/TaskScheduler/Status',
        request_serializer=masterslave__pb2.StatusRequest.SerializeToString,
        response_deserializer=masterslave__pb2.StatusResponse.FromString,
        )


class TaskSchedulerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Task(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Status(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TaskSchedulerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Task': grpc.unary_unary_rpc_method_handler(
          servicer.Task,
          request_deserializer=masterslave__pb2.TaskRequest.FromString,
          response_serializer=masterslave__pb2.TaskResponse.SerializeToString,
      ),
      'Status': grpc.unary_unary_rpc_method_handler(
          servicer.Status,
          request_deserializer=masterslave__pb2.StatusRequest.FromString,
          response_serializer=masterslave__pb2.StatusResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'TaskScheduler', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))