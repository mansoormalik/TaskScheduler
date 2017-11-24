# TaskScheduler

Docker Images
-------------------------
1. mongodb: the mongodb docker image is pulled from dockerhub
2. master: you can pull this image from docker.io/mansoormalik/master or build it using Dockerfile.master
3. slave: you can pull this image from docker.io/mansoormalik/slave or build it using Dockerfile.slave

The docker_build.sh script can be invoked to build the images for the master and slave on a local machine.

Driver
-------------------------
The driver.py program is used to launch container images and assists in testing by killing slave or master containers.


Inserting Tasks
-------------------------
The task_generator.py program is used to insert tasks into a mongodb instance.


Interprocess Communication
--------------------------
The master and slave communicate using gRPC. This provides a low-latency mechanism for the exchange of messages between the master and slave.

Master
--------------------
The master application is in master.py. The master node:
1. does not start or stop slave nodes
2. does not keep state related to slave nodes (state is captured in task structure via association of a task to a host) 
3. no explicit join or leave protocol is used

Slave
--------------------
The slave application is in slave.py. The slave nodes do not send a heartbeat to the master node as the master does not monitor the health of nodes. Instead, the following scheme is used to recover from failures. If a slave fails, the state of the task in mongodb that was (i) assigned to this host and (ii) was in a "running" state is transitioned to a "killed" state. The master is then responsible for fetching all killed tasks from mongodb and reassigning them to other slaves.

Joining or Leaving Cluster
-----------------------------
The slave nodes do not send an explicit join or leave message to the master node. The slave nodes are provided with the IP address and port of the master node. The slave nodes communicate with the master node using a wire protocol (gRPC).

The primary reason for this approach is that the slaves poll the master to see if a task is available for execution. If we had instead chosen a scheme where the master was assigning tasks to slaves then the master would need to keep track of which slaves were available. In this alternate scenario, we would have needed to devise a protocol where slaves would need to notify the master when they were joining or leaving a cluster.


Load Balancing
---------------
The number of tasks exceeds the number of slaves and the tasks are of different duration. The tasks are of equal priority. There is no interdependency between tasks and there is no requirement to schedule tasks based on their expected duration. We consider two options for distributing tasks:
1. Master assigns tasks to slaves
2. Slaves request tasks from master

The second option was selected due to its simplicity and the time constraints for implementing the system.


State Synchronization
----------------------
In our system, the state of a task changes from "created" to "running" when it is assigned to a slave. The state can then change again to either "killed" or "success". In addition, the task has a host assigned to it. For an unassigned task this field is empty. This will be updated once a slave is assigned to execute a task. It may need to be changed again if a slave dies and the task needs to be reassigned to another slave. Since either the master or one or more slaves can fail, the mongodb is used to ensure that the system is in a consistent state.

Failure and Recovery
----------------------------
Upon recovery, the master retrieves from the mongodb:
1. all unassigned tasks (state="created")
2. all killed tasks (state="killed")
These tasks are then reassiged to slaves.

At present, our implementation relies on the following workaround to handle the case of tasks in a "running" state when a master dies. These tasks are also marked as "killed". This is non-optimal as the tasks will have to be redone. But the scheme works and ensures that all tasks in the work queue are eventually completed. Given more time a more efficient scheme would have been implemented to ensure that these tasks do not have to be done a second time. The reason this is done is because when a communicate channel is broken between a master and slave, the slave can time out. Due to time constraints, a retry or recovery mechanism using gRPC was not implemented.

The recovery mechanism for the slave is simple as it is not responsible for maintaining any state. Any tasks that were in a "running" state are marked as killed. These tasks are reassigned by the master to another slave.

Logging
-------
A container running fluentd captures log events from the driver, master, and slave applications. All logs are stored in a JSON format. A sample log file is included in the github repository.