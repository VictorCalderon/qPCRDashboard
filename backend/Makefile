# .PHONY: init build run init-migration db-migrate db-upgrade

init:  build run db-check db-init db-migrate db-upgrade add-user
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-check:
	docker-compose exec web ./entrypoint.sh

db-init:
	docker-compose exec web qpcr-manager db init

db-create:
	docker-compose exec web qpcr-manager init

db-migrate:
	docker-compose exec web qpcr-manager db migrate

db-upgrade:
	docker-compose exec web qpcr-manager db upgrade

add-user:
	docker-compose exec web qpcr-manager add-user