# SPINE — contrato canónico de syv-pj (interno, no es entregable de cara al usuario)

> Documento de coordinación entre redactores. Fija las decisiones que TODOS los
> archivos deben respetar al pie de la letra para que la primera versión sea
> coherente. Si un redactor cree que una decisión es errónea, la respeta igual y
> lo anota en su frontmatter `notas:`; el líder decide en la próxima iteración.

## Qué es syv-pj (norte)

`syv-pj` es el **módulo de la entidad mínima de Subordinación y Valor (SyV): el
personaje**. Documentación + reglas + especificación de diseño en **Markdown**. Es:

- **Independiente de otros sistemas de reglas** — no referencia por ejemplo a `syv-character-kit` ni a otros, no depende de él.
- **Fiel a SyV** — usa los términos, la nomenclatura y captura el espíritu del
  universo (Anatema Mecánico, voz/gesto/banderín, milicias vs. ejército regular,
  voseo sobrio). NO es un creador "universal de cualquier universo".
- **Agnóstico al USO, no al universo** — un mismo personaje homogeneizado sirve
  para: (a) historias de **Diégesis** (vinculado por tags/vínculos Obsidian al resto
  del mundo), (b) **juego de estrategia** (estadísticas numéricas para combate), (c)
  **juego de rol**, (d) **generador de personajes visuales**. syv-pj clasifica,
  almacena y entrega; el consumidor decide.
- 100% Español, como última decisión de diseño y en curso.

## Idioma y estilo

- **Castellano voseo sobrio.** (NO inglés — esto corrige el
  `ORCHESTRATOR.md` sembrado, que pedía inglés/universo-agnóstico; el líder asume
  esta divergencia siguiendo la orden viva del usuario.)
- Markdown con **Markdown de Obsidian**: frontmatter con `title`, `tags:
  [syv/pj/...]`, `aliases`. Wikilinks `[[archivo|alias]]` entre docs. Callouts
  `> [!info]` / `> [!tip]` / `> [!warning]`. Sin emojis salvo pedido.
- Sin versionado ni changelog dentro de los docs (lanzamiento continuo). El historial
  vive en git.

## Convenciones de identificadores (idénticas al espíritu SyV)

- **Slug de personaje** (`identidad.slug`): patente opaca `^[A-Z0-9]{8}$` (ej.
  `K9F2H3M4`). No es el nombre. Estable, inmutable, referenciable.
- **Slug de tag / entidad de catálogo**: legible, `lowercase_con_underscore`, sin
  acentos (`pistola`, `lider_de_escuadra`, `ejercito_rojo`).
- **Tags**: notación punto. Por defecto `<categoria>.<slug>` (2 segmentos); `<slug>` suelto es válido; el 3er segmento `<categoria>.<parent>.<slug>` es rareza (huérfanos subjetivos, `lealtad.*`). **NO es multiconjunto**: ante repetidos, el motor se queda con el último valor.
- **Campos YAML**: `snake_case_castellano`.
- **Azar portable**: probabilidades en **porcentaje**; modificadores sobre
  atributos/estadísticas como **delta entero** (`(+1) MENTAL`); modificadores sobre
  magnitudes continuas en **porcentaje** (`-100% MOVIMIENTO`).

## La hoja de personaje — estructura canónica (NO cambiar nombres de bloques)

Seis bloques estructurales + dos colecciones persistidas + la lista plana de tags:

```yaml
personaje:
  identidad:  { slug, nombre, sobrenombre, rol, genero, edad }
  atributos:  { fis, tac, men }      # únicas magnitudes numéricas PERSISTIDAS
  tags:       [...]                   # lista plana, notación punto, NO multiconjunto (último valor gana)
  historia:   str                     # prosa biográfica, congelada al canonizar
  historial:  [...]                   # hitos temporales (registro de eventos, de solo añadir)
  aliados:    [...]                   # {ref, descripcion, desde?} — vínculos con prosa
  nemesis:    [...]                   # {ref, descripcion, desde?}
  metadatos:  { creado_en, canonizado_en, ultima_actualizacion }
  extras:     object | null           # válvula de escape para clientes
```

**Regla rectora**: todo lo que es discreto y no es identidad, atributo, prosa,
auditoría o vínculo-personal-con-prosa → **es tag**.

- Atributos base `fis, tac, men` en escala `2..7` (determinísticos por rol/rango
  en creación; mutables solo vía hito). Todo otro número (fatiga_max, moral_max,
  fza_aportada, etc.) es **derivado en caliente, no persistido** (evita desincronización).
- `aliados[]`/`nemesis[]` son colecciones (no tags) porque llevan prosa por
  entrada. Las lealtades a facción/subfacción/grupo SÍ son tags (`lealtad.*`).
- `historial[]` es **de solo añadir**; `tipo` de hito es catálogo **sugerido, abierto**.
- Canonicidad: `es_canon` se deriva de `canonizado_en != null` (no se persiste).

## Tags — sistema

- Catálogo extensible por **curaduría, no validación**. Un tag desconocido NO
  rompe la hoja. Tres ejes de extensión sin migración: nuevos slugs, nuevas
  sub-categorías, nuevas categorías enteras.
- Cuatro campos siempre obligatorios en una entrada de catálogo: `slug`, `nombre`,
  `categoria`, `descripcion`. El resto es condicional/opcional.
- `requires` (`require_all`/`require_any`, con prefijo `no:` para NOT) es
  **documentación ejecutable**, no validación dura.
- **Etiquetas huérfanas / subjetivas**: se admite un tag comunicativo sin entrada de
  catálogo todavía (`habilidad.personal.pianista`); su referencia se completa luego
  en la historia del personaje.
- Categorías de referencia (abiertas, ilustrativas — el universo de tags es abierto e
  infinito): `faccion, subfaccion, rango, grupo, mando, estado, salud, moral, mental,
  rasgo, aspecto, habilidad, entrenamiento, efecto, equipo(.arma/.utilitario/
  .vestidura), rol(.oficio/.jerarquia/.narrativo/.combate), lealtad`.

## Contratos: aspecto, habilidad, efecto (eje del usuario)

Concepto unificador: un **contrato** es una palabra o frase corta (el "nombre") que,
al aplicarse, **entrega un paquete declarado**: modificadores numéricos,
penalizaciones y/o habilitaciones. El nombre es la cara legible; el efecto, la letra
chica. Ver [[contratos|docs/habilidades.md]].

- **aspecto** — identidad mecánicamente activa (carácter, condición, marca con peso
  mecánico). Declara `efecto` (pasivo, lista de deltas sobre el vocabulario canónico)
  o `trigger` + `trigger-action` (reactivo). Polaridad mixta. `requires` solo si
  asume una condición previa.
- **habilidad** — habilitador de tirada contra su `atributo_dominante` (`fis|tac|men`);
  nunca aplica modificador directo.
- **efecto** — bloque estructurado referenciable (`efecto.*`); inline (pasivo) o
  externo (disparado por un disparador).

> [!warning] Colisión de `rasgo` — leer
> En el refactor vigente `rasgo` = **rasgo físico observable** (cicatriz, tatuaje),
> NO la identidad mecánica. La identidad mecánicamente activa es `aspecto`. (Una
> versión previa de este SPINE usaba `rasgo` al revés.)

Modelar aspecto/habilidad/efecto como variantes del mismo patrón-contrato:
`nombre legible → paquete declarado`.

## Vocabulario canónico de atributos y estadísticas (efectos apuntan solo acá)

- Atributos base: `FISICO`, `TACTICO`, `MENTAL`.
- Estadísticas calculadas (en caliente): `INICIATIVA`, `MORAL`, `FATIGA`, `MOVIMIENTO`,
  `ESTRESS`. Los `efecto` de tags solo pueden modificar estas variables.

## Diégesis y Obsidian (eje del usuario)

El personaje se conecta al resto del mundo SyV por **tags y wikilinks Obsidian**:
lealtades, grupo, facción, ubicaciones, otros personajes. **Las etiquetas SON tags
de Obsidian**: la relación es lineal e intencional — cada tag de la hoja es
directamente un tag del vault. Un doc dedicado
(`docs/diegesis-y-obsidian.md`) define la convención de linkeo para que una hoja
sea a la vez dato de juego y nodo navegable del vault de Diégesis.

## Abierto/Cerrado

El esquema extiende verticalmente sin romperse: nuevas categorías de tag, nuevos
tipos de hito, nuevos campos derivados, nuevos atributos — sin migración, sin
rupturas de compatibilidad, sin compatibilidad hacia atrás. Minimalismo: no se anticipa nada que no
haga falta todavía ("dejar la cancha preparada", no llenarla).

## Generación procedural (universalizada desde el flujo de creación SyV)

Fases: (1) identidad sorteada (nombre/género/edad de depósitos), (2) atributos
**determinísticos por rol/rango** desde tablas de configuración (cero azar en estadísticas),
(3) tags sorteados ponderados desde catálogo, (4) prosa por LLM (se congela al
canonizar), (5) relaciones sembradas. `(semilla, faccion, rol)` reproduce el mismo
efímero; el canonizado pierde reproducibilidad tras el primer hito.

## Decisiones abiertas (no escribir como cerradas hasta que el líder confirme)

- **`ventaja`**: el viejo tipo "recompensa positiva al azar sin `requires`" ya
  no es categoría propia. Propuesta a confirmar: se pliega en `aspecto`, distinguido
  por `origen`/polaridad, no por tipo. Hasta confirmar, no se escribe `ventaja` como categoría.
- **`arma`/`utilitario`/`vestidura`**: ¿siguen como subcategorías de `equipo`
  (3 segmentos) o se promueven a categorías de primer nivel (`arma.*`)?
- **Efecto → entidad `modificador`**: ¿`efecto` sigue como string-DSL (`(+1) MENTAL`)
  o migra a un mapa `{variable: delta}` en una entidad de modificadores? En
  exploración.

## Inventario de archivos de la primera versión (dueños disjuntos)

- `README.md`, `PRD.md`, `MODEL.md`, `API.md`, `AGENTS.md` (raíz)
- `docs/hoja-personaje.md` (núcleo), `docs/sistema-tags.md`,
  `docs/habilidades.md`, `docs/atributos.md`,
  `docs/generacion-procedural.md`, `docs/open-close.md`, `docs/grupos.md`,
  `docs/diegesis-y-obsidian.md`, `docs/casos-de-uso.md`

`SPINE.md` y `ORCHESTRATOR.md` NO se publican como entregables; quedan o se borran
al cierre según decida el líder.
