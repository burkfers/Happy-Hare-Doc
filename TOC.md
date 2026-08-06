# Happy Hare v4 documentation — table of contents (planning)

This is the working plan for the new documentation site. It maps every planned page to
its source material and status, so writing sessions can pick up a page without
re-deriving context. It is a planning document, not a published page — it lives at the
repo root (not under `doc/`) specifically so it's never a candidate for publishing; see
**Session log** at the bottom for where things actually stand and how to pick this back up.

## Structure decisions locked in

- **This is a separate repo from Happy Hare's source code**, added 2026-08-06 —
  everything below (`doc/`, `doc_tools/`, this file, `mkdocs.yml`) used to live
  inside the Happy-Hare repo itself; moved out to `Happy-Hare-Doc` because `doc/`
  carries a lot of screenshots and a Happy-Hare *code* checkout has no reason to
  pull that down. `doc_tools/gen_command_reference.py` and `doc_tools/capture.py`
  still need to read Happy-Hare's source tree (`extras/mmu/**`,
  `installer/Kconfig*`) to regenerate `Command-Reference.md`/screenshots — that
  happens via `HAPPY_HARE_SRC`, fetched automatically by `make
  shots`/`command_reference` (pinned to the branch/tag in `HAPPY_HARE_REF`, or
  point it at a checkout you already have). `docs`/`docs_build`/`docs_preview`
  (and this repo's CI/Pages deploy) need none of that — they only render the
  `doc/*.md` and images already committed here. See the root `README.md` for the
  contributor-facing version of this, and `doc_tools/README.md` for exactly how
  the source-fetch mechanism works.
- **Layout:** flat at `doc/` root, matching `doc_tools/shots.py`'s existing
  convention — page `doc/Foo.md`, images in sibling `doc/Foo/`. No churn to the
  Box Turtle page or its sessions. `mkdocs.yml` has `docs_dir: doc` (site output
  is `./site`, Zensical's own default — deliberately left unset in the config
  rather than renamed; see the Makefile/`mkdocs.yml` comments for why).
- **Site generator: [Zensical](https://zensical.org), not mkdocs**, reading the
  same `mkdocs.yml` format ("your current settings just work" checked out in
  practice). `doc_tools/README.md` has the full rationale and the `make
  docs`/`docs_build`/`docs_preview`/`command_reference` targets. It's genuinely
  pre-1.0 (`0.0.52` on PyPI) — see **Zensical rough edges** below before
  reaching for anything fancy in a new page.
- **Theme:** Material variant `classic` (not Zensical's newer default `modern`,
  which doesn't colour the header from `primary` at all), black primary + the
  brand's own hot pink accent (`#FF69B4`-family, matching the neon-hare logo and
  HH's own console warning colour). Logo/favicon are real assets under
  `doc/assets/images/`, generated from `wiki/resources/happy_hare_logo.jpg`.
- **No `[TOC]` marker on any page** — superseded partway through: the theme's own
  "On this page" sidebar makes an inline copy pure duplication, on every page,
  not just generated ones. See `doc_tools/README.md`'s Page Conventions section.
- **No ` ```mermaid ` fenced code blocks** — tried, found non-deterministic
  across clean rebuilds, and reverted; see **Zensical rough edges**.
  Architecture diagrams in the Developer Guide are plain ASCII in fenced code
  blocks instead. `Feature-Spoolman.md` later re-introduced Mermaid via a
  different mechanism (raw `<pre class="mermaid">` HTML, not a fence) — see
  item 33 below before assuming this bullet still means "no Mermaid anywhere."
- **Getting Started scope (v1):** Box Turtle only, walked deep. Everything else gets
  a comparison table + "same pattern, different Kconfig starter" note. Multi-unit and
  additional MMUs come later as their own pages.
- **Generated vs hand-written:** Command Reference and Printer Variable Reference
  are *generated*/*code-verified* respectively from source (see §10 below) rather
  than hand-transcribed — same "code in `doc_tools/`, output in `doc/`" split
  already established for screenshots. The four Configuration Reference pages
  (§3) are still planned as generated but not yet built. Everything else is
  hand-written prose, informed by the wiki.
- **v3→v4 flag:** any page ported from `wiki/` gets a ⚠️ in its status table
  entry until someone verifies it against v4 code. The riskiest one flagged
  this way was the Type-A/Type-B taxonomy on `Conceptual-MMU.md` — v4's real
  selector classes (`LinearSelector`, `LinearServoSelector`, `ServoSelector`,
  `IndexedSelector`, `RotarySelector`, `VirtualSelector`, plus multi-gear
  variants, documented in `doc/Dev-Code-Layout.md`) don't map cleanly onto
  the old binary split — that page is now done (§2), rewritten around the
  real hierarchy rather than ported; see the session log for how.
- **Avoid explicit counts that go stale** (test counts, command counts). Prefer
  ">900 tests" / "browse the source" phrasing over a number that will be wrong
  by the next PR — learned the hard way when a ported "69 commands, 14 tested"
  figure turned out to already be stale (`Command-Reference.md` now lists 88).
- **No v3-vs-v4 narrative in the reader-facing text of ANY page**, including
  ones written before this rule (added 2026-08-06, extended the same day once
  the user confirmed the rule is retroactive) — this is v4-only documentation;
  a fresh reader doesn't care what changed from a version they never used.
  This does NOT relax verifying against v4 *code* rather than porting the v3
  wiki's prose uncritically (see the counts bullet above and the whole reason
  `Feature-Espooler.md` exists) — it only means the verified result gets
  stated as plain fact, not as "v3 said X, v4 actually does Y."
  `Printer-Variables.md` has been retrofitted: removed its "What changed
  since v3" section and the "Not currently exposed here: servo/grip" aside
  (the servo/grip finding itself moved to `Dev-Code-Layout.md`, a developer
  page, rather than being lost), stripped the `Klipper events` table's
  `Since` column and "signature changed"/"new in v4" language, and dropped a
  stray "(unchanged from v3)". **The only meta-notation that page still
  carries is deprecation status** (the `Deprecated variables` table) — that's
  the one exception to "no version narrative" and is explicitly wanted.
- **No Happy Hare "developer" references outside the Developer Guide, on ANY
  page** (added 2026-08-06, confirmed page-genre-wide the same day — this was
  the open question below, now resolved) — no Python class/method names,
  `get_status()` citations, or file paths, whether used to *explain* behaviour
  or as a "where this number comes from" byline. Say "an extruder-movement
  monitor triggers a burst" not "`MmuExtruderMonitor` fires a callback which
  calls `advance()`"; say "The main status object" not "built by
  `MmuController.get_status()` (`extras/mmu/mmu_controller.py`)". Retrofitted
  into `Printer-Variables.md` (stripped every `Mmu*.get_status()`/file-path
  citation, the "Registered from" column, and the `FILAMENT_POS_*`/
  `TOOL_GATE_BYPASS` constant-name mentions) and `Command-Reference.md`'s
  generator (dropped `HELP_BRIEF`/`extras/mmu/`/the "regenerate with `make
  command_reference`" maintenance note from the reader-facing intro — that
  note now only needs to exist for a doc contributor, i.e. in
  `Dev-Doc-Tooling.md`, not on the page a normal user reads for command
  syntax). `mmu_parameters`/`.cfg` keys, `MMU_*` command names, Klipper
  config section names (`[mmu_espooler unit0]`), and Klipper's own API calls
  a reader would write themselves to extend Happy Hare in Python
  (`printer.send_event(...)`, `printer.register_event_handler(...)`) are NOT
  developer references — those are exactly what the reader types/edits, keep
  them. The Developer Guide (§12) is the one place all of the above is
  fair game, by design.
- **No leading "everything below was read from..." provenance paragraph** —
  dropped from `Feature-Espooler.md`; reads like an internal QA note, not
  content for the reader. The verification habit itself doesn't change (see
  the counts/no-narrative bullets above) — it just doesn't need to announce
  itself on the page. Start Feature pages directly at `## Concept`.
- **Pin aliases don't exist in v4** — `mmu_hardware.cfg` pin values are
  fully-specified `unit_mcu_name:pin_name` strings (e.g. `unit0:PA0`) filled
  in directly from the menuconfig prompt; there is no separate alias
  indirection layer in `mmu.cfg` the way the v3 wiki described. Don't port
  the wiki's "define aliases in mmu.cfg" pattern into any new config example.
- **"Filament (catchment) buffer" and "sync-feedback buffer" are two
  different Kconfig options** (`MMU_HAS_FILAMENT_BUFFER` /
  `Kconfig.filament_buffer` vs `MMU_HAS_SYNC_FEEDBACK_BUFFER` /
  `Kconfig.sync_feedback_buffer`) — don't conflate them into "sync-feedback
  filament buffer". `Feature-Espooler.md` and `Printer-Variables.md`
  (`filament_buffer` field) both had this wrong; fixed 2026-08-06. The
  catchment buffer catches loose filament on rewind for faster loading
  speeds; sync feedback is the tension/compression buffer feeding FlowGuard
  and tangle prevention. Espooler is mutually exclusive with the *catchment*
  buffer specifically, not sync feedback.
- **Every page ends with the ASCII-art footer + copyright line**, matching
  the wiki's own tradition (added 2026-08-06, retrofitted to every existing
  page including `Command-Reference.md`'s generator). Raw HTML, not a
  ` ```text ` fenced block — a fenced block goes through `codehilite` and
  picks up its box/background styling (see the code-block CSS entry above),
  which reads as "a code sample to copy," the wrong register for this. Bare
  `<pre>`/`<p>` with dedicated classes get the same monospace rendering
  without that box, and let the copyright line go genuinely small
  (`.hh-footer-copyright`, `font-size: 0.6rem` — reads as fine print, not a
  second line of body text):
  ```html
  ---

  <pre class="hh-footer-art">
    (\_/)
    ( *,*)
    (")_(") Happy Hare Ready
  </pre>
  <p class="hh-footer-copyright">Copyright (C) 2022-2026 Paul Morgan</p>
  ```
  Both classes are defined once in `doc/assets/stylesheets/extra.css`. For a
  generated page, put this in the generator (see
  `doc_tools/gen_command_reference.py`'s `render_page()`), not by hand-editing
  the output — it would be lost on the next regeneration otherwise.
- **H2 sections get a tri-colour marker + underline site-wide**, via
  `doc/assets/stylesheets/extra.css` (`.md-typeset h2::before` + border) —
  the CSS-template equivalent of the wiki's per-heading
  `![#f03c15]![#c5f015]![#1589F0]` square images, applied automatically to
  every page (present and future) rather than per-page markup. Added
  2026-08-06 on request ("liked the visual color icons... helps provide
  visual separation").
- **Reuse a wiki diagram even if its labels are stale — but only if it's an
  editable diagram, not a screenshot of real output.** Added 2026-08-06 after
  the user pushed back on `Conceptual-MMU.md` skipping the wiki's images
  entirely: a labeled mechanism drawing (`typeA_mmu.png` etc.) still shows a
  true concept even with renamed sensor labels, and gets a corrective
  caption/tip instead of being dropped. A live Mainsail/console screenshot of
  actual sensor names (`filament_sensors.png`, `endstops.png`,
  `mmu_sensors.png`) is different — that's *real output*, and republishing it
  with old names presents something a v4 reader would never actually see, no
  caption fixes that. Skipped those three specifically, flagged why rather
  than silently dropping them.
- **Previous/Next page footer nav, Discord icon, taller header with a bigger
  logo + tagline, smaller footer ASCII-art font** — all added 2026-08-06,
  site-wide via `doc/assets/stylesheets/extra.css` +
  `doc/assets/javascripts/hh-page-nav.js` + `mkdocs.yml`'s `extra.social`.
  Two non-obvious findings if touching any of this again:
  - Zensical renders **no** prev/next footer nav at all (no
    `.md-footer__link` markup on any page, checked directly) — this isn't a
    missing config flag, it's just not implemented. `hh-page-nav.js`
    computes it client-side instead, by reading the already-rendered primary
    sidebar (which lists every real page in nav order already, mixed with
    the current page's own on-page anchors — filtering out any `href`
    containing `#` leaves exactly the flat page list, so there's no second
    copy of the nav order to keep in sync with `mkdocs.yml`). Must run on
    `document$.subscribe(...)`, not `DOMContentLoaded` — `navigation.instant`
    swaps page content via `history.pushState` after the first load, and a
    plain load-event listener never fires again after that.
  - `.md-header__title`/`.md-header__ellipsis`/`.md-header__topic` have a
    hard-coded height that's load-bearing for Material's site-name → page
    -title slide-swap-on-scroll animation — making that box itself taller
    (e.g. via a naive `::after` tagline with `display:block`) doesn't grow
    it, the extra content just overflows past `.md-header`'s own background
    and appears to spill onto the page below. The tagline is instead
    `position:absolute; top:100%` off the site-name topic specifically
    (`position:relative` added there as the anchor), so it floats below
    without affecting that box's own height/animation at all;
    `.md-header__inner` separately gets a plain `min-height` bump so there's
    header background for it to float onto.
- **Don't drop wiki illustrations, admonitions, or worked examples without a
  specific reason** (added 2026-08-06) — the first `Feature-Espooler.md` draft
  over-compressed the ported wiki content (dropped the UI screenshots, the
  TIP/IMPORTANT callouts, and a worked numeric example) in the name of
  brevity, and the user pushed back hard. Default to carrying forward
  everything in the source wiki page that's still accurate; the bar for
  cutting something is "this is actively wrong/superseded," not "this feels
  long." See **Before finishing a Feature page** below for the process this
  produced.
- **Admonitions:** GitHub's `[!NOTE]`/`[!TIP]`/`[!IMPORTANT]`/`[!WARNING]`
  syntax doesn't work here (not enabled) — use the base `admonition` extension's
  `!!! type "Title"` instead. Material's shipped CSS only actually styles a
  fixed class list: `note`, `tip`, `info`, `success`, `question`, `warning`,
  `danger`, `bug`, `example`, `quote`, `abstract`, `failure` — `!!! important`
  renders with NO icon or colour (silently, no build warning) because
  "important" isn't one of them. Use `!!! warning "Important"` to get a
  styled callout with the original label preserved.
- **Code blocks are colourised** (added 2026-08-06) via `codehilite`, not
  Material's normal `pymdownx.highlight`/`pymdownx.superfences` recipe — see
  **Zensical rough edges** below, this was a deliberate workaround for the
  same non-determinism bug already known from Mermaid, newly found to affect
  plain syntax highlighting too. Practical effect for page-writing: fence
  config/command examples with `` ```yaml `` (matches Pygments' YAML lexer
  coloring `key:` / `#comment` / strings reasonably even for non-YAML `.cfg`
  content — the wiki did the same for the same reason) rather than `ini`/`text`.

## Feature page template

Every page under §5 Features uses this fixed section order (revised
2026-08-06 after the `Feature-Espooler.md` review — see the decisions above
and **Before finishing a Feature page** below):

1. Concept — illustrate it if the wiki did; don't drop a diagram/screenshot
   without a specific reason.
2. Hardware Setup — wiring table + `mmu_hardware.cfg` (and the relevant
   `mmu.cfg` pin-alias block if there is one). Include a real menuconfig
   screenshot for the hardware-facing prompts if one is easy to capture
   (`doc_tools/shots.py`, one session per feature page, `outdir` matching the
   page name) — readers care what they type into menuconfig and what comes
   out in `.cfg`, not the raw `Kconfig.*` source, which is why there's no
   separate "menuconfig" section any more (dropped from the original 9).
3. Parameter Setup — `mmu_parameters.cfg` (and `mmu.cfg` where a feature has
   settings there instead/also). Keep worked numeric examples from the wiki,
   don't compress them to one line.
4. Commands (linked to Command Reference anchors)
5. Printer variables exposed — include a UI subsection with real
   screenshots/illustrations if the feature has any visible representation in
   KlipperScreen/Mainsail/Fluidd.
6. Tuning — practical "how do I get this working" recipes belong here if the
   wiki had step-by-step setup walkthroughs for sub-modes; don't lose them
   just because there's no dedicated template slot for them.
7. Troubleshooting
8. See also

### Before finishing a Feature page

Before considering any Feature page (or any ported page) done, per explicit
request: **proofread it against its wiki source section-by-section**, then
report back what didn't carry forward and why — even content you're
confident was right to cut. The user reviews that list and can restore
anything. Don't silently decide something wasn't worth keeping.

---

### 0. Home

| Page | Source | Status |
|---|---|---|
| `index.md` (Home) | `README.md` + `wiki/Home.md` | **done (v2)** — see item 34 below for the full rewrite. v1's "card grid needs a new entry every time a section gains its first page" rule is retired: v2's card grid is one card per top-level nav section (5 cards: Getting Started, Concepts, Features, Reference, Developer Guide) rather than one per page-that-happened-to-be-first, and doesn't need touching again as pages are added within an existing section. |

### 1. Getting Started

| Page | Source | Status |
|---|---|---|
| `Installation.md` | `wiki/Installation.md` | port, verify against `install.sh`/`Makefile` flags |
| `GettingStartedWithBoxTurtle.md` | existing `doc/` page | **done**, incl. a "Picking a toolhead" step (shared toolhead/extruder geometry database, optional, reduces calibration) with two real screenshots |
| `GettingStartedWithViViD.md` | new, from `installer/mmu_types/Kconfig.vvd` + `installer/boards/custom/Kconfig.vvd` + `installer/connection/Kconfig.{mmu_mcu,buffer_mcu}` | **done** - second Getting Started page, with a real `getting-started-vivid` `doc_tools/shots.py` session (7 screenshots) for every screen except the two live serial-device-list screens (see session log for why those stay text). Covers the two-separate-MCU serial selection unique to this design, otherwise a lighter walkthrough than Box Turtle's since almost everything defaults correctly for this fully-specified design. |
| `MMU-Types-Overview.md` (comparison table: all 15 Kconfig types, selector class, gate count, status) | new, from `installer/Kconfig.mmu_types/*` | new |
| `Upgrading-from-v3.md` | `wiki/Upgrade-Notice.md`, `wiki/Change-Log.md` | rewrite for v4 |

### 2. Concepts

| Page | Source | Status |
|---|---|---|
| `Conceptual-MMU.md` | `wiki/Conceptual-MMU.md` | **done (v2)** — rewritten around the real v4 selector hierarchy (three research passes: sensor renames, vendor→selector mapping, combiner/EndlessSpool verification — see session log); vendor table extended well past the old wiki's ERCF/Tradrack/Box-Turtle set. v1 swapped the wiki's Type-A/B/C diagrams for ASCII to avoid their stale "pre-gate"/"gate" labels; v2 restored the real diagrams (`typeA/B/C_mmu.png`, `default_ercf/tradrack/box_turtle.png`) per user request, with a correction tip instead — kept skipping the three live sensor-list screenshots (`filament_sensors.png`, `endstops.png`, `mmu_sensors.png`), which show real old output rather than an editable diagram |
| `Understanding-Operation.md` | `wiki/Understanding-Operation.md` | ⚠️ verify |
| `Print-Job-State-Machine.md` | `wiki/Print-Job-State-Machine.md` | ⚠️ verify against `mmu_print_state_machine.py` |

### 3. Configuration

| Page | Source | Status |
|---|---|---|
| `Hardware-Configuration.md` | `wiki/Hardware-Configuration.md` | ⚠️ verify |
| `Movement-and-Homing.md` | `wiki/Movement-and-Homing.md` | ⚠️ verify |
| `Macro-Configuration.md` | `wiki/Macro-Configuration.md` | ⚠️ verify |
| `Configuring-mmu.cfg.md` | `config/base/mmu.cfg` | **generated** |
| `Configuring-mmu_hardware.cfg.md` | `config/base/mmu_hardware.cfg` | **generated** |
| `Configuring-mmu_parameters.cfg.md` | `config/base/mmu_parameters.cfg` | **generated** |
| `Configuring-mmu_macro_vars.cfg.md` | `config/base/mmu_macro_vars.cfg` | **generated** |

### 4. Calibration

| Page | Source | Status |
|---|---|---|
| `MMU-Calibration.md` (index/overview) | `wiki/MMU-Calibration.md` | ⚠️ rewrite against selector classes |
| `MMU-Calibration-Physical-Selector.md` | `wiki/MMU-Calibration-TypeA.md` | ⚠️ rewrite, retitle |
| `MMU-Calibration-Virtual-Selector.md` | `wiki/MMU-Calibration-TypeB.md` | ⚠️ rewrite, retitle |
| Toolhead calibration | folded into a Features page (§5) | — |

### 5. Features — template proved out on six pages, 8 to go

| Feature page | Kconfig source | Wiki source | Status |
|---|---|---|---|
| `Feature-Espooler.md` | `Kconfig.espooler` | `wiki/Espooler-Support.md` | **done (v3)** — first page written against the template (see below); code-verified against `mmu_espooler.py`, `mmu_filament_movement.py`'s `_wrap_espooler()`, and `mmu_unit_parameters.py`. v1 over-compressed the ported wiki content; v2 restored the UI screenshots, TIP/IMPORTANT callouts, the `espooler_speed_exponent` worked example, and the per-mode setup walkthroughs, added a real `doc_tools/shots.py` session for the eSpooler pins menuconfig screen; v3 dropped the leading provenance paragraph, all developer-jargon (class/method names), the (nonexistent in v4) pin-alias example, and fixed "sync-feedback" → "filament (catchment)" buffer naming — see the decisions above and the session log |
| `Feature-Encoder.md` | `Kconfig.encoder` | `wiki/Clog-Runout-EndlessSpool.md` (Optional Encoder + Clog Detection + Flowrate Monitoring sections only) | **done** - code-verified against `unit/mmu_encoder.py`, `commands/mmu_encoder.py`, `mmu_constants.py`'s `ENCODER_*`/`VARS_MMU_ENCODER_*` constants, and the `[mmu_encoder]`/`gate_endstop_to_encoder`/bowden-verification blocks in `config/base/*.cfg`. Reused `wiki/Synchronized-Gear-Extruder/Encoder_Meter.png` (an annotated FlowGuard-meter diagram, already carrying v4's real `flowguard_encoder_max_motion` param name) as the UI illustration. See the session log for what got routed to other pages and what was corrected. |
| `Feature-Sync-Feedback-Buffer.md` | `Kconfig.sync_feedback_buffer`, `Kconfig.motor_sync` | `wiki/Synchronized-Gear-Extruder.md` (Synchronized Gear/Extruder + Sync-Feedback Buffer Sensors + AutoTuner sections only — the FlowGuard clog/tangle/telemetry sections stayed off this page, see the session log) | **done** — code-verified against the real `[mmu_buffer <unit_name>]`/`mmu_parameters.cfg` keys and the live `MMU Features / Additions → Buffer config` / `Other Settings → MMU/Extruder sync` menuconfig screens (real screenshots, `feature-sync-feedback-buffer` session, boxturtle seed). Reused `Typical_Buffer.png` (with a corrective note for its stale pin names) and `Sync_Feedback_Meter.png`/two small UI-icon images from the wiki; skipped the FlowGuard telemetry/simulation images as out of scope for this page. |
| `Feature-Spoolman.md` | — (software integration, no Kconfig) | `wiki/Spoolman-Support.md` | **done** — split off the originally-planned single `Feature-NFC-Spoolman.md` into two pages (this one + `Feature-NFC.md` below), per explicit request; the two cross-reference heavily in both directions. Code-verified against `mmu_controller.py`'s `_spoolman_*` methods, `mmu_server.py` (Moonraker component), and `mmu_gate_maps.py`'s `gate_map_to_string()`. Corrected several stale wiki details: the console gate-map status labels are `On spool`/`Buffered`/`Empty`/`Unknown` (not `Spool`/`Buffer`) and the field is `Id:` not `SpoolId:`; `pending_spool_id_timeout` is actually `spoolman_pending_id_timeout`, living in `mmu.cfg` not `mmu_parameters.cfg`; the Spoolman-version requirement (0.18.1+) applies to every mode above `off`, not just push/pull (confirmed in `mmu_server.py` — `readonly` needs it too, since the same extra-fields gate blocks it); and Spoolman now has a third extra field, `RFID` (alongside `Printer Name`/`MMU Gate`), not in the wiki at all. Re-introduced the wiki's Mermaid sequence diagrams under Tuning (split `off`/`readonly`/`push`/`pull` into 6 diagrams total) via raw `<pre class="mermaid">` HTML rather than a ` ```mermaid ` fence — see item 33 below for the mechanism and its verification status. Reused all 6 of the wiki's Spoolman-UI screenshots as-is (verified each against current field names/labels — none were stale, unlike the sensor-name screenshots skipped elsewhere) plus the RFID/QR "auto-setting" workflow, generalized (see `Feature-NFC.md`'s split below). |
| `Feature-NFC.md` | `Kconfig.nfc_reader` | new (no v3 wiki page — the closest wiki content, RFID/QR tag auto-setting, was folded into `Feature-Spoolman.md`'s generic-external-reader workflow instead; NFC hardware readers, `MMU_NFC`/`MMU_NFC_SCAN`, and Spoolman auto-create are all new in v4) | **done** — the reader/hardware half of the original combined plan, cross-referencing `Feature-Spoolman.md` heavily both ways. Code-verified against `unit/mmu_nfc_manager.py`, `unit/nfc/mmu_nfc_reader.py` and `mmu_nfc_endstop.py`, `commands/mmu_nfc.py`/`mmu_nfc_scan.py`, and the `_preload_gate()`/`_home_to_gate_with_nfc()` integration in `mmu_filament_movement.py`. Marked **beta** on the page itself, matching the Kconfig's own `[[B]](BETA)[[/B]]` tag — and specifically flagged the per-gate homing-endstop path (used automatically by `MMU_PRELOAD`) as confirmed on RC522 only, per a "PROTOTYPE" comment in `mmu_nfc_endstop.py` saying PN532/PN7160 still need bench verification. No wiki content was actually stale here since none existed to be stale — this is genuinely new v4 surface, not a port. No menuconfig screenshot: the Box Turtle seed used for this site's other captures doesn't select `MMU_HAS_NFC_READER`; skipped rather than faked, same reasoning as `Feature-Encoder.md`. |
| `Feature-LEDs.md` | `Kconfig.leds` | `wiki/Led-Support.md` |
| `Feature-Endless-Spool-Runout.md` | (no dedicated Kconfig — sensor-driven) | `wiki/Clog-Runout-EndlessSpool.md` (Runout Detection + EndlessSpool + Designated Waste Gate sections only — the Optional Encoder/Clog Detection/Flowrate Monitoring sections went to `Feature-Encoder.md` instead) | **done** — code-verified against the runout/clog-vs-tangle decision logic, the EndlessSpool group-cycling and eject-gate handling, and the real `mmu.cfg`/`Kconfig.options` settings. Real menuconfig screenshot (`feature-endless-spool-runout` session, boxturtle seed, no scene setup needed since this section isn't MMU-type-specific). See the session log for what got corrected from the wiki. |
| `Feature-Gate-TTG-Maps.md` | `Kconfig.gates` | `wiki/Tool-and-Gate-Maps.md` |
| `Feature-Statistics-Counters.md` | — | `wiki/Statistics-and-Consumption-Counters.md` |
| `Feature-State-Persistence.md` | — | `wiki/State-Persistence.md` |
| `Feature-Filament-Bypass.md` | `Kconfig.bypass` | `wiki/Filament-Bypass.md` |
| `Feature-Gcode-Preprocessing.md` | — | `wiki/Gcode-Preprocessing.md` |
| `Feature-Environment-Manager.md` | `Kconfig.environment_sensor` | `wiki/Environment-Manager.md` |
| `Feature-Tip-Forming-Purging.md` | `Kconfig.tip_shaping`, `Kconfig.purging` | `wiki/Tip-Forming-and-Purging.md` |
| `Feature-FlowGuard.md` | `Kconfig.flowguard` | new (no v3 equivalent) |
| `Feature-Addon-Integrations.md` | — | `wiki/Addon-Feature-Setup.md` |

### 6. Slicer & Toolchange

| Page | Source |
|---|---|
| `Slicer-Setup.md` | `wiki/Slicer-Setup.md` |
| `Toolchange-Movement.md` | `wiki/Toolchange-Movement.md` |

### 7. Operation

| Page | Source |
|---|---|
| `Basic-Operation.md` | `wiki/Basic-Operation.md` |
| `Handling-Errors.md` | `wiki/Handling-Errors.md` |
| `KlipperScreen.md` | `wiki/KlipperScreen.md` |
| `Mainsail-Fluidd-Integration.md` | `wiki/Mainsail-Fluidd-Integration.md` |

### 8. Tuning

| Page | Source |
|---|---|
| `Blobbing-and-Stringing.md` | `wiki/Blobbing-and-Stringing.md` |

### 9. Multi-Unit (placeholder — deferred)

| Page | Source |
|---|---|
| `Multi-MMU.md` | `wiki/Multi-MMU.md` — flag as future work, not in v1 |

### 10. Reference

| Page | Source | Status |
|---|---|---|
| `Command-Reference.md` | `extras/mmu/**` (walks the whole tree, not just `commands/` — see `doc_tools/gen_command_reference.py`'s header) | **done, generated** — `make command_reference`. 88 commands. Reader-facing intro simplified 2026-08-06 to drop `HELP_BRIEF`/`extras/mmu/` citations per the no-developer-references rule |
| `Printer-Variables.md` | printer status surfaces (same as the console's `/vars`) | **done, hand-written but code-verified** (no generator yet). Retrofitted 2026-08-06: dropped the v3-vs-v4 diff and all `Mmu*`/file-path citations per the page-genre-wide rules above — the `servo`/`grip` gap found in the process moved to `Dev-Code-Layout.md`'s selector-hierarchy discussion rather than being lost |
| `Mcu-Reference.md` | `wiki/Mcu-Reference.md` + `installer/boards/Kconfig.*` | ⚠️ verify board list current |

### 11. Troubleshooting & FAQ

| Page | Source |
|---|---|
| `Troubleshooting-and-Common-Issues.md` | `wiki/Troubleshooting-and-Common-Issues.md` |
| `FAQ.md` | `wiki/FAQ.md` |

### 12. Developer Guide — **done (all 7 pages)**

| Page | Source | Notes |
|---|---|---|
| `Dev-Code-Layout.md` | new — `extras/mmu/` structure | Object-ownership tree, the 3 "extends" relationships (composition / mixin-split / command-pattern), full selector hierarchy incl. genuine multi-inheritance type-C classes, command auto-discovery pipeline, hardware-boundary quotes pulled straight from NFC/sync-feedback docstrings. The flagship page — read it first if picking this session back up. |
| `Dev-Kconfig-Structure.md` | new — `installer/Kconfig` tree, `installer/build.py`/`parser.py`/`upgrades.py` | Covers the Kconfig dialect extensions, and `./install.sh -z`/`-t` (git-update skip / sandboxed test-mode install to `/tmp/mmu_test`). Deliberately drops a "Makefile targets" table that was here — too detailed, per feedback. |
| `Dev-Testing.md` | `test/README.md` §1–7 (minus §1a) | Trimmed: no more exhaustive per-test-file table (it only grows) — one illustrative file (`test_mmu_console.py`) plus "browse `test/test_mmu_*.py`". Counts genericized to `>900`. |
| `Dev-Simulator.md` | `test/README.md` §1a — **renamed from "Console"** | Opens with a real colour screenshot (`doc/Dev-Simulator/Simulator.png`, user-supplied) of a live session before the ported detail. |
| `Dev-Doc-Tooling.md` | `doc_tools/README.md` | Kept in sync with the actual `doc_tools/README.md` — edit both together. Includes a note on the Zensical build-cache bug (see below). |
| `Dev-Installer-Docker.md` | `installer-dev/README.md`, rewritten after reading the actual Dockerfiles/compose file | Real purpose: cross-**Python-version** testing (Alpine target runs Python 2.7, matching Creality K1's busybox environment) — not just "a clean sandbox", which `-t` already gives you on your own host Python. |
| `Dev-Contributing.md` | new + `.github/CONTRIBUTING.md` | Community/PR-process guidance ported in, plus the file-header convention and links back to every other Developer Guide page. |

### 13. Community & Support

| Page | Source |
|---|---|
| `Change-Log.md` | `wiki/Change-Log.md` |
| `Donations.md` | `README.md:47-65` (PayPal link + the "monster undertaking" stats) |
| `Getting-Help.md` | `wiki/Home.md` "How to get help" section, Discord links |

---

## Zensical rough edges (found this session — check if still true before relying on them)

- **`exclude_docs` is not honoured.** A file listed there still gets built into
  the site. Worked around by keeping `TOC.md` outside `docs_dir` entirely rather
  than relying on the config option — more robust anyway.
- **The incremental build cache is unreliable**, not just slow. The same
  content, rebuilt with `--clean` four times in a row, produced a correct
  Mermaid diagram exactly once — the other three renders silently fell back to
  showing the raw ` ```mermaid ` source as plain text, with no warning. This is
  why Mermaid was dropped entirely (see above) rather than worked around — a
  diagram that renders correctly 1 time in 4 is worse than no diagram, because
  it fails silently and non-deterministically depending on which build happens
  to deploy. If a rebuild ever looks stale for *any* reason, run
  `./venv/bin/zensical build --clean` once before assuming the content is wrong.
- **Markdown table cells with an escaped pipe inside a single code span
  render the literal backslash.** `` `a \| b` `` shows `a \| b`, not `a | b` —
  Markdown doesn't process backslash-escapes inside code spans, and the table
  parser still needs the escape to not split the column. Fix: give each value
  its own code span, with the `\|` as plain text between them —
  `` `a` \| `b` ``. Bit twice this session (`Printer-Variables.md`, then
  `Dev-Simulator.md`) before the pattern stuck; grep any new page for `` \| ``
  before considering it done.
- **The incremental-build flakiness is in `pymdownx.superfences`'s custom-fence
  machinery generally, not specific to Mermaid.** Tested directly (2026-08-06,
  while trying to get colourised code blocks for `Feature-Espooler.md`):
  enabling `pymdownx.highlight` + `pymdownx.superfences` (Material's normal
  syntax-highlighting recipe, no Mermaid/custom-fence config involved at all)
  reproduced the identical bug on ordinary language fences — 2 of 4 clean
  rebuilds silently rendered with zero highlighting, same failure signature as
  the Mermaid case above. The base `codehilite` extension (Python-Markdown's
  original highlighter, not part of superfences) was deterministic across 6/6
  clean rebuilds in the same test. Fix in use: `codehilite` +
  `doc/assets/stylesheets/extra.css` re-pointing its Pygments token classes at
  Material's own `--md-code-hl-*-color` variables (Material's shipped CSS only
  styles `pymdownx.highlight`'s `<div class="highlight">`, not codehilite's
  `<div class="codehilite">`) — see the CSS file's own comment for how to
  regenerate the mapping if Pygments' class names or Material's variable names
  ever change. **Rule of thumb going forward: avoid `pymdownx.superfences` for
  anything**, not just Mermaid, until a Zensical release specifically claims to
  have fixed the underlying cache bug.
- None of the above is likely specific to this repo — worth re-checking against
  a newer Zensical release before assuming they still apply.

## Open items for later, not blocking this plan

- **Wiki-style bare links** (`[Foo](Foo)`) throughout ported pages won't resolve
  under mkdocs/Zensical — no existing Makefile target rewrites them (`fix_links`
  is unrelated, it's about Klipper symlinks). Link conversion is a real, if
  mechanical, cost per page. Zensical's own build does at least catch a broken
  internal link/anchor at build time ("page does not exist" / "anchor does not
  exist") — lean on `./venv/bin/zensical build --clean` after every new page
  rather than eyeballing links.
- **External inbound links** (README, Discord, KlipperScreen repo, YouTube videos)
  point at old wiki page names — a redirect map is worth a line item once URLs are
  final, not now.
- **`Configuring-mmu*.cfg.md` generators (§3) are still unbuilt** — the plan
  calls for generating them from the `config/base/*.cfg` Jinja templates'
  inline comments, mirroring `gen_command_reference.py`'s approach, but no
  script exists yet.
- **The `servo`/`grip` gap found while writing `Printer-Variables.md`**
  (`MmuController.get_status()` never merges `selector.get_status()`, so
  `printer.mmu.servo`/`.grip` from v3 don't exist in v4 despite the value being
  computed) is a real code question worth raising upstream, not just a doc
  footnote — flagged in both `Printer-Variables.md` and `Dev-Code-Layout.md`.

## Session log

**2026-08-05.** In order, roughly:

1. Planned this TOC from scratch (surveyed `README.md`, `wiki/`, `test/README.md`,
   `doc_tools/README.md`, `extras/mmu/commands/*.py`) after being asked for a book
   structure before writing anything.
2. Learned mkdocs basics with the user (anchor slugify rules, the `[TOC]` marker,
   themes) before building anything, per their request.
3. Built the first real page: `Command-Reference.md`, generated by a new
   `doc_tools/gen_command_reference.py` (`ast`-based, no imports). Caught and
   fixed its own scope bug mid-session — it only scanned `commands/`, missing
   commands registered from `mmu_controller.py` and `unit/selectors/*.py` (76 → 88
   commands after the fix). This is the moment the "verify against real code,
   don't assume" habit for this project got established — it paid off again
   later on `Printer-Variables.md` (the `servo`/`grip` gap) and `Dev-Testing.md`
   (the stale "69 commands" figure).
4. User asked to switch the site generator from mkdocs to **Zensical** mid-session.
   Migrated `mkdocs.yml` in place (Zensical reads it natively). Found the
   `exclude_docs` bug and the build-cache bug here (see above).
5. Branding pass on `doc/index.md` and the Material theme: real logo/favicon
   assets generated from `wiki/resources/happy_hare_logo.jpg`, black+pink palette,
   `theme.variant: classic` (Zensical's new default `modern` doesn't colour the
   header from `primary` at all — found by inspecting the shipped CSS directly,
   not documented anywhere).
6. Built `Printer-Variables.md` — fully code-verified against every `get_status()`
   in `extras/mmu/`, not carried over from the v3 wiki. Found: the `servo`/`grip`
   gap, several v3→v4 field additions (FlowGuard, tangle prevention, per-gate
   `espooler`/`drying_state`/`nfc`), a `print_state` value and four `action`
   values added since v3, and a `mmu:sync_feedback` event signature change
   (gained an `eventtime` parameter).
7. Established the `[TOC]`-for-hand-written-pages-only convention, then reversed
   it entirely a couple of turns later once the user pointed out the theme's own
   sidebar already covers it on every page, not just generated ones. Recorded
   the reversal (not just the fix) in `doc_tools/README.md` so a future session
   doesn't reintroduce it.
8. Built the entire **Developer Guide** (§12, all 7 pages) in one push — see that
   section above for what's in each page. This is where the Mermaid diagrams
   were tried, found flaky, and reverted to ASCII (see **Zensical rough edges**).
9. Cleanup pass on the Developer Guide from user feedback: trimmed `Dev-Testing.md`,
   dropped a table from `Dev-Kconfig-Structure.md`, added real detail on
   `install.sh -z`/`-t` (found by reading `install.sh` directly rather than
   guessing), and rewrote `Dev-Installer-Docker.md` after actually reading the
   Dockerfiles/compose file for the first time (the real value is Python-2.7/
   Alpine parity testing, not just "a clean sandbox").
10. Swapped the `Dev-Simulator.md` ASCII transcription for a real screenshot the
    user supplied as a file, and added the "Picking a toolhead" step to
    `GettingStartedWithBoxTurtle.md` with two new real screenshots generated via
    `doc_tools/shots.py` (extended the existing `getting-started-boxturtle`
    session, renumbering `11-spoolman-readonly.png` → `13-`). Hit and fixed a
    real `doc_tools/capture.py` quirk along the way: `toggle()` on a long
    `choice` list leaves the highlight at the top after the resize `shot()`
    triggers internally — fixed by calling `mc.autofit()` before the final
    `mc.select()`, not by re-selecting alone (see the comment in `shots.py`).
11. Wrote the first §5 Feature page, `Feature-Espooler.md`, to prove out the
    template. Read `mmu_espooler.py` (burst/print-assist state machine), the
    espooler branch of `_wrap_espooler()` in `mmu_filament_movement.py` (the
    gear-speed-driven PWM curve — not in `mmu_espooler.py` itself, easy to
    miss), `_adjust_espooler_assist()` in `mmu_controller.py` (auto-arm on
    filament-loaded), and the `espooler_*` `ParamSpec`s in
    `mmu_unit_parameters.py`. Found that BTT ViViD (`MMU_TYPE_VVD_1_0`) is the
    one MMU type that forces the feature off entirely (`select
    UNSELECT_MMU_HAS_ESPOOLER`). Added the page to `mkdocs.yml`'s nav (new
    "Features" top-level section) and to the `index.md` card grid.
12. User review of that v1 draft produced six pieces of standing feedback
    (now folded into the decisions/template above, not just this page):
    fenced blocks need real colour (`` ```yaml ``, not `` ```ini ``/`` ```text ``);
    don't drop wiki illustrations (the Espooler UI screenshots were missing
    entirely); keep TIP/IMPORTANT callouts as real admonitions, not prose;
    Kconfig source syntax isn't reader-facing — show a menuconfig screenshot
    and the resulting `.cfg` instead; rename the two config sections
    "Hardware Setup"/"Parameter Setup"; and drop the v3-vs-v4 framing
    entirely, since v4 docs don't need to justify themselves against a
    version the reader may never have used. Also asked for a
    proofread-against-wiki + summary report before any future page is called
    done — see **Before finishing a Feature page** above.
13. Rewrote `Feature-Espooler.md` (v2) against that feedback: restored the
    `assist2.png`/`rewind2.png` UI screenshots plus the console status-text
    example, added `!!! tip`/`!!! warning "Important"` admonitions (discovered
    along the way that `!!! important` silently renders unstyled — Material's
    CSS has no such class, see the new bullet above), restored the
    `espooler_speed_exponent` worked numeric example and the five per-mode
    setup walkthroughs (Rewind/Assist/Basic-print/Intelli-assist×2) as a
    "Setting up each mode" subsection under Tuning, merged the old standalone
    "menuconfig" section into Hardware Setup, and cut every "the v3 wiki
    said..." aside. Added a real menuconfig screenshot for this
    (`doc_tools/shots.py`'s new `feature-espooler` session, capturing the
    "eSpooler pins" screen under "MMU Features / Additions" — confirmed the
    boxturtle seed already has it enabled, no scene setup needed).
14. Getting that screenshot's colour scheme to match required fixing
    highlighting for the whole site, not just this page — see the new
    **Zensical rough edges** entry: Material's normal `pymdownx.highlight` +
    `pymdownx.superfences` recipe hit the exact same non-deterministic
    build-cache bug already known from Mermaid, on *ordinary* code fences.
    Switched to `codehilite` + a hand-written CSS mapping in `extra.css`
    instead (deterministic across 6/6 test rebuilds) — every existing page's
    code blocks got real syntax colour as a side effect of this fix, not
    something that needed touching per-page.
15. Second round of user feedback on the v2 draft, six more items (all now
    folded into the decisions above): drop the "sync-feedback" qualifier from
    "filament buffer" (they're two different Kconfig options — also wrong the
    same way in `Printer-Variables.md`'s `filament_buffer` field, fixed
    there too); strip developer-jargon (class names, method calls) from
    reader-facing prose; drop the leading "everything below was read
    from..." provenance paragraph entirely; the pin-alias example in Hardware
    Setup doesn't reflect v4 at all (aliases were removed — pins are
    `unit_mcu_name:pin_name` directly); add the tri-colour H2 marker as a
    site-wide CSS template feature, not per-page; and retrofit the ASCII-art
    + copyright footer to every page. Also resolved the open question from
    item 11: "no v3 narrative" IS retroactive — retrofitted
    `Printer-Variables.md` (dropped "What changed since v3" and the
    servo/grip aside entirely; moved the servo/grip *finding* itself to
    `Dev-Code-Layout.md` rather than losing it, since that's a developer page
    where citing the exact gap is appropriate) down to keeping only
    deprecation notation, per explicit instruction ("the only notation I want
    in printer variables is whether the variable is deprecated").
16. Added the footer to `doc_tools/gen_command_reference.py`'s `render_page()`
    (not hand-edited into `Command-Reference.md`, which regeneration would
    wipe), then ran `make command_reference` to pick it up.
17. Resolved the open question from item 15: user confirmed the
    no-developer-references rule is page-genre-wide, not just Feature pages.
    Stripped every `Mmu*.get_status()`/file-path/constant-name citation from
    `Printer-Variables.md` (see the updated bullet above for specifics) and
    simplified `Command-Reference.md`'s generated intro (dropped
    `HELP_BRIEF`/`extras/mmu/`/the hand-edit warning — that belongs in
    `Dev-Doc-Tooling.md`, not here). Kept Klipper's own API surface
    (`printer.send_event(...)`, `printer.register_event_handler(...)`) since
    that's literally what a reader extending Happy Hare in Python needs to
    type, not narration of Happy Hare's own internals.
18. Two small footer polish requests: made the copyright line genuinely tiny
    (`0.6rem`, ~75% of body text) and switched the ASCII art from a
    ` ```text ` fenced block to bare `<pre>`/`<p>` with dedicated CSS classes
    (`.hh-footer-art`/`.hh-footer-copyright` in `extra.css`) so it renders as
    plain monospace text rather than a "code sample" box — see the updated
    footer decision above. Rolled out with the same find/replace approach
    across all 12 pages plus the generator.
19. **Moved this entire rewrite into its own repo, `Happy-Hare-Doc`** (see the
    new "separate repo" bullet at the top of Structure decisions). Split
    `doc_tools/capture.py`'s and `gen_command_reference.py`'s single
    `REPO_ROOT` into `DOC_ROOT` (this repo, for output — unchanged
    self-relative logic) and `HAPPY_HARE_SRC` (an env var pointing at a
    Happy-Hare checkout, for reading source) — both fail fast with a clear
    error if `HAPPY_HARE_SRC` is unset or doesn't look like a real checkout.
    `capture.py`'s `os.chdir()` before the menuconfig `execve` had to move
    from the old `REPO_ROOT` to `HAPPY_HARE_SRC` too — easy to miss, since
    Kconfig's serial-port glob and `KLIPPER_HOME` handling are absolute-path
    driven and don't obviously depend on cwd, but `install.sh`/`make
    menuconfig` always run with cwd = the Happy-Hare checkout root, and this
    now faithfully matches that. New `Makefile` in this repo owns the fetch
    (`fetch-source`/`clean-source` targets, pinned via the tracked
    `HAPPY_HARE_REF` file, currently `v4`) — `docs`/`docs_build`/`docs_preview`
    need none of it, confirmed by tracing that they only ever read
    already-committed `doc/*.md`, never Happy-Hare source. Added a GitHub
    Actions → Pages deploy workflow on that same basis (no source-fetch step
    needed there either). Happy-Hare's own repo had `doc/`, `doc_tools/`,
    `mkdocs.yml` and this file removed, plus the now-dead doc-related Makefile
    targets and the `.gitignore` `site/` entry.
20. Wrote `Conceptual-MMU.md` (§2), the first page outside §5/§10/§12 in this
    rewrite. Ran three research passes in parallel (against the
    `HAPPY_HARE_SRC`-fetched checkout, same as any other page) rather than
    porting the wiki's Type-A/B/C framing directly, since TOC.md already
    flagged that framing as not mapping cleanly onto v4:
    - **Sensor renames.** The wiki's "pre-gate"/"gate"/"post-gear" sensors
      are `mmu_entry_X`/`mmu_shared_exit`/`mmu_exit_X` in v4 - confirmed by a
      literal old→new mapping table in `mmu_sensor_manager.py`'s own
      backward-compat shim (`('mmu_pre_gate', SENSOR_ENTRY_PREFIX), ('mmu_gear',
      SENSOR_EXIT_PREFIX), ('mmu_gate', SENSOR_SHARED_EXIT)`). The wiki's
      standalone `collision` endstop no longer exists by that name - it's
      folded into an encoder-based extruder-homing *mode*
      (`extruder_homing_endstop: encoder`), not a separate endstop identifier.
    - **Vendor → selector mechanism.** Cross-checked `installer/mmu_types/Kconfig.*`
      against `extras/mmu/mmu_unit.py`'s `VENDOR_PROFILES` (both must agree,
      and did): Box Turtle/Night Owl/Angry Beaver/3MS/Quattro Box/KMS/EMU are
      all the gear-per-gate family; ERCF/Tradrack use a moving carriage +
      servo; BTT ViViD uses per-gate index switches; 3D Chameleon/MMX6/Low
      Rider are rotary; MMX/PicoMMU are servo-driven. The gear-per-gate +
      moving-carriage hybrid (old wiki's "purely theoretical" type-C) is real
      in code but not a default for any vendor yet - custom-MMU-only, and one
      variant of it (`LinearMultiGearServoSelector`) has no menuconfig path
      at all, config-file-only.
    - **Combiner/splitter has no code footprint at all**, in v3 or v4 - the
      old wiki's claim that "Happy Hare will ensure different units are not
      used at the same time" to protect a shared combiner has no backing
      anywhere in `extras/mmu/**` (confirmed by grepping for
      combiner/splitter/mutual-exclusion terms) - dropped rather than ported.
    - **Found and fixed a real bug while verifying EndlessSpool**: this
      session's own `Printer-Variables.md` had carried over the wiki's stale
      claim that `endless_spool_enabled` has a value `2` ("on + pre-gate
      sensor"). The real parameter is a strict 0/1 boolean everywhere it's
      read or written (`ParamSpec(..., limits=dict(minval=0, maxval=1))`,
      every consumer branches on it as a plain boolean) - fixed on that page
      too, not just avoided here.
    - Replaced the wiki's Type-A/B/C diagrams entirely rather than reusing
      them: they're raster PNGs with sensor labels baked in as pixels
      ("pre-gate", "gate" sensor), which would have re-published exactly the
      naming this page just corrected. ASCII diagrams (same convention as
      `Dev-Code-Layout.md`) with the correct v4 names instead.
    - Judgment call flagged for the user, not resolved unilaterally: the
      wiki's per-sensor prose was much more detailed (multi-paragraph
      Primary/Secondary Functions per sensor) than the one-line-per-sensor
      table this page ships. No other planned page currently owns that depth
      - compressed here to keep a *conceptual* page from reading like a
      reference page, but flagged rather than silently decided.
21. User pushed back on item 20's ASCII-diagram substitution - restored the
    real wiki diagrams on `Conceptual-MMU.md` (with a correction tip instead
    of a swap), except the three live sensor-list screenshots, which show
    real v3 console/UI output rather than an editable diagram - see the new
    "Reuse a wiki diagram..." decision above for where the line is drawn.
    Also did a round of general layout requests, all site-wide rather than
    per-page: Previous/Next footer nav (Zensical doesn't render Material's
    own - built client-side in `hh-page-nav.js` instead, off the
    already-rendered sidebar), a Discord footer icon (`extra.social`), and a
    taller header with a bigger logo + tagline (the tagline needed
    absolute-positioning off the site-name title block rather than growing
    that block directly - see the new decision above for why). Smaller
    footer ASCII-art font size too.
22. **Second layout-polish pass (2026-08-06), six more site-wide fixes** before
    resuming page-writing work:
    - **Fixed a real bug in item 21's tagline anchoring**: giving
      `.md-header__topic:first-child` `position: relative` (so the tagline
      `::after` could hang off it) broke Material's title-swap-on-scroll
      animation, which depends on BOTH `.md-header__topic` elements being
      `position: absolute` with no offset (so each defaults to the same
      "static" position and overlaps exactly, swapping via opacity+translateX
      only). Making the first one `relative` gave it real flow height again,
      which pushed the second topic's own static position down below it -
      the page title rendered in the tagline's spot instead of sliding into
      the site-name's spot on scroll. Fixed by anchoring the tagline
      `::after` to `.md-header__ellipsis` instead (already
      `position:relative` in Material's own CSS, never touched by the swap)
      and leaving both topics alone.
    - **Double separator above the footer**: the markdown `---` before the
      footer block renders an `<hr>`, and `.hh-page-nav`'s own `border-top`
      sat directly under it - two rules back to back. Dropped the
      `border-top` from `.hh-page-nav`; the `<hr>` alone is now the one
      separator (kept in markdown rather than the CSS rule, since it's the
      copy that still works with JS disabled).
    - **Footer ASCII art still read as "too big" even after item 21's
      font-size cut** - monospace-text sizing doesn't behave consistently
      enough across the box for one font-size value to reliably look small.
      Replaced the `<pre>` block with an inline SVG (`<text>` elements, one
      `width` on the wrapping `.hh-footer-art` class controls the whole
      thing via viewBox scaling) on all 13 pages plus
      `gen_command_reference.py`'s `render_page()` - same
      python-bulk-replace-across-files approach as the original footer
      rollout. Still theme-reactive (`fill: var(--md-default-fg-color--light)`)
      because it's raw inline SVG markup in the page, not a rasterised `<img>`.
    - **Prev/Next arrows**: `hh-page-nav.js`'s label strings changed from
      `"Previous"`/`"Next"` to `"‹ Previous"`/`"Next ›"`.
    - **Dropped the search box's `⌘K`/`Ctrl+K` shortcut hint** - it's a
      `.md-search__button::after` pseudo-element in Material's own CSS
      (`content: "Ctrl+K"`, overridden to `"⌘K"` under
      `[data-platform^="Mac"]`), not markup; `display:none` on the same
      selector plus shrinking the button's now-unused right padding.
    - **Widened the main content column**: `.md-grid`'s `max-width` (61rem
      -&gt; 75rem). That one class caps the header/main/footer row alike
      (confirmed via computed styles - all three `.md-grid` instances share
      it), and since both sidebars are fixed-width, all the extra room
      lands on `.md-content` specifically with no separate content-only rule
      needed.
    - **User caught three problems with the above in the same session, all
      fixed before moving on**:
      - The tagline fix still wasn't right - it rendered *below* the header's
        own black background instead of inside it. Root cause: the `::after`
        inherits the title block's line-height (sized for the 48px
        topic-swap box, to vertically-center "Happy Hare"), so its line box
        was ~48px tall regardless of its small font-size - the box, not the
        glyph, is what has to fit inside the header, and it didn't. Fixed
        with an explicit `line-height: 1` on the `::after`, plus bumping
        `.md-header__inner`'s `min-height` to 5.6rem so there's room for
        logo + title + tagline all stacked. Verified this one with
        `document.elementFromPoint` scans down the header rather than
        screenshots, since screenshots were the unreliable part (see the
        tooling note below) - a plain rect/coordinate check doesn't have
        that problem.
      - The inline-SVG footer (previous session's fix for "still too big")
        rendered with garbled/overlapping lines in the real browser -
        reverted to the original `<pre>` text approach, just smaller
        (0.7rem -&gt; 0.5rem) rather than debugging the SVG further, per
        explicit request.
      - Logo bumped again, 1.9rem -&gt; 2.8rem.
23. **Third layout-polish round (2026-08-06), same session**: a second
    `fontawesome/brands/github` entry in `mkdocs.yml`'s `extra.social`
    (pointing at the Happy-Hare repo) alongside the existing Discord one -
    the header already has a repo widget with star/fork counts, but that's a
    separate Material feature (`repo_url`) from the footer's social-icon
    row, and the ask was specifically for the latter. Nested "On this page"
    entries (H3s under an H2, etc.) get `font-size: 0.85em` - Material nests
    a second `nav.md-nav` inside the owning heading's `li.md-nav__item`, so
    "`.md-nav__link` inside another `.md-nav` that's itself inside a
    `.md-nav__item`" selects exactly the nested set; scoped to
    `.md-sidebar--secondary` since the *primary* left-hand page-list nav
    reuses the identical nesting pattern for sub-pages and wasn't supposed
    to change. (First tried `0.7em` - visibly more than "slightly" smaller,
    dialed back to `0.85em`.) The footer's `<pre>` art and copyright line
    were plain stacked siblings with no shared wrapper, so a bottom-aligned
    right-justified copyright needed one: wrapped both in
    `<div class="hh-footer">` (flex row, `align-items: flex-end`,
    copyright gets `margin-left: auto`) across all 13 pages plus
    `gen_command_reference.py`'s generator - same bulk-replace pattern as
    the earlier footer edits. Deliberately no `markdown` attribute on that
    wrapper div (unlike `<div class="grid cards" markdown>` on the home
    page) - the content inside is plain HTML with no markdown syntax to
    process, and adding it risked the ASCII art's backslash escapes getting
    reinterpreted.
    - **Tooling note for next time**: this session's browser-preview tool
      produced a real, reproducible artifact when taking a screenshot at any
      scroll position other than 0 on a page taller than the viewport
      (either a blank frame or a doubled/stacked composite) - confirmed it
      was the *tool*, not the site, by growing the viewport height until the
      whole page fit at `scrollY=0` (`resize_window` + a short page) and
      getting a clean render every time that condition held. If a future
      session hits the same blank-screenshot symptom, resize taller before
      assuming the CSS is broken.
24. **Second Feature page: `Feature-Encoder.md`** (§5, second page to use the
    template after eSpooler). Source is `wiki/Clog-Runout-EndlessSpool.md`,
    but that wiki page is a *combined* v3 page covering five topics - only
    three belong here:
    - **Ported/verified here**: the "Optional Encoder", "Clog Detection", and
      "Flowrate Monitoring" sections.
    - **Deliberately routed elsewhere, not dropped**: "Runout Detection" and
      "EndlessSpool" (+ "Designated Waste Gate") belong to
      `Feature-Endless-Spool-Runout.md` (still open, no dedicated Kconfig) -
      this page doesn't touch sensor-driven runout/EndlessSpool at all.
    - Deep clog/tangle/runout *tuning* stayed a one-paragraph pointer rather
      than a full port, since that logic now lives behind a genuinely
      separate Kconfig (`Kconfig.flowguard`) and gets its own future page,
      `Feature-FlowGuard.md` - mentioned by parameter name only
      (`flowguard_encoder_mode`, `flowguard_encoder_max_motion`), no link,
      since the page doesn't exist yet and Zensical fails the build on a
      dangling one.

    Stale wiki content found and corrected rather than ported: `MMU_ENCODER
    ENABLE=0` doesn't exist in v4 (the real command only takes
    `POS`/`VALUE`/`QUIET` - encoder-based detection is switched on via
    `flowguard_encoder_mode` instead, not an ENABLE flag on the encoder
    itself); `encoder_clog_detection_enabled` is now `flowguard_encoder_mode`;
    the persisted calibration variable is `mmu_encoder_clog_length`, not the
    wiki's `mmu_calibration_clog_length`; and the `MMU_ENCODER` sample output
    block was replaced with the real v4 format (confirmed directly against
    `commands/mmu_encoder.py`'s `show()` output - "FlowGuard/Runout:
    Active/Inactive/Off", not "Runout detection: Disabled"). The wiki's
    `MMU_SENSORS` output block (`mmu_gate`, `mmu_pre_gate_N`) was **not**
    reproduced anywhere on this page - those are the exact pre-v4 sensor
    names `Conceptual-MMU.md` already corrected, and republishing them here
    would undo that.

    Two numbers were verified against the shipped config template rather
    than the code fallback, since they differ: `desired_headroom` ships as
    `5.0` in `mmu_hardware.cfg` even though the code default is `6.`; the
    template has no `detection_length` line at all (it's runtime/FlowGuard-only), so
    no default is claimed for it. `no_movement_samples: 10` is stated as "10
    consecutive samples" with no derived duration - the shipped comment's own
    arithmetic ("default sampling rate is 0.1s so 10=0.5s") doesn't reconcile
    (10 × 0.1s = 1.0s), so a duration wasn't invented to match it.
    `Kconfig.encoder`'s two resolution-derivation comments
    ("23.5mm rotation distance BMG gear" vs. `mmu_hardware.cfg`'s
    `24 / (2 * teeth)`) don't reconcile with each other either - the page
    shows only the resulting defaults table, not a formula.

    Reused `wiki/Synchronized-Gear-Extruder/Encoder_Meter.png` (copied to
    `doc/Feature-Encoder/encoder-meter.png`) as the "Printer variables
    exposed" UI illustration - checked first that it's safe to reuse per the
    diagram-reuse rule above: it's an annotated explainer (callout boxes over
    a real widget), and its callout labels already use the real v4 parameter
    name `flowguard_encoder_max_motion`, so no correction was needed.

    No menuconfig screenshot: confirmed `Kconfig.box_turtle` (the seed used
    by every existing screenshot session) doesn't select `MMU_HAS_ENCODER`,
    so the whole "Encoder config" menu is hidden without extra scene setup
    that wasn't done this session - omitted rather than silently faked.
25. **Fixed a footer regression from wrapping the art+copyright in
    `.hh-footer` (item 23)**: `hh-page-nav.js` inserted the Previous/Next nav
    "before `.hh-footer-art`", which used to mean "as a block sibling above
    the footer" back when the art and copyright were plain stacked siblings
    - but `.hh-footer-art` is now a flex child *inside* `.hh-footer`, so the
    nav landed as a third flex item in that same row instead, pushing the
    art/copyright to its right. Fixed by anchoring the JS on `.hh-footer`
    itself and inserting the nav before *that*, restoring it as a proper
    block sibling above the row. Caught by the user on `Feature-Encoder.md`;
    fix applies site-wide since it's the shared script.
26. **Footer spacing/size tweak, same session**: copyright font-size
    `0.6rem` -&gt; `0.45rem` (even smaller); `.hh-page-nav`'s `margin`/
    `padding-top` reduced (`1.5rem`/`1rem` -&gt; `0.5rem`/`0.5rem`) to pull the
    Previous/Next row closer to the `<hr>` above it; `.hh-footer`'s
    `margin-top` reduced (`1rem` -&gt; `0.4rem`) to pull the art/copyright row
    closer to Previous/Next above *it*.
27. **Fixed a real pin-alias slip on `Feature-Encoder.md`**: the example
    `[mmu_encoder unit0]` block had `encoder_pin : ^unit0:MMU_ENCODER` -
    `MMU_ENCODER` is a v3-wiki-style symbolic alias, not a real pin (compare
    `wiki/Hardware-Configuration.md`'s `encoder_pin: ^mmu:MMU_ENCODER`, which
    is exactly where this got half-copied from). v4 pin values are always
    fully-qualified `unit_mcu_name:pin_name` strings, per the "Pin aliases
    don't exist in v4" decision above - fixed to `^unit0:PA3`, matching the
    `unit0:PA0`-style pins already used on `Feature-Espooler.md`. Worth
    grepping any future page's example `.cfg` blocks for a bare symbolic name
    where a real pin should be, since this is an easy slip to reintroduce.
28. **Second Getting Started page: `GettingStartedWithViViD.md`.** BTT ViViD
    is a fully-specified type (`installer/mmu_types/Kconfig.vvd`) - LEDs,
    dual-sensor environment monitoring, heater, per-gate NFC readers, and the
    indexed selector are all `select`ed unconditionally, and `BOARD_TYPE`/
    `PARAM_NUM_GATES` are fixed defaults with no prompt, unlike a modular
    design. The one part that genuinely needs the reader's own input - and
    the reason this page exists rather than just a comparison-table row - is
    that a ViViD unit and its optional buffer board
    (`installer/boards/custom/Kconfig.vvd`'s `OPTION_VVD_BUFFER`, `imply`'d
    on by default) are two independent MCUs, each surfaced as its own
    "Select serial device for ..." menuconfig screen
    (`installer/connection/Kconfig.mmu_mcu` /`Kconfig.buffer_mcu`). Traced
    those screens down to the actual shell macro
    (`serial_device`/`mmu_serial_config`/`buffer_serial_config` in the root
    `installer/Kconfig`) that lists live `/dev/serial/by-id/*` devices
    filtered by `Klipper_<chip>` and lets the user pick by literal device
    name - confirming the user's claim that BTT's own naming (`vivid` vs
    `buffer` in the device string) is what makes the two screens obvious to
    tell apart, not any Kconfig-side chip-specific filtering (the filter
    pattern used for both screens is the generic substring `stm32`, matching
    either board - a `# PAUL TODO add chip as filter` comment in both
    `Kconfig.mmu_mcu`/`Kconfig.buffer_mcu` confirms this is a known, not-yet
    tightened gap upstream, which is exactly why picking the right one by
    name still matters).
    - **No real screenshots at all, this round**: confirmed via
      `doc_tools/capture.py`'s own header comment that `/dev/serial/by-id/*`
      is globbed live and "cannot be overridden" for reproducibility - a
      captured screenshot would show whatever's plugged into the capturing
      machine, not the illustrative device names the user actually asked to
      document. Used console-block text (`text` fences, not screenshots) for
      every menuconfig screen on this page instead, consistent with the
      user's own "should be quite simple" framing. Revisited next session
      once the user asked for captures after all - see item 29.
    - **Toolhead selection and the Spoolman NFC auto-create example** are
      both generic, non-ViViD-specific Kconfig options (same ones
      `GettingStartedWithBoxTurtle.md` uses) - written fresh rather than
      copy-pasted, but deliberately parallel in structure. Caught and fixed
      one own mistake before finishing: first draft implied **Select
      spoolman spool manager support** defaults to `Push` for ViViD - it
      doesn't; the default is `Off` regardless of MMU type (checked
      `Kconfig.options` directly), ViViD's built-in NFC readers just make
      turning it on worthwhile.
    - **The `./install.sh` / `./install.sh -i` sections are intentionally
      near-verbatim copies** of `GettingStartedWithBoxTurtle.md`'s own
      wording, per explicit request to include that text on this page too
      rather than just cross-reference it - this is genuinely
      installer-universal behaviour, not something to vary per MMU type.
    - **No new `index.md` card**: the "Card grid needs a new entry every
      time a section gains its first page" rule doesn't apply here - Getting
      Started already has its first card (pointing at the Box Turtle guide),
      so a second page in the same section doesn't get a second card.
29. **Added real menuconfig screenshots to `GettingStartedWithViViD.md`
    after all**, per explicit follow-up request - a new `getting-started-vivid`
    session in `doc_tools/shots.py` (seed `'none'`, same first-run approach as
    `getting-started-boxturtle`), 7 images: MMU Type (BTT ViViD + its buffer
    sub-option), Board type, the MMU and Buffer MCU-connection submenus, MMU
    Features/Additions, Toolhead, and the Spoolman NFC auto-create screen.
    Two real Kconfig-navigation mistakes surfaced and got fixed by actually
    running the capture rather than assuming the menu tree from reading
    Kconfig source alone:
    - The buffer's connection submenu's own internal choice prompt is `"MCU
      connection for sync-feedback buffer"`, but the enterable *menu* wrapping
      it (what the reader actually sees and types to reach it from the top
      level) is titled **`Buffer MCU connection`** - a different string.
      `mc.enter('MCU connection for sync-feedback buffer')` from the top menu
      reliably failed to find that text at the top level; fixed by entering
      `'Buffer MCU connection'` instead, then finding the inner prompt one
      level down. Same distinction already existed for the MMU side (top
      menu says `MCU connection`, which happens to equal its own inner
      choice's prompt too, by coincidence, not because it's the same
      pattern) - it just wasn't visible as a *distinct* name until the buffer
      side exposed it.
    - `"Spoolman"` in the Kconfig source is a `comment` (a plain section
      divider on the **Software Options** screen), not a `menu` - it isn't
      enterable at all. `mc.enter('Spoolman')` doesn't error on the comment
      itself; menuconfig's substring search instead landed the cursor on the
      *next* row containing the same substring - the **Auto-create...**
      checkbox further down the same screen - and pressing Enter on a bool
      item toggles it rather than opening a submenu, so the checkbox silently
      flipped on as a side effect before the real failure (waiting for a
      breadcrumb change that could never come) surfaced. Fixed by dropping
      the `enter('Spoolman')` step entirely - the target checkbox is
      selectable directly on the **Software Options** screen already reached
      one level up.
    - Also corrected the page's prose to match what the real screens showed
      rather than what reading the Kconfig source alone implied: "MCU
      connection" and "Buffer MCU connection" are each a *two-row submenu*
      (connection type + resolved device), not a flat Serial/CANbus toggle;
      and `MMU Features / Additions` fixes on more than LEDs/environment
      sensor/heater/NFC - the sync-feedback buffer is fixed on too (supplied
      by the buffer board), the old-style catchment filament buffer is fixed
      *off* (superseded by it), and fans/eject-buttons/encoder are the
      screen's only genuine off-by-default options for this design.
    - Still deliberately NOT captured: the two "Select serial device for
      ..." list screens themselves - unchanged reasoning from item 28, this
      machine has nothing plugged in so they'd show an empty list, not the
      illustrative device names. The two submenu screens captured instead
      (showing the connection-type row and the resolved "Other / manually
      entered" device row together) are the reproducible part of that same
      story.
30. **Third Feature page: `Feature-Endless-Spool-Runout.md`** - the other
    half of `wiki/Clog-Runout-EndlessSpool.md` (Runout Detection + EndlessSpool
    + Designated Waste Gate sections; the encoder-specific sections went to
    `Feature-Encoder.md`, see item 24). No dedicated Kconfig source, so
    verification meant reading the actual decision logic in code rather than
    a `.cfg` template:
    - **Clog/tangle vs. genuine runout is a real, code-level distinction**,
      not just wiki framing: Happy Hare checks the fitted switch sensors
      first, and only if they're inconclusive *and* an encoder is fitted
      does it nudge the gear motor and watch for encoder movement to settle
      the question. Clog/tangle always pauses regardless of EndlessSpool;
      EndlessSpool only ever acts on a confirmed runout. This is stated
      as plain fact on the page, not attributed to "the code" anywhere -
      per this session's explicit no-code-references instruction, on top of
      the standing page-genre-wide rule.
    - **Stale wiki content corrected, not ported**: `encoder_clog_detection_enabled`
      references (that content now lives on `Feature-Encoder.md`, not this
      page, so not even mentioned here); the wiki's combined
      `MMU_ENDLESS_SPOOL`+gate-status console example was replaced with the
      real, much simpler output (`EndlessSpool Groups: / Group A: Gates: ...`)
      - groups are set with numbers but reported back as letters (`0`→`A`,
        `1`→`B`, ...), confirmed directly in the formatting logic.
      - `MMU_TEST_RUNOUT` now takes an optional `TYPE=runout|clog` - the wiki's
        plain no-argument form still works but doesn't demonstrate the
        clog path.
    - **A real, easily-missed behaviour found by reading the eject-gate code
      path, not the wiki**: `endless_spool_eject_gate` is checked with `> 0`,
      so gate `0` can never be the designated waste gate through this
      setting - only gates numbered `1` and up. Stated as a plain usage rule
      on the page ("must be `1` or higher") rather than a caveat, since a
      reader hand-editing this value needs to know it either way.
    - **Image**: skipped `wiki/Quick-Start-QuattroBox/quattrobox_endless.png`
      and `wiki/Installation/questions_endless.png` deliberately - both are
      screenshots of the old v3 line-by-line install wizard (`Enable clog
      detection (y/n)?` prompts), a UI that no longer exists in v4's real
      menuconfig. Captured a fresh, real menuconfig screenshot instead (new
      `feature-endless-spool-runout` session in `doc_tools/shots.py`, plain
      boxturtle seed - this section isn't MMU-type-specific so needed no
      scene setup, same shape as the `feature-espooler` session).
    - **Waste-gate incompatibility claim softened**: the wiki flatly asserted
      "may be incompatible with type-B or C MMU designs." No such check
      exists in code either way, so the page states the real underlying
      requirement instead (a selector that can be commanded to visit an
      arbitrary gate on demand) and lets the reader judge their own design
      against it, rather than repeating an unverifiable type-letter claim.
31. **Fourth Feature page: `Feature-Sync-Feedback-Buffer.md`.** Source wiki
    page (`wiki/Synchronized-Gear-Extruder.md`) is unusually large and
    already uses v4 terminology throughout (FlowGuard, AutoTune,
    `mmu_vars.cfg`) - still verified everything against real code rather
    than trusting that, and found real gaps anyway:
    - **The wiki's `[mmu_sensors]` section name is wrong for v4** - the real
      generated section is `[mmu_buffer <unit_name>]` (confirmed directly in
      `config/base/mmu_hardware.cfg`), analogous to `[mmu_encoder ...]` and
      `[mmu_espooler ...]`. The wiki's `sync_feedback_tension_pin`/
      `sync_feedback_compression_pin` key names are wrong too - the real keys
      are plain `tension_pin`/`compression_pin` inside that section. Kept the
      wiki's `Typical_Buffer.png` diagram (it's an annotated, editable
      diagram, not live output - same reuse rule as `Conceptual-MMU.md`) but
      added a corrective note under it for exactly this key-name mismatch,
      rather than silently republishing the wrong keys as an image caption
      with no counter-signal in the text.
    - **`sync_gear_current`'s real default is `100`**, not the wiki
      example's `50` - confirmed in `Kconfig.motor_sync`.
    - **The wiki's `MMU_QUERY_PSENSOR` command doesn't exist in v4** - raw
      proportional-sensor readings are now reported by the general
      `MMU_SENSORS` command instead (confirmed directly in its output
      formatting code, which special-cases the proportional sensor to show
      both normalised and `(raw: ...)` values). Not ported.
    - **Scope boundary held firm**: FlowGuard's clog/tangle detection,
      tangle-prevention current boost, and the whole telemetry/tuning
      section (`sync_feedback_debug_log`'s plot script, interpreting
      telemetry, the AutoTune simulation plots) all stayed off this page,
      on the same "own Kconfig, own future page" reasoning as
      `Feature-Encoder.md`'s FlowGuard boundary (item 24) - mentioned only
      by parameter name (`flowguard_enabled`, `flowguard_max_relief`,
      `tangle_prevention_enabled`), no link, no deep dive. Confirmed via a
      live menuconfig dump that "FlowGuard (clog/tangle/runout detection)"
      is in fact its own separate submenu (`Other Settings → FlowGuard`),
      not nested under sync-feedback at all - the boundary is real, not
      just a documentation convenience.
    - **Images**: reused `Sync_Feedback_Meter.png` (an annotated diagram,
      same style and already-correct-param-names pattern as
      `Encoder_Meter.png` on `Feature-Encoder.md`) plus two small UI-icon
      images (`Switch_Based_Sensor_Compressed.png`, `P_Sensor_Position.png`)
      with no naming issues. Skipped `FilamentStatus.png` deliberately - a
      real Mainsail/Fluidd screenshot with "Pre-Gate"/"Gate" labels baked in,
      the exact pre-v4 sensor names `Conceptual-MMU.md` already corrected.
      Skipped every FlowGuard simulation/telemetry plot as out of scope for
      this page (see above), not because of any staleness issue with them.
    - **Real menuconfig screenshots** (`feature-sync-feedback-buffer`
      session, boxturtle seed - already ships a dual-switch Turtle Neck v2
      buffer, so no scene setup needed) for **Buffer config** and
      **Other Settings → MMU/Extruder sync**. The second screen only shows
      the buffer-feedback toggle and gear current on this seed - Box
      Turtle's gear-per-gate design always grips filament, so the
      `sync_to_extruder`/`sync_form_tip`/`sync_purge` toggles (genuine
      choices on a design that can release its grip) don't even appear -
      confirmed live rather than assumed, and stated as fact on the page
      with the screenshot cited as the example of the forced-on case.

32. **Split the planned single `Feature-NFC-Spoolman.md` into two pages**,
    `Feature-Spoolman.md` and `Feature-NFC.md`, per explicit request -
    Spoolman is a pure software/Moonraker integration with no Kconfig of its
    own, while NFC is genuinely new v4 hardware-reader surface, and the user
    wanted them cross-referencing each other rather than one combined page.
    Both are code-verified, not ported uncritically - see the §5 table
    entries above for the specific corrections found in each (stale gate-map
    status labels and a wrong/misplaced parameter name on the Spoolman page;
    the RC522-only homing-endstop caveat on the NFC page). `Feature-Spoolman.md`
    deviates from the template's "Hardware Setup" section name (retitled
    "Moonraker Setup", since there's no physical hardware to wire) - flagged
    for the user rather than silently decided, since every other Feature
    page so far has had real hardware. The wiki's four Mermaid sequence
    diagrams (one per `spoolman_support` mode) were initially dropped in
    favour of plain numbered steps under Tuning, since ` ```mermaid ` fences
    don't render reliably on this site (see **Zensical rough edges**) - later
    re-introduced by explicit request; see item 33 below. `Feature-NFC.md` is marked **beta**
    on the page itself, matching the Kconfig's own tag. Added both to
    `mkdocs.yml`'s nav; no new `index.md` card (Features already has one).

33. **Follow-up, same day: ERCF shared-reader screenshot on `Feature-NFC.md`,
    and Mermaid diagrams re-introduced on `Feature-Spoolman.md`, both by
    explicit request.**
    - The NFC screenshot half is fully done and verified: added an `ercf`
      seed to `doc_tools/capture.py`'s `BUILTIN_SEEDS`, a `_feature-nfc` scene
      to `doc_tools/shots.py` (toggles "Has NFC reader(s)" then "Has common
      NFC reader?" under the ERCF seed rather than the default Box Turtle —
      ERCF's moving-carriage/servo design fits "present one spool to one
      shared reader by hand" better than Box Turtle's gear-per-gate layout,
      matching how the page frames a shared reader), captured
      `doc/Feature-NFC/shared-reader-config.png`, and added it to the
      Hardware Setup section with explanatory prose.
    - The Mermaid half: item 32 above dropped the wiki's diagrams because
      ` ```mermaid ` fences hit the incremental-build-cache bug in
      **Zensical rough edges**. Re-introducing them here uses a different
      mechanism specifically to dodge that bug — raw `<pre class="hh-mermaid">`
      HTML (passed through untouched by the already-enabled `md_in_html`
      extension, so there's no fence-extraction step to race on), rendered
      client-side by `doc/assets/javascripts/hh-mermaid.js` against a
      pinned-version Mermaid v10 CDN script (`mermaid@10.9.1`, not a floating
      major tag) added to `mkdocs.yml`'s `extra_javascript`. **Verified
      rendering correctly, 6/6 diagrams with zero error placeholders, across
      5 separate loads (fresh tabs and same-tab reloads) plus one real
      in-app instant-navigation link click (not just a hard reload)** - see
      `doc/Feature-Spoolman.md`'s Tuning section. Getting there surfaced
      three real, distinct bugs, not one:
        1. **Mermaid's own bundled auto-render steals `class="mermaid"`
           nodes before this file's `mermaid.initialize({startOnLoad:
           false})` call can take effect** - the CDN script self-registers
           a DOMContentLoaded auto-render at load time, before
           `hh-mermaid.js` (loaded after it) runs at all, so by the time our
           code executes, auto-render has often already grabbed the nodes,
           started an async render, and lost the layout race below with
           nothing listening to retry it - confirmed directly by checking
           `document.querySelectorAll('pre.mermaid')` immediately on a
           fresh load and finding 0 (already converted and emptied). Fixed
           by never using `class="mermaid"` at all - diagrams use
           `class="hh-mermaid"` instead (styled to match via
           `doc/assets/stylesheets/extra.css`'s `.hh-mermaid` rule, since
           Material's shipped CSS only styles `.mermaid`), and
           `hh-mermaid.js` passes those nodes to `mermaid.run({nodes})`
           explicitly. This also means mermaid's own `data-processed`
           bookkeeping (tied to its own auto-scan) isn't something to rely
           on for a differently-named class - the script tracks
           processed-state itself via its own `data-hh-processed` attribute.
        2. **Material's `document$` observable fires more than once per
           load**, and calling `mermaid.run()` the instant it fires
           reliably loses a race against the browser's own layout of the
           just-swapped content — thrown outright (`Cannot read properties
           of null (reading 'getBBox')`) on an immediate call, or, just as
           often, swallowed internally by Mermaid itself and rendered as its
           own silent `aria-roledescription="error"` placeholder SVG instead
           of a real diagram, with no thrown error and no build warning
           either way (confirmed independently: `mermaid.parse()` said the
           exact source that produced a placeholder was syntactically valid,
           and a manual `mermaid.run()` moments later rendered the same
           source correctly). **Checking for `svg` presence alone is
           therefore not a valid render-success check** — check
           `svg[aria-roledescription="error"]` specifically. Mitigated with
           a real async readiness signal (`document.fonts.ready` + double
           `requestAnimationFrame`) before the first render attempt, a
           window-scoped serial queue (`window.__hhMermaidQueue`, not a
           script-local closure variable — this script's own top-level code
           was directly observed executing more than once against the same
           `window`/DOM, and a closure-local queue only serializes firings
           within its own execution, not against a second execution's
           queue), and explicit error-placeholder detection with one retry
           pass.
        3. **`requestAnimationFrame` never fires while a page is hidden**
           (backgrounded/inactive tab, per the Page Visibility API) - the
           double-rAF readiness signal from fix 2 hung indefinitely, with
           zero console output, whenever this happened. Confirmed directly:
           `document.hidden === true` on an affected tab, and a bare
           `requestAnimationFrame` call left permanently pending in that
           state. This isn't just a test-tool quirk — a real user who opens
           the page in a background browser tab would hit the identical
           stall. Fixed by racing the double-rAF against a 300ms fallback
           `setTimeout` in `hhMermaidReady()`, so the readiness gate can
           never hang forever regardless of tab visibility.
      Left in per the user's own explicit instruction to try it anyway
      ("even if they don't always render .. if I see a problem I will
      comment them out and replace with images") - that fallback ended up
      not being needed, but if a diagram ever does render broken for a real
      reader, note `doc/Feature-Spoolman/` only holds the wiki's UI
      screenshots reused elsewhere on the page, not pre-rendered images of
      these diagrams — a static-image fallback would need those re-exported
      from the wiki's original Mermaid source first.

34. **Follow-up, same day: made every Mermaid diagram legible in dark mode,
    and rewrote `index.md` (the Home page) from scratch**, both by explicit
    request.
    - The Mermaid fix, in two passes. First pass: item 33's diagrams were
      unreadable in dark mode - Mermaid's default theme hard-codes dark
      text/lines calibrated for a light page, and the SVG itself has no
      background of its own, so dark scheme showed dark text directly on
      the site's own dark background. Fixed with one rule in
      `doc/assets/stylesheets/extra.css`
      (`.hh-mermaid { background: #fff; ... }`), unconditionally on both
      schemes, rather than re-theming Mermaid itself - simpler, and doesn't
      need hh-mermaid.js to re-render on every palette toggle. Verified past
      the obvious trap: checking only the container's own
      `background-color` would have missed a real bug - Mermaid's default
      theme fills actor boxes with a pale `#ECECFF`, which reads as "light
      color, might be a dark-mode leak" out of context. Checked the actual
      painted glyph color instead (`getComputedStyle(tspan).fill` on a real
      label, in a tab confirmed via
      `document.body.getAttribute('data-md-color-scheme') === "slate"`) and
      got solid black text - the pale fill is the actor box background by
      design, sitting fine on the forced-white card, not a leftover dark-
      scheme color.
      Second pass, same day: user pointed out a white card in the middle of
      a dark page still doesn't *look* like it belongs - asked for a real
      dark background with light text/lines instead of light-mode-colours-
      on-a-white-island. Landed on a CSS filter rather than a second Mermaid
      render: `[data-md-color-scheme="slate"] .hh-mermaid { filter:
      invert(1) hue-rotate(180deg); }`, layered on top of the always-white
      card from the first pass. `invert(1)` alone flips the white
      background to black and dark text to light, but also drags Mermaid's
      one non-grey colour (the pale lavender `#ECECFF` actor-box fill)
      through a hue flip into a sickly yellow-green; `hue-rotate(180deg)`
      un-rotates exactly that shift, landing back on a dark, still
      lavender-tinted box instead. Verified against a real diagram's actual
      SVG markup pulled out of a live page (not a hand-built approximation)
      rendered standalone in an isolated test document side-by-side with
      the unfiltered version, and again in the real page by firing
      Material's own palette toggle (`input[name="__palette"]`) rather than
      just setting the attribute by hand - light scheme still shows the
      plain white card with no filter (`getComputedStyle(...).filter ===
      "none"`), dark scheme shows the inverted one. Not the literal Mermaid
      "dark" theme's exact palette, but a legible, on-brand dark-mode
      equivalent of this site's own light-mode diagrams, with no re-render
      needed on toggle.
    - The Home page: previous version (v1, see the §1 table entry above) was
      an explicit placeholder - "under construction," a stale 4-page card
      grid, no real content. Rewritten using `wiki/Home.md` and the actual
      Happy-Hare repo's `README.md` (`.happy-hare-src/README.md` when
      cloned locally - not this doc repo's own `README.md`, which is about
      building *this site*, not about Happy Hare itself) as source
      material, per explicit request. Specific content decisions:
        - Dropped the wiki's "Organization" section entirely (flagged by the
          user as incorrect) rather than trying to correct it in place - its
          job (which vendor uses which selector mechanism) is already done
          correctly and in more depth by `Conceptual-MMU.md`'s "Which
          vendors use which mechanism" table, so Home now just links there
          instead of maintaining a second, competing hardware list.
        - Dropped the wiki's Carrot Collective / TradRack Discord mention
          from "Getting help" (flagged by the user as old) - kept the main
          Happy Hare Discord and GitHub issues only.
        - Dropped README's donation appeal/paragraph and the personal
          "my setup" poem/photo (`my_voron_and_ercf.jpg`) - neither serves
          orientation, which is this page's one job per the request.
        - **Card grid rule changed**: v1's grid added one card the first
          time each *page* landed, which is why Reference had two separate
          cards (`Command-Reference.md`, then `Printer-Variables.md`) while
          Concepts had none at all despite `Conceptual-MMU.md` existing for
          days. v2 is one card per top-level *nav section* (5 total -
          Getting Started, Concepts, Features, Reference, Developer Guide),
          matching `mkdocs.yml`'s nav exactly - adding the tenth Feature
          page won't need touching this again, only a genuinely new
          top-level section will. See the updated §1 table entry above.
        - **Splash images**: three photos from the wiki's `resources/`
          (`universal_mmu_driver.png`, `my_klipperscreen.png`,
          `example_mmu_print.png`) - none are technical labeled diagrams, so
          the "reuse editable diagrams, skip stale real-output screenshots"
          rule doesn't bite here; these are just photos/UI collages used for
          orientation, not documentation of specific current field names.
          Re-encoded as JPEG and downsized before committing though (source
          PNGs were phone-camera-sized, ~4MB each for the two photos -
          `sips -Z <width> -s format jpeg -s formatOptions 82`, following
          `doc/index/` for the folder name per the established
          page-name-matched-folder convention, same as every `Feature-*`
          page's own image folder). Total added to the repo: ~800KB across
          all three, versus ~6.4MB for the untouched source PNGs.
        - Added a short "How this site is organized" section (Getting
          Started / Concepts / Features / Reference / Developer Guide, what
          each is for) plus the `MMU_LIKE_THIS`/`like_this.cfg`/
          `printer.mmu.like_this`/warning-vs-tip notational conventions -
          this is genuinely new content, not ported from either source;
          the user asked for "conventions and norms" and neither the wiki
          nor the README had anything like it since neither was written as
          a multi-page site with its own house style.
        - Kept (trimmed) the wiki's "browser plugin" analogy for what Happy
          Hare conceptually is - still accurate, still a good non-technical
          explainer, not something either source deprecated.

**To pick this back up:** the §5 Feature-page template has now been proven
out across six pages (eSpooler, Encoder, EndlessSpool & Runout Detection,
Sync-Feedback Buffer, Spoolman, NFC) - copy any of their structure and
section order for the remaining eight pages in the table above, and follow
**Before finishing a Feature page** (proofread against the wiki source,
report what didn't carry forward) before calling any of them done. Several
remaining Feature pages share the same "combined v3 wiki page, split across
several v4 pages" shape `Feature-Encoder.md`/`Feature-Endless-Spool-Runout.md`
and `Feature-Spoolman.md`/`Feature-NFC.md` just went through - check the §5
table's "Wiki source" column for other combined pages before assuming a 1:1
mapping. §2's other two pages (`Understanding-Operation.md`,
`Print-Job-State-Machine.md`) are still open too, and should lean on
`Conceptual-MMU.md`'s terminology rather than re-defining it. The four
`Configuring-mmu*.cfg.md` generators for §3 are also still open, following
the exact `gen_command_reference.py` pattern already proven out. Whatever's
next, run `./venv/bin/zensical build --clean` before calling it done, not a
plain `zensical build` - see **Zensical rough edges**.
