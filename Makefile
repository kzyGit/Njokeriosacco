build: 
	@ echo "Starting server"
	@ docker-compose build

start: 
	@ echo "Starting server"
	@ docker-compose up

test:
	@ echo "Running tests"
	@ docker-compose up