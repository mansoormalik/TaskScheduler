import time
import grpc
import masterslave_pb2
import masterslave_pb2_grpc
import sys
import pymongo
import logging
from pymongo import MongoClient
from concurrent import futures
from collections import deque

if (len(sys.argv) != 3):
    print("usage: python master.py host port")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Master is launching")

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

client = MongoClient(host, port)
db = client['scheduler']
tasks = {}
queue = deque()
    
for task in db.tasks.find({}):
    tasks[task['taskname']] = task
    queue.append(task)

class Master(masterslave_pb2_grpc.TaskSchedulerServicer):
    def SendTask(self, request, context):
        task = queue.pop()
        id = task['_id']
        task['host'] = request.slaveid
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
        logger.info("Master is placing task %s on slave", task['taskname'])
        return masterslave_pb2.TaskResponse(taskname=task['taskname'],sleeptime=task['sleeptime'])
    
    def SendStatus(self, request, context):
        task = tasks[request.taskname]
        id = task['_id']
        task['state'] = 'success'
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
        return masterslave_pb2.StatusResponse(taskname="ok")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    masterslave_pb2_grpc.add_TaskSchedulerServicer_to_server(Master(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
    
if __name__ == '__main__':
    serve()
            
