import time
import grpc
import masterslave_pb2
import masterslave_pb2_grpc
import sys
import pymongo
import threading

from pymongo import MongoClient
from concurrent import futures
from collections import deque
from fluent import sender

if (len(sys.argv) != 3):
    print("usage: python master.py mongo_host mongo_port")
    sys.exit(1)

mongo_host = sys.argv[1]
mongo_port = int(sys.argv[2])
node_id = "master"

#TODO: hardcoded values should be read from config file
master_slave_port = 50051
logger = sender.FluentSender("scheduler", "172.17.0.2", 24224)
logger.emit(node_id,{"message":"master is starting"})

CHECK_TASKS_INTERVAL_IN_SECS = 10
client = MongoClient(mongo_host, mongo_port)
db = client['scheduler']
# a queue of unassigned_tasks (state:{created,killed})
unassigned_tasks = deque()
# a dictonary used by the master for looking up tasks by tasknames
taskname_to_task = {}

# TODO: the current implementation does not use locks
#       documentation from google is sparse on gRCP and need more time to better understand how library
#       is multiplexing requests from clients and how its threading model is implemented
#       workaround for now is to set max_workers=1

class Master(masterslave_pb2_grpc.TaskSchedulerServicer):
    def Task(self, request, context):
        nr_tasks = len(unassigned_tasks)
        if (nr_tasks > 0):
            logger.emit(node_id, {"message":f"{nr_tasks} tasks are queued"})
            task = unassigned_tasks.pop()
            id = task['_id']
            taskname = task['taskname']
            sleeptime = task['sleeptime']
            task['host'] = request.slaveid
            task['state'] = "running"
            db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
            logger.emit(node_id, {"message":f"assigned task {taskname} to {request.slaveid}"})
            return masterslave_pb2.TaskResponse(taskname=taskname, sleeptime=sleeptime)
        else:
            return masterslave_pb2.TaskResponse(taskname="", sleeptime=0)
    
    def Status(self, request, context):
        task = taskname_to_task[request.taskname]
        id = task['_id']
        task['state'] = 'success'
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
        return masterslave_pb2.StatusResponse()

    def Acknowledge(self, request, context):
        return masterslave_pb2.AcknowledgeResponse()

    def AfterMasterFailure(self, request, context):
        db.tasks.update({"taskname":request.taskname},{"$set": {"state":"success"}})
        logger.emit(node_id, {"message":f"setting {request.taskname} to success after master failure"})        
        return masterslave_pb2.AfterMasterFailureResponse()

def obtain_unassigned_tasks():
    for task in db.tasks.find({"state":"created"}):
        taskname = task['taskname']
        if (taskname not in taskname_to_task):
            unassigned_tasks.append(task)
            taskname_to_task[task['taskname']] = task

def obtain_killed_tasks():
    for task in db.tasks.find({"state":"killed"}):
        taskname = task['taskname']
        if (taskname in taskname_to_task):
            existing = taskname_to_task[taskname]
            if (existing['state'] != "killed"):
                unassigned_tasks.append(task)
                taskname_to_task[taskname] = task
        else:
            unassigned_tasks.append(task)
            taskname_to_task[taskname] = task
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    masterslave_pb2_grpc.add_TaskSchedulerServicer_to_server(Master(), server)
    server.add_insecure_port(f"[::]:{master_slave_port}")
    server.start()
    try:
        while True:
            time.sleep(CHECK_TASKS_INTERVAL_IN_SECS)
            obtain_unassigned_tasks()
            obtain_killed_tasks();
    except KeyboardInterrupt:
        server.stop(0)
    
if __name__ == '__main__':
    obtain_unassigned_tasks()
    obtain_killed_tasks()
    serve()
