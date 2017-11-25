# Clean up and create docker images for master and slave
#uncomment the next three lines to free up some space before builds
#sudo docker kill $(sudo docker ps -q)
#sudo docker rm $(sudo docker ps -a -q)
#sudo docker rmi $(sudo docker images -f "dangling=true" -q)
sudo docker rmi master
sudo docker build -f Dockerfile.master -t master .
sudo docker rmi slave
sudo docker build -f Dockerfile.slave -t slave .
