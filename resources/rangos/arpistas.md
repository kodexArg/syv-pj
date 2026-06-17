---
tags: ["catalogo/rangos", "rangos/arpistas", "faccion/arpistas"]
rangos:
- slug: contacto
  nombre: Contacto
  faccion: arpistas
  probabilidad: 50
  atributos_base:
    cuerpo: 3
    mente: 3
    alma: 2
  edad_min: 18
  edad_max: 50
  mando_default: agente_arpista
- slug: agente_arpista
  nombre: Agente
  faccion: arpistas
  probabilidad: 35
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 4
  edad_min: 22
  edad_max: 55
  mando_default: jefe_celula_arpista
- slug: jefe_celula_arpista
  nombre: Célula
  faccion: arpistas
  probabilidad: 15
  atributos_base:
    cuerpo: 4
    mente: 4
    alma: 6
  edad_min: 28
  edad_max: 60
  mando_default: null
  mando: celula_arpista
---

Escalera jerárquica de **Arpistas** — [[arpistas]].
