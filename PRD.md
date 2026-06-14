---
title: PRD — syv-pj
tags:
  - syv/pj/prd
aliases:
  - PRD
  - Requerimientos
---

# PRD — syv-pj

> [!info] Visión General
> **El producto es documentación, no una aplicación.** `syv-pj` define la entidad mínima de *Subordinación y Valor* (SyV) — el personaje — como módulo autónomo, fiel al universo, agnóstico al uso. El resultado es un conjunto de contratos, catálogos y reglas en Markdown; la implementación concreta (stack, runtime, persistencia) corre por cuenta de quien consuma este módulo.

---

## 1. Propósito

`syv-pj` es el módulo de la **entidad mínima de SyV: el personaje**. Documenta su schema, su sistema de clasificación por tags, sus reglas de mutabilidad y generación, y los contratos de API que permiten operar sobre él.

El módulo es:

- **Independiente** — no referencia ni depende de ningún otro repo. Es la evolución limpia y autónoma de bosquejos previos.
- **Fiel a SyV** — usa los términos, la nomenclatura y captura el espíritu del universo: Anatema Mecánico, voz/gesto/banderín, milicias vs. ejército regular, voseo sobrio.
- **Agnóstico al uso, no al universo** — un mismo personaje homogeneizado sirve para diégesis (Obsidian, wikilinks, narrativa), juego de estrategia (stats numéricas para combate), juego de rol, y generación de fichas visuales. `syv-pj` clasifica, almacena y entrega; el consumidor decide el uso.

### 1.1. Contexto de universo

El personaje existe dentro de *Subordinación y Valor*:

- **Año 2178.** La guerra arrastra dieciocho años. El frente es la **Zanja de Alsina**, una franja arrasada que cruza la Patagonia. Niebla helada, comunicaciones rotas, ningún bando logra ruptura.
- **Confederación Argentina.** Estado centralizado con base en Ciudad Dársena. Escuadras regulares de once soldados, militarizadas, lideradas por un Sargento, cadena de mando formal. Suelen estar acompañados por miembros del Clero, usualmente la S.I.A. Sagrada Inquisición Argentina y/o del cuerpo de Capellanes. Menos común pueden asistir ingenieros o técnicos especialistas.
- **Ejército Rojo.** Conglomerado de milicias obreras y portuarias nacidas de la revolución fabril de Bahía Blanca. Sin uniformes estandarizados; cada célula obedece a un Camarada o Puntero, y las particularidades, armamento y tamaño varían enormemente de acuerdo a la facción interna que la lidere,.
- **Anatema Mecánico.** Prohibición universal de tecnología avanzada. La coordinación es voz, gesto y banderín. No hay drones, no hay computación en campo, no hay armamento inteligente.

---

## 2. Principios de diseño

- **Documentación como contrato.** Este módulo define forma y alcance. La implementación es responsabilidad de quien lo consuma.
- **Principio open/close.** El schema extiende verticalmente sin romper: nuevos tags, nuevos tipos de hito, nuevas categorías, nuevas facciones — sin migraciones, sin breaking changes.
- **Tags como modelo de primera clase.** Todo lo que es discreto y no es identidad, atributo, prosa, auditoría o vínculo-personal-con-prosa es tag. La frontera está fijada en [[hoja-personaje]] y [[sistema-tags]].
- **Stats determinísticos por rango; identidad sorteada.** En creación, los atributos base se derivan de tablas fijas por rol/rango. Cero azar en stats. Nombre, género, edad, rasgos, skills, traits, perks, equipo e historia sí se sortean.
- **Memoria viva como naturaleza del canonizado.** Un canonizado existe en el tiempo: nace, pelea, cambia. La ficha vigente no es la original. Las mutaciones ocurren vía hitos en `historial[]`.
- **Reproducibilidad por seed para efímeros.** `(seed, faccion, rango)` produce el mismo personaje efímero. Los canonizados pierden esta propiedad tras el primer hito.
- **LLM solo para prosa, solo una vez.** El modelo generativo escribe `historia` durante la creación; al canonizar, se congela.
- **Agnosis al renderer.** El schema describe qué tiene un personaje, no cómo se muestra.
- **Contratos sobre convenciones.** Los traits, perks y skills son contratos: un nombre legible que entrega un paquete declarado de efectos, modificadores y habilitaciones.

---

## 3. Mapa de artefactos

| Archivo | Propósito |
|---|---|
| [[PRD\|PRD.md]] | Este documento. Visión, principios y mapa. |
| [[MODEL\|MODEL.md]] | Contrato de persistencia: entidades, tipos, mutabilidad. |
| [[API\|API.md]] | Contrato HTTP: endpoints, payloads, catálogos dinámicos. |
| [[README\|README.md]] | Puerta de entrada al repo. |
| [[AGENTS\|AGENTS.md]] | Política editorial y convenciones para colaboradores y agentes. |
| [[hoja-personaje\|docs/hoja-personaje.md]] | Schema del personaje campo por campo. Núcleo del módulo. |
| [[sistema-tags\|docs/sistema-tags.md]] | Sistema de tags: notación, categorías, catálogo, extensibilidad. |
| [[habilidades\|docs/perks-y-traits.md]] | Contratos de traits, perks, skills y efectos. |
| [[atributos-y-stats\|docs/atributos-y-stats.md]] | Vocabulario canónico de atributos y stats calculadas. |
| [[generacion-procedural\|docs/generacion-procedural.md]] | Flujo obligatorio de creación: fases, sorteos, tabla determinística. |
| [[open-close\|docs/open-close.md]] | Política de extensibilidad: cuándo extender, cómo, sin breaking changes. |
| [[grupos\|docs/grupos.md]] | Schema de grupos y escuadras; agrupaciones tácticas. |
| [[diegesis-y-obsidian\|docs/diegesis-y-obsidian.md]] | Convención de linkeo Obsidian para la diégesis de SyV. |
| [[casos-de-uso\|docs/casos-de-uso.md]] | Catálogo de casos de uso y su mapping a endpoints. |

> [!note] Wikilinks
> Los wikilinks de esta tabla apuntan a los nombres canónicos fijados en [[SPINE|SPINE.md]]. Otros archivos del inventario se escriben en paralelo y pueden no existir todavía en el momento de leer este PRD — eso es esperado.

---

## 4. Alcance

### Cubierto por este módulo

- Schema completo de la hoja de personaje.
- Sistema de tags categorizado, con catálogo curado y extensible.
- Vocabulario canónico de atributos y stats calculadas.
- Contratos de traits, perks, skills y efectos.
- Flujo de generación procedural (fases 1–4).
- Dos facciones jugables: `confederacion_argentina` y `ejercito_rojo`.
- Rangos operativos canon de ambas facciones.
- Diégesis: convención de linkeo Obsidian para integrar el personaje al vault de SyV.
- Grupos y escuadras como agrupación táctica.
- Contrato de API HTTP ([[API|API.md]]).
- Contrato de persistencia ([[MODEL|MODEL.md]]).
- Catálogos `/meta/*` dinámicos por categoría de tag.

### Pendiente

- Motor de batalla squad vs squad (reglas completas de combate).
- Fixtures de ejemplo (personajes mock de las dos escuadras canon).

### Fuera de este módulo

- Implementación de la API en cualquier lenguaje, framework o stack.
- Persistencia concreta (motor de base, hosting, despliegue).
- Autenticación, autorización, rate limiting.
- UI, CLI de usuario final, dashboards.
- Las facciones secundarias del lore (Pueblos del Pantano, Salvajes, Poseídos).
- Personajes civiles fuera del rol `ciudadano`.
- Edición arbitraria de canonizados fuera del mecanismo de hitos.
- Reverso de hitos.
- Versionado de la prosa congelada.
