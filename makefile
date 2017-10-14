install:
	rm -rf /usr/local/bin/ical2paleventfile
	rm -rf /usr/local/bin/ical2paleventfile.py
	cp ical2paleventfile.py /usr/local/bin
	ln -s /usr/local/bin/ical2paleventfile.py /usr/local/bin/ical2paleventfile

uninstall:
	rm /usr/local/bin/ical2paleventfile
	rm /usr/local/bin/ical2paleventfile.py


