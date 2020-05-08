IPADDR := $(shell ip -f inet addr show docker0 | grep -Po 'inet \K[\d.]+')
PROXYBIND := "http://$(IPADDR):1081"

all:
	sudo docker build --build-arg http_proxy=$(PROXYBIND) \
		--build-arg https_proxy=$(PROXYBIND) \
		-t ssfdust/yt-media .

services:
	sudo systemctl start postgresql rabbitmq redis

services-off:
	sudo systemctl stop postgresql rabbitmq redis

up:
	sudo podman-compose up -d db rabbitmq redis pgadmin 
	sleep 20
	sudo podman-compose up -d web celery beat
	sleep 5
	sudo podman-compose up -d nginx

stop:
	sudo podman-compose exec beat rm -f celerybeat.pid
	sudo podman-compose stop

start:
	sudo podman-compose start
