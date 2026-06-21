#!/bin/bash

#update and upgrade the system
sudo apt update && sudo apt upgrade -y

#install docker and add the current user to the docker group
sudo curl -fsSL https://get.docker.com -o install-docker.sh
sudo sh install-docker.sh
sudo usermod -aG docker $USER

#install nginx, enable it to start on boot, and start the service
sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx

#configure nginx to proxy requests to the flask app
sudo tee /etc/nginx/sites-available/flask-app > /dev/null <<EOF
server {
    listen 80;
    location / {
        proxy_pass http://localhost:5000;
    }
}
EOF

#change the nginx configuration and restart the service
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

#build and run the container
sudo docker build -t flask-app .
sudo docker run -d -p 5000:5000 flask-app

echo "Gotowe!"