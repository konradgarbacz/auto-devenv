#!/bin/bash

#update and upgrade the system
sudo apt update && sudo apt upgrade -y

#install docker and add the current user to the docker group
sudo curl -fsSL https://get.docker.com -o install-docker.sh
sudo cat install-docker.sh
sudo sh install-docker.sh
sudo usermod -aG docker $USER

#install nginx, enable it to start on boot, and start the service
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
