# Fault Tolerant Distributed Task Scheduler

Overview
-----------
Distributed task scheduling systems typically consist of producer nodes that submit tasks, worker nodes that execute tasks, and a queueing system that decouples producers and workers. Such systems should scale easily and it should be possible to add or remove producer or worker nodes to handle load fluctuations. These system should also be highly available. The overall system should continue operating even if individual producers or workers fail.

In our implementation, we have a constraint that slaves (workers) cannot access mongodb. Only the master node can. Therefore, the master and mongodb, combined together, is behaving as a queueing system. We have no explicit producer nodes but the task_generator.py script simulates this behavior by inserting 100 tasks into mongodb. The master node pulls tasks from mongodb and keeps it in an internal queue. Upon requests from slaves, tasks are assigned. The master node updates mongodb as tasks are completed by slaves. The message exchanges between the master and slave are described in more detail later.

To simulate the fault-tolerant aspect of our implementation, we use the driver.py script. This is also described in more detail below.

Docker Images
-------------------------
1. mongodb: the mongodb docker image is pulled from dockerhub
2. master: pull this image from docker.io/mansoormalik/master or build it using Dockerfile.master
3. slave: pull this image from docker.io/mansoormalik/slave or build it using Dockerfile.slave

The docker_build.sh script can be invoked to build the images for the master and slave on a local machine.

Driver
-------------------------
The driver.py program is used to launch containers. It also assists in testing by killing slave or master containers.

Inserting Tasks
----------------
The task_generator.py program is used to insert tasks into a mongodb instance.

Master
--------------------
The master application is in master.py. The master node:
1. does not start or stop slave nodes
2. does not keep state related to slave nodes (state is captured in a task data structure via association of a task to a host) 
3. no explicit join or leave protocol is used

Slave
--------------------
The slave application is in slave.py. The slave nodes send a heartbeat to the master node as the master monitors the health of nodes. The heartbeat interval is configurable but was set at 5 seconds for testing purposes. If 3 consecutive heartbeats are missed a slave is considered dead and any tasks that it was assigned that are in a running state are transitioned to killed. The master will eventually reassign killed tasks to other slaves.

Master-Slave Communication
--------------------------
The master and slave communicate using gRPC. This provides a low-latency mechanism for the exchange of messages between the master and slave. This creates a tight coupling between master and slave nodes which may not be desirable. However, given the time limitations in completing the implementation, this was viewed as acceptable.

The protocol between the master and slave is defined in the masterslave.proto file.
1. An acknowledge message is sent by the slave to the master to verify that a channel can be established. If this fails, the slave goes into a retry loop until the master can be reached.
2. A join request is sent by the slave to a master prior to requesting new tasks. This allows a master to do the required setup to monitor heartbeats from slaves.
3. A heartbeat request is sent by the slave to the master at regular intervals.
4. A task request message is sent by a slave to a master. If the task queue is non-empty, the master responds by sending a message that describes the first task (taskname, sleeptime) in its queue. If the task queue is empty, the master responds by sending an empty task (taskname=""). If the task queue is empty, the slave waits for a small duration before trying again. For testing purposes the duration was set to 3 seconds.
5. A status update message is sent by the slave to the master when a task is completed.
6. When a master is killed, a slave completes its task and goes into a loop waiting for the master to come back on line. When the master is reacheable again, the slave sends a AfterMasterFailure request which ensures that the master updates the state of this task to success in mongodb.

Cluster Membership
--------------------------
The slave nodes send an explicit join message to the master node prior to requesting tasks and also send a heartbeat message at periodic intervals. The slave nodes are provided with the IP address and port of the master node. The slave nodes communicate with the master node using a wire protocol (gRPC).

Load-Balancing
---------------
The number of tasks exceeds the number of slaves and the tasks are of different duration. The tasks are of equal priority. There is no interdependency between tasks and there is no requirement to schedule tasks based on their expected duration. Two schemes were considered for distributing tasks:
1. master assigns tasks to slaves
2. slaves request tasks from master

The second scheme was selected due to its simplicity and the time constraints for implementing the system.


Scalability
-----------
The system has the undesirable property that there is a single master servicing slave nodes. The system scalability is therefore limited by the load that can be handled by this master node.

High-Availability
-----------------
The system's availability is determined by the availability of the master node as it is a single point of failure. When a master fails, slaves are unable to obtain new tasks. The system can withstand the failure of a single slave as long as other slaves are available to execute tasks. 

State Synchronization
---------------------
Each task has a state that can change from created, running, killed, or success. Each task also has a host associated with it. The state changes based on actions taken by the slave, master, or mongodb node. The state can diverge momentarily between nodes but it must eventually become consistent.

In our system, a master node changes the state of a task from created to running when it is receives a task request from a slave. The master node then updates mongodb. The master node then responds back to the client with the task name and sleep duration. In this scenario, the following failures are possible:
1. The slave node dies after being assigned a task from the master. At this point the state is believed to be in a running state both by the master and mongodb. The slave has stopped sending heartbeats to the master. After 3 missed heartbeats, the master considers the slave to be dead and transitions the state of the task that was assigned to the slave from running to killed. At this piont, both the master and mongodb have a consistent and correct state. The task will eventually be reassigned to another slave and once the task has completed its state will be transitioned to success.
2. The master dies after assigning a task to a slave and updating mongodb but before the slave has completed its task. In this scenario, the task is shown as running. It will not be reassigned. When the master comes back on line, the slave will send a AfterMasterFailureRequest with the taskname. The master will then update the state in mongodb. At this point, the state will be consistent.

Failure and Recovery
----------------------------
The driver program has a rudimentary test loop which kills a node every 120 secs. The master is selected 1 out of every 4 times. A random slave node is selected the other 3 times. The driver program restarts a new master or slave node 30 seconds after killing it.

When a master is killed:
1. all slaves that had pending tasks continue until the tasks are completed
2. slaves then go into a retry loop waiting for the master to come back on line
3. when a master is back on line, it receives AfterMasterFailure messages
4. upon receiving these messages, the master updates the state of these tasks to success in mongodb

When a slave is killed:
1. the slave will stop sending heartbeat messages to the master
2. after 3 heartbeat messages are missed the master will update mongodb for this slave and mark any running task as killed
3. the master will eventually reassign the killed task to another slave
4. when the killed task is completed its state will be changed to success

Logging
-------
A container running fluentd captures log events from the driver, master, and slave applications. All logs are stored in a JSON format. A sample log file is included in the github repository.

The logs show:
1. messages from the driver (starting containers, mappings between container ids and nodes, nodes being killed, task statistics in mongodb)
2. messages from the master (number of pending tasks in queue, assigning tasks upon requests from slaves, marking slaves as dead after 3 missed heartbeats)
3. messages from slaves (starting tasks, completing tasks)

For a production grade system, additional information would be included in the logs. In our case, the attributes in log messages were purposefully kept to a bare minimum so it would be easy to monitor that the overall system was progressing in completing tasks despite failures of master and slave nodes.

MongoDB Snapshots
------------------
The mongodb_snapshots directory contain a snapshot of the tasks collection at the beginging and end of a test run.