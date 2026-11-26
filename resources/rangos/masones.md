---
tags: ["catalogo/rangos", "rangos/masones", "faccion/masones"]
rangos:
- slug: aprendiz_mason
  nombre: Aprendiz
  faccion: masones
  probabilidad: 50
  atributos_base:
    cuerpo: 2
    mente: 3
    alma: 3
  edad_min: 22
  edad_max: 60
  mando_default: companero_mason
- slug: companero_mason
  nombre: Compañero
  faccion: masones
  probabilidad: 32
  atributos_base:
    cuerpo: 2
    mente: 3
    alma: 4
  edad_min: 28
  edad_max: 65
  mando_default: maestro_mason
- slug: maestro_mason
  nombre: Maestro
  faccion: masones
  probabilidad: 18
  atributos_base:
    cuerpo: 2
    mente: 4
    alma: 6
  edad_min: 35
  edad_max: 75
  mando_default: null
  mando: logia
---

Escalera jerárquica de **Masones** — [masones]().
