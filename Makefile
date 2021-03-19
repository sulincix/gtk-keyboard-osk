DESTDIR=/
build:
	: please run Make install
install:
	mkdir -p $(DESTDIR)/usr/bin/ || true
	mkdir -p $(DESTDIR)/usr/share/applications/ || true
	mkdir -p $(DESTDIR)/usr/share/icons/ || true
	install keyboard.py $(DESTDIR)/usr/bin/osk
	install osk.desktop $(DESTDIR)/usr/share/applications/
	install icon.svg $(DESTDIR)/usr/share/icons/osk.svg
