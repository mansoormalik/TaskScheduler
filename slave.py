from __future__ import print_function

import grpc
import time

import masterslave_pb2
import masterslave_pb2_grpc

def execute_task(taskname, sleeptime):
  print("taskname = " + taskname)
  print("sleeping for " + str(sleeptime) + " secs")
  time.sleep(sleeptime)

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = masterslave_pb2_grpc.TaskSchedulerStub(channel)
  for i in range(5):
    response = stub.SendTask(masterslave_pb2.TaskRequest(slaveid='slave1'))
    taskname = response.taskname
    sleeptime = response.sleeptime
    execute_task(taskname, sleeptime)
    response = stub.SendStatus(masterslave_pb2.StatusRequest(slaveid='slave1', taskname=taskname))

if __name__ == '__main__':
  run()
