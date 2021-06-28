---
title: Web gpss.py
permalink: /web
style: /web/style.css
---

# Web gpss.py
This page uses [gpss-server][gpss-server]{:target="_blank"} to run
gpss.py and the [Ace code editor][ace]{:target="_blank"}.

## Program

<div class="editor-container">
  <div id="editor" class="editor">; Barber shop
; A one-line, one-server queuing system
; Adapted from Case Study 2A of Thomas J. Schriber's "A GPSS Primer"
; (page II-36)

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
</div>
</div>

## Output

<button id="simulateBtn">Simulate</button>

~~~
Your simulation report will show up here.
~~~
{:#response}

<script src="{{ '/web/ace/ace.js' | relative_url }}" type="text/javascript" charset="utf-8"></script>
<script src="{{ '/web/script.js' | relative_url }}" type="text/javascript" charset="utf-8"></script>

[gpss-server]: https://github.com/martendo/gpss-server
[ace]: https://ace.c9.io
