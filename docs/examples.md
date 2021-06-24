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

### Output
~~~
gpss.py Simulation Report - examples/barber.gps
Generated on Thursday, June 24, 2021 at 09:10:41

============================= SIMULATION 1 =============================

Relative Clock: 480
Absolute Clock: 480

Facilities: 1

  "Barber":
    Avg. utilization: 86.04%
    Entries: 26
    Avg. time/Trans.: 15.885
    Available: no

Queues: 1

  "Line":
    Maximum content: 1
    Average content: 0.160
    Total entries: 27
    Zero entries: 12
    Percent zeros: 44.44%
    Avg. time/Trans.: 2.852
    Current content: 1

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

### Output
~~~
gpss.py Simulation Report - examples/tool-crib.gps
Generated on Thursday, June 24, 2021 at 09:11:06

============================= SIMULATION 1 =============================

Relative Clock: 28800
Absolute Clock: 28800

Facilities: 1

  "Clerk":
    Avg. utilization: 92.58%
    Entries: 147
    Avg. time/Trans.: 181.374
    Available: no

Queues: 1

  "Line":
    Maximum content: 5
    Average content: 1.294
    Total entries: 149
    Zero entries: 17
    Percent zeros: 11.41%
    Avg. time/Trans.: 250.040
    Current content: 2

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

### Output
~~~
gpss.py Simulation Report - examples/widgets.gps
Generated on Thursday, June 24, 2021 at 09:11:24

============================= SIMULATION 1 =============================

Relative Clock: 2400
Absolute Clock: 2400

Facilities: 1

  "Oven":
    Avg. utilization: 78.88%
    Entries: 237
    Avg. time/Trans.: 7.987
    Available: no

Queues: 0

Storages: 0

============================= SIMULATION 2 =============================

Relative Clock: 2400
Absolute Clock: 2400

Facilities: 1

  "Oven":
    Avg. utilization: 94.04%
    Entries: 285
    Avg. time/Trans.: 7.919
    Available: no

Queues: 0

Storages: 0

============================= SIMULATION 3 =============================

Relative Clock: 2400
Absolute Clock: 2400

Facilities: 1

  "Oven":
    Avg. utilization: 98.92%
    Entries: 295
    Avg. time/Trans.: 8.047
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

### Output
~~~
gpss.py Simulation Report - examples/inspection.gps
Generated on Thursday, June 24, 2021 at 09:11:43

============================= SIMULATION 1 =============================

Relative Clock: 4800
Absolute Clock: 4800

Facilities: 1

  "Adjustor":
    Avg. utilization: 55.54%
    Entries: 9
    Avg. time/Trans.: 296.222
    Available: yes

Queues: 2

  "InspectWait":
    Maximum content: 2
    Average content: 0.281
    Total entries: 93
    Zero entries: 50
    Percent zeros: 53.76%
    Avg. time/Trans.: 14.505
    Current content: 0

  "AdjustWait":
    Maximum content: 2
    Average content: 0.281
    Total entries: 9
    Zero entries: 4
    Percent zeros: 44.44%
    Avg. time/Trans.: 150.000
    Current content: 0

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.676
    Avg. utilization: 83.82%
    Entries: 93
    Avg. time/Trans.: 86.527
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 9600
Absolute Clock: 9600

Facilities: 1

  "Adjustor":
    Avg. utilization: 60.72%
    Entries: 20
    Avg. time/Trans.: 291.450
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.358
    Total entries: 191
    Zero entries: 84
    Percent zeros: 43.98%
    Avg. time/Trans.: 17.984
    Current content: 2

  "AdjustWait":
    Maximum content: 2
    Average content: 0.159
    Total entries: 20
    Zero entries: 12
    Percent zeros: 60.00%
    Avg. time/Trans.: 76.100
    Current content: 0

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.769
    Avg. utilization: 88.47%
    Entries: 189
    Avg. time/Trans.: 89.878
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 14400
Absolute Clock: 14400

Facilities: 1

  "Adjustor":
    Avg. utilization: 74.72%
    Entries: 37
    Avg. time/Trans.: 290.784
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 3
    Average content: 0.487
    Total entries: 293
    Zero entries: 106
    Percent zeros: 36.18%
    Avg. time/Trans.: 23.915
    Current content: 2

  "AdjustWait":
    Maximum content: 3
    Average content: 0.493
    Total entries: 37
    Zero entries: 14
    Percent zeros: 37.84%
    Avg. time/Trans.: 191.946
    Current content: 0

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.813
    Avg. utilization: 90.67%
    Entries: 291
    Avg. time/Trans.: 89.739
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 19200
Absolute Clock: 19200

Facilities: 1

  "Adjustor":
    Avg. utilization: 76.21%
    Entries: 50
    Avg. time/Trans.: 292.660
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 4
    Average content: 0.571
    Total entries: 394
    Zero entries: 125
    Percent zeros: 31.73%
    Avg. time/Trans.: 27.827
    Current content: 1

  "AdjustWait":
    Maximum content: 3
    Average content: 0.449
    Total entries: 52
    Zero entries: 18
    Percent zeros: 34.62%
    Avg. time/Trans.: 165.750
    Current content: 2

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.839
    Avg. utilization: 91.94%
    Entries: 393
    Avg. time/Trans.: 89.837
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no

============================= SIMULATION 1 =============================

Relative Clock: 24000
Absolute Clock: 24000

Facilities: 1

  "Adjustor":
    Avg. utilization: 78.84%
    Entries: 65
    Avg. time/Trans.: 291.108
    Available: no

Queues: 2

  "InspectWait":
    Maximum content: 4
    Average content: 0.598
    Total entries: 496
    Zero entries: 149
    Percent zeros: 30.04%
    Avg. time/Trans.: 28.938
    Current content: 0

  "AdjustWait":
    Maximum content: 3
    Average content: 0.535
    Total entries: 67
    Zero entries: 19
    Percent zeros: 28.36%
    Avg. time/Trans.: 191.746
    Current content: 2

Storages: 1

  "Inspection":
    Capacity: 2
    Average content: 1.849
    Avg. utilization: 92.44%
    Entries: 496
    Avg. time/Trans.: 89.458
    Maximum content: 2
    Current content: 2
    Remaining: 0
    Available: no
~~~

[gpss primer]: https://hdl.handle.net/2027.42/7464
[examples source]: {{ site.github_repo }}/tree/master/examples
