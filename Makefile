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
		cp scripts/shellcut.fish $(XDG_CONFIG_HOME)/fish/functions/; \
	fi
	@echo -e "\nPlease add 'source $(LOCALBIN)/shellcut.bash' to your .bashrc"
