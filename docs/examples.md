---
title: gpss.py Examples
permalink: /examples
layout: default
---

# Examples
All examples on this page can be found in
[gpss.py's GitHub repository][examples source]{:target="_blank"}.

## Barber Shop
This example was adapted from Case Study 2A of
[Thomas J. Schriber's "A GPSS Primer"][gpss primer]{:target="_blank"}
(page <span class="roman-numeral">II</span>-36).

### Program
~~~
; Barber shop
; A one-line, one-server queuing system
; Adapted from Case Study 2A of Thomas J. Schriber's "A GPSS Primer"

; Time unit: 1 minute

; Customer
        GENERATE    18,6        ; Customers arrive
        QUEUE       Line        ; Enter the line
        SEIZE       Barber      ; Capture the barber
        DEPART      Line        ; Leave the line
        ADVANCE     16,4        ; Use the barber
        RELEASE     Barber      ; Free the barber
        TERMINATE               ; Leave the shop

; Timer
        GENERATE    480         ; Timer arrives at time 480 (8 hours)
        TERMINATE   1           ; Shut off the run

; Control
        START       1           ; Start the run
        END                     ; Exit the program
~~~

### Sample Output
~~~
gpss.py Simulation Report - examples/barber.gps
Generated on Friday, June 11, 2021 at 22:01:02

============================= SIMULATION 1 =============================

End time: 480

Facilities: 1

  "Barber":
    Entries: 26
    Available: no

Queues: 1

  "Line":
    Maximum content: 1
    Total entries: 27
    Zero entries: 12
    Percent zeros: 44.44%
    Average content: 0.11
    Current content: 1

Storages: 0
~~~

[gpss primer]: https://hdl.handle.net/2027.42/7464
[examples source]: {{ site.github_repo }}/tree/master/examples
