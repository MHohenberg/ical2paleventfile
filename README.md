# ical2paleventfile

I love pal. Pal is a command-line calendar on unixoid systems. 

This little script converts an ical to a pal-compatible file

## Requirements

* ics 0.31 or later (pip install ics)

## configuration

ical2paleventfile reads the config file ~/.ical2paleventfile/calendars 

You can add as many calendars as you want

    [calendar0815]   # Make sure the section name is different for every calendar
    url = [URL of the ICS file]
    palname = [output pal event filename]
    name = [name of the calendar]
    shorthand = [2-character shortcode]
