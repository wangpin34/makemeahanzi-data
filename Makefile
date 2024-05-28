.PHOENY: venv

venv:
	virtualenv venv
	source venv/bin/activate
	pip install

deactivate:
	deactivate

freeze:
	pip freeze > requirements.txt

