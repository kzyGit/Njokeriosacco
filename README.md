# Njokeriosacco API

[![CircleCI](https://circleci.com/gh/kzyGit/Njokeriosacco.svg?style=svg)](https://circleci.com/gh/kzyGit/Njokeriosacco)


Njokeriosacco is a locals sacco that aims at enabling small business owners to save and request for loans

The API is built using <b>Python Django Rest Framework</b>


<h3>Technologies used</h3>

1. Django Rest Framework

2. Postgres Database

3. Docker Containorization

4. CircleCI testing



<h3>Setting up Njokerio Sacco</h3>

Clone the repository: `git clone https://github.com/kzyGit/Njokeriosacco.git`

Ensure docker is installed and running in your machine

Move to the sacco's directory: `cd Njokeriosacco`

Create a superuser/admin by running the command: `make admin` Fill in the credentials and there you have your


<h3>Njokeriosacco commands</h3>

Start the server, by running the command: `make start`

Incase you get a migrations error, run migrations: `make migrate`

To run the tests: `make test`

To run the flake8 linter: `make lint`


<h3>Functionalities / Endpoints</h3>

An admin can:

1. Create and view All users: `POST , GET -> /users/`

2. View / Delete or update single user: `GET , PUT , DELETE -> /user/(int:id)/`

3. Add or view Savings: `POST , GET -> /savings/` 

4. Get single user Savings: `GET -> /savings/(int:id)/` 

5. View / Delete or Update a single saving: `GET , PUT , DELETE -> /single_saving/(int:id)/`

6. Issue or View a users loans: `POST , GET -> /loan/` 

7. View / delete / Update a single loan: `GET , PUT , DELETE -> /loan/(int:id)/`

8. Record and View Loan repayment: `POST , GET -> /repayment/`


A member can:

1. View his profile: `GET -> /user/(int:id)/`

2. View own Savings: `GET -> /savings/` 

3. View own loans: `GET -> /loan/`

4. View Loan repayment: `GET -> /repayment/`
