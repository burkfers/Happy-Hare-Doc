# Documentation Style Guide

A practical writing guide for contributors creating or updating pages in this documentation site.

## Purpose

Use this page as the default style reference for:

- page structure and headings
- callouts and notes
- tables and code examples
- image formatting
- theme colors and icon usage

## Quick checklist

Before opening a pull request, verify:

- Page appears in [mkdocs.yml](../mkdocs.yml) nav.
- No `[TOC]` marker is present.
- Admonitions use `!!!` syntax.
- Config examples use `yaml` code fences.
- New screenshots are readable and centered where needed.
- Page ends with a single `---` line.

## Headings and section flow

Use sentence-case headings and keep section structure shallow where possible.

Example structure:

```markdown
# Feature Name

## Concept

## Hardware setup

## Parameter setup

## Commands

## Troubleshooting

## See also

---
```

## Admonitions (callouts)

Use Python-Markdown admonitions:

```markdown
!!! note "Title"
    Body text.
```

Recommended types:

| Use case | Admonition type |
| --- | --- |
| General explanation | `note` |
| Practical advice | `tip` |
| Important warning | `warning` |
| Dangerous action | `danger` |
| Known issue | `bug` |
| Worked example | `example` |

Rendered examples:

!!! note "Note"
    Use this for neutral, supporting context.

!!! tip "Tip"
    Use this for shortcuts, defaults, and practical setup hints.

!!! warning "Important"
    Use this when readers can make a costly configuration mistake.

## Tables

Use simple pipe tables with short headers. Keep units in headers or in a Notes column.

Template:

```markdown
| Parameter | Default | Typical range | Notes |
| --- | --- | --- | --- |
| `parameter_name` | `1.0` | `0.8-1.2` | What changing it does |
```

Example:

| Parameter | Default | Typical range | Notes |
| --- | --- | --- | --- |
| `extruder_homing_max` | `50` | `20-80` | Upper bound for homing movement |
| `toolhead_post_load_tighten` | `60` | `40-90` | Extra movement to seat filament |

## Code blocks and commands

Use fenced code blocks with explicit language.

- Use `yaml` for config examples (including cfg-like snippets).
- Use `bash` for commands.
- Use plain `text` only for raw output.

Examples:

```yaml
# mmu_parameters.cfg
toolhead_post_load_tighten: 60
extruder_homing_max: 50
```

```bash
make docs
make docs_build
make docs_preview
```

## Images and screenshots

For menuconfig or UI screenshots in narrative pages, center images and set width to improve readability in long pages.

```html
<p align="center">
  <img src="Feature-Example/screen-01.png" alt="Feature setup screen" width="70%">
</p>
```

Guidance:

- Prefer one screenshot per concept step.
- Keep alt text descriptive and task-oriented.
- Avoid low-contrast crops or tiny text.

## Theme and color guidance

Site theme direction (from [mkdocs.yml](../mkdocs.yml)):

- Primary: black
- Accent: pink
- Light scheme: `default`
- Dark scheme: `slate`

Use semantic styling rather than hard-coded inline colors whenever possible.

The site also applies a tri-color marker before H2 headings via CSS in [doc/assets/stylesheets/extra.css](assets/stylesheets/extra.css).

## Icons and icon repositories

This site uses Material-style icon identifiers in config (examples: `material/tablet-dashboard`, `fontawesome/brands/github`).

Useful icon references:

- Zensical: https://zensical.org
- Lucide: https://lucide.dev/icons/
- Material Design: https://pictogrammers.com/library/mdi/
- FontAwesome: https://fontawesome.com/search?m=free
- Octicons: https://octicons.github.com/
- Simple Icons: https://simpleicons.org/

Example social icon entries:

```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/moggieuk/Happy-Hare
      name: Happy Hare on GitHub
    - icon: material/tablet-dashboard
      link: https://github.com/moggieuk/KlipperScreen-Happy-Hare-Edition
      name: KlipperScreen Happy Hare Edition on GitHub
```

## Common mistakes to avoid

- Adding `[TOC]` to pages.
- Using GitHub callout syntax like `[!NOTE]`.
- Using unsupported admonition names such as `important`.
- Adding Mermaid fenced blocks where deterministic rendering is required.
- Leaving a page out of nav after creating it.

## Suggested workflow for knowledge workers

1. Draft page sections first.
2. Add callouts and tables second.
3. Add screenshots and links third.
4. Run local preview.
5. Confirm nav placement and section anchors.

---
