#!/usr/bin/env python3
"""Coverage test for the hoja-personaje v2 migration (docs/hoja-personaje.md
§9). Validates every resources/personajes/*.md sheet against the new
contract: no legacy loose fields, identidad complete with rol+especialidad,
tags in valid notation, apariencia with the three keys non-empty (placeholder
counts as present).

    uv run --with pyyaml --with pytest pytest _tools/test_roster_schema.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
PERSONAJES = ROOT / "resources" / "personajes"

LEGACY_KEYS = {
    "faccion", "subfaccion", "rango", "especialidad", "lealtad", "aspectos",
    "rasgos", "equipo", "estado", "barrio",
}

REQUIRED_IDENTIDAD_KEYS = {
    "slug", "nombre", "sobrenombre", "rol", "especialidad", "genero", "edad",
}

TAG_RE = re.compile(r"^[a-z0-9_-]+(/[A-Za-z0-9_.-]+)*$")


def _sheet_paths() -> list[Path]:
    return sorted(
        p for p in PERSONAJES.glob("*.md") if not p.name.startswith("_")
    )


def _load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    assert len(parts) >= 3, f"{path}: missing frontmatter"
    fm = yaml.safe_load(parts[1]) or {}
    return fm


@pytest.mark.parametrize("path", _sheet_paths(), ids=lambda p: p.name)
def test_no_legacy_fields(path: Path) -> None:
    fm = _load(path)
    leaked = LEGACY_KEYS & fm.keys()
    assert not leaked, f"{path.name}: legacy fields still present: {leaked}"
    assert not isinstance(fm.get("apariencia"), list), (
        f"{path.name}: apariencia still a flat list"
    )


@pytest.mark.parametrize("path", _sheet_paths(), ids=lambda p: p.name)
def test_identidad_complete(path: Path) -> None:
    fm = _load(path)
    identidad = fm.get("identidad")
    assert isinstance(identidad, dict), f"{path.name}: missing identidad block"
    missing = REQUIRED_IDENTIDAD_KEYS - identidad.keys()
    assert not missing, f"{path.name}: identidad missing keys {missing}"
    # rol / especialidad are `str | null` per docs/hoja-personaje.md §1 (a
    # character legitimately without either, e.g. an unranked hooligan) --
    # the contract requires the *keys* present, not truthy values.


@pytest.mark.parametrize("path", _sheet_paths(), ids=lambda p: p.name)
def test_tags_valid_notation(path: Path) -> None:
    fm = _load(path)
    tags = fm.get("tags")
    assert isinstance(tags, list), f"{path.name}: tags is not a list"
    for tag in tags:
        assert isinstance(tag, str) and TAG_RE.match(tag), (
            f"{path.name}: invalid tag notation: {tag!r}"
        )


@pytest.mark.parametrize("path", _sheet_paths(), ids=lambda p: p.name)
def test_apariencia_three_keys(path: Path) -> None:
    fm = _load(path)
    apariencia = fm.get("apariencia")
    assert isinstance(apariencia, dict), f"{path.name}: apariencia is not an object"
    for key in ("rostro", "figura", "presencia"):
        val = apariencia.get(key)
        assert val, f"{path.name}: apariencia.{key} is empty"
