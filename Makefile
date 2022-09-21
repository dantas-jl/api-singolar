DOCKER_COMPOSE_DEV := docker-compose -f docker-compose.yml
DJANGO_DEV := docker-compose -f docker-compose.yml exec api python manage.py

build:
	@${DOCKER_COMPOSE_DEV} build

start:
	@${DOCKER_COMPOSE_DEV} up -d

stop:
	@${DOCKER_COMPOSE_DEV} stop