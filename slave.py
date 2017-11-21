from __future__ import print_function

import grpc
import time
import logging
import sys
import masterslave_pb2
import masterslave_pb2_grpc

if (len(sys.argv) != 2):
    print("usage: python slave.py host")
    sys.exit(1)
host = sys.argv[1]

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Slave is launching")

def execute_task(taskname, sleeptime):
  logger.info("Slave started task %s", taskname)
  time.sleep(sleeptime)
  logger.info("Slave completed task %s", taskname)

def run():
  channel = grpc.insecure_channel(host + ':50051')
  stub = masterslave_pb2_grpc.TaskSchedulerStub(channel)
  for i in range(5):
    response = stub.SendTask(masterslave_pb2.TaskRequest(slaveid='slave1'))
    taskname = response.taskname
    sleeptime = response.sleeptime
    execute_task(taskname, sleeptime)
    response = stub.SendStatus(masterslave_pb2.StatusRequest(slaveid='slave1', taskname=taskname))

if __name__ == '__main__':
  run()
