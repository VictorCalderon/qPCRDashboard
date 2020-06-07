init:  build run
	@echo "Init done, containers running"

build:
	docker build --tag qpcr-frontend .

run:
	docker run --publish 8080:80 --detach --name qpcr-frontend qpcr-frontend

