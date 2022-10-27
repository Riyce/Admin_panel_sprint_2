## ----------------------------------------------------------------------
## Makefile.
## ----------------------------------------------------------------------
compose_base = -f docker-compose.yaml -f docker-compose-kafka.yaml
compose_base_m1 = -f docker-compose.yaml -f docker-compose-kafka-arm64.yaml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start_base: ## Start Admin, auth, etl, redis, elasticsearch and 2 postgres
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose_base} up -d --build --force-recreate

stop_base: ## Stop Admin, auth, etl, elasticsearch and 2 postgres
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose_base} down

start_base_m1: ## Start Admin, auth, etl, redis, elasticsearch and 2 postgres
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose_base_m1} up -d --build --force-recreate

stop_base_m1: ## Stop Admin, auth, etl, elasticsearch and 2 postgres
		 cd docker && DOCKER_BUILDKIT=1 docker-compose ${compose_base_m1} down

init:  ## First and full initialization. Create database, superuser and collect static files
	docker exec -it web_admin_panel bash -c \
	'python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py collectstatic --noinput'

migrate:  ## Apply migrations only
		docker exec -it web_admin_panel bash -c 'python manage.py migrate'

restart: stop_base start_base
restart_m1: stop_base_m1 start_base_m1
		