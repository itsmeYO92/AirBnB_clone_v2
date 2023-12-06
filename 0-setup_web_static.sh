#!/usr/bin/env bash
# this script sets up your web servers for the deployment of web_static. 


#check if Nginx is installed

if ! command -v nginx &> /dev/null; then
    sudo apt update
    sudo apt install -y nginx
fi
sudo ufw allow 'Nginx HTTP'

if [[ ! -d "/data/" ]]; then
    sudo mkdir /data/
fi

if [[ ! -d "/data/web_static/" ]]; then
    sudo mkdir /data/web_static/
fi


if [[ ! -d "/data/web_static/releases/" ]]; then
    sudo mkdir /data/web_static/releases/
fi

if [[ ! -d "/data/web_static/shared/" ]]; then
    sudo mkdir /data/web_static/shared/
fi

if [[ ! -d "/data/web_static/releases/test/" ]]; then
    sudo mkdir /data/web_static/releases/test/
fi

sudo echo "<html>
  <head>
  </head>
  <body>
    Its working
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

symlink="/data/web_static/current"
target="/data/web_static/releases/test/"

sudo ln -s -f "$target" "$symlink"

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a    location /hbnb_static {\n\t\t alias /data/web_static/current/;\n\t\t}' /etc/nginx/sites-enabled/default

sudo service nginx restart
