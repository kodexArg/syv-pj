---
title: "Obsidian — cómo se escribe la documentación de syv-pj"
tags:
  - syv/pj/obsidian
aliases:
  - obsidian
  - Obsidian Flavored Markdown
  - OFM
---

# Obsidian — cómo se escribe la documentación

> [!info] Una sola puerta
> Toda la documentación de `syv-pj` vive en un **vault de Obsidian** y se escribe en **Obsidian Flavored Markdown (OFM)**. Este doc es la **única** referencia de "cómo usar Obsidian acá"; el resto de los archivos no la repiten — la enlazan.

---

## Skills — la fuente de la sintaxis

- **`/obsidian-markdown`** — invocar **siempre, antes** de escribir un `.md` del vault. Define la sintaxis OFM: wikilinks, embeds, callouts, propiedades de frontmatter, tags, resaltado.
- **`/obsidian-bases`** — solo para archivos `.base` (vistas tipo tabla/tarjeta de Obsidian Bases: filtros, fórmulas, vistas). No hay ninguno todavía; invocarlo si se agrega uno.

No memorizar la sintaxis de memoria: invocar el skill y seguirlo.

---

## Convenciones mínimas del proyecto

Lo único que hay que tener presente al redactar un doc de `syv-pj`:

- **Frontmatter** con `title`, `tags`, `aliases`. Los **nombres de campo son contrato** — en inglés, minúscula, nunca se traducen (ver [[AGENTS|AGENTS.md]]).
- **Wikilinks entre docs**: `[[archivo|alias]]`. En propiedades YAML que son listas de vínculos, el wikilink va **entre comillas** (`"[[...]]"`).
- **Callouts**: `> [!info]` / `> [!tip]` / `> [!warning]` / `> [!note]`.
- **Resaltado** `==así==` para términos que fijan contrato.
- **Tags** = taxonomía bajo `syv/<…>`, no relaciones; las relaciones se expresan con wikilinks.

---

## El universo y el contexto

El lore de *Subordinación y Valor* (facciones, lugares, personajes canónicos) **no vive acá**: vive en el vault `syv-docs`. El puntero a esa fuente es [[diegesis|docs/diegesis.md]].
