---
title: MODEL — syv-pj
tags:
  - syv/pj/model
aliases:
  - MODEL
  - Contrato de persistencia
---

# MODEL — syv-pj

> [!info] Contrato de Persistencia
> Define las entidades, tipos de campo, reglas de mutabilidad y derivados que cualquier capa de persistencia (relacional, documental, KV) debe poder representar para servir [[API|API.md]] sin pérdida.
>
> Si una operación HTTP devuelve un campo, este documento lo tipifica. Si una operación lo muta, este documento fija la regla. **Sincronía absoluta con [[API|API.md]].**
>
> No prescribe tecnología. Castellano rioplatense, `snake_case_castellano`, tags en notación punto.

---

## Entidades

Cuatro entidades persistidas: `personaje`, `tag_catalogo`, `grupo`, `faccion`. Dos colecciones embebidas: `hito` y `vinculo`. Skills, traits, perks y equipo son **tags** y viven como entradas de `tag_catalogo`.

---

## 1. `personaje`

Resource principal. Servido por `GET /personaje/{slug}`, mutado por `POST /personaje/{slug}/evento`, creado por `POST /canonizar`.

| Campo | Tipo | Mutable | Notas |
|---|---|---|---|
| `identidad.slug` | `str` `^[A-Z0-9]{8}$` \| `null` | set una vez | PK. `null` en efímeros. Asignada por el servidor al canonizar. |
| `identidad.nombre` | `str` | inmutable | Legible. No único. |
| `identidad.sobrenombre` | `str \| null` | mutable (sin hito) | `null` si no aplica. |
| `identidad.rol` | `str` | mutable vía hito `ascenso` / `cambio_rol` | Default `"ciudadano"`. Narrativo. |
| `identidad.genero` | `str` | inmutable | Enum abierto: `masculino \| femenino \| no_binario \| otro`. |
| `identidad.edad` | `int` | mutable (sin hito) | Decisión narrativa. |
| `atributos.fis` | `int` (2..5) | vía hito `triple_cero` / `mejora_atributo` | Escala 2..7; tope absoluto 5 al crear. |
| `atributos.tac` | `int` (2..6) | vía hito `triple_cero` / `mejora_atributo` | Tope absoluto 6; creación máx 5; vía hito hasta tope. |
| `atributos.men` | `int` (2..7) | vía hito `triple_cero` / `mejora_atributo` | Tope absoluto 7; creación máx 6; vía hito hasta tope. |
| `tags[]` | `list<str>` (multiset) | vía hito `agregar_tag` / `quitar_tag` | Notación punto `<categoria>[.<subcategoria>].<slug>`. Admite repetidos. |
| `historia` | `str` | inmutable tras canonizar | 120–200 palabras. Congelada al canonizar. |
| `historial[]` | `list<hito>` (embebida) | append-only vía `POST /evento` | Ver §1.1. |
| `aliados[]` | `list<vinculo>` | mutable vía hito `formacion_lealtad` | Ver §1.2. |
| `nemesis[]` | `list<vinculo>` | mutable vía hito `identificacion_nemesis` | Misma forma que `aliados[]`. |
| `metadatos.creado_en` | `str` ISO-8601 | inmutable | |
| `metadatos.canonizado_en` | `str` ISO-8601 \| `null` | set una vez | `null` en efímeros. |
| `metadatos.ultima_actualizacion` | `str` ISO-8601 | actualiza con cada hito | |
| `extras` | `object \| null` | libre | Escape hatch. La API no inspecciona. |

### Campos derivados — computados al servir, no persistidos

- `es_canon` — `canonizado_en != null`.
- `fatiga_max` = `fis + men`.
- `moral_max` = `men`.
- `fza_aportada` — desde tags `rol.combate.*` (`heroe: 3`, `lider: 2`, valor por defecto `1`).
- `filiacion` — desde tags `rango.*` + `grupo.*`.

Aparecen en la respuesta de `GET /personaje` y `GET /personaje/{slug}` junto con los campos persistidos. Se recomputan en cada lectura; el cliente no los muta directamente.

### 1.1. `hito` (embebido en `personaje.historial[]`)

| Campo | Tipo | Notas |
|---|---|---|
| `fecha` | `str` ISO-8601 | |
| `tipo` | `str` | Enum abierto sugerido. Ver [[hoja-personaje#Historial|docs/hoja-personaje.md §Historial]]. |
| `descripcion` | `str` | Obligatorio. |
| `ref_batalla` | `str \| null` | Slug de batalla externa; referencia narrativa. |
| `metadata` | `object` | Libre. Convención: `{ atributo, delta, valor_anterior, valor_nuevo }` para mejoras; `{ categoria, valor }` para agregar/quitar tag. |

Tipos de hito sugeridos (enum abierto): `combate`, `ascenso`, `cambio_rol`, `triple_cero`, `mejora_atributo`, `agregar_tag`, `quitar_tag`, `formacion_lealtad`, `identificacion_nemesis`, `licencia`, `desercion`, `muerte`.

### 1.2. `vinculo` (embebido en `personaje.aliados[]` y `personaje.nemesis[]`)

| Campo | Tipo | Notas |
|---|---|---|
| `ref` | `str` `^[A-Z0-9]{8}$` | Patente de otro `personaje`. Sin FK enforcement (ver §5). |
| `descripcion` | `str` | Obligatorio. 1–3 frases sobre el vínculo. |
| `desde` | `str` ISO-8601 \| `null` | Opcional. |

---

## 2. `tag_catalogo`

Catálogo curado de tags. Servido por `GET /meta/{categoria}`. El catálogo se siembra desde archivos de definición al arrancar el servidor.

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `slug` | `str` lowercase + underscore | sí | Último segmento del tag. Sin acentos. |
| `nombre` | `str` | sí | Label humano legible. |
| `categoria` | `str` | sí | Primer segmento del tag en notación punto. |
| `subcategoria` | `str \| null` | condicional | Obligatorio si `categoria ∈ {equipo, rol}`. Segmento intermedio. |
| `descripcion` | `str` | sí | 1–3 frases. |
| `origen` | `str` | no (default `emergente`) | Enum: `canon \| emergente \| custom`. |
| `efecto` | `str \| list<str> \| null` | condicional | Obligatorio si `categoria = trait` (sin `trigger`) o `categoria = efecto`. Modificadores sobre vocabulario canónico. Ver [[atributos-y-stats|docs/atributos-y-stats.md]]. |
| `trigger` | `object \| null` | no | `{ evento, condicion, probabilidad?, trigger_action[] }`. Efectos reactivos. |
| `requires` | `object \| null` | no | `{ require_all[], require_any[] }`. Prefijo `"no:"` para NOT. Documentación ejecutable, no validación dura. |
| `excluye` | `list<str> \| null` | no | Tags incompatibles. |
| `peso` | `int` (0..50) | si `categoria = equipo` | Unidad: kg. |
| `peso_narrativo` | `int` (1..5) | no | Hint al sorteador procedural. |
| `atributo_dominante` | `str` \| `null` | si `categoria = skill` | `fis \| tac \| men`. |
| `tags_relacionados` | `list<str>` | no | Informativo. |
| `metadatos` | `object` | no | `{ creado_en, ultima_actualizacion }`. |

**PK sugerida**: tag completo en notación punto como string, o tupla `(categoria, subcategoria, slug)`.

**Índice operativo**: inverted index `tag_full → set<personaje.slug>` reconstruido desde `personaje.tags[]`.

**Categorías de referencia** (abiertas — enumeradas en [[sistema-tags|docs/sistema-tags.md]]): `faccion`, `subfaccion`, `rango`, `grupo`, `mando`, `estado`, `salud`, `mental`, `rasgo`, `trait`, `perk`, `efecto`, `skill`, `equipo` (`.arma` / `.utilitario` / `.vestidura`), `rol` (`.oficio` / `.jerarquia` / `.narrativo` / `.combate`), `lealtad`.

---

## 3. `grupo`

Agrupación táctica de personajes. Servido por `GET /grupos/{slug}`, modificado por altas/bajas de miembros.

| Campo | Tipo | Mutable | Notas |
|---|---|---|---|
| `identidad.slug` | `str` lowercase + underscore | inmutable | PK. Coincide con el segmento final del tag `grupo.{slug}`. |
| `identidad.nombre` | `str` | mutable | Nombre del grupo. |
| `identidad.faccion` | `str` (slug de `faccion`) | inmutable | Referencia a la facción. |
| `identidad.tipo` | `str` | inmutable | Tipo (ej. `escuadra_de_infanteria`, `celula_obrera`). |
| `miembros[]` | `list<miembro>` (embebida) | mutable | Lista ordenada de integrantes. |
| `historial[]` | `list<hito_grupo>` (embebida) | append-only | Log de eventos del grupo. |
| `metadatos.creado_en` | `str` ISO-8601 | inmutable | |
| `metadatos.ultima_actualizacion` | `str` ISO-8601 | actualiza con cada cambio | |
| `extras` | `object \| null` | libre | Escape hatch. |

### Campos derivados del grupo — computados al servir, no persistidos

- `fza_total` — suma de `fza_aportada` de miembros activos (no caídos).
- `cohesion_vigente` — promedio de `men` de miembros activos (redondeado hacia abajo). Penalizado con `(-2)` si el líder está caído/en licencia sin reemplazo; `(-1)` si el segundo al mando asume el mando vigente.
- `moral_promedio` — promedio entero de `moral_max` de todos los miembros activos.
- `fatiga_promedio` — promedio entero de `fatiga_max` de todos los miembros activos.
- `movimiento_tactico` — `min(MOVIMIENTO)` de los miembros activos.
- `puntos_totales` — suma de `puntos` de todos los miembros.
- `lider_vigente` — patente del personaje actualmente al mando.
- `estado_grupo` — `operativo | decapitado | desmembrado | retirado`.
- `cumple_template` — `bool`. Indica si la composición respeta las restricciones estructurales del `tipo`.
- `errores_validacion[]` — `list<str>`. Infracciones si `cumple_template` es `false`.

### 3.1. `miembro` (embebido en `grupo.miembros[]`)

| Campo | Tipo | Notas |
|---|---|---|
| `ref` | `str` `^[A-Z0-9]{8}$` | Patente del personaje. FK virtual. |
| `pos` | `int` | Orden táctico en la formación. |
| `puntos` | `int` | Costo en puntos de reclutamiento (escala 1..5). |
| `rango` | `str` | Slug de rango del personaje. |
| `nombre` | `str` | Nombre compuesto / de guerra. |
| `aspectos` | `list<str>` | Descriptores narrativos del miembro dentro del grupo. Mutable. Default `[]`. |

### 3.2. `hito_grupo` (embebido en `grupo.historial[]`)

| Campo | Tipo | Notas |
|---|---|---|
| `fecha` | `str` ISO-8601 | |
| `tipo` | `str` | Enum abierto: `baja_miembro`, `ascenso_miembro`, `combate_finalizado`, `reorganizacion`. |
| `descripcion` | `str` | Obligatorio. |
| `ref_batalla` | `str \| null` | Batalla de referencia si aplica. |
| `metadata` | `object` | Libre. |

---

## 4. `faccion`

| Campo | Tipo | Notas |
|---|---|---|
| `slug` | `str` minúscula + guion bajo | PK. |
| `nombre` | `str` | Legible. |
| `descripcion` | `str` | Descriptor de lore corto. |

Servido por `GET /meta/facciones`. Conjunto cerrado-curado: pocas facciones canónicas (`confederacion_argentina`, `ejercito_rojo`), todas referenciadas por `grupo.identidad.faccion` y por la tabla de rangos.

### 4.1. Relación `faccion` ↔ `subfaccion` (asimetría deliberada)

`faccion` y `subfaccion` no son simétricas:

| Aspecto | `faccion` | `subfaccion` |
|---|---|---|
| Naturaleza | Entidad de primera clase (esta §4). | Categoría de `tag_catalogo` (§2). |
| Cardinalidad | Cerrado-curado (2-3 hoy). | Abierto-emergente. |
| Endpoint | `GET /meta/facciones` (dedicado). | `GET /meta/subfaccion` (genérico `/meta/{categoria}`). |
| Referencia desde otras entidades | `grupo.identidad.faccion`; tabla de rangos. | Ninguna. Solo aparece en `personaje.tags[]`. |
| Membresía sobre personaje | Tag `faccion.{slug}` + `lealtad.faccion.{slug}`. | Tag `subfaccion.{slug}` + `lealtad.subfaccion.{slug}`. |

`faccion` ancla la geometría operativa del juego (grupos pertenecen a una facción; los rangos canónicos están definidos por facción; las batallas tienen bandos). Necesita identidad estable y endpoint dedicado. `subfaccion` agrupa narrativamente — un tercio, una célula, un sindicato armado — y el catálogo crece por curaduría a demanda.

**Dualidad entidad+tag**: tanto `faccion` como `grupo` son entidades persistidas y existen además como namespace de tag (`faccion.confederacion_argentina`, `grupo.{slug}`) para expresar membresía declarativa sobre `personaje.tags[]`. El slug del tag coincide con la clave primaria de la entidad.

---

## 5. Invariantes globales

- **`historial[]` es append-only.** No hay reversión de hito.
- **Efímeros no se persisten.** Un personaje generado pero no canonizado nunca toca la base de datos.
- **Canonización es idempotente con semilla.** La tupla `(semilla, faccion, rango)` actúa como clave única; reintentos no crean duplicados. Sin semilla, cada `POST /canonizar` genera un personaje nuevo.
- **Tags fuera de catálogo se aceptan.** Cualquier valor en `personaje.tags[]` que no exista en `tag_catalogo` es legal — se persiste tal cual. La curaduría del catálogo se hace por proceso, no por constraint.
- **Referencias en `aliados[]`/`nemesis[]` no son referencias de integridad.** Se aceptan referencias colgadas; la consistencia referencial no es responsabilidad de la capa de persistencia.
- **Idioma de los datos**: castellano rioplatense. Tags en minúscula + guion bajo, sin acentos. Campos YAML en `snake_case_castellano`.
- **`extras` es opaco.** La API lo acepta, almacena y devuelve tal cual, sin inspeccionar ni validar su contenido.
