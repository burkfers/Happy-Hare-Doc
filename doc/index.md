<p align="center">
  <img src="assets/images/logo.jpg" alt="Happy Hare" width="220">
</p>

# Happy Hare

<p align="center"><em>Universal Automated Filament Changer / MMU driver for Klipper</em></p>

Happy Hare is the original open-source filament changer controller for multi-colour
printing. Its philosophy is to provide a universal control system that adapts to
your choice of MMU (Multi-Material Unit) - switch hardware and the software
transitions seamlessly with you.

This site is under construction - see `TOC.md` in the repository root for the
planned structure. A few pages exist so far:

<div class="grid cards" markdown>

-   **Getting Started**

    ---

    New to Happy Hare? Walk through installing and configuring a Box Turtle from
    scratch, `menuconfig` screen by screen.

    [Box Turtle guide &rarr;](GettingStartedWithBoxTurtle.md)

-   **Command Reference**

    ---

    Every `MMU_*` command - parameters and examples generated straight from the
    source, never hand-transcribed.

    [Command Reference &rarr;](Command-Reference.md)

-   **Printer Variables**

    ---

    Every `printer.mmu.*` variable, and the deprecated ones still kept around
    for KlipperScreen/Mainsail/Fluidd.

    [Printer Variable Reference &rarr;](Printer-Variables.md)

-   **Features: eSpooler**

    ---

    How Happy Hare drives a DC-motor eSpooler - continuous rewind/assist tied
    to gear speed, plus burst-triggered in-print assist.

    [eSpooler &rarr;](Feature-Espooler.md)

-   **Developer Guide**

    ---

    Code layout and object ownership, the Kconfig/installer pipeline, and
    running Happy Hare - tested or interactively - with no printer attached.

    [Code Layout &rarr;](Dev-Code-Layout.md)

</div>

---

<div class="hh-footer">
<pre class="hh-footer-art">
  (\_/)
  ( *,*)
  (")_(") Happy Hare Ready
</pre>
<p class="hh-footer-copyright">Copyright (C) 2022-2026 Paul Morgan</p>
</div>
