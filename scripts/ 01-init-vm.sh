#!/bin/bash

##update and upgrade the system, set hostname, create a new user with sudo privileges

sudo apt update && sudo apt upgrade -y
sudo hostnamectl set-hostname vm01
sudo useradd -m -s /bin/bash SuperUser01
sudo passwd SuperUser01
sudo usermod -aG sudo SuperUser01

## install docker and docker-compose, usermod -aG docker SuperUser01

sudo apt update
sudo apt install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo systemctl start docker
sudo docker run hello-world
sudo usermod -aG docker SuperUser01

