from __future__ import print_function

import grpc
import time
import logging
import sys
import masterslave_pb2
import masterslave_pb2_grpc

if (len(sys.argv) != 3):
    print("usage: python slave.py host slaveid")
    sys.exit(1)
host = sys.argv[1]
id = sys.argv[2]

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info(id + " is launching")

def execute_task(taskname, sleeptime, stub):
  if (sleeptime == 0):
    time.sleep(1)
  else:
    logger.info(id + " started task %s", taskname)
    time.sleep(sleeptime)
    logger.info(id + " completed task %s", taskname)
    stub.SendStatus(masterslave_pb2.StatusRequest(slaveid=id, taskname=taskname))

def run():
  channel = grpc.insecure_channel(host + ':50051')
  stub = masterslave_pb2_grpc.TaskSchedulerStub(channel)
  while True:
    response = stub.SendTask(masterslave_pb2.TaskRequest(slaveid=id))
    taskname = response.taskname
    sleeptime = response.sleeptime
    execute_task(taskname, sleeptime, stub)

if __name__ == '__main__':
  run()
