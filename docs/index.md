---
title: gpss.py
permalink: /
layout: default
---

# gpss.py
A silly, dumb, no-good Python program to read and run GPSS programs

## Documentation
- [Syntax]({{ "/syntax" | relative_url }})
- [Examples]({{ "/examples" | relative_url }})

## Usage
~~~
python -m gpss [-S] [-d] [-o outfile] infile
~~~

Arguments:
- `infile`  
Your GPSS program. Required.
- `-o outfile`/`--output outfile`  
File to output the simulation report to. Optional. If not specified,
the simulation report is printed to the console.
- `-S`/`--no-sim` (switch)  
Don't run the simulation, but still pass it through the parser and check
for syntax errors
- `-d`/`--debug` (switch)  
Print debug messages

Also:
- `--version`  
Print gpss.py's version number and exit
- `-h`/`--help`  
Print program usage and argument descriptions
