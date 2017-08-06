#!/usr/bin/python 

from ics import Calendar
from os.path import expanduser
from urllib2 import urlopen
from ConfigParser import SafeConfigParser

homedir = expanduser("~")

config = homedir+'/.ical2paleventfile/calendars'

parser = SafeConfigParser()
parser.read(config)

for section in parser.sections():
	
	url = parser.get(section, "url")
	output = parser.get(section, "palname")
	calendarname = parser.get(section, "shorthand")+" "+parser.get(section, "name")

	print "url: "+url+"\n"
	print "pal: "+output+"\n"
	print "calendar name: "+calendarname+"\n";

	c = Calendar(urlopen(url).read().decode('utf-8'))

	f = open(output, 'w')
	f.write(calendarname+"\n")

	errorcounter = 0

	for event in c.events:

		try:
			name = event.name
			if (name.isspace() or len(name) == 0):
				name = "[Event without title]"

			beginstring = str(event.begin).replace('-','')[:8]
			endstring = beginstring
			if (event.has_end):
				endstring = str(event.end).replace('-', '')[:8]
	
			if (beginstring == endstring):
				f.write(beginstring+" "+ name+"\n")
			else:
				f.write("DAILY:"+beginstring+":"+endstring+" "+name+"\n")

		except UnicodeEncodeError:
			errorcounter = errorcounter+1
			print "Bloop "+str(errorcounter)

	f.close()

