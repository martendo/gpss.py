---
title: gpss.py Usage
permalink: /usage
layout: default
---

# Usage
{:.no_toc}

## Contents
{:.no_toc}

- Contents
{:toc}

## From the Command Line {#cli}
~~~
python3 -m gpss [-S] [-d] [-o outfile] infile
~~~

On Windows, use `py -3` instead of `python3`.

### Arguments
- `infile`\
Your GPSS program. Required.
- `-o outfile`/`--output outfile`\
File to write the simulation report to, instead of stdout. Optional.
- `-S`/`--no-sim` (switch)\
Don't run the simulation, but still pass it through the parser and check
for syntax errors.
- `-d`/`--debug` (switch)\
Print debug messages.

Also:
- `--version`\
Print gpss.py's version number and exit.
- `-h`/`--help`\
Print program usage and argument descriptions.

## gpss.py as a Package {#package}
gpss.py can be imported into another script as the `gpss` module.
~~~ python
import gpss

gpss.run("examples/barber.gps")
print(gpss.createReport())
~~~

### Functions

#### `gpss.parse(infile=None, program=None)`{:.codeh} {#parse}
Parse a gpss.py program from file `infile` or string `program`.

The parser used can be accessed through `gpss.parser`, and its error
count through `gpss.parser.error_count`.

#### `gpss.run(infile=None, program=None)`{:.codeh} {#run}
Run a simulation. If specified, file `infile` or string `program` will
be parsed with [`gpss.parse()`](#functions-parse) before running the
simulation. Otherwise, the program last parsed will be used.

A `gpss.SimulationError` will be raised if anything illegal occurs in
the simulation.

#### `gpss.createReport()`{:.codeh} {#createReport}
Return a master simulation report. Contained within are all the
simulation reports returned by
[`gpss.getReports()`](#functions-getReports).

#### `gpss.getReports()`{:.codeh} {#getReports}
Return a list of reports from each run in the simulation.
