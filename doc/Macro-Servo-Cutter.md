# Macro: Servo Cutter

## What it does

Tunes a servo-actuated cutter mounted **at the MMU** end of the bowden
(the EREC design, or similar) - additive to tip forming rather than a
replacement for it: a decent tip still needs to exist going into the cut.
See [Feature: Addon Integrations](Feature-Addon-Integrations.md#servo-cutter-erec-and-similar)
for the physical build/wiring and [Feature: Tip Forming and
Purging](Feature-Tip-Forming-Purging.md#servo-cutter-mmu-mounted) for how it
fits alongside whichever tip-forming method is active.

## Where it's applied

Defined in `mmu_servo_cutter.cfg` as `SERVO_CUTTER_ACTION` - after the
filament parks in the gate, it advances the filament, activates the cutter,
then parks again, firing a `filament_cut` event
([Feature: Statistics & Consumption Counters](Feature-Statistics-Counters.md#consumption-counters)
can count these). Unlike most of the macros on this site, enabling the
capability in menuconfig does **not** wire this one up automatically - the
Kconfig prompt's own help text says as much ("after enabling this be sure to
edit Macro variables"). Add it as a
[post-unload extension hook](Macro-Sequence.md) yourself:

```yaml
variable_user_post_unload_extension : 'SERVO_CUTTER_ACTION'
```

!!! note
    `mmu_macro_vars.cfg`'s own section banner for this block describes it as
    a "post_load_extension" - that's stale relative to the macro file's own
    header comment and the hook it's actually written to receive
    (`user_post_unload_extension`); wire it up per the macro file's own
    instruction above, not the banner text.

## Configuration

<p align="center">
  <img src="Macro-Servo-Cutter/servo-cutter.png" alt="menuconfig: Servo cutter at MMU (_MMU_SERVO_CUTTER) screen, showing servo angles/timing and feed/cut length settings" width="85%">
</p>

`_MMU_SERVO_CUTTER_VARS` in `mmu_macro_vars.cfg`, reachable from
menuconfig's **Macro Variables → Servo cutter at MMU
(\_MMU_SERVO_CUTTER)** screen shown above, once **Have servo cutter at
MMU?** is enabled under **Tip Forming / Cutting**. Full variable table:
[Macro Variables: Servo cutter,
MMU-mounted](Macro-Vars.md#servo-cutter-mmu-mounted-_mmu_servo_cutter_vars).

`feed_length` - the distance from the gate parking position to the blade -
is the one setting worth calibrating carefully rather than guessing: `48`mm
covers ERCF v2 and most other designs, `58`mm is the ERCF v1.1 value.

## See also

- [Feature: Addon Integrations](Feature-Addon-Integrations.md#servo-cutter-erec-and-similar) -
  physical build and wiring
- [Feature: Tip Forming and Purging](Feature-Tip-Forming-Purging.md#servo-cutter-mmu-mounted) -
  how this fits alongside tip forming/cutting
- [Macro Variables: Servo cutter, MMU-mounted](Macro-Vars.md#servo-cutter-mmu-mounted-_mmu_servo_cutter_vars) -
  every `_MMU_SERVO_CUTTER_VARS` setting in full
- [Macro: Sequence](Macro-Sequence.md) - the `post_load_extension` mechanism
  this macro runs through

---
