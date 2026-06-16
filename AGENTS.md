---
title: "AGENTS — Política editorial y convenciones de trabajo"
tags:
  - syv/pj/editorial
aliases:
  - AGENTS
  - AGENTS.md
---

# AGENTS.md — syv-pj

Política editorial y convenciones de trabajo de `syv-pj`, el módulo de la **entidad mínima** de *Subordinación y Valor*: el personaje. Para entender el esquema, leer [[hoja-personaje|docs/hoja-personaje.md]] (núcleo) y sus docs hermanos: [[sistema-tags|sistema-tags.md]], [[atributos-y-habilidades|atributos-y-habilidades.md]], [[contratos|contratos.md]].

> [!info] Norte del proyecto
> `syv-pj` clasifica, almacena y entrega un personaje homogeneizado; el consumidor decide el uso. Es **agnóstico al uso** (Diégesis, estrategia, juego de rol, generación visual) pero **fiel al universo** SyV. No es un creador universal de cualquier mundo, y no inventa lore: la terminología del universo se respeta, no se amplía.

---

## SPINE es la fuente — mantenerlo actualizado es obligatorio

> [!warning] Regla de precedencia
> [[SPINE]] es el **contrato canónico interno**: fija las decisiones que todos los archivos del inventario respetan al pie de la letra. Es la **fuente del resto del proyecto** — los docs derivan de SPINE, no al revés.

- **Toda decisión de diseño que cambie** (taxonomía de etiquetas, nombres canónicos, estructura de la hoja, vocabulario de atributos y estadísticas, convenciones) **se refleja en SPINE en el mismo turno**, antes de cerrar. Un cambio que no llegó a SPINE no está cerrado.
- Ante conflicto entre un doc y SPINE no quedan divergentes en silencio: o se corrige el doc, o se actualiza SPINE explícitamente.
- SPINE es interno (no se publica). Mantenerlo vivo es responsabilidad de cualquier redactor o agente que toque el esquema.

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
- **Slug de catálogo** (tag, facción): legible, `lowercase_con_underscore`, sin acentos, sin guiones (`pistola`, `lider_de_escuadra`, `ejercito_rojo`). El separador uniforme es `_` para componer en notación punto sin ambigüedad.
- **Tags**: notación punto `<categoria>[.<subcategoria>].<slug>`. **NO** es multiconjunto: ante repetidos gana el último valor. Ver [[sistema-tags|sistema-tags.md]].
- **Campos estructurales en YAML**: `snake_case_castellano` (`atributos`, `historial`, `ultima_actualizacion`).

> [!note] Asimetría deliberada de slugs
> La patente del personaje es opaca para ser estable a escala (dos personajes con el mismo nombre no colisionan; un cambio narrativo de nombre no invalida refs). El slug de catálogo es legible porque es la pieza humana de la dot notation. Una clase es para máquinas; la otra, para personas.

---

## Idioma y estilo

- **Castellano rioplatense, voseo sobrio.** Sin emojis salvo pedido explícito del usuario.
- **Obsidian Flavored Markdown**: la sintaxis (frontmatter, wikilinks, callouts, resaltado `==así==`) y los skills `/obsidian-markdown` y `/obsidian-bases` viven en [[obsidian|docs/obsidian.md]] — única referencia, no se repite acá.
- Razonamiento interno en inglés; salida en castellano.

---

## Frontmatter: los nombres de campo son contrato, no prosa

> [!warning] Intocables en cualquier iteración
> Los **nombres de campo** del frontmatter YAML son un **contrato programático** (los parsean los agentes y el tooling). **Nunca se traducen, renombran ni acentúan** — ni en esta iteración ni en ninguna futura, incluidas auditorías o traducciones masivas de inglés a castellano. Esta regla **prevalece** sobre cualquier consigna de "traducir hasta el último término en inglés".

- Quedan **siempre en inglés y minúscula**: `title`, `tags`, `aliases`, `folder`, `description`. Lista cerrada salvo decisión explícita del usuario en la conversación vigente.
- Se traduce el **valor** de un campo cuando es prosa; **jamás su clave**. `description: Texto en castellano` ✓ — `descripcion:` ✗.
- Los **valores** que son identificadores de herramienta no son prosa y se preservan tal cual: `slug` y los de control `sidebar` / `order` / `hidden`. Los valores de `aliases` sí pueden traducirse cuando no rompen la resolución de wikilinks.

---

## Azar portable — agnóstico al sistema

`syv-pj` **no fija** un sistema de resolución de azar. Para que fichas, tags y modificadores sean reutilizables entre sistemas, toda magnitud se expresa en una de **tres formas portables** según el tipo:

- **Probabilidades de evento**: porcentaje. `40% de fallar el chequeo`, `5% de paniquear bajo fuego`. Nunca una expresión atada a un sistema concreto.
- **Modificadores sobre atributos o estadísticas calculadas**: delta entero sobre la escala canónica. `(+1) MENTAL`, `(-1) INICIATIVA`, `(+2) FATIGA`. Las variables y sus escalas viven en [[atributos-y-habilidades|atributos-y-habilidades.md]].
- **Modificadores sobre tasas o magnitudes continuas**: porcentaje sobre la magnitud. `-100% MOVIMIENTO` (inmóvil), `+50% defensa por cobertura`.

> [!info] Por qué portable
> SyV es un universo, no un sistema. Atar el esquema a una mecánica concreta de dados amputa la portabilidad. El delta sobre escala canónica y el porcentaje sobre tasa son lingua franca: cualquier sistema descendente los convierte a su moneda local. Un documento auxiliar puede ilustrar mecánicas con un sistema concreto **como ejemplo didáctico**; el contrato son las tres formas de arriba.

---

## Abierto/Cerrado — el esquema extiende sin romper

El núcleo crece **verticalmente sin migración**: nuevas categorías de tag, nuevos tipos de hito, nuevos campos derivados, nuevos atributos — sin rupturas de compatibilidad ni compatibilidad hacia atrás. Minimalismo: no se anticipa nada que no haga falta todavía. "Dejar la cancha preparada", no llenarla.

---

## Trabajo con Claude / agentes de IA

- Antes de tocar el esquema, asegurar que **todos** los docs del inventario queden consistentes entre sí. El núcleo es [[hoja-personaje|docs/hoja-personaje.md]]; un cambio en un bloque se propaga a los hermanos antes de cerrar el turno.
- La prosa de `historia` y de `historial[].descripcion` es contenido editorial **irreplazable** (no-reproducible aun con semilla). Los cambios destructivos sobre datos con prosa se hacen solo con autorización explícita del usuario en la conversación vigente.
- No agregar entradas de changelog ni líneas "Versión: X". Si el modelo cambia, reescribir las secciones afectadas en lenguaje atemporal.
- **Fidelidad al universo**: antes de introducir terminología (geografía, facciones, vocabulario, personajes), verificar contra el lore canon de SyV. `syv-pj` documenta y clasifica; no inventa lore. Las decisiones de mecánica, atributos por rango y modelado del personaje son soberanía de este módulo y se documentan acá.
