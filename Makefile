build: 
	@ echo "Starting server"
	@ docker-compose build

start: 
	@ echo "Starting server"
	@ docker-compose up

test:
	@ echo "Running tests"
	@ docker-compose run web python manage.py test

lint:
	@ echo "Running flake8 linter"
	@ docker-compose run web flake8

migrate:
	@ echo "migrate database"
	@ docker-compose run web python manage.py makemigrations
	@ docker-compose run web python manage.py migrate

admin:
	@ echo "Creating admin"
	@ docker-compose run web python manage.py createsuperuser