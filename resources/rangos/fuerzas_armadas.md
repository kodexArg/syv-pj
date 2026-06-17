---
tags: ["catalogo/rangos", "rangos/fuerzas_armadas", "faccion/fuerzas_armadas"]
rangos:
- slug: recluta
  nombre: Recluta
  faccion: fuerzas_armadas
  probabilidad: 30
  atributos_base:
    cuerpo: 3
    mente: 2
    alma: 2
  edad_min: 18
  edad_max: 24
  mando_default: soldado_linea
- slug: soldado_linea
  nombre: Soldado
  faccion: fuerzas_armadas
  probabilidad: 26
  atributos_base:
    cuerpo: 4
    mente: 3
    alma: 2
  edad_min: 19
  edad_max: 30
  mando_default: cabo
- slug: cabo
  nombre: Cabo
  faccion: fuerzas_armadas
  probabilidad: 18
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 4
  edad_min: 22
  edad_max: 35
  mando_default: sargento
  mando: escuadra
- slug: sargento
  nombre: Sargento
  faccion: fuerzas_armadas
  probabilidad: 14
  atributos_base:
    cuerpo: 5
    mente: 4
    alma: 5
  edad_min: 26
  edad_max: 45
  mando_default: teniente
  mando: peloton
- slug: teniente
  nombre: Teniente
  faccion: fuerzas_armadas
  probabilidad: 8
  atributos_base:
    cuerpo: 4
    mente: 5
    alma: 5
  edad_min: 28
  edad_max: 50
  mando_default: coronel
  mando: compania
- slug: coronel
  nombre: Coronel
  faccion: fuerzas_armadas
  probabilidad: 4
  atributos_base:
    cuerpo: 4
    mente: 5
    alma: 6
  edad_min: 38
  edad_max: 60
  mando_default: null
  mando: regimiento
---

Escalera jerárquica de **Fuerzas Armadas** — [[fuerzas-armadas]].
