---
title: Web gpss.py
permalink: /web
style: /web/style.css
nav:
  - <button id="info-btn">Info</button>
  - <button id="simulate-btn">Simulate</button>
navtitle: Web gpss.py
---

<div id="editor-container">
  <div id="editor">; Barber shop
; A one-line, one-server queuing system
; Adapted from Case Study 2A of Thomas J. Schriber's "A GPSS Primer" (page II-36)

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

<div class="separator column" id="main-separator">
  <div></div>
</div>

<section class="flex-container" id="response-container">
  <div class="highlight" id="console-container" style="display: none;">
    <pre class="highlight"><code id="console"></code></pre>
  </div>

  <div class="separator row" id="response-separator" style="display: none;">
    <div></div>
  </div>

  <div class="highlight" id="output-container">
    <pre class="highlight"><code id="output">Your simulation report will show up here.</code></pre>
  </div>
</section>

<section id="info" markdown="1">
## What am I looking at?
You're looking at Web gpss.py, a web interface for gpss.py.

## What do I do?
1. Write out your gpss.py program (or use the example provided!) in the
code editor on the left side of your screen.
2. Run your simulation with the "Simulate" button in the top right
corner.
3. Analyze the simulation report that is generated or the error(s) that
have occurred, which are put into the output box on the right side of
your screen.

## How does it work?
This page uses the [gpss-server][gpss-server]{:target="_blank"} web
service to run gpss.py. The "Simulate" button at the top causes the
gpss.py program to be sent to the server and what it responds with is
put into the output box.

The [Ace code editor][ace]{:target="_blank"} is also embedded in this
page for &mdash; you guessed it &mdash; decoration, it has no real
purpose at all; it's completely useless. (It's for editing code, silly.)

[gpss-server]: https://github.com/martendo/gpss-server
[ace]: https://ace.c9.io
</section>

<script src="{{ '/web/ace/ace.js' | relative_url }}" type="text/javascript" charset="utf-8"></script>
<script src="{{ '/web/script.js' | relative_url }}" type="text/javascript" charset="utf-8"></script>
