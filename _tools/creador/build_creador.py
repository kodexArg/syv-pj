#!/usr/bin/env python3
"""Arma el creador de personajes: un HTML autónomo con los catálogos de resources/.

Lee facciones, subfacciones, rangos, especialidades, catálogos (aspecto, rasgo,
habilidad, entrenamiento, equipo), reglas y depósitos de nombres; los incrusta
como JSON en `plantilla.html` y escribe `creador-personajes.html` al lado.

Determinista: misma entrada, misma salida. Solo lee `resources/`; no lo modifica.

Uso:
    python3 _tools/creador/build_creador.py

La plantilla está escrita para publicarse como artefacto de claude.ai (sin
<!doctype>/<head>, que agrega el publicador). Para abrirla como archivo local,
este script la envuelve en un documento completo.
"""
import glob
import json
import os
import re
import sys

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
RES = os.path.join(RAIZ, "resources")
PLANTILLA = os.path.join(AQUI, "plantilla.html")
SALIDA = os.path.join(AQUI, "creador-personajes.html")


def frontmatter(path):
    texto = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", texto, re.S)
    if not m:
        return {}, texto
    return yaml.safe_load(m.group(1)) or {}, m.group(2).strip()


def primer_parrafo(cuerpo):
    for linea in cuerpo.split("\n"):
        linea = linea.strip()
        if not linea or linea.startswith(("[", "#", ">")):
            continue
        linea = re.sub(r"\[\[([^|\]]+\|)?([^\]]+)\]\]", r"\2", linea)  # wikilink
        return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", linea)  # enlace Markdown
    return ""


def archivos(carpeta):
    return sorted(
        f for f in glob.glob(os.path.join(RES, carpeta, "*.md"))
        if not os.path.basename(f).startswith("_")
    )


def campos(path, claves):
    fm, _ = frontmatter(path)
    return {k: v for k, v in fm.items() if k in claves}


def catalogo(nombre, claves):
    return [campos(f, claves) for f in archivos(os.path.join("catalogos", nombre))]


def nombres(archivo):
    out = []
    for linea in open(os.path.join(RES, "nombres", archivo), encoding="utf-8"):
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        nombre, _, apodo = linea.partition("|")
        out.append([nombre.strip(), apodo.strip() or None])
    return out


def extraer():
    d = {}
    d["facciones"] = [campos(f, ("slug", "nombre", "descripcion", "probabilidad")) for f in archivos("facciones")]
    d["subfacciones"] = [
        campos(f, ("slug", "nombre", "descripcion", "probabilidad", "faccion_padre")) for f in archivos("subfacciones")
    ]
    d["rangos"] = {}
    for f in archivos("rangos"):
        fm, _ = frontmatter(f)
        d["rangos"][os.path.basename(f)[:-3]] = [
            {k: r.get(k) for k in ("slug", "nombre", "probabilidad", "atributos_base", "edad_min", "edad_max", "mando")
             if r.get(k) is not None}
            for r in fm.get("rangos", [])
        ]
    d["especialidades"] = {}
    for carpeta in sorted(glob.glob(os.path.join(RES, "especialidades", "*", ""))):
        lista = []
        for f in sorted(glob.glob(os.path.join(carpeta, "*.md"))):
            fm, cuerpo = frontmatter(f)
            slug = None if fm["slug"] == "sin_especialidad" else fm["slug"]
            lista.append({"slug": slug, "nombre": fm["nombre"], "probabilidad": fm.get("probabilidad", 1),
                          "descripcion": primer_parrafo(cuerpo)})
        d["especialidades"][os.path.basename(os.path.normpath(carpeta))] = lista
    d["aspectos"] = catalogo("aspecto", ("slug", "nombre", "descripcion", "origen", "peso_narrativo", "efecto",
                                          "excluye", "requires", "requiere_edad_min", "sesgo_faccion"))
    d["rasgos"] = catalogo("rasgo", ("slug", "nombre", "descripcion", "peso_narrativo"))
    d["habilidades"] = catalogo("habilidad", ("slug", "nombre", "descripcion", "atributo_dominante"))
    d["entrenamientos"] = catalogo("entrenamiento", ("slug", "nombre", "descripcion", "peso_narrativo"))
    d["equipo"] = catalogo("equipo", ("slug", "nombre", "descripcion", "subcategoria", "peso", "peso_sorteo",
                                      "sesgo_faccion", "sesgo_especialidad", "sesgo_rango", "alcance",
                                      "tipo_accion", "requires"))
    d["reglas"] = {}
    for f in archivos("reglas"):
        fm, _ = frontmatter(f)
        d["reglas"][fm["clave"]] = fm["valor"]
    d["nombres"] = {
        "m": nombres("varones.txt"),
        "f": nombres("mujeres.txt"),
        "apellidos": [l.strip() for l in open(os.path.join(RES, "nombres", "apellidos.txt"), encoding="utf-8")
                      if l.strip() and not l.startswith("#")],
    }
    return d


def main():
    datos = extraer()
    plantilla = open(PLANTILLA, encoding="utf-8").read()
    if "__DATA__" not in plantilla:
        sys.exit("plantilla.html no tiene el marcador __DATA__")
    js = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    pagina = plantilla.replace("__DATA__", js)
    # Lo que va antes de </style> es <title>, metas y estilos: va al <head>.
    corte = pagina.index("</style>") + len("</style>")
    doc = (
        '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n"
        + pagina[:corte] + "\n</head>\n<body>" + pagina[corte:] + "</body>\n</html>\n"
    )
    open(SALIDA, "w", encoding="utf-8").write(doc)
    print(f"{os.path.relpath(SALIDA, RAIZ)}: {len(doc) // 1024} KB · "
          + ", ".join(f"{k} {len(v)}" for k, v in datos.items()))


if __name__ == "__main__":
    main()
