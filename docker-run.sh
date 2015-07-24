#!/bin/bash
if ! [ "$(id -u)" == "0" ]; then
	echo 'Please run as root'
	exit
fi

echo "Which port do you want Tushe application to run on?"
echo -n "Enter port number: "
read tushe_port


if [ `which docker` ]; then
	echo 'Docker installed'
else

	if [ `which wget` ]; then
		echo 'wget installed'
	else
		if [ `which apt-get` ]; then
			apt-get update
			apt-get install wget -y
		fi
		if [ `which yum` ]; then
			yum install wget -y
		fi
	fi

	echo -n "Installing docker"
	wget -qO- https://get.docker.com/ | sh
fi

mkdir /home/tushe/db/ -p

echo "Setting up database"
docker rm -f tushe_db
docker run -d --name tushe_db -v '/home/tushe/db:/data/db' -e AUTH=no tutum/mongodb

echo "Runing Tushe"
sleep 5
docker rm -f tushe
docker run --name tushe -d --link tushe_db:db -p $tushe_port:3333 ericls/tushe

echo "
==============NGINX CONF===============
# You can use the following lines as an
# example of how to set up nginx as a
# front end for Tushe

server {
	listen 80;
	server_name example.org;

	location / {
		uwsgi_pass      127.0.0.1:$tushe_port;
		include         uwsgi_params;
		uwsgi_param     SCRIPT_NAME '';
	}
}

# You can always re-run this script
# to restart Tushe application
"