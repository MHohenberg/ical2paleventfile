# ical2paleventfile

Pal is a command-line calendar on unixoid systems - it's really small and fast, especially when you work with the console a lot  to begin with. Most of us keep their calendars on some online service today, though, so synchronisation to pal is a bit of pain. 

This little script converts an ical to a pal-compatible eventfile

![Screenshot](documentation/example.png)

## License

This script is licensed under the GPLv3 or later.

## Requirements

* ics 0.31 or later (--> pip install ics)

## Configuration

ical2paleventfile reads the config file ~/.ical2paleventfile/calendars.conf

You can add as many calendars as you want

    [calendar0815]   # Make sure the section name is different for every calendar
    url = [URL of the ICS file - escape % with %%]
    palname = [output pal event filename] # always in your userdir under ~/.pal
    name = [name of the calendar]
    shorthand = [2-character shortcode]

Of course, you need to make pal aware of your file in ~/.pal/pal.conf
