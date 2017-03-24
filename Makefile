LOCALBIN = ~/.local/bin
XDG_CONFIG_HOME ?= ~/.config

all:
	@echo "make install"

install:
	mkdir -p $(LOCALBIN) $(XDG_CONFIG_HOME)/shellcut.d/
	cp config/default.yaml $(XDG_CONFIG_HOME)/shellcut.d/
	cp scripts/shellcut.py $(LOCALBIN)/s
	chmod u+x $(LOCALBIN)/s

test:
	PYTHONPATH=scripts green tests/
	autopep8 --diff -r scripts/ | colordiff
	autopep8 --diff -r tests/ | colordiff
	flake8 scripts/ tests/

testloop:
	while inotifywait -q -r -e modify .; do make test; done
