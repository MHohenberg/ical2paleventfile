#!/usr/bin/python3

#    ics2paleventfile.py
#    (c) 2017-2018 Martin Hohenberg <software@martinhohenberg.de>
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
import urllib3
from configparser import SafeConfigParser
import datetime as dt
from datetime import datetime
from dateutil import tz
import os
import urllib
from base64 import b64encode

def basic_auth(username, password):
  token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
  return f'Basic {token}'

homedir = expanduser("~")

config_file = homedir+'/.ical2paleventfile/calendars.conf'

if os.path.isfile(config_file) == False:
  raise Exception('Config file '+config_file+' does not exist')

parser = SafeConfigParser()
parser.read(config_file)

for section in parser.sections():
  url = parser.get(section, "url")
  pal_file = homedir+"/.pal/"+parser.get(section, "palname")
  calendarname = parser.get(section, "shorthand")+" "+parser.get(section, "name")
  
  print ("url: ",url)
  print ("pal: ",pal_file)
  print ("calendar name: ",calendarname)

  parsed = urllib.parse.urlparse(url)
  
  http = urllib3.PoolManager()
  headers = None
  if parsed.username is not None and parsed.password is not None:
    headers = { 'Authorization' : basic_auth(parsed.username, parsed.password) }
  response = http.request('GET', url, headers=headers)

  c = Calendar(response.data.decode('utf-8'))
  
  f = open(pal_file, 'w')
  f.write(calendarname+"\n")
  
  eventcounter = 0
  
  for event in c.events:
    eventcounter = eventcounter+1
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
      print ("UnicodeEncodeError")
          
  f.close()
  print (str(eventcounter)+" events imported \n")
