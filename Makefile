DOCKER = docker
DOCKER_COMPOSE = docker-compose

all: up

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

.PHONY: all up down image stop fclean re