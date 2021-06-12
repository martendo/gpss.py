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

## Widget Assembly Line
This example was adapted from Case Study 2D of
[Thomas J. Schriber's "A GPSS Primer"][gpss primer]{:target="_blank"}
(page <span class="roman-numeral">II</span>-99).

### Program
~~~
; Widget assembly line
; A one-line, one-server queuing system with feedback
; Adapted from Case Study 2D of Thomas J. Schriber's "A GPSS Primer"

; Time unit: 1 minute

; Widget
Key     GENERATE    ,,,4    ; Provide 4 assemblers
Back    ADVANCE     30,5    ; Assemble next widget
        SEIZE       Oven    ; Capture the oven
        ADVANCE     8,2     ; Use the oven
        RELEASE     Oven    ; Free the oven
        TRANSFER    ,Back   ; Go do the next assembly

; Timer
        GENERATE    2400    ; Timer arrives after 5 days
        TERMINATE   1       ; Shut off the run

; Control and Block redefinitions
        START       1       ; Start the 1st run
Key     GENERATE    ,,,5    ; Reconfigure for 2nd run
        CLEAR               ; Clear for 2nd run
        START       1       ; Start the 2nd run
Key     GENERATE    ,,,6    ; Reconfigure for 3rd run
        CLEAR               ; Clear for 3rd run
        START       1       ; Start the 3rd run
        END                 ; Exit the program
~~~

### Sample Output
~~~
gpss.py Simulation Report - examples/widgets.gps
Generated on Friday, June 11, 2021 at 22:04:17

============================= SIMULATION 1 =============================

End time: 2400

Facilities: 1

  "Oven":
    Entries: 236
    Available: no

Queues: 0

Storages: 0

============================= SIMULATION 2 =============================

End time: 2400

Facilities: 1

  "Oven":
    Entries: 284
    Available: no

Queues: 0

Storages: 0

============================= SIMULATION 3 =============================

End time: 2400

Facilities: 1

  "Oven":
    Entries: 298
    Available: no

Queues: 0

Storages: 0
~~~

[gpss primer]: https://hdl.handle.net/2027.42/7464
[examples source]: {{ site.github_repo }}/tree/master/examples
