.PHONY: run m u mu sm shell gcards dcards postman test superuser rufffix ruffformat ruff clean

.DEFAULT_GOAL := run

run:
	poetry run flask run --host=localhost

i:
	poetry run flask db init

m:
	poetry run flask db migrate

u:
	poetry run flask db upgrade

# migrate + upgrade
mu: m u

# upgrade + generate cards
ug: u gcards

# delete cards + generate cards
dg: dcards gcards

# showmigrations
sm:
	poetry run flask db show

shell:
	poetry run flask shell

gcards:
	poetry run flask gcards

dcards:
	poetry run flask dcards

postman:
	poetry run flask postman --export=True

ptest:
	poetry run flask test
testc:
	poetry run coverage run -m unittest discover tests/ -v

coverage:
	poetry run coverage report -m
	poetry run coverage html

test: testc coverage

superuser:
	poetry run flask createsuperuser

routes:
	poetry run flask routes

rufffix:
	poetry run ruff --fix --exit-zero .

ruffformat:
	poetry run ruff format .

ruff:
	poetry run ruff check .

clean: rufffix ruffformat ruff
