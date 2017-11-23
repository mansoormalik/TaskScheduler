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
    print("usage: python master.py host port")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
node_id = "master"

#TODO: hardcoded values should be read from config file
logger = sender.FluentSender("scheduler", host="172.17.0.2", port=24224)
logger.emit(node_id,{"message":"master is starting"})

CHECK_TASKS_INTERVAL_IN_SECS = 10
client = MongoClient(host, port)
db = client['scheduler']
taskname_to_task = {}
unassigned_tasks = deque()
tasklock = threading.Lock()

class Master(masterslave_pb2_grpc.TaskSchedulerServicer):
    def Task(self, request, context):
        nr_tasks = len(unassigned_tasks)
        if (nr_tasks > 0):
            logger.emit(node_id, {"message":f"{nr_tasks} tasks are queued"})
            tasklock.acquire()
            task = unassigned_tasks.pop()
            id = task['_id']
            taskname = task['taskname']
            sleeptime = task['sleeptime']
            task['host'] = request.slaveid
            task['state'] = "running"
            db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
            tasklock.release()
            logger.emit(node_id, {"message":f"assigned task {taskname} to {request.slaveid}"})
            return masterslave_pb2.TaskResponse(taskname=taskname, sleeptime=sleeptime)
        else:
            return masterslave_pb2.TaskResponse(taskname="", sleeptime=0)
    
    def Status(self, request, context):
        tasklock.acquire()
        task = taskname_to_task[request.taskname]
        id = task['_id']
        task['state'] = 'success'
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
        tasklock.release()
        return masterslave_pb2.StatusResponse()

def obtain_unassigned_tasks():
    tasklock.acquire()
    for task in db.tasks.find({"state":"created"}):
        taskname = task['taskname']
        if (taskname not in taskname_to_task):
            unassigned_tasks.append(task)
            taskname_to_task[task['taskname']] = task
    tasklock.release()

def obtain_killed_tasks():
    tasklock.acquire()
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
    tasklock.release()
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    masterslave_pb2_grpc.add_TaskSchedulerServicer_to_server(Master(), server)
    server.add_insecure_port('[::]:50051')
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
            
