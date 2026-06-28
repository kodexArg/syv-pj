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

Tres entidades persistidas: `personaje`, `tag_catalogo`, `faccion`. Una colección embebida: `hito`. Destrezas, rasgos, ventajas, equipo y los **vínculos** (lealtades, aliados, némesis) son **tags** y viven como entradas de `tag_catalogo` o como referencias relacionales en `personaje.tags[]`.

---

## 1. `personaje`

Resource principal. Servido por `GET /personaje/{slug}`, mutado por `POST /personaje/{slug}/evento`, creado por `POST /canonizar`.

| Campo | Tipo | Mutable | Notas |
|---|---|---|---|
| `identidad.slug` | `str` `^[A-Z0-9]{8}$` \| `null` | fijado una vez | PK. `null` en efímeros. Asignada por el servidor al canonizar. |
| `identidad.nombre` | `str` | inmutable | Legible. No único. |
| `identidad.sobrenombre` | `str \| null` | mutable (sin hito) | `null` si no aplica. |
| `identidad.especialidad` | `str \| null` | mutable vía hito `ascenso` / `cambio_especialidad` | Especialidad táctica (lo que *hace*: fusilero, médico, inquisidor…). `null` si no tiene; la vocación de pertenencia la da el `rango`. Narrativo. |
| `identidad.genero` | `str` | inmutable | Catálogo abierto: `masculino \| femenino \| no_binario \| otro`. |
| `identidad.edad` | `int` | mutable (sin hito) | Decisión narrativa. |
| `atributos.cuerpo` | `int` (2..7) | vía hito `triple_cero` / `mejora_atributo` | Escala 2..7. En prosa: Físico. (← viejo `fis`.) |
| `atributos.mente` | `int` (2..7) | vía hito `triple_cero` / `mejora_atributo` | Escala 2..7. Puntería, reflejos, lectura táctica. (← viejo `tac`.) |
| `atributos.alma` | `int` (2..7) | vía hito `triple_cero` / `mejora_atributo` | Escala 2..7. Aura, liderazgo, voluntad, temple. En prosa: Espíritu. (← viejo `men`.) |
| `apariencia` | `list<str>` | mutable (sin hito) | Descriptores visuales libres, sparse, agnósticos al generador de imágenes. Persistido; NO entra al índice invertido de tags. Ver [[hoja-personaje#§2.5 — Apariencia]] y `docs/apariencia.md`. **Pendiente de exponer en `API.md` + contrato Pydantic (downstream).** |
| `tags[]` | `list<str>` (no multiconjunto) | vía hito `agregar_tag` / `quitar_tag` | Notación punto `<categoria>[.<subcategoria>].<slug>`. NO admite repetidos: ante un repetido gana el último valor. Incluye los vínculos relacionales `lealtad/*` / `aliado/*` / `nemesis/*` (ver §1.2). |
| `historia` | `str` | inmutable tras canonizar | 120–200 palabras. Congelada al canonizar. |
| `historial[]` | `list<hito>` (embebida) | de solo añadir vía `POST /evento` | Ver §1.1. |
| `metadatos.creado_en` | `str` ISO-8601 | inmutable | |
| `metadatos.canonizado_en` | `str` ISO-8601 \| `null` | fijado una vez | `null` en efímeros. |
| `metadatos.ultima_actualizacion` | `str` ISO-8601 | actualiza con cada hito | |
| `extras` | `object \| null` | libre | Válvula de escape. La API no inspecciona. |

### Campos derivados — computados al servir, no persistidos

- `es_canon` — `canonizado_en != null`.
- `fatiga_max` = `cuerpo + alma`.
- `moral_max` = `alma`.
- `fza_aportada` — desde tags `especialidad/combate/*` (`heroe: 3`, `lider: 2`, valor por defecto `1`).
- `filiacion` — desde tags `rango/*` + `faccion/*`.

Aparecen en la respuesta de `GET /personaje` y `GET /personaje/{slug}` junto con los campos persistidos. Se recomputan en cada lectura; el cliente no los muta directamente.

### 1.1. `hito` (embebido en `personaje.historial[]`)

| Campo | Tipo | Notas |
|---|---|---|
| `fecha` | `str` ISO-8601 | |
| `tipo` | `str` | Catálogo abierto sugerido. Ver [[historial|docs/historial.md]]. |
| `actores` | `list<str>` (patentes `^[A-Z0-9]{8}$`) | Personajes involucrados en el evento. Por defecto `[]`. Sin integridad referencial (ver §4). |
| `descripcion` | `str` | Obligatorio. |
| `encuentro` | `str \| null` | Patente de batalla/encuentro externo; referencia narrativa. |
| `metadata` | `object` | Libre. Convención: `{ atributo, delta, valor_anterior, valor_nuevo }` para mejoras; `{ categoria, valor }` para agregar/quitar tag. A futuro puede portar adjuntos. |

Tipos de hito sugeridos (catálogo abierto): `combate`, `ascenso`, `cambio_especialidad`, `triple_cero`, `mejora_atributo`, `agregar_tag`, `quitar_tag`, `formacion_lealtad`, `identificacion_nemesis`, `licencia`, `desercion`, `muerte`.

### 1.2. Vínculos relacionales (tags `lealtad/*` / `aliado/*` / `nemesis/*`)

Los vínculos del personaje **no son una colección aparte**: son **tags relacionales** dentro de `personaje.tags[]`, en forma plana `<categoria>.<slug>`.

| Categoría | Significado | Destino del `<slug>` |
|---|---|---|
| `lealtad` | Adhesión institucional o personal vigente. | Facción, subfacción, grupo, religión o personaje (patente). |
| `aliado` | Alianza personal vigente. | Personaje (patente), facción, subfacción o grupo. |
| `nemesis` | Enemistad vigente, sin restricción de bando. | Ídem `aliado`. |

- El `<slug>` es una **referencia**: patente `^[A-Z0-9]{8}$` para personajes, slug legible de catálogo para entidades. Sin imposición de integridad referencial (ver §4).
- La **prosa** del vínculo (cómo se formó) vive en el `hito` que lo introdujo (`formacion_lealtad` / `identificacion_nemesis`), no en el tag. La fecha del vínculo es la `fecha` de ese hito.
- Se agregan/quitan como cualquier tag. Detalle en [[lealtad|docs/lealtad.md]] y [[nemesis-y-aliados|docs/nemesis-y-aliados.md]].

---

## 2. `tag_catalogo`

Catálogo curado de tags. Servido por `GET /meta/{categoria}`. El catálogo se siembra desde archivos de definición al arrancar el servidor.

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `slug` | `str` minúsculas + guion bajo | sí | Último segmento del tag. Sin acentos. |
| `nombre` | `str` | sí | Nombre legible para humanos. |
| `categoria` | `str` | sí | Primer segmento del tag en notación punto. |
| `subcategoria` | `str \| null` | condicional | Obligatorio si `categoria ∈ {equipo, especialidad}`. Segmento intermedio. |
| `descripcion` | `str` | sí | 1–3 frases. |
| `origen` | `str` | no (por defecto `emergente`) | Catálogo: `canon \| emergente \| custom`. |
| `efecto` | `str \| list<str> \| null` | condicional | Obligatorio si `categoria = rasgo` (sin `trigger`) o `categoria = efecto`. Modificadores sobre vocabulario canónico. Ver [[atributos-y-habilidades|docs/atributos-y-habilidades.md]]. |
| `trigger` | `object \| null` | no | `{ evento, condicion, probabilidad?, trigger_action[] }`. Efectos reactivos. |
| `requires` | `object \| null` | no | `{ require_all[], require_any[] }`. Prefijo `"no:"` para NOT. Documentación ejecutable, no validación dura. |
| `excluye` | `list<str> \| null` | no | Tags incompatibles. |
| `peso` | `int` (0..50) | si `categoria = equipo` | Unidad: kg. |
| `peso_narrativo` | `int` (1..5) | no | Pista al sorteador procedural. |
| `atributo_dominante` | `str` \| `null` | si `categoria = habilidad` | `cuerpo \| mente \| alma`. |
| `tags_relacionados` | `list<str>` | no | Informativo. |
| `metadatos` | `object` | no | `{ creado_en, ultima_actualizacion }`. |

**Clave primaria sugerida**: tag completo en notación punto como cadena, o tupla `(categoria, subcategoria, slug)`.

**Índice operativo**: índice invertido `tag_full → set<personaje.slug>` reconstruido desde `personaje.tags[]`.

**Categorías de referencia** (abiertas — enumeradas en [[sistema-tags|docs/sistema-tags.md]]): `faccion`, `subfaccion`, `rango`, `mando`, `estado`, `salud`, `mental`, `rasgo`, `ventaja`, `destreza`, `efecto`, `equipo` (`.arma` / `.utilitario` / `.vestidura`), `especialidad` (`.oficio` / `.jerarquia` / `.narrativo` / `.combate`), y las relacionales `lealtad`, `aliado`, `nemesis`.

---

## 3. `faccion`

| Campo | Tipo | Notas |
|---|---|---|
| `slug` | `str` minúscula + guion bajo | PK. |
| `nombre` | `str` | Legible. |
| `descripcion` | `str` | Descriptor de lore corto. |

Servido por `GET /meta/facciones`. Conjunto cerrado-curado: pocas facciones canónicas (`confederacion_argentina`, `ejercito_rojo`), todas referenciadas por la tabla de rangos.

### 3.1. Relación `faccion` ↔ `subfaccion` (asimetría deliberada)

`faccion` y `subfaccion` no son simétricas:

| Aspecto | `faccion` | `subfaccion` |
|---|---|---|
| Naturaleza | Entidad de primera clase (esta §3). | Categoría de `tag_catalogo` (§2). |
| Cardinalidad | Cerrado-curado (2-3 hoy). | Abierto-emergente. |
| Ruta | `GET /meta/facciones` (dedicado). | `GET /meta/subfaccion` (genérico `/meta/{categoria}`). |
| Referencia desde otras entidades | Tabla de rangos. | Ninguna. Solo aparece en `personaje.tags[]`. |
| Membresía sobre personaje | Tag `faccion.{slug}` + `lealtad.{slug}`. | Tag `subfaccion.{slug}` + `lealtad.{slug}`. |

`faccion` ancla la geometría operativa del juego (los rangos canónicos están definidos por facción; las batallas tienen bandos). Necesita identidad estable y ruta dedicada. `subfaccion` agrupa narrativamente — un tercio, una célula, un sindicato armado — y el catálogo crece por curaduría a demanda.

**Dualidad entidad+tag**: `faccion` es entidad persistida y existe además como namespace de tag (`faccion/confederacion_argentina`) para expresar membresía declarativa sobre `personaje.tags[]`. El slug del tag coincide con la clave primaria de la entidad.

---

## 4. Invariantes globales

- **`historial[]` es de solo añadir.** No hay reversión de hito.
- **Efímeros no se persisten.** Un personaje generado pero no canonizado nunca toca la base de datos.
- **Canonización es idempotente con semilla.** La tupla `(semilla, faccion, rango)` actúa como clave única; reintentos no crean duplicados. Sin semilla, cada `POST /canonizar` genera un personaje nuevo.
- **Tags fuera de catálogo se aceptan.** Cualquier valor en `personaje.tags[]` que no exista en `tag_catalogo` es legal — se persiste tal cual. La curaduría del catálogo se hace por proceso, no por constraint.
- **Las referencias de los tags relacionales (`lealtad/*`/`aliado/*`/`nemesis/*`) y de `historial[].actores[]` no son referencias de integridad.** Se aceptan referencias colgadas; la consistencia referencial no es responsabilidad de la capa de persistencia.
- **Idioma de los datos**: castellano rioplatense. Tags en minúscula + guion bajo, sin acentos. Campos YAML en `snake_case_castellano`.
- **`extras` es opaco.** La API lo acepta, almacena y devuelve tal cual, sin inspeccionar ni validar su contenido.
