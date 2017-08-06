#!/usr/bin/python 

from ics import Calendar
from urllib2 import urlopen # import requests
url = '[your URL]'
output = '[your homedir]/.pal/google.pal'
c = Calendar(urlopen(url).read().decode('utf-8'))

# could also use 'requests' here
# c = Calendar(requests.get(url).text)

f = open(output, 'w')
f.write("G1 Google Kalender \n")

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

