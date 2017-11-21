# TaskScheduler

TBD: Description for a fault tolerant task scheduler...

Requirements:
3 Docker Images
(1) mongodb
(2) master: run a master program eg master.py
(3) slave: run a slave program eg. slave.py

slave cannot access the mongodb, only master can access mongodb

create an offline script to generate 100 "tasks" and insert into mongodb container
the task collection has the following fields
{
  taskname: eg task1
  sleeptime: eg. 60 seconds
  state: one of ['created', 'running', 'killed', 'success']
  host: eg slave1
}

initially only taskname, sleeptime, and state are present; taskname and sleeptime is randomly generated and state is 'created'
every time a task runs it will just sleep for the given sleeptime seconds
each slave can work on one task at a time
add more mongo fields or collections if necessary
slaves know the identity of master; master allows any number of slaves to join or leave
any component of the scheduler except the mongodb can be unavailable
if master becomes unavailable it should recover in a short period of time

during testing start one copy of master and 3 copies of slaves
for fault tolerance randomly docker rm -f master and some slave containers
then start the killed docker after some time

make sure:
1. all tasks eventually finish; the state in mongodb should be 'success'
2. killing master won't affect running tasks
3. killing a slave will kill tasks running on it
4. killed tasks will be rerun from scratch (sleep the whole time)

include mongodb entries in text format, all scripts, and logs showing master, slaves, and tasks status changes with timestamp:
1. master and slave launch and relaunch after kill
2. task state changes, eg placed on a slave, killed, finished



