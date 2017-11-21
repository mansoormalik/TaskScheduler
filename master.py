from concurrent import futures
import time

import grpc

import masterslave_pb2
import masterslave_pb2_grpc

import sys
import pymongo
from pymongo import MongoClient

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

if (len(sys.argv) != 3):
    print("usage: python master.py host port")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

client = MongoClient(host, port)
db = client['scheduler']
tasks = []
nr_task = 0
    
for task in db.tasks.find({}):
    tasks.append(task)

class Master(masterslave_pb2_grpc.TaskSchedulerServicer):
    def SendTask(self, request, context):
        global nr_task
        global tasks
        task = tasks[nr_task]
        nr_task += 1
        return masterslave_pb2.TaskResponse(taskname=task['taskname'],sleeptime=task['sleeptime'])
    


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
            
