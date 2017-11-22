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

POLLING_INTERVAL_NO_TASKS_IN_SECS = 3
FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info(id + " is launching")


# if task queue was empty master will send empty taskname
# slave should wait for configurable interval and poll again
def execute_task(taskname, sleeptime, stub):
    if (len(taskname) == 0):
        time.sleep(POLLING_INTERVAL_NO_TASKS_IN_SECS)
    else:
        logger.info(f"{id} started task {taskname}")
        time.sleep(sleeptime)
        logger.info(f"{id} completed task {taskname}")
        stub.Status(masterslave_pb2.StatusRequest(slaveid=id, taskname=taskname))
        
def run():
    channel = grpc.insecure_channel(host + ':50051')
    grpc.channel_ready_future(channel).result()
    stub = masterslave_pb2_grpc.TaskSchedulerStub(channel)
    while True:
        response = stub.Task(masterslave_pb2.TaskRequest(slaveid=id))
        taskname = response.taskname
        sleeptime = response.sleeptime
        execute_task(taskname, sleeptime, stub)

if __name__ == '__main__':
    run()
