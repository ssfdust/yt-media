IPADDR := $(shell ip -f inet addr show docker0 | grep -Po 'inet \K[\d.]+')
PROXYBIND := "http://$(IPADDR):9987"

all:
	docker build --build-arg http_proxy=$(PROXYBIND) \
		--build-arg https_proxy=$(PROXYBIND) \
		-t ssfdust/yt-media .