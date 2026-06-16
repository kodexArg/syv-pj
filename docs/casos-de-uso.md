---
title: Casos de uso — Un personaje, muchos consumidores
tags:
  - syv/pj/casos-de-uso
  - syv/pj/consumidores
aliases:
  - casos-de-uso
  - UCs
  - Catálogo de UCs
---

# Casos de uso — Responde a la pregunta ¿Para qué sirve syv-pj, el creador de personajes?

> [!info] El eje de homogeneización
> `syv-pj` entrega un único personaje bien definido consumible por cualquier otro sistema, como creadores de personaje o juegos de estrategia.

---

## Referencias de íconos

> [!note] Cómo leer las tablas
> Columna **🎭** = quién pide. El primer ícono de **Quiere** = la acción; **Para** es el propósito, en prosa.

**🎭 Actores**

| | | | |
|---|---|---|---|
| 🎰 Generador de personajes | 🪶 Autor narrativo | 👓 Lector del vault | 🛡️ Curador de canon |
| ⚔️ Motor de batalla | 🎲 Árbitro | 🎮 Jugador | 🎨 Proyección visual |
| 🔌 Cualquier cliente | 🧪 Control de calidad | | |

**Acciones**

| | | | |
|---|---|---|---|
| 👁️ consultar · ver · leer | 📥 pedir | 🔍 filtrar | 🧭 navegar |
| 📝 registrar · agregar | 🏛️ canonizar | ✅ auditar | 📋 listar |
| ✨ producir | ⚙️ aplicar | 🌱 sembrar | 🔄 regenerar |
| ✍️ escribir | | | |

---

## §1 — Los consumidores

| Consumidor | Qué le interesa del personaje |
|---|---|
| 🎰 **Generadores de personaje** | El catálogo de tags y sus pesos, las tablas de atributos por rango, las restricciones cruzadas y el azar portable — todo lo necesario para producir una hoja válida y, si corresponde, canonizarla. |
| 📖 **Diégesis** | Tags de lealtad y vínculos, wikilinks a facción, ubicación y demás entidades del vault, historia en prosa, historial como línea de tiempo. |
| ⚔️ **Motor de batalla** | Atributos base, estadísticas derivadas (`fza_aportada`, `movimiento`, `moral`, `fatiga`), tags de equipo y habilidades. |
| 🎲 **Motor de juego** | Tags de aspectos/habilidades, contratos (efectos declarados), historial de hitos, vínculos (tags `aliado/*` / `nemesis/*` / `lealtad/*`). |
| 🎨 **Generador visual** | Tags de vestidura, rango, facción, género, edad y rasgos — los lee para su proyección; cómo los renderiza es asunto suyo. |

Ningún consumidor necesita el personaje completo. El esquema es único; la proyección varía.

---

## §2 — Catálogo de UCs

### Bloque A — Generadores de personaje

Cómo se completa una hoja desde el azar portable vive en [[generacion-procedural|generacion-procedural.md]].

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-G01 | 🎰 | ✨ un efímero por `(semilla, facción, especialidad)` | Poblar un contexto (combatientes, civiles, PNJ) con hojas válidas |
| UC-G02 | 🎰 | ⚙️ restricciones cruzadas (p. ej. rango → edad mínima) | Sortear cada campo dentro del subconjunto válido |
| UC-G03 | 🎰 | 🔄 un efímero con la misma semilla | Previsualizar variantes sin perder la versión original |
| UC-G04 | 🎰 | 🌱 vínculos iniciales (`aliado/*` / `nemesis/*`) | Arrancar la red de relaciones del personaje en campaña |
| UC-G05 | 🎰 | 🏛️ un efímero (idempotente) | Elevarlo a entidad permanente y abrir su `historial[]` |

### Bloque B — Diégesis

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-D01 | 🪶 | 👁️ la hoja de un canonizado | Escribir una escena con coherencia de personaje |
| UC-D02 | 🪶 | 📝 un hito narrativo | Registrar un evento que el personaje vivió |
| UC-D03 | 🪶 | 🔍 personajes por facción y rango | Encontrar candidatos para un papel narrativo |
| UC-D04 | 👓 | 🧭 desde una facción a sus personajes | Explorar quién pertenece a la Confederación Argentina |
| UC-D05 | 👓 | 🧭 desde un personaje a sus aliados y enemigos | Entender la red de vínculos de un personaje |
| UC-D06 | 👓 | 👁️ el `historial[]` de un personaje | Leer su evolución como línea de tiempo |
| UC-D07 | 🛡️ | ✅ todos los canonizados por facción | Mantener la coherencia del corpus de personajes canónicos |

### Bloque C — Motor de batalla

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-B01 | ⚔️ | 📥 un combatiente por patente con sus estadísticas derivadas | Cargarlo al encuentro o recargarlo entre turnos |
| UC-B02 | ⚔️ | 🔍 por `rango/tirador_designado` | Armar un pelotón de tiradores |
| UC-B03 | ⚔️ | 🔍 `especialidad/jerarquia/lider` y `faccion/confederados` | Encontrar candidatos al mando ante la caída del líder |
| UC-B04 | ⚔️ | 📝 una baja (`triple_cero`) | Reflejar la caída de un combatiente en la hoja |
| UC-B05 | ⚔️ | 📝 la captura de un arma enemiga | Actualizar el equipo vigente del personaje |

### Bloque D — Motor de juego

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-J01 | 🎲 | 📥 un PNJ al azar por facción | Rellenar un encuentro improvisado |
| UC-J02 | 🎲 | 📥 un personaje con `aspecto/miope` | Forzar una complicación narrativa específica |
| UC-J03 | 🎲 | 👁️ los contratos activos de un personaje | Saber qué efectos pasivos están en juego |
| UC-J04 | 🎲 | 📝 un vínculo nuevo (`aliado/*`) | Que ambos personajes recuerden el lazo formado |
| UC-J05 | 🎲 | 📝 una ruptura de lealtad (`ruptura_lealtad`) | Que el personaje pase a tener un nuevo enemigo |
| UC-J06 | 🎲 | 👁️ aliados y enemigos de un personaje | Preparar tensiones dramáticas para la sesión |
| UC-J07 | 🎮 | 👁️ los aspectos de origen narrativo disponibles para su rango | Elegir una recompensa narrativa tras un hito |

### Bloque E — Generador visual

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-V01 | 🎨 | 👁️ los tags de vestidura y equipo | Vestir al personaje fiel al lore, en el medio que sea |
| UC-V02 | 🎨 | 👁️ facción, rango y género | Resolver la presentación según bando y jerarquía |
| UC-V03 | 🎨 | 👁️ edad y rasgos (`rasgo/*`) | Ajustar la apariencia del personaje |
| UC-V04 | 🎨 | 👁️ el catálogo de `equipo/vestidura` | No inventar prendas fuera del canon de SyV |

> [!note] El medio es asunto del consumidor
> `syv-pj` solo expone los tags. Si la proyección termina en una imagen, una ficha o una página publicada —y cómo la arma— no es asunto de este módulo.

---

## §3 — Lo que el personaje NO hace

`syv-pj` clasifica, almacena y entrega. No renderiza, no genera imágenes, no corre el motor de batalla, no compone grupos, no escribe prosa narrativa por sí solo.

| Lo hace el personaje | Lo hace el consumidor |
|---|---|
| Declara `tags[]` con equipo, rasgos y lealtades | Interpreta esos tags para su proyección visual |
| Declara `efecto[]` en contratos (aspectos/habilidades) | Aplica esos efectos durante la resolución del encuentro |
| Persiste `historial[]` con hitos de solo añadir | Renderiza el historial como línea de tiempo o ficha de juego |
| Expone atributos base `{cuerpo, mente, alma}` | Deriva `iniciativa`, `moral`, `fatiga` para el turno actual |
| Declara los vínculos como tags `aliado/*` / `nemesis/*` / `lealtad/*` (prosa en su hito) | Usa esos vínculos para preparar tensiones dramáticas |
| Entrega **un** personaje a la vez | Compone grupos y calcula cohesión y movimiento de unidad (vive en el motor de batalla) |

---

## §4 — UCs sobre el catálogo y la meta-operación

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-M01 | 🔌 | 👁️ el catálogo de una categoría de tag | Construir interfaces sin codificar enumeraciones |
| UC-M02 | 🧪 | 📋 todos los personajes de ejemplo | Correr el motor sobre la población de referencia |
| UC-M03 | 🧪 | 👁️ `tag_categories` | Verificar que el generador no produce tags fuera del catálogo |
| UC-M04 | 🛡️ | 📋 todos los `equipo/arma` del catálogo | Auditar el inventario armamentístico |

---

## §5 — Restricciones transversales

Comportamientos que todos los consumidores deben asumir.

- **Los personajes de ejemplo son inmutables.** Ningún consumidor puede registrar hitos sobre los personajes de ejemplo — son fichas de referencia, no entidades vivas.
- **Los efímeros no acumulan hitos.** Sin patente persistida, no hay historia que registrar. El consumidor que quiera evolucionar un efímero debe canonizarlo primero.
- **La canonización es idempotente.** `(semilla, facción, especialidad)` no produce duplicados si ya existe. El consumidor puede reintentar sin riesgo.
- **`?campos=` poda solo nivel superior.** El motor de batalla puede pedir solo `atributos` y `tags`; el generador visual puede pedir solo `tags` e `identidad`. La poda no atraviesa subdocumentos.
- **Filtros `?tag=` son Y lógico.** `?tag=A&tag=B` devuelve personajes que tienen ambos. O no está soportado en v1 — el consumidor hace N llamadas y une los resultados.
- **Vínculos personales sí son filtrables por tag.** Aliados, némesis y lealtades son tags `aliado/*` / `nemesis/*` / `lealtad/*` en `tags[]`: se filtran por `?tag=` y se cuentan como cualquier etiqueta. La prosa del vínculo vive en su hito (ver [[nemesis-y-aliados|nemesis-y-aliados.md]]).
- **Hitos con `tipo` desconocido son legales.** El consumidor descendente los trata como operación-nula sobre los campos que conoce.
