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

# Casos de uso — Un personaje, muchos consumidores

> [!info] El eje de homogeneización
> `syv-pj` entrega un único personaje bien definido. Lo que varía es quién lo consume y para qué. Este documento cataloga los usos que el módulo homogeneiza: historias de Diégesis, juego de estrategia, juego de rol y generación de personajes visuales. Un personaje, cuatro consumidores.

---

## §1 — Los consumidores

| Consumidor | Qué le interesa del personaje |
|---|---|
| **Diégesis** | Tags de lealtad, wikilinks a facción/grupo/ubicación, historia en prosa, historial como línea de tiempo. |
| **Motor de estrategia** | Atributos base, estadísticas derivadas (`fza_aportada`, `MOVIMIENTO`, `MORAL`, `FATIGA`), tags de equipo y destrezas. |
| **Motor de rol** | Tags de rasgos/ventajas/destrezas, contratos (efectos declarados), historial de hitos, vínculos (tags `aliado.*` / `nemesis.*`). |
| **Generador visual** | Tags de vestidura, rango, facción, género, edad — suficiente para construir el indicador de imagen. |

Ningún consumidor necesita el personaje completo. El esquema es único; la proyección varía.

---

## §2 — Catálogo de UCs

### Bloque A — Diégesis

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-D01 | Autor narrativo | Consultar la hoja de un canonizado | Escribir una escena con coherencia de personaje |
| UC-D02 | Autor narrativo | Canonizar un efímero | Elevarlo a entidad permanente del corpus de Diégesis |
| UC-D03 | Autor narrativo | Agregar un hito narrativo | Registrar un evento que el personaje vivió |
| UC-D04 | Autor narrativo | Filtrar personajes por facción y rango | Encontrar candidatos para un rol narrativo |
| UC-D05 | Lector del vault | Navegar desde una facción a sus personajes | Explorar quién pertenece a la Confederación Argentina |
| UC-D06 | Lector del vault | Navegar desde un personaje a sus aliados y enemigos | Entender la red de vínculos de un personaje |
| UC-D07 | Lector del vault | Ver el `historial[]` de un personaje | Leer su evolución como línea de tiempo |
| UC-D08 | Curador de canon | Auditar todos los canonizados por facción | Mantener la coherencia del elenco canónico |

### Bloque B — Juego de estrategia

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-E01 | Motor de batalla | Pedir la composición y estadísticas de un grupo | Evaluar su capacidad táctica antes del encuentro |
| UC-E02 | Motor de batalla | Pedir un personaje exacto por patente | Recargar a un combatiente entre turnos |
| UC-E03 | Motor de batalla | Filtrar por `destreza.tirador_designado` | Armar un pelotón de tiradores |
| UC-E04 | Motor de batalla | Filtrar `rol.lider AND faccion.confederados` | Encontrar candidatos al mando ante caída del líder |
| UC-E05 | Motor de batalla | Registrar una baja (triple-cero) | Reflejar la caída de un combatiente en la hoja |
| UC-E06 | Motor de batalla | Registrar la captura de un arma enemiga | Actualizar el equipo vigente del personaje |
| UC-E07 | Motor de batalla | Asignar un personaje a un grupo | Derivar `grupo.<slug>` y activar su slot en el elenco |
| UC-E08 | Motor de batalla | Remover un combatiente del grupo | Registrar una baja o traslado en el elenco táctico |
| UC-E09 | Motor de batalla | Consultar el `movimiento_tactico` del grupo | Determinar cuánto avanza la unidad en un turno |
| UC-E10 | Motor de batalla | Consultar `cohesion_vigente` tras caída del líder | Aplicar penalización por cadena de mando rota |

### Bloque C — Juego de rol

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-R01 | Árbitro | Pedir un PNJ al azar por facción | Rellenar un encuentro improvisado |
| UC-R02 | Árbitro | Pedir un personaje con `rasgo.miope` | Forzar una complicación narrativa específica |
| UC-R03 | Árbitro | Consultar los contratos activos de un personaje | Saber qué efectos pasivos están en juego |
| UC-R04 | Árbitro | Registrar un vínculo nuevo | Que ambos personajes recuerden el lazo formado |
| UC-R05 | Árbitro | Registrar una ruptura de lealtad | Que el personaje pase a tener un nuevo enemigo |
| UC-R06 | Árbitro | Consultar aliados y enemigos de un personaje | Preparar tensiones dramáticas para la sesión |
| UC-R07 | Jugador | Regenerar su personaje efímero con la misma semilla | Revisar variantes sin perder la versión original |
| UC-R08 | Jugador | Ver todas las ventajas disponibles para su rango | Elegir recompensa narrativa tras un hito |

### Bloque D — Generador visual

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-V01 | Tubería visual | Leer los tags de vestidura de un personaje | Construir el indicador de imagen con equipo fiel al lore |
| UC-V02 | Tubería visual | Leer facción, rango y género | Determinar uniforme, insignias y postura |
| UC-V03 | Tubería visual | Leer edad y rasgos (`rasgo.*`) | Ajustar fisionomía y expresión en la imagen |
| UC-V04 | Tubería visual | Filtrar personajes canonizados sin imagen generada | Procesar el atraso de ilustraciones pendientes |
| UC-V05 | Tubería visual | Consultar el catálogo de `equipo.vestidura` | Evitar inventar prendas fuera del canon de SyV |

---

## §3 — Lo que el personaje NO hace

`syv-pj` clasifica, almacena y entrega. No renderiza, no genera imágenes, no corre el motor de batalla, no escribe prosa narrativa por sí solo.

| Lo hace el personaje | Lo hace el consumidor |
|---|---|
| Declara `tags[]` con equipo, rasgos y lealtades | Interpreta esos tags para armar el indicador visual |
| Declara `efecto[]` en contratos (rasgos/ventajas) | Aplica esos efectos durante la resolución del encuentro |
| Persiste `historial[]` con hitos de solo añadir | Renderiza el historial como línea de tiempo o ficha de juego |
| Expone atributos base `{fis, tac, men}` | Deriva `INICIATIVA`, `MORAL`, `FATIGA` para el turno actual |
| Declara los vínculos como tags `aliado.*` / `nemesis.*` (prosa en su hito) | Usa esos vínculos para preparar tensiones dramáticas |

---

## §4 — UCs sobre el catálogo y la meta-operación

| UC | Actor | Quiere | Para |
|---|---|---|---|
| UC-M01 | Cualquier cliente | Consultar el catálogo de una categoría de tag | Construir interfaces sin codificar enumeraciones |
| UC-M02 | Tubería de control de calidad | Listar todos los personajes de ejemplo del elenco | Correr el motor sobre la población canónica |
| UC-M03 | Control de calidad | Consultar `tag_categories` | Verificar que el generador no produce tags fuera del catálogo |
| UC-M04 | Curador | Listar todos los `equipo.arma` del elenco | Auditar el inventario armamentístico |

---

## §5 — Restricciones transversales

Comportamientos que todos los consumidores deben asumir.

- **Los personajes de ejemplo son inmutables.** Ningún consumidor puede registrar hitos sobre los 22 personajes de ejemplo — son fichas de referencia, no entidades vivas.
- **Los efímeros no acumulan hitos.** Sin patente persistida, no hay historia que registrar. El consumidor que quiera evolucionar un efímero debe canonizarlo primero.
- **La canonización es idempotente.** `(semilla, faccion, rango)` no produce duplicados si ya existe. El consumidor puede reintentar sin riesgo.
- **`?campos=` poda solo nivel superior.** El motor de estrategia puede pedir solo `atributos` y `tags`; el generador visual puede pedir solo `tags` e `identidad`. La poda no atraviesa subdocumentos.
- **Filtros `?tag=` son Y lógico.** `?tag=A&tag=B` devuelve personajes que tienen ambos. O no está soportado en v1 — el consumidor hace N llamadas y une los resultados.
- **Vínculos personales sí son filtrables por tag.** Aliados y némesis son tags `aliado.*` / `nemesis.*` en `tags[]`: se filtran por `?tag=` y se cuentan como cualquier etiqueta. La prosa del vínculo vive en su hito (ver [[nemesis-y-aliados|nemesis-y-aliados.md]]).
- **Hitos con `tipo` desconocido son legales.** El consumidor descendente los trata como operación-nula sobre los campos que conoce.
