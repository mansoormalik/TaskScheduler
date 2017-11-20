"""
The generator script inserts 100 random tasks into mongodb.
"""
import string
import random
import pymongo
from pymongo import MongoClient
from random import randint

NUM_TASKS = 100
TASK_NAME_LENGTH = 32
MAX_TASK_DURATION_IN_SECS = 60

client = MongoClient('172.17.0.2', 27017)
db = client['scheduler']
tasks = db.tasks

for i in range(0,NUM_TASKS):
    taskname = ''.join(random.choice(string.ascii_lowercase) for _ in range(TASK_NAME_LENGTH))
    sleeptime = randint(0, MAX_TASK_DURATION_IN_SECS)
    task = {"taskname": taskname, "sleeptime": sleeptime, "state": "created", "host": ""}
    tasks.insert_one(task)





