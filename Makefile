DESTDIR=/
build:
	: please run Make install
install:
	install keyboard.py $(DESTDIR)/usr/bin/osk
	install osk.desktop $(DESTDIR)/usr/share/applications/
