---
tags: ["catalogo/rangos", "rangos/iglesia", "faccion/iglesia"]
rangos:
- slug: lego
  nombre: Lego
  faccion: iglesia
  probabilidad: 24
  atributos_base:
    cuerpo: 2
    mente: 2
    alma: 2
  edad_min: 16
  edad_max: 60
  mando_default: novicio
- slug: novicio
  nombre: Novicio
  faccion: iglesia
  probabilidad: 22
  atributos_base:
    cuerpo: 2
    mente: 3
    alma: 3
  edad_min: 17
  edad_max: 30
  mando_default: hermano
- slug: hermano
  nombre: Hermano
  faccion: iglesia
  probabilidad: 20
  atributos_base:
    cuerpo: 3
    mente: 3
    alma: 3
  edad_min: 20
  edad_max: 55
  mando_default: sacerdote
- slug: sacerdote
  nombre: Sacerdote
  faccion: iglesia
  probabilidad: 15
  atributos_base:
    cuerpo: 3
    mente: 4
    alma: 6
  edad_min: 28
  edad_max: 65
  mando_default: canonigo
  mando: parroquia
- slug: canonigo
  nombre: Canónigo
  faccion: iglesia
  probabilidad: 10
  atributos_base:
    cuerpo: 3
    mente: 4
    alma: 6
  edad_min: 35
  edad_max: 70
  mando_default: obispo
  mando: dicasterio
- slug: obispo
  nombre: Obispo
  faccion: iglesia
  probabilidad: 6
  atributos_base:
    cuerpo: 3
    mente: 5
    alma: 7
  edad_min: 45
  edad_max: 75
  mando_default: cardenal
  mando: diocesis
- slug: cardenal
  nombre: Cardenal
  faccion: iglesia
  probabilidad: 3
  atributos_base:
    cuerpo: 2
    mente: 5
    alma: 7
  edad_min: 50
  edad_max: 80
  mando_default: null
  mando: curia
---

Escalera jerárquica de **Iglesia Católica** — [[iglesia]].
