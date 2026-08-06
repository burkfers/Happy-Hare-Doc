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
- **No Mermaid diagrams** — tried, and reverted; see **Zensical rough edges**.
  Architecture diagrams in the Developer Guide are plain ASCII in fenced code
  blocks instead.
- **Getting Started scope (v1):** Box Turtle only, walked deep. Everything else gets
  a comparison table + "same pattern, different Kconfig starter" note. Multi-unit and
  additional MMUs come later as their own pages.
- **Generated vs hand-written:** Command Reference and Printer Variable Reference
  are *generated*/*code-verified* respectively from source (see §10 below) rather
  than hand-transcribed — same "code in `doc_tools/`, output in `doc/`" split
  already established for screenshots. The four Configuration Reference pages
  (§3) are still planned as generated but not yet built. Everything else is
  hand-written prose, informed by the wiki.
- **v3→v4 flag:** any page ported from `wiki/` gets a ⚠️ until someone verifies it
  against v4 code. The riskiest is the Type-A/Type-B taxonomy — v4's real selector
  classes (`LinearSelector`, `LinearServoSelector`, `ServoSelector`,
  `IndexedSelector`, `RotarySelector`, `VirtualSelector`, plus multi-gear variants,
  now fully documented in `doc/Dev-Code-Layout.md`) don't map cleanly onto the old
  binary split, so that page needs a rewrite, not a port.
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
| `index.md` (Home) | `README.md` + `wiki/Home.md` | **done (v1)** — hero logo, tagline, card grid to what exists so far, ASCII bunny. Card grid needs a new entry every time a section gains its first page. |

### 1. Getting Started

| Page | Source | Status |
|---|---|---|
| `Installation.md` | `wiki/Installation.md` | port, verify against `install.sh`/`Makefile` flags |
| `GettingStartedWithBoxTurtle.md` | existing `doc/` page | **done**, incl. a "Picking a toolhead" step (shared toolhead/extruder geometry database, optional, reduces calibration) with two real screenshots |
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

### 5. Features — template proved out on eSpooler, 13 pages to go

| Feature page | Kconfig source | Wiki source | Status |
|---|---|---|---|
| `Feature-Espooler.md` | `Kconfig.espooler` | `wiki/Espooler-Support.md` | **done (v3)** — first page written against the template (see below); code-verified against `mmu_espooler.py`, `mmu_filament_movement.py`'s `_wrap_espooler()`, and `mmu_unit_parameters.py`. v1 over-compressed the ported wiki content; v2 restored the UI screenshots, TIP/IMPORTANT callouts, the `espooler_speed_exponent` worked example, and the per-mode setup walkthroughs, added a real `doc_tools/shots.py` session for the eSpooler pins menuconfig screen; v3 dropped the leading provenance paragraph, all developer-jargon (class/method names), the (nonexistent in v4) pin-alias example, and fixed "sync-feedback" → "filament (catchment)" buffer naming — see the decisions above and the session log |
| `Feature-Encoder.md` | `Kconfig.encoder` | part of `wiki/Clog-Runout-EndlessSpool.md` |
| `Feature-Sync-Feedback-Buffer.md` | `Kconfig.sync_feedback_buffer`, `Kconfig.motor_sync` | `wiki/Synchronized-Gear-Extruder.md` |
| `Feature-NFC-Spoolman.md` | `Kconfig.nfc_reader` | `wiki/Spoolman-Support.md` |
| `Feature-LEDs.md` | `Kconfig.leds` | `wiki/Led-Support.md` |
| `Feature-Endless-Spool-Runout.md` | (no dedicated Kconfig — sensor-driven) | `wiki/Clog-Runout-EndlessSpool.md` |
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

**To pick this back up:** the §5 Feature-page template is proven out across
three rounds of revision (v1 → v2 → v3) - copy `Feature-Espooler.md`'s
*current* structure and section order (no provenance paragraph, no dev-jargon,
ends with the footer) for the remaining thirteen pages in the table above, and
follow **Before finishing a Feature page** (proofread against the wiki source,
report what didn't carry forward) before calling any of them done. §2's other
two pages (`Understanding-Operation.md`, `Print-Job-State-Machine.md`) are
now open too, and should lean on `Conceptual-MMU.md`'s terminology rather than
re-defining it. The four `Configuring-mmu*.cfg.md` generators for §3 are also
still open, following the exact `gen_command_reference.py` pattern already
proven out. Whatever's next, run `./venv/bin/zensical build --clean` before
calling it done, not a plain `zensical build` - see **Zensical rough edges**.
