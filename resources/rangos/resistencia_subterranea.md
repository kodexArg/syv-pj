---
tags: ["rangos", "rangos/resistencia_subterranea", "faccion/resistencia_subterranea"]
rangos:
- slug: simpatizante
  nombre: Simpatizante
  faccion: resistencia_subterranea
  rol_cultural: Simpatizante
  probabilidad: 45
  atributos_base:
    cuerpo: 3
    mente: 3
    alma: 2
  edad_min: 16
  edad_max: 50
  mando_default: militante_resistencia
- slug: militante_resistencia
  nombre: Militante
  faccion: resistencia_subterranea
  rol_cultural: Militante
  probabilidad: 40
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 4
  edad_min: 18
  edad_max: 45
  mando_default: cabecilla
- slug: cabecilla
  nombre: Cabecilla
  faccion: resistencia_subterranea
  rol_cultural: Cabecilla
  probabilidad: 15
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 6
  edad_min: 24
  edad_max: 55
  mando_default: null
  mando: celula_anarquista
---

Escalera jerárquica de **Resistencia Subterránea** — [[resistencia-subterranea]].
