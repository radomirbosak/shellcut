all:
	@echo "Available:"
	@echo "make test"
	@echo "make testloop"

test:
	PYTHONPATH=shellcut green tests/ --quiet-stdout
	autopep8 --diff -r shellcut/ | colordiff
	autopep8 --diff -r tests/ | colordiff
	autopep8 --diff setup.py | colordiff
	flake8 shellcut/ tests/ setup.py

testloop:
	while inotifywait -q -r -e modify --exclude .git .; do \
		clear; make test; \
	done
