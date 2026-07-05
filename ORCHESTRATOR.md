# /kdx-orchestrator — Extracción del Creador de Personajes syv-pj

## TU ROL
Sos el orquestador del proyecto syv-pj. DEBES usar el sistema de subagentes de Claude Code (@agent o Task) para paralelizar el trabajo. NO hagas todo vos — delegá en subagentes especializados.

## CONTEXTO
syv-character-kit en /home/kodex/Dev/SyV/syv-character-kit/ es un sistema de fichas específico del universo SyV con lore incrustado (Confederación Argentina, Ejército Rojo, año 2178, etc.). Tiene acoplamiento profundo al dominio.

El nuevo proyecto syv-pj en /home/kodex/Dev/SyV/syv-pj/ debe ser una **especificación completamente agnóstica, agnóstica al framework, agnóstica al lenguaje** — una ficha de personaje universal que sirva para CUALQUIER universo de juego, cualquier sistema, cualquier género.

## OBJETIVO
Extraé la lógica de CREACIÓN DE PERSONAJES de syv-character-kit y producí una especificación limpia, universal, agnóstica en /home/kodex/Dev/SyV/syv-pj/.

La ficha de personaje sigue el **principio Abierto/Cerrado**: abierto para extensión (nuevas destrezas, rasgos, ventajas, equipo, facciones, etc.) sin modificar el esquema núcleo.

## ARCHIVOS DE SALIDA REQUERIDOS (TODOS deben crearse)

### 1. PRD.md — Documento de Requerimientos del Producto
- Visión: creador universal de personajes, agnóstico al universo
- La ficha de personaje es un "documento vivo" — los personajes evolucionan vía eventos/historial
- Abierto/cerrado: nuevas categorías de tag, nuevos tipos de evento, nuevos campos derivados — todo sin migración de esquema
- Sin lore incrustado, sin facciones incrustadas, sin rangos incrustados
- Todos los patrones buenos de syv-character-kit (tags como primera clase, estadísticas determinísticas, generación procedural, reproducibilidad de semilla) — pero UNIVERSALIZADOS

### 2. MODEL.md — Contrato de Persistencia
- Definiciones de entidades: personaje, tag_catalogo, grupo/escuadra, facción
- Tipos de campo, reglas de mutabilidad, campos derivados
- El sistema de tags: notación punto, categorías, multiset, catálogo abierto
- Sistema de eventos/historial: append-only, tipos abiertos
- Todo universalizado — sin enums ni valores específicos de SyV

### 3. API.md — Contrato de API HTTP
- Endpoints CRUD para personajes, grupos, facciones
- Endpoints de catálogo de tags
- Endpoints de registro de eventos
- Endpoint de generación procedural (basado en semilla)
- Endpoint de canonización (efímero → persistente)
- Todas las cargas usan el esquema universal

### 4. docs/character-sheet.md — El Esquema de Ficha (EL DOCUMENTO NÚCLEO)
Esta es LA especificación definitiva. Debe cubrir:
- Los 6 bloques estructurales: identidad, atributos, historial, event_log, metadatos, extras
- La colección plana de tags[] — el corazón del sistema
- Notación de tags: `<categoria>[.<subcategoria>]<slug>`
- Categorías de tags: abierto por diseño (habilidad, rasgo, aspecto, equipo, especialidad, faccion, custom...)
- Campos derivados: computados en lectura, no persistidos
- Matriz de mutabilidad: qué cambia vía eventos vs qué es inmutable
- El sistema de eventos: tipos, efectos sobre campos, append-only
- Relaciones: aliados, nemesis, membresía de grupo
- El flujo de generación procedural (universalizado desde GDDR-01 de SyV)
- Reproducibilidad basada en semilla para personajes efímeros
- Canonización: congelación de narrativa, asignación de identidad

### 5. docs/tag-system.md — Especificación del Sistema de Tags
- Diseño universal del catálogo de tags
- Convenciones de categorías (abierto, no cerrado)
- Efectos de tags: cómo los tags modifican atributos/estadísticas
- Sistema de disparadores: activación reactiva a eventos
- Peso/peso narrativo para ordenamiento procedural
- Reglas de compatibilidad/exclusión

### 6. docs/procedural-generation.md — Flujo de Generación Procedural
- Pipeline universalizado de creación (desde GDDR-01 de SyV)
- Fase 1: Identidad (nombre, género, edad — desde pools)
- Fase 2: Atributos (determinísticos por rango desde tablas de configuración)
- Fase 3: Tags (aleatorio ponderado desde catálogo)
- Fase 4: Narrativa (historia de trasfondo generada por LLM — congelada al canonizar)
- Fase 5: Relaciones (aleatorio sembrado desde pool)
- Reproducibilidad de semilla: (semilla, facción, rango) → mismo personaje
- Todo impulsado por configuración, sin valores incrustados

### 7. docs/open-close-principle.md — Documento de Diseño Abierto/Cerrado
- Cómo el esquema se extiende sin romperse
- Agregación de nuevas categorías de tags
- Agregación de nuevos tipos de eventos
- Agregación de nuevos campos derivados
- Agregación de nuevos tipos de atributos
- Estrategia de versionado: lanzamiento continuo, sin carga de compatibilidad hacia atrás
- Patrones de extensión sin migración

### 8. docs/group-system.md — Sistema de Grupos/Escuadras (universalizado desde escuadra)
- Grupos como unidades tácticas/organizacionales
- Membresía, roles dentro de grupos
- Estadísticas derivadas a nivel grupo (cohesión, fuerza total, etc.)
- Eventos/historial de grupo
- Universalizado — sin estructura específica de SyV

### 9. docs/faction-system.md — Sistema de Facciones
- Facciones como entidades de primera clase
- Sub-facciones como tags (diseño asimétrico de SyV)
- Membresía en facción vía tags
- Seguimiento de lealtad
- Universalizado — sin facciones incrustadas

### 10. docs/attribute-system.md — Sistema de Atributos y Estadísticas
- Atributos núcleo: conjunto abierto (no incrustado a FIS/TAC/MEN)
- Escalas de atributos configurables
- Estadísticas derivadas: computadas desde atributos + tags
- Sistema de efectos: tags modifican atributos vía deltas
- Universalizado — cualquier conjunto de atributos funciona

## ESTRATEGIA DE SUBAGENTES (OBLIGATORIA)
DEBES usar subagentes para trabajo en paralelo. División sugerida:

1. **Subagente A**: PRD.md + MODEL.md (visión de producto + persistencia)
2. **Subagente B**: API.md (contrato HTTP)
3. **Subagente C**: docs/character-sheet.md + docs/tag-system.md (esquema núcleo)
4. **Subagente D**: docs/procedural-generation.md + docs/attribute-system.md (generación + estadísticas)
5. **Subagente E**: docs/group-system.md + docs/faction-system.md + docs/open-close-principle.md (grupos, facciones, diseño)

Cada subagente lee los archivos fuente relevantes de syv-character-kit y produce la versión universalizada.

## ARCHIVOS FUENTE A LEER (desde syv-character-kit)
- /home/kodex/Dev/SyV/syv-character-kit/PRD.md
- /home/kodex/Dev/SyV/syv-character-kit/MODEL.md
- /home/kodex/Dev/SyV/syv-character-kit/API.md
- /home/kodex/Dev/SyV/syv-character-kit/AGENTS.md
- /home/kodex/Dev/SyV/syv-character-kit/docs/hoja-modelo.md
- /home/kodex/Dev/SyV/syv-character-kit/docs/tag-modelo.md
- /home/kodex/Dev/SyV/syv-character-kit/docs/atributos-y-efectos.md
- /home/kodex/Dev/SyV/syv-character-kit/docs/escuadra-modelo.md
- /home/kodex/Dev/SyV/syv-character-kit/gddr/01-flujo-obligatorio-creacion.md
- /home/kodex/Dev/SyV/syv-character-kit/docs/user-stories.md

## REGLAS
- TODA salida en español rioplatense (el universo SyV es castellano)
- SIN lore incrustado, SIN facciones incrustadas, SIN rangos incrustados
- TODOS los patrones de syv-character-kit deben ser UNIVERSALIZADOS
- Tags siempre de primera clase
- Principio abierto/cerrado, siempre
- Event log append-only, siempre
- Estadísticas determinísticas desde tablas de configuración, siempre
- Reproducibilidad de semilla para efímeros, siempre
- LLM solo para prosa narrativa, congelada al canonizar, siempre
- Después de que TODOS los archivos estén escritos, crea un reporte de resumen en /home/kodex/Dev/SyV/syv-pj/REPORT.md

## PASO FINAL
Después de que todos los docs estén completos, escribí /home/kodex/Dev/SyV/syv-pj/REPORT.md con:
- Resumen de lo que se extrajo y se universalizó
- Decisiones de diseño clave
- Inventario de archivos
- Lo que un desarrollador necesita para implementar esto
