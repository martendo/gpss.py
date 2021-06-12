---
title: gpss.py Syntax
permalink: /syntax
layout: default
---

# Syntax

## Basics

### Statements
A gpss.py program contains a bunch of statements that create a model.
There is one statement per line. For example:
~~~
GENERATE
QUEUE
ADVANCE
DEPART
TERMINATE
~~~
But this is no good &mdash; the statements need Operands!

### Operands
Most statements will take Operands. These Operands appear directly after
the statement on the same line, separated from the statement by
whitespace. Individual Operands are separated with commas, **with no
whitespace in between.**

Here's an example of a really short Transaction program:
~~~
GENERATE    18,6
TERMINATE   1
~~~
In the example above, there are two statements: `GENERATE` and
`TERMINATE`. Both of these statements have Operands: the `GENERATE`
Block has an A Operand of 18 and a B Operand of 6. The `GENERATE`
Block can take more Operands, but they're optional, so if left out,
default values are assumed. The `TERMINATE` Block has just one Operand
specified, the A Operand, and its value is 1.

To skip over Operands (e.g. specifying A and C but not B), simply leave
its spot blank, like so:
~~~
GENERATE    10,,50
~~~
The above specifies 10 as the A Operand and 50 as the C Operand, but it
doesn't specify the B Operand, making the B Operand assume its default
value.

### Comments
Comments in a gpss.py program are started with either a semicolon (`;`)
or an asterisk (`*`). These can be placed anywhere, and everything that
follows a comment character will be ignored by gpss.py.

~~~
; I'm a comment!
* I'm a comment too!

GENERATE    1   ; That GENERATE is a statement, but I'm still a comment!
TERMINATE       * I'm also still a comment!
~~~

### Labels
Labels can be declared in two ways:
- Before the statement it is "tagging", on the same line:

~~~
Wait    ADVANCE     12      ; This ADVANCE Block has the label "Wait"
~~~

- On its own line, with the label name followed by a colon (`:`):

~~~
ExtremelyCoolLabel:
        QUEUE       Line    ; This QUEUE Block has the label "ExtremelyCoolLabel"
~~~

### Notes
- Blank lines are allowed and ignored
- Amount of whitespace between fields doesn't matter, as long as there's
some
  - OK: `GENERATE 1`
  - Not OK: `GENERATE1`
- There are no restrictions on entity names other than that they must be
non-empty (or not all whitespace), since that would likely be a mistake

## Differences from original GPSS
gpss.py programs look very similar what an original GPSS program would
look like, but there are a few differences:
- Fields don't have to be placed at specific columns, but need to be
separated by whitespace
- Comments must start with a semicolon (`;`) or an asterisk (`*`), but
can appear anywhere
- A `SIMULATE` Block does not have to be present in the program to run
the simulation. To only check for syntax errors, run gpss.py with the
`--no-sim` or `-S` flag.
