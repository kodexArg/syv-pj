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

> [!NOTE]
> **Qué es este documento**
>
> El **núcleo** de `syv-pj`: define la hoja de personaje campo por campo. Todo lo demás lo referencia. Acá vive el contrato estructural; los ejes que se ramifican tienen su propio documento hermano.
>
> **Documentos hermanos**:
> - [sistema-tags.md](sistema-tags.md) — la lista plana `tags[]`: notación, categorías, catálogo y curaduría.
> - [atributos.md](atributos.md) — escalas de `cuerpo/mente/alma`, estadísticas derivadas y vocabulario canónico de efectos.
> - [apariencia.md](apariencia.md) — el campo `apariencia`: descriptores visuales libres, sparse y agnósticos al generador de imágenes.
> - [contratos.md](contratos.md) — aspectos, habilidades y efectos como contratos.
> - [historial.md](historial.md) — el registro `historial[]`: campos del hito, catálogo de tipos, `actores[]` y la regla de solo-añadir.
> - [nemesis-y-aliados.md](nemesis-y-aliados.md) — los vínculos personales (`aliado/*` / `nemesis/*`) como etiquetas relacionales.
> - [lealtad.md](lealtad.md) — la lealtad (`lealtad/*`) como etiqueta relacional plana.
> - [generacion-procedural.md](generacion-procedural.md) — cómo se completa una hoja desde el azar portable.
> - [diegesis.md](diegesis.md) — el contexto del universo (facciones, lugares, lore) vive en `syv-docs`; este doc redirige.

---

## §0 — Estructura de la hoja

La hoja del personaje es la **entidad mínima** de *Subordinación y Valor*. Un mismo personaje homogeneizado sirve a la Diégesis, al motor de batalla, al motor de juego y a la proyección visual sin cambiar de forma: la hoja clasifica, almacena y entrega; el consumidor decide el uso.

Seis bloques estructurales y una lista plana de tags:

```yaml
personaje:
  identidad:    { slug, nombre, sobrenombre, rol, especialidad, genero, edad }
  atributos:    { cuerpo, mente, alma }   # únicas magnitudes numéricas persistidas
  tags:         [...]               # lista plana, notación punto, NO multiconjunto (último valor gana)
                                    # incluye los vínculos personales: aliado/* / nemesis/*
  historia:     str                 # prosa biográfica, congelada al canonizar
  historial:    [...]               # hitos temporales (registro de eventos, de solo añadir)
  metadatos:    { creado_en, canonizado_en, ultima_actualizacion }
  extras:       object | null       # válvula de escape para clientes
  apariencia:   { rostro, figura, presencia }   # tres párrafos descriptivos, al cierre (ver §2.5)
```

> [!NOTE]
> **`apariencia` cierra la hoja, no es un bloque más en el medio**
>
> El bloque `apariencia` figura al **final** de la tabla deliberadamente: es el destilado visual de todo lo anterior (identidad, atributos, tags) y no se puede escribir bien sin conocerlos primero. Ver el porqué en §2.5 y en [apariencia.md §6](apariencia.md#6--forma-largo-y-mutabilidad).

> [!TIP]
> **Regla rectora — lo discreto es etiqueta**
>
> Todo lo que es **discreto** y no es identidad, atributo, prosa o auditoría → **es etiqueta**. Sin excepciones: incluso los vínculos personales (aliados, némesis) son etiquetas.
> Esa única regla decide dónde va cada dato nuevo. Si dudás entre crear un campo o una etiqueta, casi siempre es etiqueta. La justificación detallada vive en [sistema-tags.md](sistema-tags.md).

> [!NOTE]
> **Tres clases de dato**
>
> La hoja distingue tres clases que no hay que confundir:
> - **Persistido** — se guarda al canonizar y solo cambia por las reglas de su bloque (`identidad`, `atributos`, `tags`, `historia`, `historial`, `metadatos`, `extras`).
> - **Derivado-no-persistido** — se calcula en caliente al servir y nunca se guarda, para evitar desincronización (`filiacion`, `fatiga_max`, `moral_max`, `fza_aportada`, `sobrenombre` cuando es derivable, `es_canon`).
> - **Volátil** — vive solo durante un encuentro y no es parte de la hoja persistida (estados de combate; viven en el motor de batalla, no acá).

---

## §1 — Identidad

Quién es el personaje, fuera de su contexto operativo. La capa operativa (rango, mando, equipo, lealtades) vive en `tags[]`, no acá.

> **Ejemplo — `rol` y `especialidad` conviven — ejemplo**
>
> **Florencia Bustos** tiene `rol: "Cabo Primero"` (su lugar en la cadena de mando, lectura humana del tag `rango/cabo_primero`) y `especialidad: "Apuntadora"` (lo que hace en combate). Son dos etiquetas humanas distintas de la misma persona: una responde "¿qué jerarquía tiene?", la otra "¿qué función cumple?". Ninguna reemplaza a la otra ni al tag operativo que las respalda.

### 1.1. `slug` — la patente del personaje

El `slug` es la **patente opaca** del personaje. **No es su nombre.** Es el identificador estable que el sistema usa para referenciarlo en cualquier vínculo: como destino de un tag `aliado/*` / `nemesis/*` (ver [§3.4](#34-vínculos-personales)), en los `actores[]` de un hito, en ediciones por API, en nodos del vault.

```yaml
slug:
  formato:     ^[A-Z0-9]{8}$          # patente opaca, ej. K9F2H3M4
  ejemplos:    [K9F2H3M4, SLG3D7K2, NMC8H5P9]
  generacion:  El servidor genera al persistir (random + chequeo de colisión).
  custom:      Admitido para datos de ejemplo o curaduría manual; mismo regex, mismo chequeo.
  mutable:     false
```

> [!NOTE]
> **Por qué patente y no nombre**
>
> Dos personajes pueden llamarse igual; sus patentes no colisionan. Una refactorización narrativa (cambio de apellido por casamiento, alias revolucionario) no invalida refs existentes. Los renderers muestran `nombre`; los sistemas guardan `slug`.

> [!NOTE]
> **Patente opaca ≠ slug de catálogo**
>
> El `slug` del personaje es opaco (`^[A-Z0-9]{8}$`) precisamente para ser estable y predecible a escala. Los slugs de catálogo (tags, facciones) son legibles (`lowercase_con_underscore`, ej. `pistola`, `ejercito_rojo`). La asimetría es deliberada: la patente es para máquinas; el slug legible es la pieza humana de la notación punto. Ver [sistema-tags.md](sistema-tags.md).

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
  tipo:       string | null
  default:    null
  proposito:  Jerarquía legible — cómo se nombra al personaje por su lugar en la cadena de mando. Lectura humana del tag `rango/*`.
  ejemplos:   ["Cabo Primero", "Teniente", "Comandante de Escuadra"]
  mutacion:   Hito `ascenso` / `cambio_rango`.
  aclaracion: NO confundir con el viejo campo `rol` (legado), que en realidad nombraba la especialidad. Ese significado migró a `especialidad`.

especialidad:
  tipo:       string | null
  default:    null
  proposito:  Especialidad táctica narrativa (lo que el personaje *hace*). La vocación de pertenencia la da el `rol`.
  ejemplos:   ["Fusilero", "Inquisidor", "Médico de campaña"]
  aclaracion: Se materializa además como tag especialidad/* en tags[] (la capa operativa).

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

Tres valores numéricos que definen la capacidad base, en escala `2..7` (entero, más es mejor). Son las **únicas magnitudes numéricas persistidas** de la hoja.

```yaml
cuerpo:  { significado: "Resistencia, potencia bruta. En prosa: Físico.",       rango: 2..7 }
mente:   { significado: "Precisión, coordinación, reflejos, lectura táctica.",   rango: 2..7 }
alma:    { significado: "Aura, liderazgo, voluntad, temple ante el miedo. En prosa: Espíritu.", rango: 2..7 }
```

> [!TIP]
> **Determinísticos en creación, mutables solo vía hito**
>
> En creación los atributos son **determinísticos por rango** desde tablas de configuración (cero azar en estadísticas). Después solo cambian vía hito (`triple_cero` o `mejora_atributo`).
> Toda otra capacidad numérica (fatiga máxima, moral máxima, fuerza aportada, mando vigente) es **derivada en caliente con fórmulas fijas y no se persiste**, para evitar desincronización. Topes, fórmulas y el vocabulario canónico de estadísticas viven en [atributos.md](atributos.md).

> [!NOTE]
> **Azar portable**
>
> Las magnitudes se expresan en formato portable, agnóstico al sistema de resolución: probabilidades en **porcentaje** (`40% de fallar`), modificadores sobre atributos/estadísticas como **delta entero** (`(+1) ALMA`), modificadores sobre magnitudes continuas en **porcentaje** (`-100% MOVIMIENTO`). Detalle en [atributos.md](atributos.md) y la política editorial en [AGENTS.md](../AGENTS.md).

---

## §2.5 — Apariencia: tres párrafos descriptivos

Cómo **luce** el personaje: **tres párrafos de prosa descriptiva agnóstica** —`rostro`, `figura`, `presencia`— sobre ejes fijos. No es un prompt, no es una lista de átomos, no es sintaxis de generador: es un contrato visual portable que cualquier proyección (ComfyUI, Flux, una ilustración, un avatar) consume sin reinventarlo.

```yaml
apariencia:
  rostro:    str | null   # zoom a la cara
  figura:    str | null   # cuerpo entero, porte, cómo lleva lo que viste
  presencia: str | null   # cómo ocupa el espacio, la luz, la impresión que deja
default:     null          # los tres ausentes ⇒ todo librado al render
largo:       40-80 palabras por párrafo (sugerido, no duro)
persist:     persistido — mutable sin hito (bajo peso narrativo, como edad)
```

> [!IMPORTANT]
> **Regla rectora — cómo se ve, no cuánto ni qué**
>
> Cada párrafo responde **"¿cómo se ve el personaje?"**, nunca cuánto (eso lo dicen los atributos) ni qué lleva (eso lo dicen los tags). Anti-redundancia de tres caras: **integers dicen cuánto · tags dicen qué · párrafos dicen cómo se ve**. Un párrafo con un número (`fuerza 6`) o el nombre de una prenda/arma (`pistola 9mm`) está invadiendo el territorio de otro bloque.

> [!TIP]
> **Los tres ejes, fijos**
>
> - `rostro` — la cara en primer plano: facciones, mirada, piel, pelo, gesto habitual.
> - `figura` — cuerpo entero y porte: cómo se para, cómo **lleva** lo que viste (nunca **qué** viste).
> - `presencia` — la impresión que deja: luz, aire, cómo cambia una habitación cuando entra.
>
> Los tres ejes no se agregan ni se quitan: son el contrato. Detalle, ejemplos por eje y la tabla completa de anti-redundancia viven en [apariencia.md](apariencia.md).

> [!TIP]
> **Sparse por diseño — lo no dicho queda librado al azar**
>
> Se escribe **solo lo que el canon quiere fijar**; un párrafo puede ser rico y otro escueto, o los tres pueden faltar (`apariencia: null`). La ausencia no es un dato faltante: es el azar portable del kit aplicado al eje visual.

> [!IMPORTANT]
> **Complementa, no duplica**
>
> No re-codifica lo que ya tiene hogar: cicatrices con contrato → `rasgos`, prendas y armas → `equipo`, porte/expresión con efecto de juego → `aspectos`, corpulencia base → atributo `cuerpo`. La proyección visual lee **todo el conjunto** junto (párrafos + tags + atributos). La frontera del agnosticismo (hecho visual vs directiva de render) vive en [apariencia.md](apariencia.md).

---

## §2.6 — La hoja tiene en mente el retrato (sin parametrizarlo)

El retrato de un personaje se piensa en **tres niveles**, pero la hoja **solo aporta inputs del nivel 2** — nunca parametriza el retrato en sí (sin sliders, sin `lora_slug`/`strength`, sin `prompt_generado`: eso queda fuera de la hoja, como ya rechazado en otras vueltas del esquema).

```yaml
N1 — escena común:    fuera de la hoja. Encuadre/cámara/composición uniforme a todos los retratos.
N2 — el personaje:    inputs que sí vienen de la hoja:
  2.a presentación:   identidad + atributos + tags → quién es, leído como base del retrato.
  2.b LoRAs por referencia externa: fuera del alcance de esta hoja (curaduría de assets, no dato de personaje).
  2.c vestimenta y espíritu: equipo (tags) + apariencia.{rostro, figura, presencia} → encuadre bust-up 3/4.
N3 — cierre común:    fuera de la hoja. Fondo oscuro + spot + triggers técnicos, uniforme a todos.
```

> [!NOTE]
> **Por qué se documenta sin parametrizar**
>
> N1 y N3 son comunes a todo el roster; parametrizarlos en la hoja rompería esa uniformidad y metería sintaxis de generador donde no corresponde (ver [apariencia.md §5](apariencia.md#5--la-frontera-del-agnosticismo)). La hoja describe **qué personaje es**, no **cómo se renderiza**: eso es trabajo del armador de prompt, aguas abajo.

---

## §3 — Tags

Lista plana de cadenas en notación punto. Es la **fuente de verdad de todo lo discreto** del personaje: rango, mando, equipo, salud, estado mental, rasgos, aspectos, habilidades, lealtades a facción/subfacción y los **vínculos personales** —aliados y némesis— como etiquetas relacionales.

> [!IMPORTANT]
> **El contrato vive en sistema-tags.md**
>
> La definición completa, las categorías canónicas, el formato y las reglas de catálogo viven en [sistema-tags.md](sistema-tags.md). Acá solo se fija el contrato con la hoja.

```yaml
forma:   <categoria>[.<subcategoria>].<slug>
tipo:    list[str]                # NO multiconjunto — ante repetidos gana el último valor
default: []
```

### 3.1. Derivaciones desde etiquetas (no persistidas)

El motor calcula al servir, sin persistir, para evitar desincronización:

```yaml
filiacion:    { fuente: "tags rango/* + faccion/*",   nota: "null si falta alguno" }
fatiga_max:   { fuente: "cuerpo + alma",              tipo: int }
moral_max:    { fuente: "alma",                       tipo: int }
fza_aportada: { fuente: "tags especialidad/combate/*",         valores: "{heroe: 3, lider: 2, default: 1}" }
```

Las fórmulas canónicas y sus escalas viven en [atributos.md](atributos.md). Cambios post-creación en `tags[]` se registran como hito `agregar_tag` / `quitar_tag` con metadatos `{tag}`.

### 3.2. Etiquetas relacionales

Algunas etiquetas no describen un atributo del personaje sino un **vínculo dirigido** hacia otra entidad. El último segmento es la referencia al destino:

- A una **entidad de catálogo** (facción, subfacción, grupo, religión): el slug legible de esa entidad — `lealtad/ejercito_rojo`, `aliado/pelicanos`.
- A **otro personaje**: su patente — `aliado/K9F2H3M4`, `nemesis/R7T3W1X5`.

Todas se cuentan y se filtran como cualquier tag. La prosa de un vínculo personal —cómo se formó— no vive en la etiqueta sino en su hito de [historial.md](historial.md). Definición completa en [nemesis-y-aliados.md](nemesis-y-aliados.md).

### 3.3. Extensibilidad

El catálogo canónico es andamiaje, no jaula: etiqueta nueva, subcategoría nueva o categoría nueva entera entran **sin migración**. Una etiqueta desconocida no rompe la hoja. La mitigación es curaduría, no validación. Detalle en [sistema-tags.md](sistema-tags.md).

### 3.4. Vínculos personales

Los aliados y los némesis de un personaje son **etiquetas**, no un bloque aparte de la hoja.

```yaml
donde:   tags[]                       # conviven con el resto de las etiquetas
forma:   aliado.<slug> | nemesis.<slug>
slug:    patente del personaje, o slug de facción/subfacción/grupo
prosa:   en el hito que formó el vínculo (historial[]), no en la etiqueta
```

El contrato del tag está en [sistema-tags.md §5](sistema-tags.md); el porqué del cambio, los tipos de destino y el ciclo de vida, en [nemesis-y-aliados.md](nemesis-y-aliados.md); la prosa del vínculo, en el hito de [historial.md](historial.md).

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

> [!WARNING]
> **No-determinismo asumido**
>
> La prosa es no-reproducible aun con semilla: ninguna semilla la regenera idéntica. Se persiste como **artefacto**, no como derivado. Por eso la hoja no expone un campo `semilla`, y el modelo generativo no se rastrea en metadatos: una vez congelada, la prosa es opaca.

---

## §5 — Historial

Array de hitos. Cada entrada describe un evento temporal sobre el personaje ya canonizado. Es un **registro de eventos de solo añadir**.

> [!IMPORTANT]
> **El contrato detallado vive en historial.md**
>
> La definición campo por campo, el catálogo completo de tipos, la semántica de `actores[]` y la proyección en Diégesis viven en [historial.md](historial.md). Acá solo se fija el contrato con la hoja.

```yaml
fecha:       ISO-8601
tipo:        string          # catálogo sugerido, abierto
actores:     [string]        # patentes de personajes involucrados; [] válido, normalmente varios
descripcion: string          # obligatorio
encuentro:   slug | null     # batalla externa, opcional
metadata:    object          # libre (a futuro puede portar adjuntos)
```

> [!NOTE]
> **Tipos de hito — sugeridos, abiertos**
>
> Catálogo sugerido: `triple_cero`, `ascenso`, `herida`, `recuperacion`, `agregar_tag`, `quitar_tag`, `traslado`, `condecoracion`, `mejora_atributo`, `cambio_rango`, `cambio_mando`, `cambio_estado`, `cambio_salud`, `cambio_mental`, `identificacion_nemesis`, `formacion_lealtad`, `ruptura_lealtad`.
> El catálogo es **sugerido, no cerrado**: tipos personalizados son legítimos. La mitigación es curaduría, no validación. Personajes recién creados arrancan con `historial: []`.

> [!NOTE]
> **De solo añadir**
>
> No hay reverso de hito: un error se corrige con un hito compensatorio nuevo, no borrando el anterior. La línea de tiempo es íntegra por construcción.

---

## §6 — Metadatos

Campos de auditoría. No mutables por hitos, solo por el motor.

```yaml
creado_en:            ISO-8601          # creación en memoria volátil
canonizado_en:        ISO-8601 | null   # fecha de persistencia; null en efímeros
ultima_actualizacion: ISO-8601          # se actualiza con cada hito
```

> [!NOTE]
> **Canonicidad derivada**
>
> `es_canon` se deriva de `canonizado_en != null` — **no se persiste**. Un personaje efímero (sin canonizar) tiene `canonizado_en: null` y nunca toca la base de datos. Canonizar congela la `historia` y abre el `historial` a hitos.

---

## §7 — Extras

Compuerta de escape para clientes del ecosistema (motor de batalla, motor de juego, generador visual, Diégesis).

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
| `atributos.{cuerpo, mente, alma}` | vía hito | `triple_cero` / `mejora_atributo` |
| `tags[]` | vía hito | `agregar_tag` / `quitar_tag` (metadata `{tag}`) |
| `tags[]` vínculos (`aliado/*`, `nemesis/*`) | vía hito | `formacion_lealtad` / `identificacion_nemesis` / `ruptura_lealtad` |
| `identidad.rol` | vía hito | `ascenso` / `cambio_rango` |
| `identidad.especialidad` | vía hito | `ascenso` / `cambio_especialidad` |
| `historial[]` | vía hito | de solo añadir (`POST /evento`) |
| `metadatos.ultima_actualizacion` | automático | en cada hito |
| `identidad.edad` | sin hito | decisión narrativa explícita |
| `apariencia.rostro` | sin hito | decisión narrativa explícita (bajo peso, como `edad`) |
| `apariencia.figura` | sin hito | decisión narrativa explícita (bajo peso, como `edad`) |
| `apariencia.presencia` | sin hito | decisión narrativa explícita (bajo peso, como `edad`) |
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

> [!TIP]
> **Cómo leer la matriz**
>
> **Vía hito**: el cambio deja rastro en `historial[]` — la línea de tiempo del personaje lo registra. **Sin hito**: cambio de bajo peso narrativo, no necesita evento. **Inmutable**: fijado al canonizar; cambiarlo sería otro personaje. **Derivado**: nunca se escribe; se calcula. La frontera entre vía-hito y sin-hito es la pregunta "¿esto es parte de la historia del personaje?"

---

## §9 — Regla de refactor de esquema

Todo cambio de **forma** de una entidad (campo agregado o renombrado, migración lista→objeto como la de `apariencia`, o cualquier otro refactor estructural) se aplica al roster existente con:

1. Un **script Python determinista e idempotente** que transforma cada ficha existente a la nueva forma. Determinista: misma entrada, misma salida, siempre. Idempotente: correrlo dos veces no rompe nada.
2. Un **test de cobertura total** que verifica que **todos** los personajes del roster migran sin pérdida de dato.

> [!IMPORTANT]
> **El test verde es condición de merge**
>
> No se mergea un refactor de esquema sin su test en verde. La migración de datos existentes nunca es "a mano" ni "después se ve": es parte del mismo cambio, verificada antes de cerrar el PR.

Esta regla es la que dejó pendiente, deliberadamente, la migración de los 34+ mocks de `resources/personajes/` a la forma de tres párrafos de `apariencia`: el cierre de esquema documentado acá no ejecuta esa migración — la habilita, bajo esta regla, como trabajo downstream.
