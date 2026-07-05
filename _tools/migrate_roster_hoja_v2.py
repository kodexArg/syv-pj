#!/usr/bin/env python3
"""Migrate resources/personajes/*.md from the legacy loose-field frontmatter
to the hoja-personaje v2 contract (docs/hoja-personaje.md §9 refactor rule).

Deterministic, idempotent: loose fields (`faccion`, `subfaccion`, `rango`,
`especialidad`, `lealtad`, `aspectos`, `rasgos`, `equipo`, `estado`, `barrio`)
fold into `tags[]` using the canonical dotted/slashed notation already
present in the catalogs (resources/catalogos/*, resources/rangos/*,
resources/especialidades/*). `apariencia` (old flat list of descriptors)
becomes the three-paragraph object `{rostro, figura, presencia}`, splitting
existing descriptor words by keyword; empty slots get the literal
placeholder "PENDIENTE: redactar (regla §2.5)" — no prose is invented here.

`identidad.rol` is the readable rango name (resources/rangos/<faccion>.md
-> rangos[].nombre for the matching slug). `identidad.especialidad` keeps
the existing free-text value from the old `especialidad` field only when it
already reads as human text; when it's a catalog slug
(`especialidad-combate-lider` style) it is resolved via the matching
resources/especialidades/<faccion>/<slug>.md `nombre` field for that faccion.

Idempotent: a file already migrated (no legacy loose fields present, has
identidad/atributos/tags/apariencia-object shape) is left untouched.

    uv run python _tools/migrate_roster_hoja_v2.py            # dry-run
    uv run python _tools/migrate_roster_hoja_v2.py --apply    # write
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PERSONAJES = ROOT / "resources" / "personajes"
CATALOGOS = ROOT / "resources" / "catalogos"
RANGOS = ROOT / "resources" / "rangos"
ESPECIALIDADES = ROOT / "resources" / "especialidades"

PLACEHOLDER = "PENDIENTE: redactar (regla §2.5)"

ROSTRO_KW = [
    "cara", "ojo", "ojos", "piel", "pelo", "cabello", "ceja", "cejas",
    "mirada", "rostro", "tez", "barba", "barbudo", "barbado", "canoso",
    "canosa", "canas", "afeitado", "bigote", "lampino", "rasgos", "trenza",
]
FIGURA_KW = [
    "corpulento", "corpulenta", "fornido", "fornida", "enjuto", "enjuta",
    "obeso", "obesa", "alto", "alta", "fibrosa", "fibra", "nervudo",
    "hombros", "porte", "cuerpo", "constitucion", "constitución",
    "manos",
]


def _slug_to_tag(catalog_dir: Path, slug: str) -> str | None:
    """Look up a wikilinked catalog slug's canonical tag from its own
    frontmatter `tags` list (first entry with a `/` and matching last
    segment)."""
    path = catalog_dir / f"{slug}.md"
    if not path.exists():
        return None
    fm = _read_frontmatter(path)
    if not fm:
        return None
    for t in fm.get("tags", []) or []:
        if "/" in t and t.rsplit("/", 1)[-1] == slug:
            return t
    return None


def _find_in_any(root: Path, slug: str) -> str | None:
    for sub in root.rglob(f"{slug}.md"):
        fm = _read_frontmatter(sub)
        if not fm:
            continue
        for t in fm.get("tags", []) or []:
            if "/" in t and t.rsplit("/", 1)[-1] == slug:
                return t
    return None


def _read_frontmatter(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None


def _rango_nombre(faccion: str, rango_slug: str) -> str | None:
    path = RANGOS / f"{faccion}.md"
    fm = _read_frontmatter(path)
    if not fm:
        return None
    for r in fm.get("rangos", []) or []:
        if r.get("slug") == rango_slug:
            return r.get("nombre")
    return None


def _especialidad_nombre(faccion: str | None, esp_slug: str) -> str | None:
    if faccion:
        path = ESPECIALIDADES / faccion / f"{esp_slug}.md"
        if path.exists():
            fm = _read_frontmatter(path)
            if fm:
                return fm.get("nombre")
    for sub in ESPECIALIDADES.rglob(f"{esp_slug}.md"):
        fm = _read_frontmatter(sub)
        if fm:
            return fm.get("nombre")
    return None


def _unlink(items: list[str]) -> list[str]:
    """Strip `[[slug]]` wikilink wrapper down to the bare slug."""
    out = []
    for it in items:
        s = it.strip()
        if s.startswith("[[") and s.endswith("]]"):
            s = s[2:-2].split("|", 1)[0]
        out.append(s)
    return out


def _split_apariencia(items: list[str]) -> dict[str, str]:
    rostro, figura, presencia = [], [], []
    for raw in items:
        low = raw.lower()
        if any(kw in low for kw in ROSTRO_KW):
            rostro.append(raw)
        elif any(kw in low for kw in FIGURA_KW):
            figura.append(raw)
        else:
            presencia.append(raw)
    return {
        "rostro": ", ".join(rostro) if rostro else PLACEHOLDER,
        "figura": ", ".join(figura) if figura else PLACEHOLDER,
        "presencia": ", ".join(presencia) if presencia else PLACEHOLDER,
    }


LEGACY_KEYS = {
    "faccion", "subfaccion", "rango", "especialidad", "lealtad", "aspectos",
    "rasgos", "equipo", "estado", "barrio",
}


def is_legacy(fm: dict) -> bool:
    return bool(LEGACY_KEYS & fm.keys()) or isinstance(fm.get("apariencia"), list)


def migrate(fm: dict) -> dict:
    faccion = fm.get("faccion")
    tags: list[str] = []

    if faccion:
        tags.append(f"faccion/{faccion}")
    if fm.get("subfaccion"):
        tags.append(f"subfaccion/{fm['subfaccion']}")

    rango_slug = fm.get("rango")
    rol = None
    if rango_slug and faccion:
        tags.append(f"rango/{rango_slug}")
        rol = _rango_nombre(faccion, rango_slug)

    especialidad_slug = fm.get("especialidad")
    especialidad_txt = especialidad_slug
    if especialidad_slug:
        resolved_tag = _slug_to_tag(ESPECIALIDADES, especialidad_slug) or _find_in_any(
            ESPECIALIDADES, especialidad_slug
        )
        if resolved_tag:
            tags.append(resolved_tag)
        nombre = _especialidad_nombre(faccion, especialidad_slug)
        if nombre:
            especialidad_txt = nombre

    if fm.get("estado"):
        tags.append(f"estado/{fm['estado']}")
    if fm.get("barrio"):
        tags.append(f"ubicacion/{fm['barrio']}")

    for aspecto in _unlink(fm.get("aspectos") or []):
        resolved = _slug_to_tag(CATALOGOS / "aspecto", aspecto) or _find_in_any(CATALOGOS, aspecto)
        tags.append(resolved or f"aspecto/{aspecto}")

    for rasgo in _unlink(fm.get("rasgos") or []):
        resolved = _slug_to_tag(CATALOGOS / "rasgo", rasgo) or _find_in_any(CATALOGOS, rasgo)
        tags.append(resolved or f"rasgo/{rasgo}")

    for eq in _unlink(fm.get("equipo") or []):
        resolved = _slug_to_tag(CATALOGOS / "equipo", eq) or _find_in_any(CATALOGOS, eq)
        tags.append(resolved or f"equipo/{eq}")

    for lealtad in _unlink(fm.get("lealtad") or []):
        tags.append(f"lealtad/{lealtad}")

    tags.extend(fm.get("tags") or [])

    new_fm = dict(fm)
    for k in LEGACY_KEYS:
        new_fm.pop(k, None)

    new_fm["identidad"] = {
        "slug": fm.get("slug"),
        "nombre": fm.get("nombre"),
        "sobrenombre": None,
        "rol": rol,
        "especialidad": especialidad_txt,
        "genero": fm.get("genero"),
        "edad": fm.get("edad"),
    }
    new_fm.pop("genero", None)
    new_fm.pop("edad", None)
    new_fm.pop("nombre", None)

    new_fm["atributos"] = fm.get("atributos", {})

    old_apariencia = fm.get("apariencia")
    if isinstance(old_apariencia, list):
        new_fm["apariencia"] = _split_apariencia(old_apariencia)
    elif not isinstance(old_apariencia, dict):
        new_fm["apariencia"] = {
            "rostro": PLACEHOLDER,
            "figura": PLACEHOLDER,
            "presencia": PLACEHOLDER,
        }

    new_fm["tags"] = tags

    ordered_keys = [
        "slug", "aliases", "description", "identidad", "atributos", "tags",
    ]
    result = {k: new_fm[k] for k in ordered_keys if k in new_fm}
    for k, v in new_fm.items():
        if k not in result:
            result[k] = v
    result["apariencia"] = result.pop("apariencia")
    return result


def process(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2]

    if not is_legacy(fm):
        return None

    new_fm = migrate(fm)
    dumped = yaml.dump(
        new_fm, allow_unicode=True, sort_keys=False, default_flow_style=False,
        width=1000,
    )
    return f"---\n{dumped}---{body}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    args = ap.parse_args()

    changed: list[Path] = []
    for path in sorted(PERSONAJES.glob("*.md")):
        if path.name.startswith("_"):
            continue
        new_text = process(path)
        if new_text is not None:
            changed.append(path)
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    mode = "APPLIED" if args.apply else "DRY-RUN (no files written)"
    print(f"== migrate_roster_hoja_v2 -- {mode} ==")
    for p in changed:
        print(f"  {p.relative_to(ROOT)}")
    print(f"-- {len(changed)} file(s) migrated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
