DOCKER = docker
DOCKER_COMPOSE = docker-compose 
SUDO_DOCKER_COMPOSE = sudo docker-compose

all: up

sudo_up:
	$(SUDO_DOCKER_COMPOSE) up -d --build

up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

image:
	$(DOCKER_COMPOSE) images

stop:
	$(DOCKER_COMPOSE) stop

fclean:
	$(DOCKER_COMPOSE) down --rmi all

prune: down fclean
	$(DOCKER) system prune -a -f

re: fclean all

.PHONY: all up down image stop fclean re sudo_up