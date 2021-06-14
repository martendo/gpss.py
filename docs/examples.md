---
title: gpss.py Examples
permalink: /examples
layout: default
---

# Examples
All examples on this page can be found in
[gpss.py's GitHub repository][examples source]{:target="_blank"}.

## Contents
- [Barber Shop](#barber-shop)
- [Tool Crib](#tool-crib)
- [Widget Assembly Line](#widget-assembly-line)
- [Inspection Station](#inspection-station)

## Barber Shop
A one-line, one-server queuing system. Adapted from Case Study 2A of
[Thomas J. Schriber's "A GPSS Primer"][gpss primer]{:target="_blank"}
(page <span class="roman-numeral">II</span>-36).

### Program
~~~
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
Generated on Sunday, June 13, 2021 at 21:08:51

============================= SIMULATION 1 =============================

Relative Clock: 480
Absolute Clock: 480

Facilities: 1

  "Barber":
    Avg. utilization: 83.75%
    Entries: 27
    Avg. time/Trans.: 14.889
    Available: no

Queues: 1

  "Line":
    Maximum content: 1
    Average content: 0.085
    Total entries: 27
    Zero entries: 16
    Percent zeros: 59.26%
    Avg. time/Trans.: 1.519
    Current content: 0

Storages: 0
~~~

## Tool Crib
A one-line, one-server queuing system with 2 customer types and priority
distinctions. Adapted from Case Study 2C of
[Thomas J. Schriber's "A GPSS Primer"][gpss primer]{:target="_blank"}
(page <span class="roman-numeral">II</span>-84).

### Program
~~~
; Time unit: 1 second

; Category 1 Mechanic
        GENERATE    420,360,,,1     ; Category 1 Mechanics arrive
        QUEUE       Line            ; Enter "Category 1 Segment" of line
        SEIZE       Clerk           ; Capture the clerk
        DEPART      Line            ; Leave the line
        ADVANCE     300,90          ; Use the clerk
        RELEASE     Clerk           ; Free the clerk
        TERMINATE                   ; Leave the tool crib area

; Category 2 Mechanic
        GENERATE    360,240,,,2     ; Category 2 Mechanics arrive
        QUEUE       Line            ; Enter "Category 2 Segment" of line
        SEIZE       Clerk           ; Capture the clerk
        DEPART      Line            ; Leave the line
        ADVANCE     100,30          ; Use the clerk
        RELEASE     Clerk           ; Free the clerk
        TERMINATE                   ; Leave the tool crib area

; Timer
        GENERATE    28800           ; Timer arrives after 8 hours
        TERMINATE   1               ; Shut off the run

; Control
        START       1               ; Start the run
        END                         ; Exit the program
~~~

### Sample Output
~~~
gpss.py Simulation Report - examples/tool-crib.gps
Generated on Sunday, June 13, 2021 at 21:09:43

============================= SIMULATION 1 =============================

Relative Clock: 28800
Absolute Clock: 28800

Facilities: 1

  "Clerk":
    Avg. utilization: 92.66%
    Entries: 143
    Avg. time/Trans.: 186.622
    Available: no

Queues: 1

  "Line":
    Maximum content: 7
    Average content: 1.831
    Total entries: 148
    Zero entries: 15
    Percent zeros: 10.14%
    Avg. time/Trans.: 356.345
    Current content: 5

Storages: 0
~~~

## Widget Assembly Line
A one-line, one-server queuing system with feedback. Adapted from Case
Study 2D of
[Thomas J. Schriber's "A GPSS Primer"][gpss primer]{:target="_blank"}
(page <span class="roman-numeral">II</span>-99).

### Program
~~~
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
Generated on Sunday, June 13, 2021 at 21:10:03

============================= SIMULATION 1 =============================

Relative Clock: 2400
Absolute Clock: 2400

Facilities: 1

  "Oven":
    Avg. utilization: 80.79%
    Entries: 240
    Avg. time/Trans.: 8.079
    Available: yes

Queues: 0

Storages: 0

============================= SIMULATION 2 =============================

Relative Clock: 2400
Absolute Clock: 2400

Facilities: 1

  "Oven":
    Avg. utilization: 94.83%
    Entries: 281
    Avg. time/Trans.: 8.100
    Available: no

Queues: 0

Storages: 0

============================= SIMULATION 3 =============================

Relative Clock: 2400
Absolute Clock: 2400

Facilities: 1

  "Oven":
    Avg. utilization: 98.71%
    Entries: 301
    Avg. time/Trans.: 7.870
    Available: no

Queues: 0

Storages: 0
~~~

## Inspection Station
Adapted from Case Study 2F of
[Thomas J. Schriber's "A GPSS Primer"][gpss primer]{:target="_blank"}
(page <span class="roman-numeral">II</span>-144).

### Program
~~~
; Time unit: 0.1 minutes

; Storage capacity definition
Inspection STORAGE 2

; Television set
        GENERATE    55,20           ; Sets arrive from preceding station
Inspect QUEUE       InspectWait     ; Enter inspection waiting area
        ENTER       Inspection      ; Capture an inspector
        DEPART      InspectWait     ; Leave the waiting area
        ADVANCE     90,30           ; Set is being inspected
        LEAVE       Inspection      ; Free the inspector
        TRANSFER    .15,,Adjust     ; Proceed to packing or adjustment station
        TERMINATE                   ; Set moves on to packing
Adjust  QUEUE       AdjustWait      ; Enter adjustment waiting area
        SEIZE       Adjustor        ; Capture the adjustor
        DEPART      AdjustWait      ; Leave the waiting area
        ADVANCE     300,100         ; Set is being adjusted
        RELEASE     Adjustor        ; Free the adjustor
        TRANSFER    ,Inspect        ; Go back to be inspected

; Timer
        GENERATE    4800            ; Timer arrives at end of each day
        TERMINATE   1               ; Provide snap output or shut off the run

; Control
        START       5,,1            ; Start the run
        END                         ; Exit the program
~~~

### Sample Output
~~~
gpss.py Simulation Report - examples/inspection.gps
Generated on Sunday, June 13, 2021 at 20:56:42

============================= SIMULATION 1 =============================

Relative Clock: 4800
Absolute Clock: 4800

Facilities: 1

  "Adjustor":
    Avg. utilization: 78.46%
    Entries: 13
    Avg. time/Trans.: 289.692
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.759
    Total entries: 101
    Zero entries: 14
    Percent zeros: 13.86%
    Avg. time/Trans.: 36.050
    Current content: 1

  "AdjustWait":
    Maximum content: 3
    Average content: 1.060
    Total entries: 15
    Zero entries: 2
    Percent zeros: 13.33%
    Avg. time/Trans.: 339.133
    Current content: 2

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.907
    Avg. utilization: 95.36%
    Entries: 100
    Avg. time/Trans.: 91.550
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 9600
Absolute Clock: 9600

Facilities: 1

  "Adjustor":
    Avg. utilization: 86.31%
    Entries: 27
    Avg. time/Trans.: 306.889
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.903
    Total entries: 205
    Zero entries: 29
    Percent zeros: 14.15%
    Avg. time/Trans.: 42.302
    Current content: 2

  "AdjustWait":
    Maximum content: 3
    Average content: 1.088
    Total entries: 28
    Zero entries: 3
    Percent zeros: 10.71%
    Avg. time/Trans.: 372.893
    Current content: 1

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.922
    Avg. utilization: 96.10%
    Entries: 203
    Avg. time/Trans.: 90.897
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 14400
Absolute Clock: 14400

Facilities: 1

  "Adjustor":
    Avg. utilization: 91.06%
    Entries: 43
    Avg. time/Trans.: 304.953
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.883
    Total entries: 308
    Zero entries: 40
    Percent zeros: 12.99%
    Avg. time/Trans.: 41.289
    Current content: 0

  "AdjustWait":
    Maximum content: 6
    Average content: 1.831
    Total entries: 43
    Zero entries: 3
    Percent zeros: 6.98%
    Avg. time/Trans.: 613.279
    Current content: 0

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.936
    Avg. utilization: 96.79%
    Entries: 308
    Avg. time/Trans.: 90.503
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 19200
Absolute Clock: 19200

Facilities: 1

  "Adjustor":
    Avg. utilization: 89.22%
    Entries: 57
    Avg. time/Trans.: 300.526
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.775
    Total entries: 409
    Zero entries: 72
    Percent zeros: 17.60%
    Avg. time/Trans.: 36.372
    Current content: 0

  "AdjustWait":
    Maximum content: 6
    Average content: 1.468
    Total entries: 57
    Zero entries: 9
    Percent zeros: 15.79%
    Avg. time/Trans.: 494.614
    Current content: 0

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.924
    Avg. utilization: 96.20%
    Entries: 409
    Avg. time/Trans.: 90.318
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 24000
Absolute Clock: 24000

Facilities: 1

  "Adjustor":
    Avg. utilization: 84.05%
    Entries: 67
    Avg. time/Trans.: 301.075
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.674
    Total entries: 505
    Zero entries: 119
    Percent zeros: 23.56%
    Avg. time/Trans.: 32.012
    Current content: 0

  "AdjustWait":
    Maximum content: 6
    Average content: 1.305
    Total entries: 73
    Zero entries: 14
    Percent zeros: 19.18%
    Avg. time/Trans.: 429.082
    Current content: 6

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.895
    Avg. utilization: 94.73%
    Entries: 505
    Avg. time/Trans.: 90.036
    Maximum content: 2
    Current content: 1
    Remaining: 1
    Available: yes
~~~

[gpss primer]: https://hdl.handle.net/2027.42/7464
[examples source]: {{ site.github_repo }}/tree/master/examples
