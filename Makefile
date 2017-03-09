LOCALBIN = ~/.local/bin
LOCALCONFIG = ~/.config

all:
	@echo "make install"

install:
	mkdir -p $(LOCALBIN) $(LOCALCONFIG)/shellcut.d/
	cp config/default.yaml $(LOCALCONFIG)/shellcut.d/
	cp process.py $(LOCALBIN)/_shellcut.py
	cp process.sh $(LOCALBIN)/s
	chmod u+x $(LOCALBIN)/s $(LOCALBIN)/_shellcut.py
