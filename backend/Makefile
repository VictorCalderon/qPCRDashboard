# .PHONY: init init-migration build run db-migrate

init:  build run
	docker-compose exec web qpcr-manager db init
	docker-compose exec web qpcr-manager db upgrade
	docker-compose exec web qpcr-manager init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec qpcr-backend qpcr-manager db migrate

db-upgrade:
	docker-compose exec qpcr-backend qpcr-manager db upgrade
