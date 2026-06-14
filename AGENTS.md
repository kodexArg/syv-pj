---
title: "AGENTS — Política editorial y convenciones de trabajo"
tags:
  - syv/pj/editorial
aliases:
  - AGENTS
  - AGENTS.md
---

# AGENTS.md — syv-pj

Política editorial y convenciones de trabajo de `syv-pj`, el módulo de la **entidad mínima** de *Subordinación y Valor*: el personaje. Para entender el esquema, leer [[hoja-personaje|docs/hoja-personaje.md]] (núcleo) y sus docs hermanos: [[sistema-tags|sistema-tags.md]], [[atributos-y-stats|atributos-y-stats.md]], [[habilidades|perks-y-traits.md]].

> [!info] Norte del proyecto
> `syv-pj` clasifica, almacena y entrega un personaje homogeneizado; el consumidor decide el uso. Es **agnóstico al uso** (Diégesis, estrategia, rol, generación visual) pero **fiel al universo** SyV. No es un creador universal de cualquier mundo, y no inventa lore: la terminología del universo se respeta, no se amplía.

---

## Lanzamiento continuo sin registro de cambios en los docs

Toda la documentación de `syv-pj` es **de versión única**: refleja solo el estado vigente. No hay, dentro de los docs:

- **Versionado**: no se escribe `v0.5.0`, `Reemplaza:`, etc. Si un campo ya no existe, simplemente no aparece. Si una decisión cambió, se reescribe la sección — no se anota "antes era Y".
- **Registro de cambios**: no hay sección de historial. El historial vive en `git log`; la intención de un cambio vive en el mensaje del commit. Los docs no son un diario.
- **Compatibilidad hacia atrás**: los docs no documentan migración desde una versión previa. Para reconstruir el contrato pasado, se lee `git log` del archivo.

> [!tip] Cuándo sí preservar el porqué
> Decisiones de diseño cuyo *razonamiento sigue vivo* se documentan en lenguaje **atemporal**, como "tensión asumida" o "decisión de diseño" — sin fecha ni versión. Ejemplo útil hoy: "El sistema acepta tags fuera del catálogo; costo: fragmentación silenciosa; mitigación: curaduría, no validación." Lo que NO aporta: "antes el esquema validaba estrictamente, después se abrió."

---

## Convenciones de identificadores

- **Slug de personaje** (`identidad.slug`): ==patente opaca== `^[A-Z0-9]{8}$` (ej. `K9F2H3M4`). No es el nombre. Estable, inmutable, referenciable. Ver [[hoja-personaje#1.1. slug — la patente del personaje|docs/hoja-personaje.md §1.1]].
- **Slug de catálogo** (tag, facción, escuadra, grupo): legible, `lowercase_con_underscore`, sin acentos, sin guiones (`pistola`, `lider_de_escuadra`, `ejercito_rojo`). El separador uniforme es `_` para componer en notación punto sin ambigüedad.
- **Tags**: notación punto `<categoria>[.<subcategoria>].<slug>`, multiset. Ver [[sistema-tags|sistema-tags.md]].
- **Campos estructurales en YAML**: `snake_case_castellano` (`atributos`, `historial`, `ultima_actualizacion`).

> [!note] Asimetría deliberada de slugs
> La patente del personaje es opaca para ser estable a escala (dos personajes con el mismo nombre no colisionan; un cambio narrativo de nombre no invalida refs). El slug de catálogo es legible porque es la pieza humana de la dot notation. Una clase es para máquinas; la otra, para personas.

---

## Idioma y estilo

- **Castellano rioplatense, voseo sobrio.** Sin emojis salvo pedido explícito del usuario.
- **Obsidian Flavored Markdown**: frontmatter con `title`, `tags`, `aliases`; wikilinks `[[archivo|alias]]` entre docs; callouts `> [!info]` / `> [!tip]` / `> [!warning]` / `> [!note]`. Resaltado `==así==` para términos que fijan contrato.
- Razonamiento interno en inglés; salida en castellano.

---

## Azar portable — agnóstico al sistema

`syv-pj` **no fija** un sistema de resolución de azar. Para que fichas, tags y modificadores sean reutilizables entre sistemas, toda magnitud se expresa en una de **tres formas portables** según el tipo:

- **Probabilidades de evento**: porcentaje. `40% de fallar el chequeo`, `5% de paniquear bajo fuego`. Nunca una expresión atada a un sistema concreto.
- **Modificadores sobre atributos o estadísticas calculadas**: delta entero sobre la escala canónica. `(+1) MENTAL`, `(-1) INICIATIVA`, `(+2) FATIGA`. Las variables y sus escalas viven en [[atributos-y-stats|atributos-y-stats.md]].
- **Modificadores sobre tasas o magnitudes continuas**: porcentaje sobre la magnitud. `-100% MOVIMIENTO` (inmóvil), `+50% defensa por cobertura`.

> [!info] Por qué portable
> SyV es un universo, no un sistema. Atar el esquema a una mecánica concreta de dados amputa la portabilidad. El delta sobre escala canónica y el porcentaje sobre tasa son lingua franca: cualquier sistema downstream los convierte a su moneda local. Un documento auxiliar puede ilustrar mecánicas con un sistema concreto **como ejemplo didáctico**; el contrato son las tres formas de arriba.

---

## Abierto/Cerrado — el esquema extiende sin romper

El núcleo crece **verticalmente sin migración**: nuevas categorías de tag, nuevos tipos de hito, nuevos campos derivados, nuevos atributos — sin rupturas de compatibilidad ni compatibilidad hacia atrás. Minimalismo: no se anticipa nada que no haga falta todavía. "Dejar la cancha preparada", no llenarla. El detalle del contrato de extensión vive en [[open-close|open-close.md]].

---

## Trabajo con Claude / agentes de IA

- Antes de tocar el esquema, asegurar que **todos** los docs del inventario queden consistentes entre sí. El núcleo es [[hoja-personaje|docs/hoja-personaje.md]]; un cambio en un bloque se propaga a los hermanos antes de cerrar el turno.
- La prosa de `historia` y de `historial[].descripcion` es contenido editorial **irreplazable** (no-reproducible aun con seed). Los cambios destructivos sobre datos con prosa se hacen solo con autorización explícita del usuario en la conversación vigente.
- No agregar entradas de changelog ni líneas "Versión: X". Si el modelo cambia, reescribir las secciones afectadas en lenguaje atemporal.
- **Fidelidad al universo**: antes de introducir terminología (geografía, facciones, vocabulario, personajes), verificar contra el lore canon de SyV. `syv-pj` documenta y clasifica; no inventa lore. Las decisiones de mecánica, atributos por rol/rango y modelado del personaje son soberanía de este módulo y se documentan acá.
