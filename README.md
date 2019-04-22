# Njokeriosacco APi

Njokeriosacco is a locals sacco that aims at enabling small business owners to save and request for loans

The API is built using <b>Python Django Rest Framework</b>

<h3>Setting up Njokerio Sacco</h3>
<ul>
<li>Clone the repository: `git clone https://github.com/kzyGit/Njokeriosacco.git`</li>
<li>Ensure docker is installed and running in your machine</li>
<li>Move to the sacco's directory: `cd Njokeriosacco`</li>
<li>Create a superuser/admin by running the command: `make admin` Fill in the credentials and there you have your</li>
</ul>

<h3>Njokeriosacco commands</h3>
<ul>
<li>Start the server, by running the command: `make start`</li>

<li>Incase you get a migrations error, run migrations: `make migrate`</li>

<li>To run the tests: `make test`</li>

<li>To run the flake8 linter: `make lint`</li>
</ul>



<h3>Functionalities / Endpoints</h3>

An admin can:

<ol>
<li>Create and view All users: `POST , GET -> /users/`</li>
<li>View / Delete or update single user: `GET , PUT , DELETE -> /user/(int:id)/`</li>
<li>Add or view Savings: `POST , GET -> /savings/` </li>
<li>Get single user Savings: `GET -> /savings/(int:id)/` </li>
<li>View / Delete or Update a single saving: `GET , PUT , DELETE -> /single_saving/(int:id)/`</li>
<li>Issue or View a users loans: `POST , GET -> /loan/` </li>
<li>View / delete / Update a single loan: `GET , PUT , DELETE -> /loan/(int:id)/`</li>
<li>Record and View Loan repayment: `POST , GET -> /repayment/` </li>
</ol>


