""" The generator script inserts 100 random tasks into mongodb."""

import string
import random
import pymongo
import sys
from pymongo import MongoClient
from random import randint

# modify parameters as required
NUM_TASKS = 20
TASK_NAME_LENGTH = 32
MAX_TASK_DURATION_IN_SECS = 10

if (len(sys.argv) != 3):
    print("usage: python task_generator.py host port")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

client = MongoClient(host, port)
db = client['scheduler']
tasknames = []

def random_unique_task_name():
    while True:
        taskname = ''.join(random.choice(string.ascii_lowercase) for _ in range(TASK_NAME_LENGTH))
        if (taskname not in tasknames):
            tasknames.append(taskname)
            return taskname

def random_sleep_time():
    return randint(1, MAX_TASK_DURATION_IN_SECS)

for i in range(0, NUM_TASKS):
    taskname = random_unique_task_name()
    sleeptime = random_sleep_time()
    task = {"taskname": taskname, "sleeptime": sleeptime, "state": "created", "host": ""}
    db.tasks.insert_one(task)




