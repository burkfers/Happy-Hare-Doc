# Happy Hare documentation tooling
#
# Generates doc/Command-Reference.md from the real command metadata scattered
# across extras/mmu/ - the same HELP_BRIEF / HELP_PARAMS / HELP_SUPPLEMENT
# strings a user sees from `<CMD> HELP=1` on a printer, and the same CATEGORY_*
# grouping BaseCommand.register() uses. See doc_tools/README.md for the split
# between this directory (code) and doc/ (its output).
#
# This file lives in the Happy-Hare-Doc repo; extras/mmu/ lives in Happy-Hare -
# see HAPPY_HARE_SRC below (set for you by `make command_reference`, or point it
# at a checkout you already have).
#
# Commands are NOT confined to extras/mmu/commands/: mmu_controller.py registers
# a few Klipper-wrapper commands directly, and each selector family
# (extras/mmu/unit/selectors/*.py) registers its own MMU_CALIBRATE_* /
# MMU_GRIP / MMU_RELEASE / MMU_SOAKTEST_SELECTOR commands. So this walks the
# whole extras/mmu/ tree rather than one directory - grep for
# "self.register(" across extras/mmu if this ever needs re-checking.
#
# Nothing here imports Happy Hare or Klipper: CMD / HELP_BRIEF / HELP_PARAMS /
# HELP_SUPPLEMENT are plain class-body assignments that only ever reference each
# other (never self., never an import), so they're extracted with ast and
# re-executed in isolation - accurate for f-strings and %-formatting alike,
# without needing the fake klippy tree test/ builds.
#
# Anchors: a command's heading is its bare CMD (e.g. `### MMU_LOAD`), which
# python-markdown's toc extension slugifies to lowercase with underscores kept
# (`#mmu_load`) - that's the stable anchor other pages should link to.

import argparse
import ast
import os
import pathlib
import sys

DOC_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_FILE = DOC_ROOT / "doc" / "Command-Reference.md"

HAPPY_HARE_SRC = os.environ.get("HAPPY_HARE_SRC")
if not HAPPY_HARE_SRC or not (pathlib.Path(HAPPY_HARE_SRC) / "extras" / "mmu").is_dir():
    raise SystemExit(
        "HAPPY_HARE_SRC must point at a Happy-Hare checkout (containing extras/mmu/) - "
        "run via `make command_reference`, which fetches one and sets this for you, or "
        "set it yourself to an existing checkout for faster local iteration."
    )
MMU_DIR = pathlib.Path(HAPPY_HARE_SRC) / "extras" / "mmu"
BASE_COMMAND_FILE = MMU_DIR / "commands" / "mmu_base_command.py"
CONSTANTS_FILE = MMU_DIR / "mmu_constants.py"

HELP_FIELDS = ("CMD", "HELP_BRIEF", "HELP_PARAMS", "HELP_SUPPLEMENT")

# Display order; categories not listed here (STEPS, INTERNAL) are developer-only
# and rendered in their own appendix rather than mixed in with user commands.
CATEGORY_ORDER = [
    "CATEGORY_GENERAL",
    "CATEGORY_TESTING",
    "CATEGORY_MACROS",
    "CATEGORY_CALLBACKS",
    "CATEGORY_OTHER",
]
APPENDIX_CATEGORIES = ["CATEGORY_STEPS", "CATEGORY_INTERNAL"]


def extract_categories(source):
    """CATEGORY_* = "..." constants at module scope in mmu_base_command.py."""
    tree = ast.parse(source)
    categories = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith("CATEGORY_"):
                    categories[target.id] = ast.literal_eval(node.value)
    return categories


def extract_register_category(class_node):
    """Find self.register(...) inside the class and return its category name
    (e.g. "CATEGORY_STEPS"), whether passed as a keyword or positionally."""
    for node in ast.walk(class_node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "register"
        ):
            for kw in node.keywords:
                if kw.arg == "category" and isinstance(kw.value, ast.Name):
                    return kw.value.id
            # Positional form: register(name, handler, help_brief, help_params,
            # help_supplement, category, ...) - category is the 6th argument.
            if len(node.args) >= 6 and isinstance(node.args[5], ast.Name):
                return node.args[5].id
    return "CATEGORY_OTHER"  # BaseCommand.register()'s own default


def extract_help_strings(class_node, source, constants):
    """Pull CMD / HELP_BRIEF / HELP_PARAMS / HELP_SUPPLEMENT class-body assignments
    and re-execute them in encounter order so later f-strings/%-formats referencing
    earlier ones (e.g. HELP_PARAMS using CMD and HELP_BRIEF), or UI constants like
    UI_DEGREE from the commands' `from ..mmu_constants import *`, resolve correctly."""
    assigns = {}
    for node in class_node.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id in HELP_FIELDS:
                assigns[target.id] = node

    if "CMD" not in assigns or "HELP_BRIEF" not in assigns:
        return None

    namespace = dict(constants)
    for field in HELP_FIELDS:
        node = assigns.get(field)
        if node is None:
            continue
        segment = ast.get_source_segment(source, node)
        exec(segment, namespace)  # noqa: S102 - static source, not user input

    return {
        "cmd": namespace.get("CMD", ""),
        "help_brief": namespace.get("HELP_BRIEF", ""),
        "help_params": namespace.get("HELP_PARAMS", ""),
        "help_supplement": namespace.get("HELP_SUPPLEMENT", ""),
    }


def load_constants():
    """mmu_constants.py has no imports of its own, so it's safe to exec directly -
    this is where UI_DEGREE and friends, referenced from HELP_* strings, come from."""
    namespace = {}
    exec(CONSTANTS_FILE.read_text(), namespace)  # noqa: S102 - static source, not user input
    return namespace


def collect_commands():
    categories = extract_categories(BASE_COMMAND_FILE.read_text())
    constants = load_constants()
    commands = []
    skipped = []

    for path in sorted(MMU_DIR.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        source = path.read_text()
        if "self.register(" not in source:
            continue  # cheap pre-filter - most files under extras/mmu/ define no commands
        tree = ast.parse(source, filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            help_strings = extract_help_strings(node, source, constants)
            if help_strings is None:
                continue  # a mixin or helper class with no CMD of its own
            if not help_strings["cmd"]:
                continue
            category_name = extract_register_category(node)
            commands.append(
                {
                    **help_strings,
                    "category": category_name,
                    "category_label": categories.get(category_name, category_name),
                    "file": str(path.relative_to(HAPPY_HARE_SRC)),
                }
            )

    seen = set()
    for cmd in commands:
        if cmd["cmd"] in seen:
            skipped.append(cmd["cmd"])
        seen.add(cmd["cmd"])

    return commands, categories, skipped


def strip_heading_line(help_params):
    """HELP_PARAMS's first line is always "CMD: brief" (BaseCommand.format_help()
    parses it that way) - drop it here since the page already shows CMD as the
    heading and HELP_BRIEF as the description right under it."""
    lines = help_params.splitlines()
    if lines and ":" in lines[0]:
        lines = lines[1:]
    return "\n".join(line for line in lines if line.strip())


def render_command(cmd):
    lines = [f"### {cmd['cmd']}", "", f"*{cmd['help_brief']}*", ""]

    params = strip_heading_line(cmd["help_params"])
    if params:
        lines += ["**Parameters**", "", "```", params, "```", ""]

    supplement = cmd["help_supplement"].strip()
    if supplement:
        # HELP_SUPPLEMENT is shown verbatim - it's exactly what `CMD HELP=1` prints
        # on a real printer, "Examples:" line included.
        lines += ["```", supplement, "```", ""]

    return "\n".join(lines)


def render_page(commands, categories):
    by_category = {}
    for cmd in commands:
        by_category.setdefault(cmd["category"], []).append(cmd)
    for cmds in by_category.values():
        cmds.sort(key=lambda c: c["cmd"])

    out = [
        "# Command Reference",
        "",
        "Every `MMU_*` command Happy Hare provides - generated directly from the",
        "same help text `<CMD> HELP=1` prints at a real printer, so it's always",
        "in sync with what you'll actually see.",
        "",
    ]

    for category_name in CATEGORY_ORDER:
        cmds = by_category.get(category_name, [])
        if not cmds:
            continue
        out += [f"## {categories.get(category_name, category_name)}", ""]
        out += [render_command(cmd) for cmd in cmds]

    appendix = [c for cat in APPENDIX_CATEGORIES for c in by_category.get(cat, [])]
    if appendix:
        appendix.sort(key=lambda c: (c["category"], c["cmd"]))
        out += [
            "## Internal / developer commands",
            "",
            "Not part of the supported user interface - individual loading/unloading",
            "steps and internal machinery, useful when working on Happy Hare itself.",
            "See the [Developer Guide](Dev-Code-Layout.md).",
            "",
        ]
        out += [render_command(cmd) for cmd in appendix]

    out += [
        "",
        "---",
        "",
        '<pre class="hh-footer-art">',
        "  (\\_/)",
        "  ( *,*)",
        '  (")_(") Happy Hare Ready',
        "</pre>",
        '<p class="hh-footer-copyright">Copyright (C) 2022-2026 Paul Morgan</p>',
    ]

    return "\n".join(out).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if doc/Command-Reference.md is stale instead of writing it",
    )
    args = parser.parse_args()

    commands, categories, skipped = collect_commands()
    if skipped:
        print(f"warning: duplicate CMD definitions for: {', '.join(sorted(set(skipped)))}", file=sys.stderr)

    page = render_page(commands, categories)

    if args.check:
        current = OUT_FILE.read_text() if OUT_FILE.exists() else ""
        if current != page:
            print(f"{OUT_FILE} is stale - run `make command_reference`", file=sys.stderr)
            return 1
        return 0

    OUT_FILE.write_text(page)
    print(f"wrote {OUT_FILE} ({len(commands)} commands)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
