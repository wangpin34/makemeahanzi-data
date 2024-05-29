.PHOENY: venv

venv:
	python3 -m venv .venv
	. .venv/bin/activate

use_venv:
	. .venv/bin/activate

install: venv
	pip install -r requirements.txt

deactivate:
	deactivate

freeze:
	pip freeze > requirements.txt

