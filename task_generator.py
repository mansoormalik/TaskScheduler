"""
The generator script inserts 100 random tasks into mongodb.
"""
import string
import random
import pymongo
import sys
from pymongo import MongoClient
from random import randint

NUM_TASKS = 100
TASK_NAME_LENGTH = 32
MAX_TASK_DURATION_IN_SECS = 60

if (len(sys.argv) != 3):
    print("usage: python task_generator.py hostname port")

hostname = sys.argv[1]
port = int(sys.argv[2])

client = MongoClient(hostname, port)
db = client['scheduler']
tasks = db.tasks
tasknames = []

def random_unique_task_name():
    while True:
        taskname = ''.join(random.choice(string.ascii_lowercase) for _ in range(TASK_NAME_LENGTH))
        if (taskname not in tasknames):
            tasknames.append(taskname)
            return taskname

def random_sleep_time():
    return randint(0, MAX_TASK_DURATION_IN_SECS)

for i in range(0, NUM_TASKS):
    taskname = random_unique_task_name()
    sleeptime = random_sleep_time()
    task = {"taskname": taskname, "sleeptime": sleeptime, "state": "created", "host": ""}
    tasks.insert_one(task)




