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

pull:
	sudo podman-compose pull

up:
	sudo podman-compose up -d

down:
	sudo podman-compose down

stop:
	sudo podman-compose stop
	rm -rf ./celery.pid

start:
	sudo podman-compose start
