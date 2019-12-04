CONTAINER=harryr/0bin
NAME=0bin

all: data
	@echo "make build run"
	@echo "  -- alternatively --"
	@echo "make build create"
	@echo "make stop"
	@echo "make start"

data:
	mkdir -p $@
	chmod 777 data

build:
	docker build -t $(CONTAINER) .

start:
	docker start $(NAME)

stop:
	docker stop $(NAME)

destroy:
	docker rm $(NAME) -f

run: data
	docker run --rm --name $(NAME) -p "8000:8000" -v `pwd`/data:/data -ti $(CONTAINER)

create: data build
	docker run -d --name $(NAME) -p "8000:8000" --restart unless-stopped -v `pwd`/data:/data -ti $(CONTAINER)
