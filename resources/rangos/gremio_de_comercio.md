---
tags: ["catalogo/rangos", "rangos/gremio_de_comercio", "faccion/gremio_de_comercio"]
rangos:
- slug: aprendiz_gremio
  nombre: Aprendiz
  faccion: gremio_de_comercio
  probabilidad: 34
  atributos_base:
    cuerpo: 3
    mente: 3
    alma: 2
  edad_min: 15
  edad_max: 25
  mando_default: mercader
- slug: mercader
  nombre: Mercader
  faccion: gremio_de_comercio
  probabilidad: 38
  atributos_base:
    cuerpo: 3
    mente: 4
    alma: 3
  edad_min: 20
  edad_max: 55
  mando_default: socio
- slug: socio
  nombre: Socio
  faccion: gremio_de_comercio
  probabilidad: 20
  atributos_base:
    cuerpo: 2
    mente: 4
    alma: 5
  edad_min: 30
  edad_max: 65
  mando_default: magnate
  mando: red_comercial
- slug: magnate
  nombre: Magnate
  faccion: gremio_de_comercio
  probabilidad: 8
  atributos_base:
    cuerpo: 2
    mente: 5
    alma: 6
  edad_min: 40
  edad_max: 75
  mando_default: null
  mando: consejo_gremial
---

Escalera jerárquica de **Gremio de Comercio** — [[gremio-de-comercio]].
