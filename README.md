# TaskScheduler

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
-------------------------
The task_generator.py program is used to insert tasks into a mongodb instance.

Master
--------------------
The master application is in master.py. The master node:
1. does not start or stop slave nodes
2. does not keep state related to slave nodes (state is captured in task structure via association of a task to a host) 
3. no explicit join or leave protocol is used

Slave
--------------------
The slave application is in slave.py. The slave nodes do not send a heartbeat to the master node as the master does not monitor the health of nodes. Instead, the following scheme is used to recover from failures. If a slave fails, the state of the task in mongodb that was assigned to this host and was in a "running" state is transitioned to a "killed" state. The master is then responsible for fetching all killed tasks from mongodb and reassigning them to other slaves.

Master-Slave Communication
--------------------------
The master and slave communicate using gRPC. This provides a low-latency mechanism for the exchange of messages between the master and slave. This is not a good design choice for a production grade system as it creates a tight coupling between the master and slave nodes. It was chosen due to time constraints in getting a minimal system up and running. For a production grade system, a better design choice is to use a managed message queueing system such as AWS SQS	.

Joining or Leaving Cluster
--------------------------
The slave nodes do not send an explicit join or leave message to the master node. The slave nodes are provided with the IP address and port of the master node. The slave nodes communicate with the master node using a wire protocol (gRPC).

The primary reason for this approach is that the slaves poll the master to see if a task is available for execution. If we had instead chosen a scheme where the master was assigning tasks to slaves then the master would need to keep track of which slaves were available. In this alternate scenario, we would have needed to mechanism where slaves would need to notify the master when they were joining or leaving a cluster. A system such as Zookeper could be a good choice for this scenario.


Load Balancing
---------------
The number of tasks exceeds the number of slaves and the tasks are of different duration. The tasks are of equal priority. There is no interdependency between tasks and there is no requirement to schedule tasks based on their expected duration. We consider two options for distributing tasks:
1. Master assigns tasks to slaves
2. Slaves request tasks from master

The second option was selected due to its simplicity and the time constraints for implementing the system.


State Synchronization
---------------------
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

The logs show:
1. messages from the driver program (starting containers, mappings between container ids and nodes, nodes being killed, task statistics in mongodb)
2. messages from the master (number of pending tasks in queue, assigning tasks upon requests from slaves)
3. messages from slaves (starting tasks, completing tasks)

For a production grade system, much more information would be included in the logs. In our case, the attributes in log messages were purposefully kept to a bare minimum so it would be obvious that the overall system was progressing in completing tasks despite failures of master and slave nodes.

Testing
-------
The driver program has a rudimentary test loop which kills a node every 60 secs. The master is selected 1 out of every 4 times. A random slave node is selected the other 3 times. The driver program restarts a new master or slave node 30 seconds after killing it.

