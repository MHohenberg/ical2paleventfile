#!/usr/bin/python 

#    ics2paleventfile.py
#    (c) 2017 Martin Hohenberg <software@martinhohenberg.de>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ics import Calendar
from os.path import expanduser
from urllib2 import urlopen
from ConfigParser import SafeConfigParser
import datetime as dt
from datetime import datetime
from dateutil import tz

homedir = expanduser("~")

config_file = homedir+'/.ical2paleventfile/calendars.conf'

parser = SafeConfigParser()
parser.read(config_file)

for section in parser.sections():
    
    url = parser.get(section, "url")
    pal_file = homedir+"/.pal/"+parser.get(section, "palname")
    calendarname = parser.get(section, "shorthand")+" "+parser.get(section, "name")

    print "url: "+url
    print "pal: "+pal_file
    print "calendar name: "+calendarname

    c = Calendar(urlopen(url).read().decode('utf-8'))

    f = open(pal_file, 'w')
    f.write(calendarname+"\n")

    for event in c.events:
        
        try:
            name = event.name.encode("utf-8")
            if (name.isspace() or len(name) == 0):
                name = "[Event without title]"
            
            begin_date_local = event.begin.astimezone(tz.tzlocal())
            
            begin_date = str(begin_date_local).replace('-','')[:8]
            begin_time = str(begin_date_local).replace('-','')[9:14]
	    end_date = begin_date
            
	    if (event.has_end):
                end_date = str(event.end).replace('-', '')[:8]
                
            if (begin_date == end_date):
                f.write(begin_date+" ["+begin_time+"] "+ name+"\n")
            else:
                f.write("DAILY:"+begin_date+":"+end_date+" "+name+"\n")

        except UnicodeEncodeError:
            print "UnicodeEncodeError"
    
    f.close()

