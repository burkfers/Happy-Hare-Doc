# Getting Started with Enrage Rabbit Carrot Feeder (ERCF)

The Enraged Rabbit Carrot Feeder (ERCF) is the original Multi Material Unit for Voron printers that started it all.
It's evolved considerably since it's formative v1.0 release. This guide walks through the initial
**`menuconfig`** pass for setting up an ERCF‑style MMU — the screens you’ll encounter, the order they appear in,
and the handful of selections that actually matter to getting core ERCF functionality up and running.

As it's evolved (v1, v1.1, v2, v2.5, and v3), the ERCF ecosystem has expanded into a wide range of permutations
including:

* Jack Rabbit, servo-less selector variants
* Multiple selector servo options
* Different encoder options (TCRT, and Binky optical encoders)
* Direct‑drive and geared NEMA 14 & 17 options
* Optional entry sensors
* Optional LEDS/Neopixel bling
* Optional integrated filament buffer

Each revision introduces its own mechanical differences, quality of life improvements and optional features, 
which means the exact configuration screens you see — and the choices worth pausing on — depend on the 
hardware you’ve built.

**The goal here is simple:** get your ERCF‑style MMU installed, recognized by Klipper, and performing 
base load/unload operations. Once operational, optional capabilities like LED's, entry sensors and
more advanced Happy Hare features can be enabled, configured and calibrated.

## Menuconfig Installer
From your Happy-Hare checkout/directory:

```bash
./install.sh
```

If this is the very first time you've run `./install.sh`, there's no `.mmu_config` yet, so the installer
drops you straight into the interactive `menuconfig` mode — no separate `-i` flag needed.

<p align="center">
  <img src="GettingStarted-ERCF/01-first-run.png" alt="First run: nothing configured yet" width="70%">
</p>
<br>

This is the installer's default state: `MMU Type` is `Custom Design`, the board is unknown, and the
**`CONFIG WARNINGS / ERRORS`** panel at the bottom lists exactly that — four things still need a decision.
As soon as you pick a real MMU type, most of these clear themselves.

### Choosing the MMU type
Highlight **`MMU Type`** and press Enter. Move down to **`ERCF - Enraged Rabbit Carrot Feeder`** and press
++space++ to select it. Once selected (`(X) ERCF - Enraged Rabbit Carrot Feeder`), five new options appear
indented underneath — **`Version`**,**`Number of gates/lanes`**, **`Selector servo type`**,
 **`Project Options`** and **`Design attributes`** — options that only make sense once Happy Hare knows this
 is an ERCF. Other settings and options are also enabled based on the MMU design choice.
<br>

<p align="center">
  <img src="GettingStarted-ERCF/02-mmu-type-ercf.png" alt="MMU Type list, with ERCF selected" width="70%">
</p>
<br>
<br>
Enter the **`Number of gates/lanes`** to match your ERCF build. Different ERCF generations use different
gate conventions, so lane counts typically fall into multiples of **`3`** or **`4`** depending on the generation
built (e.g. versions < v2.x, groups of **`3`**, others groups of **`4`**).

The default is **`8`** gates, but you can change it to match your build — in this case, setting it to **`6`** gates.

<p align="center">
  <img src="GettingStarted-ERCF/03-lanes.png" alt="Defaults to 10" width="70%">
</p>
<br>
<br>
Next, select the **`Selector servo type`**. For most ERCF v3 builds the default is the **`GuoHua A0090`**, 
with several other common kit servos included in the list — **`GDW DS041MG`** and **`MG‑90S`** among them.

You’ll also find the **`Savox SH‑0255MG`**, a community‑favourite and widely regarded as the _Gucci_, 
ultra‑reliable option thanks to its consistent torque and proven, long‑term durability.

If your build uses a different servo, select **`Not listed`**. Servo settings such as min/max
pulse widths, etc. are managed using `(Top) → Other Settings → Selector servo` options later in the
`menuconfig` workflow.

In this example, we have selected the **`Savox SH-0255MG`** servo.

<p align="center">
  <img src="GettingStarted-ERCF/04-selector-servo-type.png" alt="Selector servo type" width="70%">
</p>
<br>
<br>
Next, review applicable Project Options. If your ERCF build uses the servo-less selector or integrated
**Enraged Rabbit Cotton Tail** (ERCT) Filament Buffer, select and enable these here.

<p align="center">
  <img src="GettingStarted-ERCF/05-project-options.png" alt="Project Options" width="70%">
</p>
<br>
<br>
Back out twice (++esc++, ++esc++) to return to the top menu, and review the warnings panel again. Three of the 
four warnings are already gone. The one that's left — *"`Toolhead type is 'other'`"* — is exactly what it sounds
like: Happy Hare still doesn't know your toolhead, and that's covered in a different getting-started page. 
Don't worry about it here.

<p align="center">
  <img src="GettingStarted-ERCF/06-root-warnings.png" alt="Root menu after choosing ERCF - one warning left" width="70%">
</p>

### Board type
Enter **Controller Board type**. Because you’ve already told the configurator this is an ERCF and its version, 
Happy Hare pre‑selects `BTT MMB v2.0 with CANbus` — the most common controller for more recent ERCF kits and builds.
If your ERCF runs a different controller, this is where you’d choose it; default pins for steppers, sensors, and
TMC drivers throughout the rest of `menuconfig` are derived from whatever controller you select here.

<p align="center">
  <img src="GettingStarted-ERCF/07-board-type.png" alt="Board type list, BTT MMB v2.0 with CANBus already selected" width="70%">
</p>

### MCU connection
++esc++ and back out to the top menu and open **`MCU connection`**. ERCF defaults to USB serial, but if your setup
uses CANBus, select CAN instead. The installer attempts to auto‑detect USB serial device IDs and CANBus UUIDs where
possible for you to choose from. Unfortunately, if Klipper has previously claimed a CANBus device, UUID's can’t
be rediscovered easily unless you remove/comment all references from your Klipper/Kalico Happy Hare configuration and 
power cycle the printer.

If you’re unsure of the USB serial or CANBus UUID's when migrating to v4, you can check your saved
`mmu.v3/base/mmu_hardware.cfg` configuration or `klippy.log` for previous device ID's/UUID's. The installer will
then prompt you for your serial device or CANBus UUID, depending on the option selected.
Existing connection selections/mapping's are retained and not overwritten once saved.

The first discovered serial device is selected by default. Press enter to choose a different discovered device.

<p align="center">
  <img src="GettingStarted-ERCF/08-mcu-connection.png" alt="MCU connection" width="70%">
</p>
<br>

In this example, we are going to switch to CANBus. Open **`MCU connection`** and select **`CANbus`**:
<p align="center">
  <img src="GettingStarted-ERCF/08-mcu-connection-canbus.png" alt="MCU connection" width="70%">
</p>
<br>

A list of discovered CANBus UUIDs is shown. If more than one device is found, select the one that corresponds to 
your ERCF controller. If only one device is detected, it will be selected automatically.
If no UUIDs are discovered, choose **`Other / manually entered`** and enter the correct CANBus UUID manually.
<p align="center">
  <img src="GettingStarted-ERCF/08-mcu-connection-canbus-uuids.png" alt="MCU connection" width="70%">
</p>

### Pins: gear and selector direction
++esc++ and back out to the top menu and open **`Pins / TMC`**, then **`Gear pins`**. GPIO Pin defaults are set based
on your MCU controller board and ERCF MMU version selection. Review all pin settings for **`Gear`** and **`Selector`**
steppers to make sure they are correct for your build. Gear direction especially is the one setting that is impossible
to set correctly by default or guessing and depends on how the stepper cable is _actually wired_. You will validate
this later when you buzz the steppers to verify their direction in
[Stepper direction and homing](GettingStarted-ERCF/10-stepper-direction-and-homing.md).

This is where you would change the stepper direction if needed.

<p align="center">
  <img src="GettingStarted-ERCF/09-gear-pins.png" alt="Gear pins list - one row per gate" width="70%">
</p>
<br>

If the stepper spins the wrong way, you can invert it here without rewiring or hand-editing the configuration.
Highlight the **`Gear dir pin`** for the stepper and press Enter to open its editor. If that stepper needs reversing,
add a `!` in front of the pin name — Klipper's standard way of inverting a pin's polarity.

<p align="center">
  <img src="GettingStarted-ERCF/09-gear-dir-inverted.png" alt="Gear dir pin editor, showing the default pin" width="70%">
</p>
<br>

**Repeat** this for the **`selector stepper`**.

### Encoder
ERCF uses an encoder for filament loading, and ... Happy Hare requires one viable gate sensor — either a switch or an encoder. Most Tradrack builds use a single 

<p align="center">
  <img src="GettingStarted-ERCF/11-Endstops.png" alt="Endstops" width="70%">
</p>

### Picking a toolhead
From the top menu, select **Toolhead**. This step is optional — if you skip it, Happy Hare falls back to generic
**`Other/Unknown`** default  dimensions, which is a perfectly fine starting point. But if your toolhead 
(extruder + hotend combo) appears in the list, selecting it gives you real, community‑contributed measurements
instead of generic estimates. Here we’ve chosen **`A4T WWBMG for A4T Dragon Ace`** to illustrate.

<p align="center">
  <img src="GettingStarted-ERCF/10-toolhead-selected.png" alt="Toolhead list, Stealthburner Clockwork2 Rapido HF selected" width="70%">
</p>
<br>

++esc++ to backout to the top menu and select **Toolhead sensors/settings**. This is where you can enable other features 
such as **`Toolhead cutter`**, **`toolhead`** and **`extruder entry`** sensors if fitted. The community-contributed
measurements for **`Extruder entrance to nozzle`** and **`Residual filament`**, under **`Toolhead dimensions`**,
can be reviewed and tuned if necessary. For **`Stealthburner Clockwork2 Rapido HF`**, the values are`88` and `36.5`.

The other two distances Happy Hare can use (**`Toolhead sensor to nozzle`** & **`Extruder sensor to entry`**) 
only appear when you have enabled the sensors and remain hidden when disabled.

<p align="center">
  <img src="GettingStarted-ERCF/10-all-toolhead-dimensions-combined.png" alt="Toolhead dimensions, pre-filled from the selected combo" width="70%">
</p>
<br>

This is a shortcut, not a substitute: even with community-sourced toolhead measurements, it's useful to learn how to 
measure and calibrate your own eventually, since small build variations and mods add up. But it's a genuinely good 
starting point. If your exact combo isn't listed, select **`Other/Unknown`** and follow the manual calibration
[`MMU_CALIBRATE_TOOLHEAD`](Calibration-Toolhead.md) process.

### MMU Features / Additions
Optional ERCF features can be enabled or disabled based on your ERCF build here. Popular community contributed 
extensions like Sync-feedback buffers (sensors) such as Annex Belay or more recent analog Proportional Sync 
Feedback sensors, Encoder, etc. can be enabled here.

Note the Encoder is mandatory and is enabled by default as it's required for the ERCF to function correctly.

<p align="center">
  <img src="GettingStarted-ERCF/12-mmu-features.png" alt="MMU features" width="70%">
</p>

## Validating Hardware setup & initial calibration
### Stepper direction and homing
### Selector calibration
### Encoder calibration
## Checking Basic Operation
That's it, you should now be able to load and unload filament using your ERCF MMU. The bowden length will be automatically calibrated
the first time you attempt to load filament (`autocal_bowden_length: 1` setting) using collision based homing by default, extruder
sensors, or compression / proportional sync feedback sensors if defined and set as the **`extruder homing endstop`** in **`menuconfig`**.

Outside of a print, confirm the basics work end to end (if using ASB/ASA, preheat the extruder to an appropriate temperature as the default
minimum preheat temperature is 210°C).

Issue the following commands to validate the basic load/unload operation:

```{.text .console-command}
MMU_SELECT GATE=0
MMU_LOAD
MMU_UNLOAD
```

Each command should complete without error — no pauses, no "not calibrated" warnings you weren't expecting. If something goes wrong here, 
it's much easier to diagnose now than mid-print; see [Operation: Debugging Problems](Operation.md#debugging-problems) if any of 
it doesn't behave as expected.

## What Next?
- [Gear Rotation Distance Calibration](Calibration-Gear.md) - It's worthwhile manually calibrating the gear stepper rotation 
  distance to fine tune out-of-the-box defaults as BMG extruder gear manufacturing tolerances do matter, affecting accuracy. 
  As the ERCF uses separate BMG gearsets for each gate, each gate needs to be calibrated individually. You can also enable
  **`Autotune rotation distance`** in `(Top) → Other Settings → Calibration/Autotuning` to enable Happy Hare to automatically
  tune `rotation distance`** for each gate when it's loaded. **NOTE** This can mask other selector build issues so defaults
  to **OFF**.
- [Purge and Tip Forming](Purge-Tip-Forming.md) to get your ERCF ready for printing
- Install [KlipperScreen (Happy Hare edition)](KlipperScreen.md) if you
  want a touchscreen front end, or drive everything from [Mainsail /
  Fluidd](Mainsail-Fluidd-Integration.md) — either works, and both are
  covered.
- From here, explore the rest of this site's [Features](Feature-Espooler.md)
  section one page at a time as you actually need them — Spoolman
  integration, Toolhead cutter, **`Blobifier`**, Shared NFC/RFID reader, EndlessSpool, and the rest. Trying to absorb
  all of it before your first print is the fastest way to feel overwhelmed by an MMU that, day to day, mostly just works.

---
