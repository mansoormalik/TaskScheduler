from __future__ import print_function
import grpc
import time
import sys
import masterslave_pb2
import masterslave_pb2_grpc
from fluent import sender

if (len(sys.argv) != 3):
    print("usage: python slave.py master_host slave_id")
    sys.exit(1)
master_host = sys.argv[1]
node_id = sys.argv[2]

#TODO: hardcoded values should be read from config file
master_slave_port = 50051
POLLING_INTERVAL_NO_TASKS_IN_SECS = 3
WAIT_AFTER_CONNECTION_FAILURE_IN_SECS = 5
logger = sender.FluentSender("scheduler", "172.17.0.2", 24224)
logger.emit(node_id,{"message":"slave is starting"})

channel = None
stub = None
response = None
taskname = ""
is_master_fail_during_task_exec = False

def start_task_execution_loop():
    global stub
    global taskname
    global is_master_fail_during_task_exec
    while True:
        taskname = ""
        is_master_fail_during_task_exec = False
        try:
            response = stub.Task(masterslave_pb2.TaskRequest(slaveid=node_id))
            taskname = response.taskname
            sleeptime = response.sleeptime
            # if task queue was empty master will send empty taskname
            # slave should wait for configurable interval and poll again
            if (len(taskname) == 0):
                time.sleep(POLLING_INTERVAL_NO_TASKS_IN_SECS)
            else:
                logger.emit(node_id, {"message": f"starting task {taskname}"})
                time.sleep(sleeptime)
                logger.emit(node_id, {"message": f"completed task {taskname}"})
                stub.Status(masterslave_pb2.StatusRequest(slaveid=node_id, taskname=taskname))
        except:
            if (len(taskname) != 0):
                is_master_fail_during_task_exec = True
            logger.emit(node_id, {"message": f"lost connection to master"})
            wait_and_run_later()

def try_server_connection():
    global channel
    global stub
    try:
        channel = grpc.insecure_channel(f"{master_host}:{master_slave_port}")
        stub = masterslave_pb2_grpc.TaskSchedulerStub(channel)
        stub.Acknowledge(masterslave_pb2.AcknowledgeRequest())
        return True
    except:
        return False

def wait_and_run_later():
    global is_master_fail_during_task_exec
    while True:
        logger.emit(node_id, {"message":
                              f"unable to connect to master, wait and try again"})
        time.sleep(WAIT_AFTER_CONNECTION_FAILURE_IN_SECS)
        if try_server_connection():
            break
    if (is_master_fail_during_task_exec):
        stub.AfterMasterFailure(masterslave_pb2.AfterMasterFailureRequest(slaveid=node_id,taskname=taskname))
    start_task_execution_loop()
    
def run():
    if try_server_connection():
        start_task_execution_loop()
    else:
        wait_and_run_later()

if __name__ == '__main__':
    run()
