from __future__ import print_function

import grpc

import masterslave_pb2
import masterslave_pb2_grpc


def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = masterslave_pb2_grpc.TaskSchedulerStub(channel)
  for i in range(100):
    response = stub.SendTask(masterslave_pb2.TaskRequest(slaveid='slaveid'))
    print("taskname=" + response.taskname + " " + "sleeptime=" + str(response.sleeptime))

if __name__ == '__main__':
  run()
