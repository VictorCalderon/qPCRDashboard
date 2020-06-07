# .PHONY: init init-migration build run db-migrate test tox

init:  build run
	docker-compose exec web corona db upgrade
	docker-compose exec web corona init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec covid-backend corona db migrate

db-upgrade:
	docker-compose exec covid-backend corona db upgrade