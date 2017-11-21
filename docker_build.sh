# Create docker images for master and slave

sudo docker build -f Dockerfile.master -t master .
sudo docker build -f Dockerfile.slave -t slave .
