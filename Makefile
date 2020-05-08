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
	sudo podman pull ssfdust/psql_jieba_swsc
	sudo podman pull redis:5.0.9-alpine
	sudo podman pull rabbitmq:3.8.3-management-alpine
	sudo podman pull jwilder/nginx-proxy
	sudo podman pull ssfdust/smorest-sfs
	sudo podman pull dpage/pgadmin4

stop:
	sudo podman-compose exec beat rm -f celerybeat.pid
	sudo podman-compose stop

start:
	sudo podman-compose start
