import subprocess
import time
import pymongo
import sys
from subprocess import call
from subprocess import check_output
from pymongo import MongoClient
from random import randint
from fluent import sender

node_id = "driver"
mongo_container = ""
mongo_host = ""
mongo_port = 27017
master_container = ""
master_host = ""
slave_idx_to_container = {}
MAX_SLAVE_CONTAINERS = 4
next_slave_idx = 0
mongo_client = None
db = None

logger = sender.FluentSender("scheduler", host="172.17.0.2", port=24224)
logger.emit(node_id,{"message":"driver is starting"})

def run_mongodb_container():
    global mongo_container
    global mongo_host
    global mongo_client
    global db
    cmd = "sudo docker run -d mongo"
    call(cmd, shell=True)
    cmd = "sudo docker ps -l -q"
    mongo_container = check_output(cmd, shell=True).strip().decode()
    cmd = "sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + mongo_container
    mongo_host = check_output(cmd, shell=True).strip().decode()
    mongo_client = MongoClient(mongo_host, mongo_port)
    db = mongo_client['scheduler']

def run_task_generator():
    cmd = f"python task_generator.py {mongo_host} {mongo_port}"
    check_output(cmd, shell=True)

def run_master_container():
    global master_container
    global master_host
    cmd = f"sudo docker run -d master python /opt/scheduler/master.py {mongo_host} {mongo_port}"
    call(cmd, shell=True)
    cmd = "sudo docker ps -l -q"
    master_container = check_output(cmd, shell=True).strip().decode()
    cmd = "sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + master_container
    master_host = check_output(cmd, shell=True).strip().decode()

def run_slave_container():
    global next_slave_idx
    cmd = f"sudo docker run -d slave python /opt/scheduler/slave.py {master_host} slave-{next_slave_idx}"
    call(cmd, shell=True)
    cmd = "sudo docker ps -l -q"
    container = check_output(cmd, shell=True).strip().decode()
    slave_idx_to_container[next_slave_idx] = container
    next_slave_idx += 1

    
def run_slave_containers(num_containers):
    for idx in range(0, num_containers):
        run_slave_container()

def kill_random_slave_container():
    num_containers = len(slave_idx_to_container)
    counter = randint(0, num_containers-1)
    for idx, container in slave_idx_to_container.items():
        if (counter == 0):
            cmd = f"sudo docker rm -f {container}"
            call(cmd, shell=True)
            slave_idx_to_container.pop(idx)
            host = "slave-" + str(idx)
            logger.emit(node_id,{"message":f"killing {host}"})
            for task in db.tasks.find({"host": host, "state": "running"}):
                id = task['_id']
                task['state'] = "killed"
                logger.emit(node_id,{"message":f"changing status of task {id} to killed"})
                db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)
            return
        counter -= 1

def kill_master_container():
    logger.emit(node_id,{"message":"killing master"})
    cmd = f"sudo docker rm -f {master_container}"
    call(cmd, shell=True)
    # all slaves will die due to channel failure with master so mark these tasks as failed
    # all tasks should either be in success, killed, or created state
    for task in db.tasks.find({"state": "running"}):
        id = task['_id']
        task['state'] = "killed"
        logger.emit(node_id,{"message":f"changing status of task {id} to killed"})
        db.tasks.update_one({'_id':id}, {"$set":task}, upsert=False)

def restart_after_killing_master_container():
    run_master_container()
    run_slave_containers(MAX_SLAVE_CONTAINERS)

def enter_testing_loop():
    counter = 0
    while True:
        if (counter % 4 == 0):
            kill_master_container()
            time.sleep(30)
            restart_after_killing_master_container()
            time.sleep(30)
        else:
            kill_random_slave_container()
            time.sleep(30)
            run_slave_container()
            time.sleep(30)
        counter += 1    

if __name__ == '__main__':
    run_mongodb_container()
    run_task_generator()
    run_master_container()
    run_slave_containers(MAX_SLAVE_CONTAINERS)
    time.sleep(60)
    enter_testing_loop()
    """
    sys.exit(0)
    time.sleep(5)
    kill_master_container()
    time.sleep(10)
    restart_after_killing_master_container()
    kill_random_slave_container()
    time.sleep(5)
    kill_random_slave_container()
    time.sleep(5)
    run_slave_container()
    """

