# Feature: NFC/RFID Reading

!!! warning "Important"
    NFC/RFID support is **beta**. The core reading and Spoolman-resolution
    path is solid, but using a reader as a homing target (see
    [Per-gate readers: automatic reads during preload](#per-gate-readers-automatic-reads-during-preload)
    below) has only been confirmed on the RC522 (SPI) reader - the PN532 and
    PN7160 (I2C) haven't yet had the same bench verification.

## Concept

An NFC/RFID reader scans the tag on a filament spool and reports its UID -
a fixed identifier unique to that tag. On its own, a UID is just a string;
what makes it useful is [Spoolman](Feature-Spoolman.md), which resolves that
UID to a spool record and, from there, to filament attributes and gate
assignment. **This page covers the readers and the scan itself; what
happens with a resolved spool is [Feature: Spoolman Integration](Feature-Spoolman.md).**
The two pages cross-reference constantly - if you're setting this up for
the first time, read both.

Happy Hare supports two reader arrangements, and a unit can have either or
both at once:

- **A shared reader.** One reader, presented with a spool by hand - not
  built into any particular gate. It polls automatically once configured;
  present a tag and Happy Hare resolves it in the background. The result is
  held as a **pending spool ID** until the next filament is loaded or
  preloaded, at which point it's applied to that gate - the same "pending"
  mechanism [`MMU_GATE_MAP NEXT_SPOOLID=`](Feature-Spoolman.md#tuning) uses,
  and governed by the same `spoolman_pending_id_timeout`.
- **Per-gate readers.** One reader per gate, positioned to see the tag on
  whatever spool is loaded into that specific gate. These aren't polled
  continuously - see [Per-gate readers](#per-gate-readers-automatic-reads-during-preload)
  below for exactly when they're read.

A read can be shallow or deep:

- **UID-only** - just the tag's identifier. Enough to resolve a spool that's
  already registered in Spoolman.
- **Deep read** (`nfc_deep_read`, on by default) - also parses the tag's
  own stored data, when the tag carries any. Several third-party tag
  formats are recognised (Bambu, Creality, and the plain NDEF format used by
  OpenSpool/OpenTag-style tags and printable QR/NFC combo tags), giving
  material, color, vendor and temperature straight from the tag - useful
  on its own, and it's *also* what feeds
  [Spoolman auto-create](Feature-Spoolman.md#parameter-setup) for a tag
  Spoolman has never seen before. A tag in a format Happy Hare doesn't
  recognise still yields its UID; it just won't have parsed metadata.

## Hardware Setup

Enable this in menuconfig with **Has NFC reader(s) for RFID tag?** under
**_RFID (BETA)**, which opens an **NFC reader config** menu:

**Shared reader** (toggle **Has common NFC reader?**):

| Setting | Purpose |
|---|---|
| `NFC reader name` | Klipper object name - defaults to `<unit>_nfc` |
| `Reader type` | RC522/SPI, PN5180/SPI, PN532/I2C, PN532/UART, PN532/SPI, or PN7160/I2C |
| *(SPI types)* `CS pin`, `SPI bus name`, `SPI speed` | Chip-select pin is required; bus/speed are optional (defaults to the MCU's hardware SPI bus, 1MHz) |
| *(PN5180 only)* `BUSY pin`, `RST pin` | Both required - PN5180 has no interrupt line, so BUSY is how the driver knows a command finished, and RST is the only recovery if the chip stops responding |
| *(PN532/PN7160)* `I2C MCU name`, `I2C address`, `I2C bus type` | Address defaults to `0x24` (PN532, fixed) or `0x28` (PN7160, range `0x28`-`0x2B`) |
| *(software I2C)* `SCL pin`, `SDA pin` | Bit-banged I2C on any two GPIO pins - the only way to run more than one PN532 (fixed address) on the same MCU |
| *(UART)* `Serial device path`, `Baud rate` | PN532 in HSU mode over a USB-serial adapter plugged into the host, not an MCU - one reader per adapter |
| *(PN7160 only)* `VEN pin`, `IRQ pin` | Both optional; `IRQ pin` is recommended - it lets the presence probe ask the line directly instead of a speculative read every tick |

<p align="center">
  <img src="Feature-NFC/shared-reader-config.png" alt="NFC reader config menuconfig screen with Has common NFC reader enabled, showing the RC522/SPI defaults - reader name, CS pin, SPI bus and speed" width="70%">
</p>

A single shared reader - one physical reader a spool is presented to by
hand, not built into any gate - fits a moving-carriage design like ERCF
above particularly well, since there's naturally only one place on the
machine to put it. Per-gate readers (below) are available on any MMU
type regardless of selector design - it's purely a choice of how much
reader hardware you want to build, not something ERCF's mechanism
precludes.

**Per-gate readers** (toggle **Per-gate NFC readers?**): the same setting
group repeats per gate, each independently pointed at its own reader -
useful for the software-I2C case above, where every gate gets its own bus
and the shared `0x24`/`0x28` address stops being a conflict.

That produces one `[mmu_nfc_reader <name>]` section per reader in
`mmu_hardware.cfg`. A shared RC522 over SPI:

```ini
[mmu_nfc_reader unit0_nfc]
reader_type : rc522
cs_pin      : unit0:PA4
spi_speed   : 1000000
debug       : 0
```

A per-gate PN532, wired for software I2C so each gate gets an independent
bus at the shared `0x24` address:

```ini
[mmu_nfc_reader unit0_nfc0]
reader_type          : pn532
i2c_mcu              : unit0
i2c_address          : 36
i2c_software_scl_pin : unit0:PB8
i2c_software_sda_pin : unit0:PB9
i2c_speed            : 100000
debug                : 0
```

The owning `[mmu_unit]` in the same file then names the reader(s) it uses -
`nfc_reader` for a shared reader, or `nfc_readers` (one name per gate, blank
for a gate with none) for per-gate:

```ini
nfc_reader  : unit0_nfc               # Shared reader
nfc_readers : unit0_nfc0, unit0_nfc1  # Per-gate, one per gate slot
```

!!! tip
    A single unit can mix both: a shared reader for spools you present by
    hand, plus per-gate readers on the gates that have room for one.

No menuconfig screenshot on this page yet - the Box Turtle configuration
used for this site's other screenshots doesn't select `MMU_HAS_NFC_READER`,
and capturing one would need extra scene setup not done this session.

## Parameter Setup

In `mmu_parameters.cfg` (per unit):

```ini
nfc_deep_read               : 1        # Parse full tag contents, not just the UID
nfc_gate_jog_scan_window    : -50, 50  # Max retract/extrude (mm) when jogging to find a tag during MMU_NFC_SCAN. "0, 0" disables jogging
nfc_preload_jog_scan_window : -50, 50  # Same, but for the compound NFC/gate home MMU_PRELOAD runs (see Tuning). Defaults to nfc_gate_jog_scan_window's value
nfc_led_segment             : auto     # auto | status | exit | entry - which LED segment shows read/fail feedback
```

`nfc_deep_read` gates everything metadata-related: with it off, readers
still resolve tags to spools by UID, but never parse tag contents, never
populate the gate map from tag data directly, and never feed Spoolman
auto-create. `nfc_gate_jog_scan_window` and `nfc_preload_jog_scan_window`
only matter for per-gate readers - each is the range a different operation
will jog the filament while hunting for a tag that isn't already sitting on
the reader: [`MMU_NFC_SCAN`](#commands) uses the former,
`MMU_PRELOAD`'s automatic reader/endstop race (see [Tuning](#tuning)) uses
the latter. They're independently tunable because preload frequently homes
against a different endstop (the gate's own entry sensor) than a normal gate
load does, making the two moves' safe jogging range not always the same -
but `nfc_preload_jog_scan_window` defaults to whatever
`nfc_gate_jog_scan_window` is set to, so most setups never need to touch it
separately. Keep both inside your gate's safe travel, and size them
generously (480mm+) if you want a full spool rotation's worth of reach.
`nfc_led_segment: auto` follows the reader type - `status` for a
shared/bypass reader, `exit` for a per-gate one.

Spoolman's side of this - `spoolman_nfc_auto_create` (create an unknown tag
as a new spool) and `spoolman_pending_id_timeout` (how long a shared read
stays pending) - live in `mmu.cfg` and are documented on
[Feature: Spoolman Integration](Feature-Spoolman.md#parameter-setup).

## Commands

Full parameter reference: [`MMU_NFC`](Command-Reference.md#mmu_nfc),
[`MMU_NFC_SCAN`](Command-Reference.md#mmu_nfc_scan).

`MMU_NFC` is the day-to-day status/control command, addressing either the
shared reader, one gate, or several:

```text
MMU_NFC                        # Status of every configured reader
MMU_NFC DETAILS=1              # As above, but show the actual cached UIDs
MMU_NFC GATE=3 READ=1          # Read the reader on gate 3 once, report the result
MMU_NFC SHARED=1 READ=1 DEEP=1 # Read the shared reader and report parsed tag metadata
MMU_NFC SHARED=1 REGISTER=1    # Read + resolve/auto-create in Spoolman, report only (no gate map change)
MMU_NFC GATE=2 REGISTER=1      # Read on gate 2 and apply to the gate map, as if auto-scanned
MMU_NFC GATE=2 REGISTER=1 APPEND=1  # Read a 2nd tag on gate 2 and bind it onto the spool already assigned there
MMU_NFC GATE=2 ENABLE=0        # Hard-disable the reader on gate 2 (a disabled reader is never read)
MMU_NFC GATE=2 INIT=1          # (Re)initialize a reader that isn't responding
MMU_NFC INIT_ALL=1             # (Re)initialize every reader on every unit
```

```{.text .console-output}
MMU_NFC DETAILS=1
MMU NFC readers:
shared:  enabled=1 active=1 alive=1 tag=none
gate 0:  enabled=1 active=1 alive=1 tag=E2003412
gate 1:  enabled=1 active=0 alive=1 tag=none
```

`MMU_NFC_SCAN` re-reads the tag on a gate that's already parked - useful if
you swapped the spool without unloading/reloading, or a reader missed the
tag the first time. It jogs the filament within
`nfc_gate_jog_scan_window` until the tag reaches the reader, reads it, then
re-parks:

```text
MMU_NFC_SCAN        # Scan the current gate
MMU_NFC_SCAN GATE=2 # Scan a specific gate
```

`APPEND=1` on a `REGISTER=1` read is for a spool with more than one physical
tag - e.g. one stuck on each side, so either side scans to the same spool.
It only makes sense on a per-gate reader whose gate *already* has a spool
assigned (from an earlier scan, or set manually with
[`MMU_GATE_MAP`](Feature-Spoolman.md#commands)/[`MMU_SPOOLMAN`](Feature-Spoolman.md#commands)):
the newly-read tag is bound directly onto that spool instead of being
resolved/auto-created as if it were unknown. Two cases fall back instead of
binding:

- **`SHARED=1 REGISTER=1 APPEND=1`** - the shared reader has no gate
  assignment to bind onto, so this is rejected; use [`MMU_SPOOLMAN_TAG
  SPOOLID=<id> RFID=<uid> APPEND=1`](Feature-Spoolman.md#mmu_spoolman_tag-registering-a-tag-uid)
  directly instead, naming the spool explicitly.
- **The addressed gate has no spool assigned yet** - `APPEND=1` is ignored
  (logged, not an error) and the read falls back to normal resolve/
  auto-create, the same as without `APPEND=1`.

Two related commands live on the Spoolman side, for binding a UID onto a
spool record directly rather than scanning for one:
[`MMU_SPOOLMAN_TAG ... RFID=`](Feature-Spoolman.md#mmu_spoolman_tag-registering-a-tag-uid)
(which has its own `APPEND=1` for the same "second tag on one spool" case,
plus `RFID=''` to clear every tag from a spool, and a `REGISTER=1` mode for
binding a tag that's already been scanned onto a gate but didn't resolve at
the time - see [Registering an unresolved
tag](#registering-an-unresolved-tag-after-the-fact) below) and the `RFID=`
parameter on [`MMU_GATE_MAP`](Command-Reference.md#mmu_gate_map).

### Advanced: raw per-reader commands

Each `[mmu_nfc_reader <name>]` also answers three low-level commands that
talk to that one reader chip directly, bypassing Happy Hare's gate map,
Spoolman lookup, and enabled/active guards entirely - useful for bench-
testing a reader in isolation, less useful for normal operation (prefer
`MMU_NFC` for that): `MMU_RFID_INIT`, `MMU_RFID_READ [TIMEOUT=0.5]`,
`MMU_RFID_RELEASE`. All three take `NAME=<reader>`, only required if more
than one reader is configured.

## Printer variables exposed

`printer.mmu.nfc` is a list of per-unit dicts, present only when at least
one unit has a reader configured:

```{.text .console-output}
{'unit': 'unit0', 'polling': True,
 'shared': {'enabled': True, 'active': True, 'alive': True, 'present': False, 'uid': None},
 'gates': {0: {'enabled': True, 'active': True, 'alive': True, 'present': True, 'uid': 'E2003412'}}}
```

`gate_spool_rfid` (per-gate list, on `printer.mmu`) holds the same cached
UID, indexed by global gate number instead of nested by unit - the more
convenient form for a macro that only cares about one gate. Full reference:
[Printer Variables: NFC](Printer-Variables.md#nfc).

If LEDs are configured, reads and failures get a brief flash on the segment
`nfc_led_segment` selects - there's no separate persistent NFC indicator
beyond that transient effect.

## Tuning

### Shared reader workflow

1. Present the spool's tag to the reader.
2. Happy Hare resolves it via Spoolman in the background - nothing to run
   manually. If it resolves to a known spool, configured LEDs (see
   [Feature: LEDs](Feature-LEDs.md#parameter-setup)) pulse a slow purple
   breathing effect (`effect_pending_spoolid`) to show a spool ID is
   waiting to be claimed - the same overlay [`MMU_GATE_MAP
   NEXT_SPOOLID=`](Feature-Spoolman.md#tuning) uses, since it's the same
   underlying pending mechanism either way.
3. The pulse speeds up (`effect_pending_spoolid_expiring`) a few seconds
   before `spoolman_pending_id_timeout` runs out, as a last warning before
   the assignment is voided and the tag would need to be re-presented.
4. Load or preload filament as normal (`MMU_PRELOAD`, or just load into the
   gate if you have entry sensors) before the timeout expires. The resolved
   spool ID is applied to whichever gate that operation targets, and the
   pulsing overlay stops.

This is the same underlying mechanism as
[Spoolman's generic external-reader workflow](Feature-Spoolman.md#auto-setting-from-a-qr-code-or-any-external-reader) -
a shared NFC reader is simply one source that can produce a pending spool
ID; a QR code scanned by hand is another.

### Per-gate readers: automatic reads during preload

A gate with its own reader doesn't need a separate scan step in the normal
case: running `MMU_PRELOAD` on that gate automatically homes against
*whichever comes first* of the gate's physical endstop and its reader. The
console banner changes to confirm it - "Preloading gate N with NFC
scan...". Two outcomes:

- The **reader** triggers first (tag was between the park position and the
  endstop): the tag is read immediately, then homing continues on to the
  physical endstop as normal.
- The **endstop** triggers first (tag is further in): Happy Hare sweeps
  forward through `nfc_preload_jog_scan_window` looking for the tag, then
  re-homes back to the endstop before parking.

Use [`MMU_NFC_SCAN`](#commands) instead when the gate is already parked and
you want to (re-)read its tag without a full unload/preload cycle - e.g.
you physically swapped spools without telling Happy Hare.

### Auto-creating spools from unknown tags

To have an unregistered tag mint a new Spoolman spool automatically instead
of just failing to resolve:

1. `nfc_deep_read: 1` on the unit (default) - auto-create needs the parsed
   tag data, not just a UID.
2. `spoolman_nfc_auto_create: 1` in `mmu.cfg`.
3. `spoolman_support: push` or `pull` in `mmu.cfg` - `off`/`readonly` never
   write to Spoolman, so auto-create is suppressed regardless of this
   setting in those modes.

With all three set, scanning a brand-new tag that carries recognisable
filament data (see [Concept](#concept)) creates the spool in Spoolman and
registers the tag against it in the same step - the next scan of that same
tag resolves normally.

### Registering an unresolved tag after the fact

Auto-create needs a tag that actually carries usable filament data - a
blank tag, or one in a format Happy Hare can't parse, has nothing for
auto-create to work from and just won't resolve, even with everything above
enabled. That's fine - the UID is still recorded on the gate regardless of
whether it resolved (see [Concept](#concept)), so nothing about the scan
needs to be redone once a matching spool exists. A typical sequence for a
per-gate reader:

1. Remove the old spool, unbox the new filament, and stick a blank (or
   otherwise unregistered) tag on it.
2. `MMU_PRELOAD` it into the gate as normal. The console confirms the scan
   happened ("Preloading gate N with NFC scan...", or "tag ... recorded for
   gate N (no usable filament data)" for a blank tag) - but with no match
   in Spoolman and no metadata to auto-create from, nothing resolves.
3. Create the spool in Spoolman by hand, away from the printer - often
   easiest with the new filament's box in front of you to copy its
   parameters across.
4. Back at the printer:
   [`MMU_SPOOLMAN_TAG GATE=LAST SPOOLID=456
   REGISTER=1`](Feature-Spoolman.md#mmu_spoolman_tag-registering-a-tag-uid) -
   `GATE=LAST` picks up whichever gate was just preloaded, so there's
   nothing to look up. Happy Hare binds the gate's already-cached UID onto
   spool 456, and the gate map updates as a result, no re-scan needed.

See [Feature: Spoolman Integration: `MMU_SPOOLMAN_TAG`](Feature-Spoolman.md#mmu_spoolman_tag-registering-a-tag-uid)
for the command in full, including why `REGISTER=1` needs
`spoolman_support: readonly` or `push` specifically.

### Registering a second tag on the same spool

A spool can carry more than one physical tag - e.g. one stuck on each side,
so it resolves correctly no matter which way round it gets loaded. Reading
a second, previously-unseen UID normally treats it as an entirely different,
unregistered tag; it has to be bound onto the existing spool explicitly
instead. Two equivalent ways to do that:

1. **Scan it in** - load (or preload) the gate that already has the first
   tag's spool assigned, present the second tag to that gate's reader, then
   `MMU_NFC GATE=<n> REGISTER=1 APPEND=1` binds whatever it reads onto that
   gate's already-assigned spool.
2. **Type it in** - if both UIDs are already known, skip the reader
   entirely: `MMU_SPOOLMAN_TAG SPOOLID=<id> RFID=<new-uid> APPEND=1`.

Either path ends up calling the same underlying Spoolman write, so the
result is identical - pick whichever is more convenient at the time. A UID
that turns out to already be registered against a *different* spool is
moved over automatically either way (and the move is logged), rather than
silently leaving both spools claiming it - useful if a tag was bound to the
wrong spool by mistake earlier.

### Multiple same-address readers

PN532 is fixed at I2C address `0x24` and PN7160 at `0x28`-`0x2B` - two
PN532s (e.g. one per gate) can't share a hardware I2C bus. Give each its
own software I2C pin pair instead (see [Hardware Setup](#hardware-setup))
and the fixed address stops mattering, since each is now its own private
bus.

## Troubleshooting

- **Reader reports `alive=0`** - check wiring and the pin/address settings
  match the physical board; try `MMU_NFC ... INIT=1` (or `INIT_ALL=1`)
  after fixing anything, since a reader that came up dead at boot isn't
  retried automatically.
- **Reads report `enabled=0`** - the reader was explicitly disabled
  (`MMU_NFC ... ENABLE=0`, or it starts that way); re-enable with
  `ENABLE=1`, which also re-initializes it.
- **A deep read returns the UID but no metadata** - the tag isn't in one of
  the recognised formats (see [Concept](#concept)), or it's genuinely
  blank. UID-only resolution still works if the tag is already registered
  in Spoolman.
- **`MMU_NFC_SCAN` errors "gate is empty"** - it homes filament to find the
  tag, so there has to be filament in the gate first; preload it
  (`MMU_PRELOAD`) or, if that's wrong, mark the gate available with
  `MMU_GATE_MAP GATE=<n> AVAILABLE=1`.
- **A shared-reader tag never resolves** - confirm Spoolman is reachable and
  at a compatible version (see
  [Feature: Spoolman Integration troubleshooting](Feature-Spoolman.md#troubleshooting));
  an unresolved tag also won't retry on its own until it's removed and
  re-presented.
- **Homing to a per-gate reader behaves oddly on PN532/PN7160** - this path
  is confirmed only on RC522 so far (see the beta note at the top of this
  page); fall back to `MMU_NFC_SCAN` (a plain read after the fact, not a
  homing target) if preload's automatic behaviour is unreliable on your
  reader.
- **A scan logs "tag ... was registered to spool X - moving it to spool
  Y"** - informational, not an error: the tag was already bound to a
  different spool and Happy Hare re-pointed it to the one just scanned (see
  [Registering a second tag on the same spool](#registering-a-second-tag-on-the-same-spool)).
  Expected after re-tagging a spool or fixing a mistyped UID; worth
  double-checking the spool IDs named in the message if it appears
  unexpectedly.

## See also

- [Feature: Spoolman Integration](Feature-Spoolman.md) - what a resolved
  tag actually does: activation, attributes, auto-create
- [Command Reference: `MMU_NFC`](Command-Reference.md#mmu_nfc)
- [Command Reference: `MMU_NFC_SCAN`](Command-Reference.md#mmu_nfc_scan)
- [Command Reference: `MMU_SPOOLMAN`](Command-Reference.md#mmu_spoolman)
- [Command Reference: `MMU_SPOOLMAN_TAG`](Command-Reference.md#mmu_spoolman_tag)
- [Command Reference: `MMU_GATE_MAP`](Command-Reference.md#mmu_gate_map)
- [Printer Variables: NFC](Printer-Variables.md#nfc)

---

