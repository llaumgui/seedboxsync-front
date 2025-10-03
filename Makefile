.PHONY: virtualenv run test test-ci pytest pytest-xml comply markdownlint mypy clean dist publish

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

test: comply markdownlint mypy

test-ci: comply mypy

pytest:
	python -m pytest -v --cov=seedboxsync_front --cov-report=term --cov-report=html:coverage-report --capture=sys tests/
test-pytest-xml:
	python -m pytest -v --cov=seedboxsync --cov-report=term --cov-report=xml --capture=sys tests/

comply:
	flake8 seedboxsync_front/

markdownlint:
	markdownlint -c .markdownlint.yaml *.md

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
