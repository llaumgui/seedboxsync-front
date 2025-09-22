.PHONY: test virtualenv run pytest comply comply-fix comply-typing docs

test: comply

virtualenv:
	virtualenv --prompt '|> seedboxsync-front <| ' env
	env/bin/pip install -e ".[dev]"
	@echo
	@echo "VirtualENV Setup Complete. Now run: source env/bin/activate"
	@echo

run:
	flask --app seedboxsync_front run --debug

pytest:
	python -m pytest -v --cov=seedboxsync_front --cov-report=term --cov-report=html:coverage-report --capture=sys tests/

comply:
	flake8 seedboxsync_front/	

comply-fix:
	autopep8 -ri seedboxsync_front/

clean:
	find . -name '*.py[co]' -delete

dist: clean
	rm -rf dist/*
	npm run build
	flit build
