## ----------------------------------------------------------------------
## Makefile.
## ----------------------------------------------------------------------
compose_files_m1=-f docker-compose.yaml -f docker-compose-mongo.yaml -f docker-compose-kafka-arm64.yaml
#					-f docker-compose-clickhouse-arm64.yaml
compose_files=-f docker-compose.yaml -f docker-compose-mongo.yaml -f docker-compose-kafka.yaml
#					-f docker-compose-clickhouse.yaml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start_m1:  ## Start project infrastructure.
		cd docker && DOCKER_BUILDKIT=1 docker-compose $(compose_files_m1) up -d --build --force-recreate
stop_m1:  ## Stop infrastructure.
		cd docker && docker-compose $(compose_files_m1) down

start_base: ## Start Admin, auth, etl, redis, elasticsearch and 2 postgres
		 cd docker && DOCKER_BUILDKIT=1 docker-compose -f docker-compose-base.yaml up -d --build --force-recreate

stop_base: ## Stop Admin, auth, etl, elasticsearch and 2 postgres
		 cd docker && DOCKER_BUILDKIT=1 docker-compose -f docker-compose-base.yaml down

start_dev:  ## Start project infrastructure.
		cd docker && DOCKER_BUILDKIT=1 docker-compose $(compose_files) up -d --build
stop_dev:  ## Stop infrastructure.
		cd docker && docker-compose $(compose_files) down

init:  ## First and full initialization. Create database, superuser and collect static files
	docker exec -it web_admin_panel bash -c \
	'python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py collectstatic --noinput'

migrate:  ## Apply migrations only
		docker exec -it web_admin_panel bash -c 'python manage.py migrate'

restart: stop start
		