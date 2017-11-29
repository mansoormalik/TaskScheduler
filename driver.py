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
MAX_SLAVE_CONTAINERS = 3
next_slave_idx = 0
mongo_client = None
db = None

#TODO: hardcoded values should be read from config file
logger = sender.FluentSender("scheduler", "172.17.0.2", 24224)
logger.emit(node_id,{"message":"driver is starting"})

def start_mongodb_container():
    global mongo_container
    global mongo_host
    global mongo_client
    global db
    cmd = "sudo docker run -d mongo"
    call(cmd, shell=True)
    cmd = "sudo docker ps -l -q"
    mongo_container = check_output(cmd, shell=True).strip().decode()
    logger.emit(node_id,{"message":"started mongod container",
                         "container_id":f"{mongo_container}"})
    cmd = "sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + mongo_container
    mongo_host = check_output(cmd, shell=True).strip().decode()
    mongo_client = MongoClient(mongo_host, mongo_port)
    db = mongo_client['scheduler']

def stop_mongodb_container():
    global mongo_container
    cmd = f"sudo docker stop {mongo_container}"
    call(cmd, shell=True)
    logger.emit(node_id,{"message": f"stopped mongo container {mongo_container}"})
    
def start_task_generator():
    cmd = f"python task_generator.py {mongo_host} {mongo_port}"
    check_output(cmd, shell=True)
    logger.emit(node_id,{"message": "executed task_generator.py"})

def mongodb_tasks_snapshot(filename):
    cmd = f"mongoexport --host {mongo_host} --db scheduler --collection tasks --out {filename}"
    call(cmd, shell=True)
    logger.emit(node_id,{"message": f"saved snapshot from scheduler.tasks collection to {filename}"})
    
def start_master_container():
    global master_container
    global master_host
    cmd = f"sudo docker run -d master python /opt/scheduler/master.py {mongo_host} {mongo_port}"
    call(cmd, shell=True)
    cmd = "sudo docker ps -l -q"
    master_container = check_output(cmd, shell=True).strip().decode()
    logger.emit(node_id,{"message":"started master container",
                         "container_id":f"{master_container}"})
    cmd = "sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + master_container
    master_host = check_output(cmd, shell=True).strip().decode()

def stop_master_container():
    global master_container
    cmd = f"sudo docker stop {master_container}"
    call(cmd, shell=True)
    logger.emit(node_id,{"message": f"stopped master container {master_container}"})
    
def start_slave_container():
    global next_slave_idx
    cmd = f"sudo docker run -d slave python /opt/scheduler/slave.py {master_host} slave-{next_slave_idx}"
    call(cmd, shell=True)
    cmd = "sudo docker ps -l -q"
    container = check_output(cmd, shell=True).strip().decode()
    logger.emit(node_id,{"message":f"started slave-{next_slave_idx} container",
                         "container_id":f"{container}"})
    slave_idx_to_container[next_slave_idx] = container
    next_slave_idx += 1

    
def start_slave_containers(num_containers):
    for idx in range(0, num_containers):
        start_slave_container()

def stop_slave_containers():
    for idx, container in slave_idx_to_container.items():
        cmd = f"sudo docker stop {container}"
        call(cmd, shell=True)
        logger.emit(node_id,{"message": f"stopped slave container {container}"})
        
def send_tasks_summary_to_log():
    created = db.tasks.count({"state":"created"})
    running = db.tasks.count({"state":"running"})
    killed = db.tasks.count({"state":"killed"})
    success = db.tasks.count({"state":"success"})
    logger.emit(node_id,{"message":"tasks summary", "created":f"{created}",
                         "running":f"{running}", "killed":f"{killed}",
                         "success":f"{success}"})

def is_task_queue_empty():
    created = db.tasks.count({"state":"created"})
    running = db.tasks.count({"state":"running"})
    killed = db.tasks.count({"state":"killed"})
    if (created == 0 and running == 0 and killed == 0):
        return True
    return False
        
    
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
            return
        counter -= 1

def kill_master_container():
    logger.emit(node_id,{"message":"killing master"})
    cmd = f"sudo docker rm -f {master_container}"
    call(cmd, shell=True)

def restart_after_killing_master_container():
    start_master_container()

def test_until_all_tasks_completed():
    counter = 0
    while (not is_task_queue_empty()):
        if (counter % 4 == 0):
            kill_master_container()
            send_tasks_summary_to_log()
            time.sleep(30)
            restart_after_killing_master_container()
            time.sleep(90)
        else:
            kill_random_slave_container()
            send_tasks_summary_to_log()
            time.sleep(30)
            start_slave_container()
            time.sleep(90)
        counter += 1    

if __name__ == '__main__':
    start_mongodb_container()
    start_task_generator()
    mongodb_tasks_snapshot("tasks-at-start.json")
    send_tasks_summary_to_log()
    start_master_container()
    start_slave_containers(MAX_SLAVE_CONTAINERS)
    time.sleep(60)
    test_until_all_tasks_completed()
    mongodb_tasks_snapshot("tasks-at-end.json")
    send_tasks_summary_to_log()
    stop_slave_containers()
    stop_master_container()
    stop_mongodb_container()
