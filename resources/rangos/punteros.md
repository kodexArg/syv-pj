---
tags: ["catalogo/rangos", "rangos/punteros", "faccion/punteros"]
rangos:
- slug: peon
  nombre: Peón
  faccion: punteros
  probabilidad: 55
  atributos_base:
    cuerpo: 3
    mente: 3
    alma: 2
  edad_min: 16
  edad_max: 50
  mando_default: soldado_de_clan
- slug: soldado_de_clan
  nombre: Soldado de Clan
  faccion: punteros
  probabilidad: 30
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 4
  edad_min: 18
  edad_max: 45
  mando_default: puntero
  mando: banda
- slug: puntero
  nombre: Puntero
  faccion: punteros
  probabilidad: 15
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 6
  edad_min: 25
  edad_max: 60
  mando_default: null
  mando: turf
---

Escalera jerárquica de **Punteros** — [[barrios-del-muro]].
