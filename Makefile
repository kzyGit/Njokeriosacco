build: 
	@ echo "Starting server"
	@ docker-compose build

start: 
	@ echo "Starting server"
	@ docker-compose up

test:
	@ echo "Running tests"
	@ python manage.py test Espace/api/tests
	