---
title: "Hoja de Personaje — el documento núcleo"
tags:
  - syv/pj/esquema
  - syv/pj/nucleo
aliases:
  - Hoja de Personaje
  - hoja-personaje
  - esquema del personaje
---

# Hoja de Personaje

> [!info] Qué es este documento
> El **núcleo** de `syv-pj`: define la hoja de personaje campo por campo. Todo lo demás lo referencia. Acá vive el contrato estructural; los ejes que se ramifican tienen su propio documento hermano.
>
> **Documentos hermanos**:
> - [[sistema-tags|sistema-tags.md]] — la lista plana `tags[]`: notación, categorías, catálogo y curaduría.
> - [[atributos-y-habilidades|atributos-y-habilidades.md]] — escalas de `fis/tac/men`, estadísticas derivadas y vocabulario canónico de efectos.
> - [[contratos|contratos.md]] — aspectos, habilidades, destrezas y efectos como contratos.
> - [[generacion-procedural|generacion-procedural.md]] — cómo se completa una hoja desde el azar portable.
> - [[diegesis-y-obsidian|diegesis-y-obsidian.md]] — cómo la hoja se vuelve nodo navegable del vault de Diégesis.

---

## §0 — Estructura de la hoja

La hoja del personaje es la **entidad mínima** de *Subordinación y Valor*. Un mismo personaje homogeneizado sirve para Diégesis, estrategia, rol y generación visual sin cambiar de forma: la hoja clasifica, almacena y entrega; el consumidor decide el uso.

Seis bloques estructurales, dos colecciones persistidas y una lista plana de tags:

```yaml
personaje:
  identidad:    { slug, nombre, sobrenombre, rol, genero, edad }
  atributos:    { fis, tac, men }   # únicas magnitudes numéricas persistidas
  tags:         [...]               # lista plana, notación punto, NO multiconjunto (último valor gana)
  historia:     str                 # prosa biográfica, congelada al canonizar
  historial:    [...]               # hitos temporales (registro de eventos, de solo añadir)
  aliados:      [...]               # {ref, descripcion, desde?} — vínculo con prosa
  nemesis:      [...]               # {ref, descripcion, desde?}
  metadatos:    { creado_en, canonizado_en, ultima_actualizacion }
  extras:       object | null       # válvula de escape para clientes
```

> [!tip] Regla rectora — lo discreto es etiqueta
> Todo lo que es **discreto** y no es identidad, atributo, prosa, auditoría o vínculo-personal-con-prosa → ==es etiqueta==.
> Esa única regla decide dónde va cada dato nuevo. Si dudás entre crear un campo o una etiqueta, casi siempre es etiqueta. La justificación detallada vive en [[sistema-tags|sistema-tags.md]].

> [!note] Tres clases de dato
> La hoja distingue tres clases que no hay que confundir:
> - **Persistido** — se guarda al canonizar y solo cambia por las reglas de su bloque (`identidad`, `atributos`, `tags`, `historia`, `historial`, `aliados`, `nemesis`, `metadatos`, `extras`).
> - **Derivado-no-persistido** — se calcula en caliente al servir y nunca se guarda, para evitar desincronización (`filiacion`, `fatiga_max`, `moral_max`, `fza_aportada`, `sobrenombre` cuando es derivable, `es_canon`).
> - **Volátil** — vive solo durante un encuentro y no es parte de la hoja persistida (estados de combate; viven en el motor de batalla, no acá).

---

## §1 — Identidad

Quién es el personaje, fuera de su contexto operativo. La capa operativa (rango, escuadra, mando, equipo, lealtades) vive en `tags[]`, no acá.

### 1.1. `slug` — la patente del personaje

El `slug` es la ==patente opaca== del personaje. **No es su nombre.** Es el identificador estable que el sistema usa para referenciarlo en cualquier vínculo: entradas de `aliados[].ref` y `nemesis[].ref` (ver [[#§3.4 — Aliados y némesis|§3.4]]), refs de hitos, ediciones por API, nodos del vault.

```yaml
slug:
  formato:     ^[A-Z0-9]{8}$          # patente opaca, ej. K9F2H3M4
  ejemplos:    [K9F2H3M4, SLG3D7K2, NMC8H5P9]
  generacion:  El servidor genera al persistir (random + chequeo de colisión).
  custom:      Admitido para datos de ejemplo o curaduría manual; mismo regex, mismo chequeo.
  mutable:     false
```

> [!note] Por qué patente y no nombre
> Dos personajes pueden llamarse igual; sus patentes no colisionan. Una refactorización narrativa (cambio de apellido por casamiento, alias revolucionario) no invalida refs existentes. Los renderers muestran `nombre`; los sistemas guardan `slug`.

> [!info] Patente opaca ≠ slug de catálogo
> El `slug` del personaje es opaco (`^[A-Z0-9]{8}$`) precisamente para ser estable y predecible a escala. Los slugs de catálogo (tags, facciones, escuadras) son legibles (`lowercase_con_underscore`, ej. `pistola`, `ejercito_rojo`). La asimetría es deliberada: la patente es para máquinas; el slug legible es la pieza humana de la notación punto. Ver [[sistema-tags|sistema-tags.md]].

### 1.2. Resto del bloque

```yaml
nombre:
  tipo:    string
  ejemplo: "Walter Aguirre"
  mutable: false                       # inmutable tras canonizar

sobrenombre:
  tipo:       string | null
  derivacion: Derivable al servir desde nombre + tags de rango y de mando.
  nota:       null cuando no hay distinción con el nombre real.

rol:
  tipo:       string
  default:    ciudadano
  proposito:  Identidad narrativa base (no posición operativa).
  ejemplos:   ["Sargento Confederado", "Líder Revolucionario", "Médico de campaña"]
  aclaracion: NO confundir con tags rol.* — esos viven en tags[] y expresan la capa operativa.

género:
  tipo:        string
  enum_abierto: [masculino, femenino, no_binario, otro]
  mutable:     false

edad:
  tipo:    int
  nota:    Años al momento de creación. Mutable por decisión narrativa explícita, sin hito formal.
```

---

## §2 — Atributos

Tres valores numéricos que definen la capacidad base, en escala `2..7` (entero, más es mejor). Son las ==únicas magnitudes numéricas persistidas== de la hoja.

```yaml
fis:  { significado: "Resistencia, potencia bruta.",                  rango: 2..5 }
tac:  { significado: "Precisión, coordinación, reflejos.",            rango: 2..6 }
men:  { significado: "Liderazgo, moral base, resistencia psíquica.",  rango: 2..7 }
```

> [!tip] Determinísticos en creación, mutables solo vía hito
> En creación los atributos son **determinísticos por rol/rango** desde tablas de configuración (cero azar en estadísticas). Después solo cambian vía hito (`triple_cero` o `mejora_atributo`).
> Toda otra capacidad numérica (fatiga máxima, moral máxima, fuerza aportada, mando vigente) es **derivada en caliente con fórmulas fijas y no se persiste**, para evitar desincronización. Topes, fórmulas y el vocabulario canónico de estadísticas viven en [[atributos-y-habilidades|atributos-y-habilidades.md]].

> [!info] Azar portable
> Las magnitudes se expresan en formato portable, agnóstico al sistema de resolución: probabilidades en **porcentaje** (`40% de fallar`), modificadores sobre atributos/estadísticas como **delta entero** (`(+1) MENTAL`), modificadores sobre magnitudes continuas en **porcentaje** (`-100% MOVIMIENTO`). Detalle en [[atributos-y-habilidades|atributos-y-habilidades.md]] y la política editorial en [[AGENTS|AGENTS.md]].

---

## §3 — Tags

Lista plana de cadenas en notación punto. Es la **fuente de verdad de todo lo discreto** del personaje: rango, escuadra, mando, equipo, salud, estado mental, rasgos, lealtades a facción/subfacción/grupo, destrezas, ventajas, rasgos.

> [!important] El contrato vive en sistema-tags.md
> La definición completa, las categorías canónicas, el formato y las reglas de catálogo viven en [[sistema-tags|sistema-tags.md]]. Acá solo se fija el contrato con la hoja.

```yaml
forma:   <categoria>[.<subcategoria>].<slug>
tipo:    list[str]                # NO multiconjunto — ante repetidos gana el último valor
default: []
```

### 3.1. Derivaciones desde etiquetas (no persistidas)

El motor calcula al servir, sin persistir, para evitar desincronización:

```yaml
filiacion:    { fuente: "tags rango.* + escuadra.*",  nota: "null si falta alguno" }
fatiga_max:   { fuente: "fis + men",                  tipo: int }
moral_max:    { fuente: "men",                        tipo: int }
fza_aportada: { fuente: "tags rol.combate.*",         valores: "{heroe: 3, lider: 2, default: 1}" }
```

Las fórmulas canónicas y sus escalas viven en [[atributos-y-habilidades|atributos-y-habilidades.md]]. Cambios post-creación en `tags[]` se registran como hito `agregar_tag` / `quitar_tag` con metadatos `{tag}`.

### 3.2. Etiqueta relacional vs. vínculo personal

Cuando una etiqueta referencia una **entidad de catálogo** (facción, subfacción, escuadra, grupo), el último segmento es el slug legible de esa entidad: `lealtad.faccion.ejercito_rojo`, `lealtad.escuadra.columna_mansilla`. Son membresías declarativas, se leen sin prosa.

Cuando el vínculo apunta a **otro personaje**, ==no se usa etiqueta==: se usa una entrada en `aliados[]` o `nemesis[]` con `ref` a la patente del otro. La distinción operativa: la etiqueta afirma la relación; la colección la **cuenta** (lleva prosa). Ver [[#§3.4 — Aliados y némesis|§3.4]].

### 3.3. Extensibilidad

El catálogo canónico es andamiaje, no jaula: etiqueta nueva, subcategoría nueva o categoría nueva entera entran **sin migración**. Una etiqueta desconocida no rompe la hoja. La mitigación es curaduría, no validación. Detalle en [[sistema-tags|sistema-tags.md]].

### 3.4. Aliados y némesis

Vínculos dirigidos a otros personajes. **No son derivados de etiquetas** — son colecciones persistidas de primera clase, como `historial`. Cada entrada lleva referencia a la patente del otro personaje más prosa breve sobre el vínculo.

```yaml
aliados:
  tipo:    list[{ref, descripcion, desde?}]
  default: []
  forma:
    ref:         patente ^[A-Z0-9]{8}$ del aliado
    descripcion: 1-3 frases sobre cómo se formó el vínculo
    desde:       ISO-8601 opcional

nemesis:
  tipo:    list[{ref, descripcion, desde?}]
  default: []
  nota:    Sin restricción de bando — un némesis del propio bando es legal (traición personal, vieja deuda).
  forma:   { ref, descripcion, desde? }   # idéntica a aliados[]
```

> [!note] Por qué colecciones y no etiquetas
> La relación lleva **prosa** (la descripción del vínculo). Una etiqueta solo puede afirmar la relación; no puede contar cómo se formó. Las colecciones llevan la textura narrativa que el motor descendente necesita.
> **Relación con `lealtad.*`**: las lealtades a facciones, subfacciones y grupos son etiquetas (`lealtad.*`) porque son membresías sin prosa. Los vínculos a otro personaje viven exclusivamente acá, con descripción obligatoria.
> **Ciclo de vida**: ambas arrancan vacías. Se pueblan en caliente vía hito `formacion_lealtad` (aliado) / `identificacion_nemesis` (némesis), o por curaduría directa.

---

## §4 — Historia

Prosa biográfica original. El relato de quién es el personaje, no sus datos.

```yaml
tipo:            string
largo:           120-200 palabras
generacion:      Modelo de lenguaje al crear el personaje en memoria volátil.
idioma:          Castellano rioplatense, voz narrativa.
inmutable_tras:  Canonización. Se congela como artefacto.
```

> [!warning] No-determinismo asumido
> La prosa es no-reproducible aun con semilla: ninguna semilla la regenera idéntica. Se persiste como **artefacto**, no como derivado. Por eso la hoja no expone un campo `semilla`, y el modelo generativo no se rastrea en metadatos: una vez congelada, la prosa es opaca.

---

## §5 — Historial

Array de hitos. Cada entrada describe un evento temporal sobre el personaje ya canonizado. Es un **registro de eventos de solo añadir**.

```yaml
fecha:       ISO-8601
tipo:        string          # catálogo sugerido, abierto
descripcion: string          # obligatorio
ref_batalla: slug | null     # batalla externa, opcional
metadata:    object          # libre
```

> [!info] Tipos de hito — sugeridos, abiertos
> Catálogo sugerido: `triple_cero`, `ascenso`, `herida`, `recuperacion`, `agregar_tag`, `quitar_tag`, `traslado`, `condecoracion`, `mejora_atributo`, `cambio_rango`, `cambio_mando`, `cambio_estado`, `cambio_salud`, `cambio_mental`, `asignacion_escuadra`, `identificacion_nemesis`, `formacion_lealtad`, `ruptura_lealtad`.
> El catálogo es **sugerido, no cerrado**: tipos personalizados son legítimos. La mitigación es curaduría, no validación. Personajes recién creados arrancan con `historial: []`.

> [!note] De solo añadir
> No hay reverso de hito: un error se corrige con un hito compensatorio nuevo, no borrando el anterior. La línea de tiempo es íntegra por construcción.

---

## §6 — Metadatos

Campos de auditoría. No mutables por hitos, solo por el motor.

```yaml
creado_en:            ISO-8601          # creación en memoria volátil
canonizado_en:        ISO-8601 | null   # fecha de persistencia; null en efímeros
ultima_actualizacion: ISO-8601          # se actualiza con cada hito
```

> [!info] Canonicidad derivada
> `es_canon` se deriva de `canonizado_en != null` — ==no se persiste==. Un personaje efímero (sin canonizar) tiene `canonizado_en: null` y nunca toca la base de datos. Canonizar congela la `historia` y abre el `historial` a hitos.

---

## §7 — Extras

Compuerta de escape para clientes del ecosistema (estrategia, rol, generador visual, Diégesis).

```yaml
tipo:      object | null
reglas:    El motor no inspecciona ni valida su contenido.
proposito: Que un cliente externo persista metadatos propios sin romper el esquema.
```

Soporta cualquier llave y estructura anidada. Si un cliente necesita guardar algo que no encaja en etiquetas ni en los bloques canónicos, va acá. Esto mantiene el núcleo estable mientras el ecosistema crece.

---

## §8 — Matriz de mutabilidad

Qué cambia, y cómo:

| Campo | Mutabilidad | Mecanismo |
|---|---|---|
| `atributos.{fis, tac, men}` | vía hito | `triple_cero` / `mejora_atributo` |
| `tags[]` | vía hito | `agregar_tag` / `quitar_tag` (metadata `{tag}`) |
| `identidad.rol` | vía hito | `ascenso` / `cambio_rol` |
| `aliados[]` | vía hito | `formacion_lealtad` |
| `nemesis[]` | vía hito | `identificacion_nemesis` |
| `historial[]` | vía hito | de solo añadir (`POST /evento`) |
| `metadatos.ultima_actualizacion` | automático | en cada hito |
| `identidad.edad` | sin hito | decisión narrativa explícita |
| `identidad.sobrenombre` | sin hito | derivado al servir |
| `extras` | sin hito | libre, escritura del cliente |
| `identidad.slug` | inmutable | fijado una vez al canonizar |
| `identidad.nombre` | inmutable | — |
| `identidad.genero` | inmutable | — |
| `historia` | inmutable | congelada al canonizar |
| `metadatos.creado_en` | inmutable | — |
| `metadatos.canonizado_en` | inmutable | fijado una vez al canonizar |
| `filiacion`, `fatiga_max`, `moral_max`, `fza_aportada` | derivado | recomputado al servir |
| `sobrenombre` (cuando deriva), `es_canon` | derivado | recomputado al servir |

> [!tip] Cómo leer la matriz
> **Vía hito**: el cambio deja rastro en `historial[]` — la línea de tiempo del personaje lo registra. **Sin hito**: cambio de bajo peso narrativo, no necesita evento. **Inmutable**: fijado al canonizar; cambiarlo sería otro personaje. **Derivado**: nunca se escribe; se calcula. La frontera entre vía-hito y sin-hito es la pregunta "¿esto es parte de la historia del personaje?"
