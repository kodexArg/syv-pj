#!/usr/bin/env python3
"""Verifies every backtick-quoted slug cited in docs/generacion-procedural.md
against the real catalogs under resources/.

Prevents the drift that motivated this script: prose citing facciones/rangos/
entrenamientos/habilidades/aspectos that don't exist as real resource files
(e.g. `confederados`, `ejercito_rojo`, a `tirador_designado` rango that was
never created, a `veterano_de_campo` aspecto that doesn't match the real
`veterano` slug).

Checks four tag families, each backtick-quoted with its own prefix:
  - `faccion/<slug>`        → resources/facciones/<slug>.md (frontmatter slug:)
  - `rango/<slug>`          → any `slug: <slug>` inside a `rangos:` list in
                              resources/rangos/*.md
  - `entrenamiento/<slug>`  → resources/catalogos/entrenamiento/<slug>.md
  - `habilidad/<slug>`      → resources/catalogos/habilidad/<slug>.md
  - `aspecto/<slug>`        → resources/catalogos/aspecto/<slug>.md
  - `especialidad/<path>`   → resources/especialidades/**/*.md (frontmatter slug:)

Exit code 1 and a list of orphans if any citation has no matching resource.

    uv run python _tools/verificar_slugs_doc.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "generacion-procedural.md"
RESOURCES = ROOT / "resources"

TAG_PATTERN = re.compile(
    r"`(faccion|rango|entrenamiento|habilidad|aspecto|especialidad)/([a-z_][a-z0-9_/]*)`"
)


def _frontmatter_slugs(folder: Path) -> set[str]:
    """slug: values declared in top-level frontmatter of every *.md in folder (non-recursive)."""
    slugs: set[str] = set()
    for f in folder.glob("*.md"):
        if f.name.startswith("_moc"):
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^slug:\s*(\S+)\s*$", text, re.MULTILINE)
        if m:
            slugs.add(m.group(1).strip('"'))
        else:
            slugs.add(f.stem)
    return slugs


def _especialidad_slugs() -> set[str]:
    slugs: set[str] = set()
    for f in (RESOURCES / "especialidades").rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^slug:\s*(\S+)\s*$", text, re.MULTILINE)
        if m:
            slugs.add(m.group(1).strip('"').removeprefix("especialidad/"))
    return slugs


def _rango_slugs() -> set[str]:
    slugs: set[str] = set()
    for f in (RESOURCES / "rangos").glob("*.md"):
        if f.name.startswith("_moc"):
            continue
        text = f.read_text(encoding="utf-8")
        slugs.update(re.findall(r"^\s*-\s*slug:\s*(\S+)\s*$", text, re.MULTILINE))
    return slugs


def load_catalogs() -> dict[str, set[str]]:
    return {
        "faccion": _frontmatter_slugs(RESOURCES / "facciones"),
        "rango": _rango_slugs(),
        "entrenamiento": _frontmatter_slugs(RESOURCES / "catalogos" / "entrenamiento"),
        "habilidad": _frontmatter_slugs(RESOURCES / "catalogos" / "habilidad"),
        "aspecto": _frontmatter_slugs(RESOURCES / "catalogos" / "aspecto"),
        "especialidad": _especialidad_slugs(),
    }


def find_orphans(doc_text: str, catalogs: dict[str, set[str]]) -> list[str]:
    orphans = []
    for family, slug in TAG_PATTERN.findall(doc_text):
        if slug not in catalogs[family]:
            orphans.append(f"`{family}/{slug}`")
    return orphans


def main() -> int:
    doc_text = DOC.read_text(encoding="utf-8")
    catalogs = load_catalogs()
    orphans = find_orphans(doc_text, catalogs)
    if orphans:
        print(f"FAIL: {len(orphans)} slug(s) cited in {DOC.relative_to(ROOT)} "
              f"have no matching resource:")
        for o in sorted(set(orphans)):
            print(f"  - {o}")
        return 1
    print(f"OK: all cited slugs in {DOC.relative_to(ROOT)} exist in resources/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
