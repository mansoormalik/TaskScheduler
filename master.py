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
from heartbeats import Heartbeats
from threading import Thread

if (len(sys.argv) != 3):
    print("usage: python master.py mongo_host mongo_port")
    sys.exit(1)

mongo_host = sys.argv[1]
mongo_port = int(sys.argv[2])
node_id = "master"

#TODO: hardcoded values should be read from config file
master_slave_port = 50051
HEARTBEAT_INTERVAL_IN_SECS = 5
MAX_MISSED_HEARTBEATS = 3
CHECK_TASKS_INTERVAL_IN_SECS = 10
logger = sender.FluentSender("scheduler", "172.17.0.2", 24224)
logger.emit(node_id,{"message":"master is starting"})
client = MongoClient(mongo_host, mongo_port)
db = client['scheduler']

# a queue of unassigned_tasks (state:{created,killed})
unassigned_tasks = deque()

# a dictonary used by the master for looking up tasks by tasknames
taskname_to_task = {}

# a dictionary used by the master to track heartbeats from slaves
slaveid_to_heartbeats = {}

# TODO: the current implementation does not use locks
#       documentation from google is sparse on gRCP and need more time to better understand how library
#       is multiplexing requests from clients and how its threading model is implemented
#       workaround for now is to set max_workers=1

class Master(masterslave_pb2_grpc.TaskSchedulerServicer):

    #TODO: need to check that the request is from a valid slave before assigning task
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

    #TODO: need to check that the request is from a valid slave before handling status update
    def Status(self, request, context):
        task = taskname_to_task[request.taskname]
        id = task['_id']
        task['state'] = 'success'
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
        return masterslave_pb2.StatusResponse()

    def Acknowledge(self, request, context):
        return masterslave_pb2.AcknowledgeResponse()

    #TODO: this works if master has actually failed and has restarted; it does not
    #      work if there was a network partition and master marked slave as failed due
    #      missed heartbeats and reassigned task; in that case this message should be
    #      ignored and the slave should be instructed to shut off
    def AfterMasterFailure(self, request, context):
        db.tasks.update({"taskname":request.taskname},{"$set": {"state":"success"}})
        logger.emit(node_id, {"message":f"setting {request.taskname} to success after master failure"})        
        return masterslave_pb2.AfterMasterFailureResponse()

    # TODO: implementation does not yet address the case where a slave may send multiple join requests
    def Join(self, request, context):
        heartbeats = Heartbeats()
        slaveid_to_heartbeats[request.slaveid] = heartbeats
        return masterslave_pb2.JoinResponse()

    # TODO: implementation ignores heartbeats from slaves that may have timed out from 3 missed heartbeats
    # but were not actually dead; add mechanism that tells the slave to shut off if it was marked dead
    def Heartbeat(self, request, context):
        if (request.slaveid in slaveid_to_heartbeats):
            heartbeats = slaveid_to_heartbeats[request.slaveid]
            heartbeats.set_new_heartbeat()
        return masterslave_pb2.HeartbeatResponse()

def send_tasks_summary_to_log():
    created = db.tasks.count({"state":"created"})
    running = db.tasks.count({"state":"running"})
    killed = db.tasks.count({"state":"killed"})
    success = db.tasks.count({"state":"success"})
    logger.emit(node_id,{"message":"tasks summary", "created":f"{created}",
                         "running":f"{running}", "killed":f"{killed}",
                         "success":f"{success}"})
    
def handle_max_missed_heartbeats(slaveid):
    for task in db.tasks.find({"host": slaveid, "state": "running"}):
        id = task['_id']
        taskname = task['taskname']
        task['state'] = "killed"
        logger.emit(node_id,{"message":f"task {taskname} assigned to {slaveid} is in running state"})
        logger.emit(node_id,{"message":f"changing state of task {taskname} to killed"})
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)

# this function is invoked in a seperate thread
# the Heartbeat class uses locks to ensure thread safety
def check_missed_heartbeats():
    while True:
        time.sleep(HEARTBEAT_INTERVAL_IN_SECS)
        now = time.time()
        dead = []
        for slaveid, heartbeats in slaveid_to_heartbeats.items():
            if (now > heartbeats.get_last_heartbeat() + HEARTBEAT_INTERVAL_IN_SECS):
                heartbeats.add_missed_heartbeat()
            if (heartbeats.get_missed_consec_heartbeats() >= MAX_MISSED_HEARTBEATS):
                msg = f"missed {MAX_MISSED_HEARTBEATS} consecutive heartbeats from {slaveid}"
                logger.emit(node_id, {"message": msg})
                handle_max_missed_heartbeats(slaveid)
                send_tasks_summary_to_log()
                dead.append(slaveid)
        for slaveid in dead:
            del slaveid_to_heartbeats[slaveid]
    
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
    Thread(target=check_missed_heartbeats).start()
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
