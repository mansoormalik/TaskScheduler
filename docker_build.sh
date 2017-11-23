# Clean up and create docker images for master and slave
sudo docker kill $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker rmi master
sudo docker build -f Dockerfile.master -t master .
sudo docker rmi slave
sudo docker build -f Dockerfile.slave -t slave .
