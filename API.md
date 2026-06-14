---
title: API — syv-pj
tags:
  - syv/pj/api
aliases:
  - API
  - Contrato HTTP
---

# API — syv-pj

> [!info] Fuente de Verdad del Contrato HTTP
> Cualquier mención a rutas en [[PRD|PRD.md]], `docs/*` o fixtures se resuelve contra este archivo. Si una ruta no figura acá, no existe en el contrato.
>
> Los tipos de campo y reglas de mutabilidad viven en [[MODEL|MODEL.md]]. **Sincronía absoluta con [[MODEL|MODEL.md]].**
>
> Convenciones de carga: ver [[hoja-personaje|docs/hoja-personaje.md]] y [[sistema-tags|docs/sistema-tags.md]]. Castellano rioplatense, `snake_case_castellano`.

---

## Convención `GET /meta/{categoria}` — catálogos dinámicos

`GET /meta/{categoria}` devuelve el catálogo curado de esa categoría de tag. La estructura de cada entrada es la definida en [[sistema-tags|docs/sistema-tags.md]].

Las categorías curadas de referencia (`destreza`, `rasgo`, `ventaja`, `rasgo`, `equipo`, `rol`, etc.) se detallan en [[sistema-tags#Categorías de referencia|docs/sistema-tags.md]]. Categorías nuevas se exponen automáticamente bajo `/meta/{categoria}` desde que existen — no requieren entrada en este archivo.

Para sub-categorías: `GET /meta/equipo/arma`, `GET /meta/rol/oficio`, etc. La notación de la ruta usa barras (`/meta/equipo/arma`); la notación interna del tag usa punto (`equipo.arma`).

**Casos que NO siguen la convención genérica** (la carga difiere o agrega datos derivados):

- `GET /meta/facciones` — facciones con descriptor de lore corto (ver §5.1).
- `GET /meta/rangos` — rangos con tabla determinística de atributos y rol cultural por facción (ver §5.2).
- `GET /meta/tipos_hito` — enumeración sugerida de tipos de hito; catálogo abierto (ver §5.3).
- `GET /meta/encuentro/nuevo` — generador de patente de encuentro, no un catálogo (ver §6.1).

---

## 1. Personajes

### `GET /personaje`

Genera un personaje **efímero**. Parámetros opcionales vía cadena de consulta:

| Parámetro | Tipo | Notas |
|---|---|---|
| `faccion` | `str` | Slug de facción. |
| `rango` | `str` | Slug de rango. |
| `semilla` | `str` | Semilla para reproducibilidad. `(semilla, faccion, rango)` reproduce el mismo efímero. |
| `campos` | `str` CSV de rutas de punto | Poda la respuesta. Ej: `campos=identidad.slug,atributos.fis`. |
| `tag` | `str` (repetible) | Filtrado en AND lógico. El efímero debe portar todos los tags exigidos. OR no está soportado — el cliente lo resuelve con N llamadas + unión. |

Devuelve un `personaje` con:
- `identidad.slug: null` (los efímeros no tienen slug hasta canonizarse).
- `historial: []`, `aliados: []`, `nemesis: []`.
- `metadatos.canonizado_en: null`.
- Tags mínimos `estado.disponible` y `grupo.*` si corresponde.

Si la combinación de tags exigidos es inviable, devuelve **409**.

Incluye los campos derivados (`es_canon`, `fatiga_max`, `moral_max`, `fza_aportada`, `filiacion`) calculados en tiempo real.

### `GET /personaje/{slug}`

Devuelve la ficha vigente del personaje con `identidad.slug` exacto. 404 si no existe. Acepta `campos=` (rutas de punto CSV) para podar la respuesta. Incluye los campos derivados definidos en [[MODEL#1. personaje|MODEL.md §1]].

### `GET /personaje/{slug}/historial`

Devuelve solo `historial[]` del personaje. Sin paginación en v1.

### `POST /personaje/{slug}/evento`

Registra un hito sobre un personaje canonizado. Cuerpo: una entrada de `hito` (estructura en [[hoja-personaje#Historial|docs/hoja-personaje.md]]).

Efecto: añade el hito, aplica su efecto sobre los campos vigentes, actualiza `metadatos.ultima_actualizacion`, devuelve la ficha actualizada.

- **404** si el slug no existe.
- **409** si el personaje es una prueba inmutable (mocks).

Tipos de hito y sus efectos sobre la ficha:

| Tipo | Efecto sobre la ficha |
|---|---|
| `agregar_tag` | Añade `metadata.valor` a `tags[]`. |
| `quitar_tag` | Elimina primera ocurrencia de `metadata.valor` de `tags[]`. |
| `mejora_atributo` | Incrementa `atributos.{metadata.atributo}` en `metadata.delta`. |
| `triple_cero` | Modifica `atributos.{metadata.atributo}` según la regla del triple-cero. |
| `ascenso` / `cambio_rol` | Actualiza `identidad.rol`. |
| `formacion_lealtad` | Añade entrada a `aliados[]`. |
| `identificacion_nemesis` | Añade entrada a `nemesis[]`. |
| Otros tipos | Solo añaden el hito. Los efectos colaterales son responsabilidad del cliente. |

### `POST /canonizar`

Persiste un personaje efímero como canonizado. Cuerpo: la carga del efímero (resultado de `GET /personaje`).

Efecto: asigna `identidad.slug` (patente `^[A-Z0-9]{8}$` generada en el servidor), congela `historia`, fija `metadatos.canonizado_en` con la marca de tiempo actual. Devuelve la ficha canonizada.

Idempotente por `(semilla, faccion, rango)`: si ya existe un canonizado con esa combinación, devuelve el existente sin crear duplicado.

---

## 2. Grupos

### `GET /grupos`

Lista todos los grupos persistidos. Acepta parámetro opcional `faccion` para filtrar por slug de facción.

### `GET /grupos/{slug}`

Devuelve la ficha detallada del grupo. Incluye `identidad`, `miembros[]`, `historial[]` y todos los campos derivados (`fza_total`, `cohesion_vigente`, `moral_promedio`, `fatiga_promedio`, `movimiento_tactico`, `puntos_totales`, `lider_vigente`, `estado_grupo`, `cumple_template`, `errores_validacion[]`).

### `POST /grupos`

Crea y persiste un nuevo grupo. Cuerpo:

```yaml
identidad:
  nombre: str
  faccion: str          # slug de facción
  tipo: str             # tipo de grupo (ej. escuadra_de_infanteria)
miembros: []            # opcional; lista inicial de miembro
```

### `POST /grupos/{slug}/miembro`

Añade un personaje como miembro del grupo. Cuerpo:

```yaml
ref: str                # patente del personaje ^[A-Z0-9]{8}$
pos: int                # orden táctico en la formación
puntos: int             # costo en puntos de reclutamiento (1..5)
aspectos: []            # opcional; valor por defecto []
```

Efectos colaterales:
- Añade la entrada de `miembro` a `grupo.miembros[]`.
- Añade los tags `grupo.{slug}` y `lealtad.grupo.{slug}` a la ficha del personaje.
- Registra un hito `asignacion_grupo` en `personaje.historial[]` y un hito `incorporacion_miembro` en `grupo.historial[]`.

### `DELETE /grupos/{slug}/miembro/{char_slug}`

Remueve a un miembro del grupo.

Efectos colaterales:
- Quita la referencia de `grupo.miembros[]`.
- Elimina los tags `grupo.{slug}` y `lealtad.grupo.{slug}` del personaje.
- Registra un hito `traslado` en `personaje.historial[]` y un hito `reorganizacion` en `grupo.historial[]`.

---

## 3. Generación procedural

### `GET /generar`

Equivalente semántico de `GET /personaje` con énfasis en el flujo completo de generación. Acepta los mismos parámetros (`faccion`, `rango`, `semilla`, `campos`, `tag`).

Internamente ejecuta las cuatro fases de generación procedural documentadas en [[generacion-procedural|docs/generacion-procedural.md]]:

1. Identidad sorteada (nombre, género, edad desde pools).
2. Atributos determinísticos por rol/rango desde tabla de configuración.
3. Tags sorteados ponderados desde catálogo.
4. Prosa generada por LLM (120–200 palabras).

Devuelve la misma carga que `GET /personaje`: un efímero listo para ser canonizado con `POST /canonizar`.

---

## 4. Canonización

### `POST /canonizar`

Ver §1 — el endpoint vive bajo personajes porque la canonización es el acto de persistir un personaje.

---

## 5. Catálogos `/meta/*`

### 5.1. `GET /meta/facciones`

Devuelve las facciones canónicas. Cada entrada:

```yaml
slug: str
nombre: str
descripcion: str        # descriptor de lore corto
```

### 5.2. `GET /meta/rangos`

Devuelve los rangos operativos con su tabla determinística de atributos base y rol cultural por facción. Cada entrada:

```yaml
slug: str
nombre: str
faccion: str            # slug de facción; rangos son específicos de facción
atributos_base:
  fis: int
  tac: int
  men: int
mando_default: str      # slug de rango inmediato superior
rol_cultural: str       # título usado por esa facción (ej. "Camarada Puntero" vs "Sargento")
```

### 5.3. `GET /meta/tipos_hito`

Devuelve la enumeración sugerida de tipos de hito. Lista abierta — el servidor la sirve, el cliente puede usar tipos fuera de esta lista.

### 5.4. `GET /meta/{categoria}`

Ver convención genérica al inicio de este documento. Devuelve las entradas de `tag_catalogo` para esa categoría.

---

## 6. Encuentro (entidad implícita)

### 6.1. `GET /meta/encuentro/nuevo`

Genera y devuelve una patente opaca de encuentro para uso en el estado volátil de combate de los miembros del grupo.

Respuesta:

```yaml
patente: str            # ^[A-Z0-9]{8}$; único contra patentes ya vistas
```

Sin parámetros. Sin efectos colaterales: `syv-pj` no persiste la patente en una tabla de encuentros; solo garantiza no repetirla. El motor de batalla que consume esta API es responsable de modelar el encuentro como entidad si lo necesita.

---

## 7. Tabla plana de endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/personaje` | Genera un personaje efímero |
| GET | `/personaje/{slug}` | Ficha vigente del canonizado |
| GET | `/personaje/{slug}/historial` | Historial del canonizado |
| POST | `/personaje/{slug}/evento` | Registra un hito |
| POST | `/canonizar` | Persiste un efímero como canonizado |
| GET | `/generar` | Flujo completo de generación procedural |
| GET | `/grupos` | Lista grupos persistidos |
| GET | `/grupos/{slug}` | Ficha detallada del grupo |
| POST | `/grupos` | Crea un grupo |
| POST | `/grupos/{slug}/miembro` | Añade un miembro al grupo |
| DELETE | `/grupos/{slug}/miembro/{char_slug}` | Remueve un miembro del grupo |
| GET | `/meta/{categoria}` | Catálogo de una categoría de tag |
| GET | `/meta/facciones` | Facciones canónicas con lore |
| GET | `/meta/rangos` | Rangos con tabla determinística de atributos |
| GET | `/meta/tipos_hito` | Enumeración sugerida de tipos de hito |
| GET | `/meta/encuentro/nuevo` | Genera patente de encuentro |

Catálogo completo de casos de uso en [[casos-de-uso|docs/casos-de-uso.md]].
