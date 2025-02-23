.PHONY: run m u mu sm shell gcards dcards postman test superuser rufffix ruffformat ruff clean

.DEFAULT_GOAL := run

run:
	pdm run flask run --host=localhost

i:
	pdm run flask db init

m:
	pdm run flask db migrate

u:
	pdm run flask db upgrade

# migrate + upgrade
mu: m u

# upgrade + generate cards
ug: u gcards

# delete cards + generate cards
dg: dcards gcards

# showmigrations
sm:
	pdm run flask db show

shell:
	pdm run flask shell

gcards:
	pdm run flask gcards

dcards:
	pdm run flask dcards

postman:
	pdm run flask postman --export=True

ptest:
	pdm run flask test
testc:
	pdm run coverage run -m unittest discover tests/ -v

coverage:
	pdm run coverage report -m
	pdm run coverage html

test: testc coverage

superuser:
	pdm run flask createsuperuser

routes:
	pdm run flask routes

rufffix:
	pdm run ruff --fix --exit-zero .

ruffformat:
	pdm run ruff format .

ruff:
	pdm run ruff check .

clean: rufffix ruffformat ruff
