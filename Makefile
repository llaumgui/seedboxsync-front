.PHONY: virtualenv run i18n-extract i18n-update i18n-compile test test-ci pytest pytest-xml comply markdownlint hadolint mypy clean dist publish

virtualenv:
	virtualenv --prompt '|> seedboxsync-front <| ' env
	env/bin/pip install -e ".[dev]"
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

run:
	export FLASK_SECRET_KEY=dev ; \
	export FLASK_CACHE_TYPE=NullCache ; \
	flask --app seedboxsync_front run --debug

i18n-extract:
	pybabel extract -F babel.cfg -o seedboxsync_front/messages.pot .

i18n-update:
	pybabel update -i seedboxsync_front/messages.pot -d seedboxsync_front/translations

i18n-compile:
	pybabel compile -d seedboxsync_front/translations

test: comply mypy pytest markdownlint hadolint

test-ci: comply mypy i18n-compile pytest-xml

pytest:
	python -m pytest -v --cov=seedboxsync_front --cov-report=term --cov-report=html:coverage-report --capture=sys tests/
pytest-xml:
	python -m pytest -v --cov=seedboxsync --cov-report=term --cov-report=xml --capture=sys tests/

comply:
	flake8 seedboxsync_front/ tests/

markdownlint:
	markdownlint -c .markdownlint.yaml *.md

hadolint:
	hadolint Dockerfile

mypy:
	mypy

clean:
	find . -name '*.py[co]' -delete

dist: clean
	rm -rf dist/*
	npm run build
	flit build

publish:
	flit publish
