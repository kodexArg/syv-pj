#!/usr/bin/env python3
"""Track B data-only normalizer for the syv-pj resource catalogs.

Re-runnable, frontmatter-only, line-surgical. Touches ONLY free fields the
syv-pj-api contract never reads, and rewrites ONLY the matched lines — the
rest of the frontmatter (including the `rangos:` structure) is left byte-for-
byte intact. A full ruamel round-trip was rejected because it normalizes
unrelated nodes (e.g. `mando_default: null` → bare null) inside the locked
`rangos:` block.

Transforms:
  1. `tags:` first element in facciones/, subfacciones/, rangos/ → catalog
     pattern `catalogo/<cat>` (matches the aspecto/equipo/habilidad style).
     Only the inline `tags: [...]` form used by these folders is handled.
  2. legacy `atributo_dominante:` in catalogos/habilidad/ → tac→mente,
     fis→cuerpo, men→alma (dead key, not read).

Never touches slug/nombre/descripcion/probabilidad/doc/faccion_padre/
atributos_base/subcategoria/peso_sorteo/peso_narrativo/sesgo_*/requires/
excluye or the `rangos:` structure.

Dry-run by default; pass --apply to write.

    uv run python _tools/normalize_tags.py            # dry-run
    uv run python _tools/normalize_tags.py --apply    # write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RESOURCES = Path(__file__).resolve().parents[1] / "resources"

# folder -> the bare first-tag token that must become catalogo/<token>
TAG_FOLDERS = {
    "facciones": "faccion",
    "subfacciones": "subfaccion",
    "rangos": "rangos",
}

ATRIBUTO_MAP = {"tac": "mente", "fis": "cuerpo", "men": "alma"}


def _frontmatter_bounds(lines: list[str]) -> tuple[int, int] | None:
    """Index range [start, end) of frontmatter body lines, or None."""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 1, i
    return None


def _rewrite_tags_line(line: str, token: str) -> str | None:
    """Replace bare first tag `"<token>"` with `"catalogo/<token>"` in an
    inline `tags: ["<token>", ...]` line. Returns new line or None if no match."""
    m = re.match(r'^(\s*tags:\s*\[\s*)(["\'])' + re.escape(token) + r'\2', line)
    if not m:
        return None
    prefix, q = m.group(1), m.group(2)
    rest = line[m.end():]
    return f"{prefix}{q}catalogo/{token}{q}{rest}"


def _rewrite_atributo_line(line: str) -> str | None:
    m = re.match(r'^(\s*atributo_dominante:\s*)([A-Za-z]+)(\s*)$', line)
    if not m:
        return None
    val = m.group(2)
    if val not in ATRIBUTO_MAP:
        return None
    return f"{m.group(1)}{ATRIBUTO_MAP[val]}{m.group(3)}"


def _process(path: Path, rewrite) -> str | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    bounds = _frontmatter_bounds(lines)
    if bounds is None:
        return None
    start, end = bounds
    changed = False
    for i in range(start, end):
        body = lines[i].rstrip("\n")
        nl = "\n" if lines[i].endswith("\n") else ""
        new = rewrite(body)
        if new is not None and new != body:
            lines[i] = new + nl
            changed = True
            break  # at most one target line per file
    return "".join(lines) if changed else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = ap.parse_args()

    changed: list[tuple[str, Path]] = []

    for folder, token in TAG_FOLDERS.items():
        for path in sorted((RESOURCES / folder).glob("*.md")):
            if path.name.startswith("_"):
                continue
            new_text = _process(path, lambda ln, t=token: _rewrite_tags_line(ln, t))
            if new_text is not None:
                changed.append(("tags", path))
                if args.apply:
                    path.write_text(new_text, encoding="utf-8")

    for path in sorted((RESOURCES / "catalogos" / "habilidad").glob("*.md")):
        if path.name.startswith("_"):
            continue
        new_text = _process(path, _rewrite_atributo_line)
        if new_text is not None:
            changed.append(("atributo_dominante", path))
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY-RUN (no files written)"
    print(f"== normalize_tags — {mode} ==")
    by_kind: dict[str, int] = {}
    for kind, path in changed:
        by_kind[kind] = by_kind.get(kind, 0) + 1
        print(f"  [{kind}] {path.relative_to(RESOURCES.parent)}")
    print(f"-- {len(changed)} file(s): " + ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
