#!/usr/bin/python3

#    vcard2paleventfile.py
#    (c) 2022 Sven Hesse <drmccoy@drmccoy.de>
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

import vobject
from os.path import expanduser
import urllib3
from configparser import ConfigParser
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

config_file = homedir+'/.ical2paleventfile/contacts.conf'

if os.path.isfile(config_file) == False:
  raise Exception('Config file '+config_file+' does not exist')

parser = ConfigParser()
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

  f = open(pal_file, 'w')
  f.write(calendarname+"\n")

  eventcounter = 0

  vc = vobject.readComponents(response.data.decode('utf-8'))
  while (vo := next(vc, None)) is not None:
    if 'bday' in vo.contents:
      for bday in vo.contents['bday']:
        bday_datetime = datetime.strptime(bday.value, "%Y-%m-%d")
        age_str = ""
        if str(bday_datetime.year) not in bday.params.get('X-APPLE-OMIT-YEAR', []):
          age_str = f", {bday_datetime.year} (!{bday_datetime.year}!)"
        f.write(f"0000{bday_datetime.month:02d}{bday_datetime.day:02d} {vo.fn.value}{age_str}\n")
        eventcounter = eventcounter+1

  f.close()
  print (str(eventcounter)+" events imported \n")
