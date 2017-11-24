# Fault Tolerant Distributed TaskScheduler

Overview
-----------
Distributed task queueing systems often consist of producer nodes that create tasks, worker nodes that execute tasks, and a queuing system that decouples producers and workers. Such systems should scale easily - it should be possible to add producer or worker nodes as needed. The system should also be highly available. Individual producers or workers can fail but the overall system should continue working.

In our implementation, we have a constraint that slaves (workers) cannot access mongodb. Only the master node can. Therefore, the master node + mongodb are behaving as a queueing system. We have no explicit producer nodes but the task_generator.py script simulates this behavior by inserting 100 tasks into mongodb. The master node pulls tasks from mongodb and keeps it in an internal queue. Upon requests from slaves, tasks are assigned. The master node updates mongodb as tasks are completed by slaves. The message exchanges between the master and slave are described in more detail later.

To simulate the fault-tolerance aspect of our implementation, we use the driver.py script. This is also described in more detail below.

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
The slave application is in slave.py. The slave nodes do not send a heartbeat to the master node as the master does not monitor the health of nodes. Instead, the following scheme is used to recover from failures. If a slave is killed, the state of the task in mongodb that was assigned to this host and was in a "running" state is transitioned to a "killed" state. The driver is responsible for killing the slave and for updating mongodb. The master is then responsible for fetching all killed tasks from mongodb and reassigning them to other slaves.

Master-Slave Communication
--------------------------
The master and slave communicate using gRPC. This provides a low-latency mechanism for the exchange of messages between the master and slave. This does however creates a tight coupling between a master and slave nodes which may not be desirable. However, given the time limitations in completing the implementation, this was viewed as acceptable.

The protocol between the master and slave is defined in the masterslave.proto file. It consists of:
1. a task request message that is initiated by a slave
   if the task queue is non-empty, the master responds by sending the first task in the queue
   if the task queue is empty, the master responds by sending an empty task (taskname="")
   the the task queue is empty, the slave waits for a small duration before trying again; for testing purposes the duration was set to 3 seconds
2. a status update message that is sent by the slave to the master when a task is completed
   

Cluster Membership
--------------------------
The slave nodes do not send an explicit join or leave message to the master node. The slave nodes are provided with the IP address and port of the master node. The slave nodes communicate with the master node using a wire protocol (gRPC).

The primary reason for this approach is that the slaves poll the master to see if a task is available for execution. If we had instead chosen a scheme where the master was assigning tasks to slaves then the master would need to keep track of which slaves were available. In this alternate scenario, we would have needed to mechanism where slaves would need to notify the master when they were joining or leaving a cluster.

Load Balancing
---------------
The number of tasks exceeds the number of slaves and the tasks are of different duration. The tasks are of equal priority. There is no interdependency between tasks and there is no requirement to schedule tasks based on their expected duration. Two schemes were considered for distributing tasks:
1. master assigns tasks to slaves
2. slaves request tasks from master

The second option was selected due to its simplicity and the time constraints for implementing the system.


Scalability
-----------
The system has the undesirable property that there is a single master servicing slave nodes. The system scalability is therefore limited by the load that can be handled by this master node.

High-Availability
-----------------
The system's availability is determined by the availability of the master node as it is a single point of failure. When a master fails, slaves are unable to obtain new tasks. The system can withstand the failure of a single slave nodes if other slave nodes are still available to execute tasks. 

State Synchronization
---------------------
In our system, the state of a task changes from "created" to "running" when it is assigned to a slave. The state can then change again to either "killed" or "success". In addition, the task has a host assigned to it. For an unassigned task this field is empty. This will be updated once a slave is assigned to execute a task. It may need to be changed again if a slave dies and the task needs to be reassigned to another slave. Since either the master or one or more slaves can fail, the mongodb is used to ensure that the system is in a consistent state.

Failure and Recovery
----------------------------
The driver program has a rudimentary test loop which kills a node every 60 secs. The master is selected 1 out of every 4 times. A random slave node is selected the other 3 times. The driver program restarts a new master or slave node 30 seconds after killing it.

Upon recovery, the master retrieves from the mongodb:
1. all unassigned tasks (state="created")
2. all killed tasks (state="killed")
These tasks are then reassiged to slaves.

At present, our implementation relies on the following workaround to handle the case of tasks in a "running" state when a master dies. These tasks are also marked as "killed". This is non-optimal as the tasks will have to be redone. But the scheme works and ensures that all tasks in the work queue are eventually completed. Given more time a more efficient scheme would have been implemented to ensure that these tasks do not have to be done a second time. The reason this is done is because when a communicate channel is broken between a master and slave, the slave can time out. Due to time constraints, a retry or recovery mechanism using gRPC was not implemented.

The recovery mechanism for the slave is simple as it is not responsible for maintaining any state. Any tasks that were in a "running" state are marked as killed. These tasks are reassigned by the master to another slave.

Logging
-------
A container running fluentd captures log events from the driver, master, and slave applications. All logs are stored in a JSON format. A sample log file is included in the github repository.

The logs show:
1. messages from the driver (starting containers, mappings between container ids and nodes, nodes being killed, task statistics in mongodb)
2. messages from the master (number of pending tasks in queue, assigning tasks upon requests from slaves)
3. messages from slaves (starting tasks, completing tasks)

For a production grade system, additional information would be included in the logs. In our case, the attributes in log messages were purposefully kept to a bare minimum so it would beeasy to monitor that the overall system was progressing in completing tasks despite failures of master and slave nodes.

