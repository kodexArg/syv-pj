---
title: syv-pj
tags:
  - syv/pj
aliases:
  - syv-pj
---

# syv-pj

`syv-pj` es el módulo de la entidad mínima de *Subordinación y Valor* (SyV): el personaje. No es una aplicación — es un conjunto de contratos, catálogos y reglas en Markdown que define qué es un personaje en este universo, cómo se clasifica, cómo muta en el tiempo y cómo se opera sobre él a través de una API. El módulo es autónomo: no depende de ningún otro repo y sirve de base para cualquier uso — diégesis y narrativa, juego de estrategia, juego de rol, generación de fichas visuales — sin favorecer ninguno.

El universo en que habita este personaje es *Subordinación y Valor*: año 2178, la guerra arrastra dieciocho años en la Zanja de Alsina, la Confederación Argentina y el Ejército Rojo se enfrentan bajo el Anatema Mecánico — sin drones, sin computación en campo, con voz, gesto y banderín. El módulo es fiel a ese universo: usa su terminología, sus facciones, sus rangos, su espíritu. El consumidor decide el uso; `syv-pj` clasifica, almacena y entrega.

---

## Cómo navegar esta documentación

| Querés saber... | Empezá acá |
|---|---|
| Qué es este módulo, sus principios y alcance | [[PRD\|PRD.md]] |
| Qué campos tiene un personaje y cómo mutan | [[hoja-personaje\|docs/hoja-personaje.md]] |
| Cómo funciona el sistema de tags | [[sistema-tags\|docs/sistema-tags.md]] |
| Qué son los contratos (rasgos, ventajas, destrezas) | [[habilidades\|docs/perks-y-traits.md]] |
| Qué son los atributos y las estadísticas calculadas | [[atributos-y-stats\|docs/atributos-y-stats.md]] |
| Cómo se genera un personaje proceduralmente | [[generacion-procedural\|docs/generacion-procedural.md]] |
| Cómo extiender el esquema sin romper nada | [[open-close\|docs/open-close.md]] |
| Cómo funcionan los grupos y escuadras | [[grupos\|docs/grupos.md]] |
| Cómo conectar el personaje al vault de diégesis | [[diegesis-y-obsidian\|docs/diegesis-y-obsidian.md]] |
| Casos de uso concretos | [[casos-de-uso\|docs/casos-de-uso.md]] |
| Entidades, tipos y reglas de persistencia | [[MODEL\|MODEL.md]] |
| Operaciones, cargas y contratos HTTP | [[API\|API.md]] |
| Convenciones editoriales para colaboradores | [[AGENTS\|AGENTS.md]] |

---

## Índice de documentos

### Raíz

- [[PRD|PRD.md]] — Visión, principios de diseño, mapa de artefactos y alcance.
- [[MODEL|MODEL.md]] — Contrato de persistencia: entidades, tipos, mutabilidad, derivados, invariantes.
- [[API|API.md]] — Contrato HTTP: operaciones, cargas, catálogos dinámicos.
- [[AGENTS|AGENTS.md]] — Política editorial, convenciones de identificadores, idioma, colaboración.

### docs/

- [[hoja-personaje|docs/hoja-personaje.md]] — Esquema del personaje campo por campo. Núcleo del módulo.
- [[sistema-tags|docs/sistema-tags.md]] — Sistema de tags: notación punto, multiset, catálogo, extensibilidad.
- [[habilidades|docs/perks-y-traits.md]] — Contratos de rasgos, ventajas, destrezas y efectos.
- [[atributos-y-stats|docs/atributos-y-stats.md]] — Vocabulario canónico de atributos base y estadísticas calculadas.
- [[generacion-procedural|docs/generacion-procedural.md]] — Flujo de creación procedural: cuatro fases, sorteos, tabla determinística.
- [[open-close|docs/open-close.md]] — Política de extensibilidad: cómo agregar sin romper.
- [[grupos|docs/grupos.md]] — Esquema de grupos y escuadras; campos derivados tácticos.
- [[diegesis-y-obsidian|docs/diegesis-y-obsidian.md]] — Convención de linkeo para integrar el personaje al vault Obsidian de SyV.
- [[casos-de-uso|docs/casos-de-uso.md]] — Catálogo de casos de uso con mapeo a operaciones.
