#!/bin/bash

docker_run="sudo docker run --log-driver=fluentd -d"

# run fluentd container
#sudo docker run -it -p 24224:24224 -v $PWD/fluentd.conf:/fluentd/etc/fluentd.conf -e FLUENTD_CONF=fluentd.conf fluent/fluentd:latest

# run mongodb docker container
sudo docker run -d mongo
mongo_container=$(sudo docker ps -l -q)
mongo_host=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $mongo_container)
mongo_port=27017

# run task generator script
$(python task_generator.py $mongo_host $mongo_port)

# run master
master_run="python /opt/scheduler/master.py $mongo_host $mongo_port"
$docker_run master $master_run
master_container=$(sudo docker ps -l -q)
master_host=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $master_container)

# run slave
max_slaves=4
slave_nr=0
slave_containers=()
for i in `seq  $slave_nr $(($max_slaves-1))`; do
    $docker_run slave python /opt/scheduler/slave.py $master_host slave-$slave_nr
    slave_container=$(sudo docker ps -l -q)
    slave_containers+=($slave_container)
    slave_nr=$(($slave_nr+1))
done

for slave_container in "${slave_containers[@]}"; do
    echo $slave_container
done

# kill worker
echo '{"source":"driver","message":"killing worker"}' | fluent-cat stdout

max_sleep_in_secs=5
for index in `seq 0 1`; do
    sleep $(($RANDOM % max_sleep_in_secs))
    idx=$(($RANDOM % max_slaves))
    slave_container=${slave_containers[$idx]}
    #echo "{"message":"stopping container $slave_container"}" | fluent-cat stdout
    echo "stopping container $slave_container associated with slave-$idx"
    sudo docker stop $slave_container
    sleep 5
done
