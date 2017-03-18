LOCALBIN = ~/.local/bin
XDG_CONFIG_HOME ?= ~/.config

all:
	@echo "make install"

install:
	mkdir -p $(LOCALBIN) $(XDG_CONFIG_HOME)/shellcut.d/
	cp config/default.yaml $(XDG_CONFIG_HOME)/shellcut.d/
	cp scripts/shellcut.py $(LOCALBIN)/_shellcut.py
	chmod u+x $(LOCALBIN)/_shellcut.py

	# bash
	cp scripts/shellcut.bash $(LOCALBIN)/
	# fish
	if [ -d $(XDG_CONFIG_HOME)/fish/functions/ ]; then \
		cp scripts/shellcut.fish $(XDG_CONFIG_HOME)/fish/functions/s.fish; \
	fi
	@echo -e "\nPlease add 'source $(LOCALBIN)/shellcut.bash' to your .bashrc"

test:
	PYTHONPATH=scripts green tests/
	python3-autopep8 --diff -r scripts/ | colordiff
	python3-autopep8 --diff -r tests/ | colordiff
	python3-flake8 scripts/ tests/
