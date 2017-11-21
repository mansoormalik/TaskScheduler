# run mongodb docker container
sudo docker run -d mongo
mongo_container=$(sudo docker ps -l -q)
mongo_host=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $mongo_container)
mongo_port=27017

# run task generator script
$(python task_generator.py $mongo_host $mongo_port)


