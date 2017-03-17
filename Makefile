LOCALBIN = ~/.local/bin
LOCALCONFIG = ~/.config

all:
	@echo "make install"

install:
	mkdir -p $(LOCALBIN) $(LOCALCONFIG)/shellcut.d/
	cp config/default.yaml $(LOCALCONFIG)/shellcut.d/
	cp scripts/shellcut.py $(LOCALBIN)/_shellcut.py
	chmod u+x $(LOCALBIN)/_shellcut.py

	# bash
	cp scripts/shellcut.bash $(LOCALBIN)/
	# fish
	if [ -d $(LOCALCONFIG)/fish/functions/ ]; then \
		cp scripts/shellcut.fish $(LOCALCONFIG)/fish/functions/; \
	fi
	@echo -e "\nPlease add 'source $(LOCALBIN)/shellcut.bash' to your .bashrc"
