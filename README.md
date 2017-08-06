# ical2paleventfile

Pal is a command-line calendar on unixoid systems - and it's really small, fast and cool, especially when you work with the console a lot of time to begin with. Most of us keep their calendars in some kind of online way today, though, so synchronisation is a bit of a pain. 

This little script converts an ical to a pal-compatible eventfile

![Screenshot](documentation/example.png)

## License

This script is licensed under the GPLv3 or later

## Requirements

* ics 0.31 or later (--> pip install ics)

## Configuration

ical2paleventfile reads the config file ~/.ical2paleventfile/calendars.conf

You can add as many calendars as you want

    [calendar0815]   # Make sure the section name is different for every calendar
    url = [URL of the ICS file]
    palname = [output pal event filename] # always in your userdir under ~/.pal
    name = [name of the calendar]
    shorthand = [2-character shortcode]

Of course, you need to make pal aware of your file in ~/.pal/pal.conf
