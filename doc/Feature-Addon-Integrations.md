# Feature: Addon Integrations

## Concept

A few community hardware add-ons have become common enough companions to an
MMU that Happy Hare has first-class support for them - but unlike the older
`[include mmu/addons/...]` file-copying approach, that support is now native
menuconfig-driven configuration, the same as everything else on this site.
This page is the index for those add-ons: most of them are now documented in
depth elsewhere, and this page just points you to the right place. Eject
buttons are the one add-on with no other home, so it gets full treatment
here.

## Servo Cutter (EREC and similar)

<p align="center">
  <img src="Feature-Addon-Integrations/erec-logo.jpg" alt="EREC filament cutter" width="45%">
</p>

An MMU-mounted servo cutter that trims the filament tip after unload -
originally the EREC design, but the feature supports any similar
servo-actuated cutter at the MMU end of the bowden. Fully native now: enable
**Have servo cutter at MMU?** under menuconfig's Tip Forming/Cutting screen,
wire the servo pin, and tune it in `mmu_macro_vars.cfg`. See [Feature: Tip
Forming and Purging](Feature-Tip-Forming-Purging.md#servo-cutter-mmu-mounted)
for full setup - this isn't a separate `[include ...]` file to copy in
anymore. You'll still need the physical build/wiring instructions from
[EREC's own project page](https://github.com/kevinakasam/ERCF_Filament_Cutter).

## Blobifier

<p align="center">
  <img src="Feature-Addon-Integrations/blobifier.jpg" alt="Blobifier purge system" width="45%">
</p>

A standalone purge system that replaces the slicer's wipe tower with a small
tray/bucket mechanism - also fully native now, via menuconfig's Purging
screen (**Have Blobifier?**). See [Feature: Tip Forming and
Purging](Feature-Tip-Forming-Purging.md) for the `purge_macro`/parking
setup; Blobifier's own large set of tuning variables (purge speed, brush
geometry, tray positions, bucket-shaker behaviour) live in
`mmu_macro_vars.cfg`'s `_BLOBIFIER_VARS` once enabled - see [Macro
Variables: Blobifier](Macro-Vars.md#blobifier-_blobifier_vars) for the full
list. Physical build instructions are at [Blobifier's own project
page](https://github.com/Dendrowen/Blobifier).

!!! note
    Parking the nozzle over the tray during a swap is better handled through
    the standard parking configuration in `mmu_macro_vars.cfg` than the
    older `variable_user_post_form_tip_extension: 'BLOBIFIER_PARK'`
    approach - the newer mechanism accounts for toolhead movement more
    generally rather than being specific to this one add-on.

## DC eSpooler

Fully absorbed into Happy Hare's own built-in eSpooler support - not a
separate add-on to install at all any more. See [Feature:
eSpooler](Feature-Espooler.md).

## Eject Buttons

Some designs (QuattroBox, for example) fit a physical button per gate that
ejects that gate's filament directly. Enable under **MMU Features /
Additions**:

<p align="center">
  <img src="Feature-Addon-Integrations/eject-buttons.png" alt="Mmu eject buttons config screen: one pin prompt per gate, blank by default" width="80%">
</p>

Each configured pin produces a `[gcode_button ...]` in `mmu_hardware.cfg`
that calls [`MMU_EJECT`](Command-Reference.md#mmu_eject) for that specific
gate:

```yaml
[gcode_button unit0_eject0]
pin: ^unit0_gate0:PB2
press_gcode:
    MMU_EJECT UNIT=unit0 LGATE=0
```

`LGATE=` (local gate index) is exactly what a physical per-gate button
needs and isn't something you'd normally type by hand on the console -
`MMU_EJECT GATE=<n>` (the global gate number) is the everyday form for
manual use.

!!! warning "Important"
    Pin polarity depends on your button's wiring, not just its pin number.
    Most eject buttons are normally-closed switches and want a plain
    pull-up pin (`^unit0_gate0:PB2`). Normally-open momentary buttons (like
    the EMU LED Button Board) need an **inverted** pin instead
    (`^!unit0_gate0:PB2`) - get this backwards and Klipper can see the
    button as already pressed right after a restart, ejecting filament on
    its own.

## Troubleshooting

- **A gate ejects on its own after a restart** - the eject button's pin
  polarity doesn't match how it's wired; see the warning above.
- **Looking for the old `mmu/addons/` files for EREC/Blobifier/DC eSpooler**
  - they don't exist any more; all three are native menuconfig features
  now, documented on the pages linked above.

## See also

- [Feature: Tip Forming and Purging](Feature-Tip-Forming-Purging.md) - EREC/servo cutter and Blobifier setup
- [Feature: eSpooler](Feature-Espooler.md) - the native replacement for the old DC eSpooler add-on
- [Command Reference: `MMU_EJECT`](Command-Reference.md#mmu_eject)

---

<div class="hh-footer">
<pre class="hh-footer-art">
  (\_/)
  ( *,*)
  (")_(") Happy Hare Ready
</pre>
<p class="hh-footer-copyright">Copyright (C) 2022-2026 Paul Morgan</p>
</div>
