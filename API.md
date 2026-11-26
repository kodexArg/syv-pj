---
title: API — syv-pj
tags:
  - syv/pj/api
aliases:
  - API
  - Contrato HTTP
---

# API — syv-pj

> [!NOTE]
> **Fuente de Verdad del Contrato HTTP**
>
> Cualquier mención a rutas en [PRD.md](PRD.md), `docs/*` o datos de ejemplo se resuelve contra este archivo. Si una ruta no figura acá, no existe en el contrato.
>
> Los tipos de campo y reglas de mutabilidad viven en [MODEL.md](MODEL.md). **Sincronía absoluta con [MODEL.md](MODEL.md).**
>
> Convenciones de carga: ver [docs/hoja-personaje.md](docs/hoja-personaje.md) y [docs/sistema-tags.md](docs/sistema-tags.md). Castellano rioplatense, `snake_case_castellano`.

---

## Convención `GET /meta/{categoria}` — catálogos dinámicos

`GET /meta/{categoria}` devuelve el catálogo curado de esa categoría de tag. La estructura de cada entrada es la definida en [docs/sistema-tags.md](docs/sistema-tags.md).

Las categorías curadas de referencia (`destreza`, `rasgo`, `ventaja`, `equipo`, `especialidad`, etc.) se detallan en [docs/sistema-tags.md](docs/sistema-tags.md#3--categorías-de-referencia). Categorías nuevas se exponen automáticamente bajo `/meta/{categoria}` desde que existen — no requieren entrada en este archivo.

Para sub-categorías: `GET /meta/equipo/arma`, `GET /meta/especialidad/oficio`, etc. La ruta y el tag interno comparten la **misma notación de barras**: `/meta/equipo/arma` carga el catálogo del tag `equipo/arma`. (Los `campos=` de poda siguen usando puntos —`identidad.slug`—, porque direccionan el árbol de la respuesta, no tags.)

**Casos que NO siguen la convención genérica** (la carga difiere o agrega datos derivados):

- `GET /meta/facciones` — facciones con descriptor de lore corto (ver §4.1).
- `GET /meta/rangos` — rangos con tabla determinística de atributos por facción (ver §4.2).
- `GET /meta/tipos_hito` — enumeración sugerida de tipos de hito; catálogo abierto (ver §4.3).
- `GET /meta/encuentro/nuevo` — generador de patente de encuentro, no un catálogo (ver §5.1).

---

## 1. Personajes

### `GET /personaje`

Genera un personaje **efímero**. Parámetros opcionales vía cadena de consulta:

| Parámetro | Tipo | Notas |
|---|---|---|
| `faccion` | `str` | Slug de facción. |
| `rango` | `str` | Slug de rango. |
| `semilla` | `str` | Semilla para reproducibilidad. `(semilla, faccion, rango)` reproduce el mismo efímero. |
| `campos` | `str` CSV de rutas de punto | Poda la respuesta. Ej: `campos=identidad.slug,atributos.cuerpo`. |
| `tag` | `str` (repetible) | Filtrado en Y lógico. El efímero debe portar todos los tags exigidos. OR no está soportado — el cliente lo resuelve con N llamadas + unión. |

Devuelve un `personaje` con:
- `identidad.slug: null` (los efímeros no tienen slug hasta canonizarse).
- `historial: []` (sin tags de vínculo `aliado/*` / `nemesis/*` todavía).
- `metadatos.canonizado_en: null`.
- Tag mínimo `estado/disponible`.

Si la combinación de tags exigidos es inviable, devuelve **409**.

Incluye los campos derivados (`es_canon`, `fatiga_max`, `moral_max`, `fza_aportada`, `filiacion`) calculados en tiempo real.

### `GET /personaje/{slug}`

Devuelve la ficha vigente del personaje con `identidad.slug` exacto. 404 si no existe. Acepta `campos=` (rutas de punto CSV) para podar la respuesta. Incluye los campos derivados definidos en [MODEL.md §1](MODEL.md#1-personaje).

### `GET /personaje/{slug}/historial`

Devuelve solo `historial[]` del personaje. Sin paginación en v1.

### `GET /personaje/{slug}/workflow`

Devuelve el **workflow de ComfyUI** (formato API-JSON, listo para `POST /prompt`)
que genera el retrato del personaje canonico. 404 si el slug no existe.

Determinista: la `semilla` del personaje fija el `seed` del sampler; los `tags`
del personaje fijan el `lora_stack`; no hay aleatoriedad en la composicion del
workflow. El campo `prompt` de cada nodo `CLIPTextEncode` es un ensamblado
determinista de tres bloques fijos (estilo comun, personaje, cierre comun) mas
un cuerpo especifico al personaje (identidad + LoRAs + vestimenta) — ver
`docs/prompt-imagen.md` para el detalle del template.

Respuesta: `application/json`, el grafo de nodos ComfyUI verbatim (claves
numericas de nodo → `class_type`/`inputs`), no envuelto en el contrato
`personaje` existente.

### `POST /personaje/{slug}/evento`

Registra un hito sobre un personaje canonizado. Cuerpo: una entrada de `hito` (estructura en [docs/historial.md](docs/historial.md)).

Efecto: añade el hito, aplica su efecto sobre los campos vigentes, actualiza `metadatos.ultima_actualizacion`, devuelve la ficha actualizada.

- **404** si el slug no existe.
- **409** si el personaje es un personaje de ejemplo inmutable.

Tipos de hito y sus efectos sobre la ficha:

| Tipo | Efecto sobre la ficha |
|---|---|
| `agregar_tag` | Añade `metadata.valor` a `tags[]`; si ya existe, gana el último valor (no se duplica). |
| `quitar_tag` | Elimina `metadata.valor` de `tags[]`. |
| `mejora_atributo` | Incrementa `atributos.{metadata.atributo}` en `metadata.delta`. |
| `triple_cero` | Modifica `atributos.{metadata.atributo}` según la regla del triple-cero. |
| `ascenso` / `cambio_especialidad` | Actualiza `identidad.especialidad`. |
| `formacion_lealtad` | Añade el tag `aliado.<ref>` (o `lealtad.<ref>`) a `tags[]`; la prosa del vínculo viaja en `descripcion`. |
| `identificacion_nemesis` | Añade el tag `nemesis.<ref>` a `tags[]`; la prosa del vínculo viaja en `descripcion`. |
| Otros tipos | Solo añaden el hito. Los efectos colaterales son responsabilidad del cliente. |

> [!NOTE]
> **`actores[]` y `encuentro` se registran tal cual**
>
> Ningún tipo de hito deriva efectos de `actores[]` ni de `encuentro`: se persisten en el hito sin tocar la ficha vigente. Alimentan la línea de tiempo y el grafo de Diégesis (ver [docs/historial.md §4](docs/historial.md)).

### `POST /canonizar`

Persiste un personaje efímero como canonizado. Cuerpo: la carga del efímero (resultado de `GET /personaje`).

Efecto: asigna `identidad.slug` (patente `^[A-Z0-9]{8}$` generada en el servidor), congela `historia`, fija `metadatos.canonizado_en` con la marca de tiempo actual. Devuelve la ficha canonizada.

Idempotente por `(semilla, faccion, rango)`: si ya existe un canonizado con esa combinación, devuelve el existente sin crear duplicado.

---

## 2. Generación procedural

### `GET /generar`

Equivalente semántico de `GET /personaje` con énfasis en el flujo completo de generación. Acepta los mismos parámetros (`faccion`, `rango`, `semilla`, `campos`, `tag`).

Internamente ejecuta las cuatro fases de generación procedural documentadas en [docs/generacion-procedural.md](docs/generacion-procedural.md):

1. Identidad sorteada (nombre, género, edad desde depósitos).
2. Atributos determinísticos por rango desde tabla de configuración.
3. Tags sorteados ponderados desde catálogo.
4. Prosa generada por LLM (120–200 palabras).

Devuelve la misma carga que `GET /personaje`: un efímero listo para ser canonizado con `POST /canonizar`.

---

## 3. Canonización

### `POST /canonizar`

Ver §1 — la ruta vive bajo personajes porque la canonización es el acto de persistir un personaje.

---

## 4. Catálogos `/meta/*`

### 4.1. `GET /meta/facciones`

Devuelve las facciones canónicas. Cada entrada:

```yaml
slug: str
nombre: str
descripcion: str        # descriptor de lore corto
```

### 4.2. `GET /meta/rangos`

Devuelve los rangos operativos con su tabla determinística de atributos base por facción. Cada entrada:

```yaml
slug: str
nombre: str
faccion: str            # slug de facción; rangos son específicos de facción
atributos_base:
  cuerpo: int
  mente: int
  alma: int
mando_default: str      # slug de rango inmediato superior
```

### 4.3. `GET /meta/tipos_hito`

Devuelve la enumeración sugerida de tipos de hito. Lista abierta — el servidor la sirve, el cliente puede usar tipos fuera de esta lista.

### 4.4. `GET /meta/{categoria}`

Ver convención genérica al inicio de este documento. Devuelve las entradas de `tag_catalogo` para esa categoría.

---

## 5. Encuentro (entidad implícita)

### 5.1. `GET /meta/encuentro/nuevo`

Genera y devuelve una patente opaca de encuentro, referenciable desde el campo `encuentro` de un hito de `personaje.historial[]` (ver [docs/historial.md](docs/historial.md)).

Respuesta:

```yaml
patente: str            # ^[A-Z0-9]{8}$; único contra patentes ya vistas
```

Sin parámetros. Sin efectos colaterales: `syv-pj` no persiste la patente en una tabla de encuentros; solo garantiza no repetirla. El motor de batalla que consume esta API es responsable de modelar el encuentro como entidad si lo necesita.

---

## 6. Tabla plana de endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/personaje` | Genera un personaje efímero |
| GET | `/personaje/{slug}` | Ficha vigente del canonizado |
| GET | `/personaje/{slug}/historial` | Historial del canonizado |
| POST | `/personaje/{slug}/evento` | Registra un hito |
| POST | `/canonizar` | Persiste un efímero como canonizado |
| GET | `/generar` | Flujo completo de generación procedural |
| GET | `/meta/{categoria}` | Catálogo de una categoría de tag |
| GET | `/meta/facciones` | Facciones canónicas con lore |
| GET | `/meta/rangos` | Rangos con tabla determinística de atributos |
| GET | `/meta/tipos_hito` | Enumeración sugerida de tipos de hito |
| GET | `/meta/encuentro/nuevo` | Genera patente de encuentro |

Catálogo completo de casos de uso en [docs/casos-de-uso.md](docs/casos-de-uso.md).
