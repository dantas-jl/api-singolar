DOCKER_COMPOSE_DEV := docker-compose -f docker-compose.yml
DJANGO_DEV := docker-compose -f docker-compose.yml exec api python manage.py

build:
	@${DOCKER_COMPOSE_DEV} build

start:
	@${DOCKER_COMPOSE_DEV} up -d

up:
	@${DOCKER_COMPOSE_DEV} up


stop:
	@${DOCKER_COMPOSE_DEV} stop

test:
	@${DJANGO_DEV} test

migrations:
	@${DJANGO_DEV} makemigrations

migrate:
	@${DJANGO_DEV} migrate

shell:
	@${DJANGO_DEV} shell

superuser:
	@${DJANGO_DEV} createsuperuser