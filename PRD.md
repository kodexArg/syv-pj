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
> **El producto es documentación, no una aplicación.** `syv-pj` define la entidad mínima de *Subordinación y Valor* (SyV) — el personaje — como módulo autónomo, fiel al universo, agnóstico al uso. El resultado es un conjunto de contratos, catálogos y reglas en Markdown; la implementación concreta (tecnología, entorno de ejecución, persistencia) corre por cuenta de quien consuma este módulo.

---

## 1. Propósito

`syv-pj` es el módulo de la **entidad mínima de SyV: el personaje**. Documenta su esquema, su sistema de clasificación por tags, sus reglas de mutabilidad y generación, y los contratos de API que permiten operar sobre él.

El módulo es:

- **Independiente** — no referencia ni depende de ningún otro repo. Es la evolución limpia y autónoma de bosquejos previos.
- **Fiel a SyV** — usa los términos, la nomenclatura y captura el espíritu del universo: Anatema Mecánico, voz/gesto/banderín, milicias vs. ejército regular, voseo sobrio.
- **Agnóstico al uso, no al universo** — un mismo personaje homogeneizado sirve para diégesis (tags y enlaces entre notas, narrativa), juego de estrategia (estadísticas numéricas para combate), juego de rol, y generación de fichas visuales. `syv-pj` clasifica, almacena y entrega; el consumidor decide el uso.

### 1.1. Contexto de universo

El personaje existe dentro de *Subordinación y Valor*:

- **Año 2178.** La guerra arrastra dieciocho años. El frente es la **Zanja de Alsina**, una franja arrasada que cruza la Patagonia. Niebla helada, comunicaciones rotas, ningún bando logra ruptura.
- **Confederación Argentina.** Estado centralizado con base en Ciudad Dársena. Escuadras regulares de once soldados, militarizadas, lideradas por un Sargento, cadena de mando formal. Suelen estar acompañados por miembros del Clero, usualmente la S.I.A. Sagrada Inquisición Argentina y/o del cuerpo de Capellanes. Menos común pueden asistir ingenieros o técnicos especialistas.
- **Ejército Rojo.** Conglomerado de milicias obreras y portuarias nacidas de la revolución fabril de Bahía Blanca. Sin uniformes estandarizados; cada célula obedece a un Camarada o Puntero, y las particularidades, armamento y tamaño varían enormemente de acuerdo a la facción interna que la lidere,.
- **Anatema Mecánico.** Prohibición universal de tecnología avanzada. La coordinación es voz, gesto y banderín. No hay drones, no hay computación en campo, no hay armamento inteligente.

---

## 2. Principios de diseño

- **Documentación como contrato.** Este módulo define forma y alcance. La implementación es responsabilidad de quien lo consuma.
- **Principio abierto/cerrado.** El esquema extiende verticalmente sin romper: nuevos tags, nuevos tipos de hito, nuevas categorías, nuevas facciones — sin migraciones, sin rupturas de compatibilidad.
- **Tags como modelo de primera clase.** Todo lo que es discreto y no es identidad, atributo, prosa o auditoría es tag —incluidos los vínculos personales (aliados, némesis, lealtades). La frontera está fijada en [hoja-personaje](docs/hoja-personaje.md) y [sistema-tags](docs/sistema-tags.md).
- **Estadísticas determinísticas por rango; identidad sorteada.** En creación, los atributos base se derivan de tablas fijas por rango. Cero azar en estadísticas. Nombre, género, edad, rasgos, destrezas, rasgos de clase, ventajas, equipo e historia sí se sortean.
- **Memoria viva como naturaleza del canonizado.** Un canonizado existe en el tiempo: nace, pelea, cambia. La ficha vigente no es la original. Las mutaciones ocurren vía hitos en `historial[]`.
- **Reproducibilidad por semilla para efímeros.** `(semilla, faccion, rango)` produce el mismo personaje efímero. Los canonizados pierden esta propiedad tras el primer hito.
- **LLM solo para prosa, solo una vez.** El modelo generativo escribe `historia` durante la creación; al canonizar, se congela.
- **Agnosis al renderizador.** El esquema describe qué tiene un personaje, no cómo se muestra.
- **Contratos sobre convenciones.** Los rasgos, ventajas y destrezas son contratos: un nombre legible que entrega un paquete declarado de efectos, modificadores y habilitaciones.

---

## 3. Mapa de artefactos

| Archivo | Propósito |
|---|---|
| [PRD.md]() | Este documento. Visión, principios y mapa. |
| [MODEL.md](MODEL.md) | Contrato de persistencia: entidades, tipos, mutabilidad. |
| [API.md](API.md) | Contrato HTTP: operaciones, cargas, catálogos dinámicos. |
| [README.md](README.md) | Puerta de entrada al repo. |
| [AGENTS.md](AGENTS.md) | Política editorial y convenciones para colaboradores y agentes. |
| [docs/hoja-personaje.md](docs/hoja-personaje.md) | Esquema del personaje campo por campo. Núcleo del módulo. |
| [docs/sistema-tags.md](docs/sistema-tags.md) | Sistema de tags: notación, categorías, catálogo, extensibilidad. |
| [docs/contratos.md](docs/contratos.md) | Contratos de rasgos, ventajas, destrezas y efectos. |
| [docs/atributos.md](docs/atributos.md) | Vocabulario canónico de atributos y estadísticas calculadas. |
| [docs/generacion-procedural.md](docs/generacion-procedural.md) | Flujo obligatorio de creación: fases, sorteos, tabla determinística. |
| [docs/diegesis.md](docs/diegesis.md) | Puntero al universo SyV: el lore (facciones, lugares, nombres) vive en `syv-docs`. |
| [docs/casos-de-uso.md](docs/casos-de-uso.md) | Catálogo de casos de uso y su mapeo a operaciones. |

> [!note] Enlaces
> Los enlaces de esta tabla apuntan a los nombres canónicos fijados en [SPINE.md](SPINE.md). Otros archivos del inventario se escriben en paralelo y pueden no existir todavía en el momento de leer este PRD — eso es esperado.

---

## 4. Alcance

### Cubierto por este módulo

- Esquema completo de la hoja de personaje.
- Sistema de tags categorizado, con catálogo curado y extensible.
- Vocabulario canónico de atributos y estadísticas calculadas.
- Contratos de rasgos, ventajas, destrezas y efectos.
- Flujo de generación procedural (fases 1–4).
- Catálogo abierto de facciones jugables.
- Rangos operativos canon por facción.
- Diégesis: puntero al universo — el contexto (facciones, lugares, lore) vive en `syv-docs`, no acá.
- Contrato de API HTTP ([API.md](API.md)).
- Contrato de persistencia ([MODEL.md](MODEL.md)).
- Catálogos `/meta/*` dinámicos por categoría de tag.

### Pendiente

- Datos de ejemplo (personajes maqueta canon).

### Fuera de este módulo

- El alcance de este módulo es **un único personaje**. Las agrupaciones de personajes (grupos, escuadras) y su simulación táctica pertenecen a otra herramienta del ecosistema; acá, a lo sumo, un personaje puede portar un tag opcional de pertenencia sin que el módulo lo defina.
- Implementación de la API en cualquier lenguaje, framework o pila tecnológica.
- Persistencia concreta (motor de base, hosting, despliegue).
- Autenticación, autorización, limitación de peticiones.
- Interfaz gráfica, interfaz de línea de comandos de usuario final, dashboards.
- Las facciones secundarias del lore (Pueblos del Pantano, Salvajes, Poseídos).
- Personajes civiles sin especialidad ni afiliación militar.
- Edición arbitraria de canonizados fuera del mecanismo de hitos.
- Reverso de hitos.
- Versionado de la prosa congelada.
