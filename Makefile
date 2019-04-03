build: 
	@ echo "Starting server"
	@ docker-compose build

start: 
	@ echo "Starting server"
	@ docker-compose up

test:
	@ echo "Running tests"
	@ docker-compose run web python manage.py test Espace/api/tests

lint:
	@ echo "Running flake8 linter"
	@ flake8