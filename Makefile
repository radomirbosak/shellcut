LOCALBIN = ~/.local/bin
LOCALCONFIG = ~/.config

all:
	@echo "make install"

install:
	cp config/shellcut.yaml $(LOCALCONFIG)/
	cp process.py $(LOCALBIN)/_shellcut.py
	cp process.sh $(LOCALBIN)/s
	chmod u+x $(LOCALBIN)/s $(LOCALBIN)/_shellcut.py
