---
slug: _moc-personajes
nombre: Personajes de ejemplo
description: Catálogo de los personajes canónicos de ejemplo, agrupados por facción. Referencia para el motor generador y guía de estilo/contenido para el LLM.
tipo: moc
---

# Personajes de ejemplo — catálogo

Estos son los personajes canónicos de ejemplo del universo *Subordinación y Valor*. Cada uno es una instancia real de la [[hoja-de-personaje|hoja de personaje]] y funciona como referencia concreta para el motor generador y como guía de estilo/contenido para el LLM.

> [!abstract] Profundidad: estereotipos, no protagonistas
> A diferencia de los personajes de **`syv-docs/3_personajes/`** —donde cada figura (los `principales/` y `secundarios/`) se desarrolla a fondo: sus secretos, sus vínculos, su contexto, su arco—, las fichas de `syv-pj` son **estereotipos**: tienen la profundidad de un **recién conocido**. Un nombre, una facción, un rango, cómo se ve, a qué le pega. Son molde para el motor generador, no biografía canónica; por eso la prosa es corta y sin secretos.
> Los personajes de `syv-docs/3_personajes/` están **TBD** para incorporarse también acá, como instancias de la hoja (la profundidad narrativa se queda en la SSOT; lo que baja a `syv-pj` es el estereotipo operativo).

> [!important] Convención de autoría — campos dedicados, no el espejo de tags planos
> Estas fichas son la **proyección Obsidian** de la hoja: cada dimensión controlada vive en **su propio campo** (`faccion`, `rango`, `especialidad`, `estado`, `lealtad`, `aspectos`, `rasgos`, `equipo`, `apariencia`) y las relaciones son **wikilinks** —conforme a `.claude/rules/tags-taxonomy.md` y `.claude/rules/wikilinks-relations.md`—. **No** se duplica la serialización plana `tags/<categoria>/<slug>` del motor: ese espejo redundante era un anti-patrón (dos fuentes de verdad en un archivo a mano) y fue retirado; `tags` queda como **vivero** (`[]`). El motor (`syv-pj-api`) conserva su forma canónica de `tags[]` planos intacta: es su formato de cable/persistencia, separado de cómo se autora una ficha-ejemplo.
> Todo nuevo campo visual va en `apariencia` (sparse, agnóstico al generador) — ver [[apariencia|docs/apariencia.md]].

## Cómo se arma una hoja

El contrato del modelo (campo por campo) vive en [[hoja-personaje|hoja de personaje]] y la notación de tags en [[sistema-tags]]. Acá está el **cómo se llena** una ficha-ejemplo, con un caso real.

> [!tip] Regla rectora — lo discreto es campo, lo descriptivo es prosa
> Todo dato **discreto y controlado** (facción, rango, equipo, aspecto…) va a **su campo**. Todo lo **descriptivo y libre** (cómo se ve, quién es) va a `apariencia` o a la `historia`. Ante la duda preguntate: *¿el motor lo filtra, lo cuenta o lo resuelve contra un catálogo?* → campo. *¿Solo lo lee una persona?* → prosa.

### Anatomía — ficha anotada

[[ovidio-gauna-sargento|Ovidio Gauna]] (sargento de las Fuerzas Armadas) como patrón. Cada línea, comentada:

```yaml
slug: ovidio-gauna-sargento     # patente del archivo (kebab, único). Identidad estable, no el nombre.
nombre: Ovidio Gauna            # nombre de display
aliases:                        # nombre propio + variantes (protege ante renombres) — regla del vault
  - Ovidio Gauna
  - Sargento Gauna
description: Sargento curtido…   # 1 línea, obligatoria
barrio: barrios-del-muro        # ubicación del atlas (entidad existente)
faccion: fuerzas_armadas        # ← CANON CERRADO: resuelve a facciones/fuerzas_armadas.md
rango: sargento                 # ← CANON CERRADO: resuelve a rangos/fuerzas_armadas.md
especialidad: especialidad-combate-lider   # ← CANON CERRADO: especialidades/<faccion>/…  (o null)
estado: disponible              # ← VOCABULARIO CONTROLADO: exactamente uno
lealtad:                        # ← RELACIONAL: wikilink a una entidad existente
  - "[[confederacion]]"
atributos:                      # únicas magnitudes numéricas; enteros 2..7; deterministas por rango
  cuerpo: 4
  mente: 4
  alma: 5
edad: 40
genero: m
apariencia:                     # ← LIBRE: descriptores de texto plano, sin catálogo
  - criollo
  - canoso
  - bigote
aspectos:                       # ← CATÁLOGO: wikilinks a catalogos/aspecto/*  (mecánicamente activos)
  - "[[veterano]]"
rasgos:                         # ← CATÁLOGO: wikilinks a catalogos/rasgo/*  (observables, SIN efecto)
  - "[[tatuaje_de_unidad]]"
equipo:                         # ← CATÁLOGO: wikilinks a catalogos/equipo/*  (subcat arma/utilitario/vestidura/…)
  - "[[subfusil]]"
  - "[[pistola_9mm]]"
  - "[[chaleco_asalto]]"
  - "[[uniforme_linea]]"
  - "[[insignia_rango_militar]]"
  - "[[radio]]"
tags: []                        # ← VIVERO: etiqueta emergente a filtrar exacto. Casi siempre []
```

> [!note] Campos vacíos
> Si un eje no aplica, va como lista vacía (`aspectos: []`) o se omite (un personaje sin rasgos no lleva `rasgos:`). `especialidad: null` es válido. Nunca dejes un wikilink a una entidad que no existe.

### Los campos, uno por uno

| Campo | Qué guarda | Forma | ¿Se inventa? |
|---|---|---|---|
| `faccion` | Bando macro | átomo → `facciones/*` | **No** — canon cerrado |
| `subfaccion` | Grupo subordinado (cuando aplica) | átomo → `subfacciones/*` | **No** — canon cerrado |
| `rango` | Jerarquía de campo | átomo → `rangos/<faccion>.md` | **No** — canon cerrado |
| `especialidad` | Lo que el personaje *hace* | `especialidad-<eje>-<slug>` → `especialidades/<faccion>/*` · ejes: `combate`, `investigacion`, `oficio`, `paranormal` | **No** — canon cerrado (o `null`) |
| `estado` | Disponibilidad operativa | átomo (`disponible`, …), **exactamente uno** | **No** — vocabulario controlado |
| `lealtad` | Adhesión vigente | lista de wikilinks a entidad existente | **No** — apunta a algo que ya existe |
| `barrio` | Dónde opera | slug de ubicación del atlas | **No** — entidad existente |
| `atributos` | Capacidad base | `{cuerpo, mente, alma}` enteros 2..7 | n/a — deterministas por rango |
| `apariencia` | Cómo se ve | lista de **strings libres** | **Sí, siempre** — texto plano |
| `aspectos` | Identidad con peso mecánico | wikilinks → `catalogos/aspecto/*` | Sí, **creando la entrada** de catálogo |
| `rasgos` | Marca física observable, **sin** efecto | wikilinks → `catalogos/rasgo/*` | Sí, **creando la entrada** de catálogo |
| `equipo` | Lo que carga | wikilinks → `catalogos/equipo/*` | Sí, **creando la entrada** de catálogo |
| `tags` | Vivero abierto | lista plana, normalmente `[]` | Sí — pero la curaduría lo gradúa a campo |

### Qué se puede inventar y qué no

Tres niveles, de más rígido a más libre:

1. **Canon cerrado — NO se inventa al escribir una ficha.** `faccion`, `subfaccion`, `rango`, `especialidad`, `estado`, `lealtad`, `barrio`. Resuelven contra entidades que ya existen (`facciones/`, `subfacciones/`, `rangos/`, `especialidades/`, el atlas). Acuñar un valor nuevo es **modificar el canon**, no llenar una hoja: va por PR a su directorio, no inline. Un wikilink de `lealtad` que apunte a la nada es un error.
2. **Catálogo que crece por curaduría — se inventa creando la entrada.** `aspectos`, `rasgos`, `equipo` (y `habilidad`, `entrenamiento`). Podés sumar un valor nuevo, pero **creás el archivo en `catalogos/`** con `origen: emergente` y sus campos obligatorios (ver [[sistema-tags]] §6). No basta el wikilink: si no existe la entrada, no está catalogado.
3. **Libre — se inventa siempre, sin catálogo.** `apariencia` (descriptores de texto plano) y la `historia` (prosa). Acá describís al personaje con tus palabras. Lo que es **descriptivo** (joven, enjuto, mirada fría) NO es un tag ni un rasgo: la semántica lo encuentra sola. Solo graduá a `rasgo` lo que sea una **marca concreta y nombrable** (una cicatriz, un tatuaje de unidad).

> [!important] El vivero `tags[]` no es un atajo
> `tags: []` existe para etiquetas emergentes que querés filtrar exacto y que **aún no merecen campo propio**. No metas ahí dimensiones controladas (van a su campo) ni palabras-tema descriptivas (las halla la semántica). Lo que se usa seguido se gradúa a campo. En la práctica casi todas las fichas lo llevan vacío.

### Coherencia prosa ↔ campos

La `historia` y el frontmatter describen al mismo personaje: no pueden contradecirse.

- **Todo objeto, arma, cicatriz o aspecto nombrado en la prosa tiene respaldo en un campo** (`equipo`, `rasgos`, `aspectos`, `apariencia`). Si el relato dice que empuña un subfusil, `equipo` lo lista. Y al revés: lo que está en los campos suele asomar en la prosa.
- **Los campos respetan las reglas de facción y rol.** Ejemplo real: un [[baltasar-quevedo-inquisidor|inquisidor]] nunca carga arma de fuego ni chaleco; a lo sumo, los raros llevan arma blanca o bastón. Entonces ni `equipo` ni la prosa pueden darle un fusil o un `chaleco_asalto`. La hoja es coherente con el canon de la entidad, no solo consigo misma.

### Receta desde cero

1. Identidad: `slug` (kebab único), `nombre`, `aliases`, `description`, `barrio`.
2. Capa operativa **contra el canon**: `faccion` → `subfaccion` (si aplica) → `rango` → `especialidad` → `estado` → `lealtad`. Verificá que cada valor exista en su directorio.
3. `atributos` por rango, más `edad`, `genero`.
4. `apariencia`: 2–4 descriptores libres.
5. `aspectos` / `rasgos` / `equipo`: wikilinks al catálogo; si falta una entrada, **creala primero** en `catalogos/`. Respetá las restricciones de facción/rol.
6. `tags: []` (vivero, salvo etiqueta emergente real).
7. `historia`: prosa corta y coherente con todos los campos, en la voz del universo (estereotipo, no biografía).

---

Las secciones de abajo agrupan los ejemplos por el átomo de `faccion` que carga cada ficha: el título de cada `##` lleva ese valor canónico entre código, de modo que el índice sea verificable 1:1 contra el dato.

## Fuerzas Armadas · `fuerzas_armadas`

- [[dario-sandoval-interrogador|Darío Sandoval]]
- [[elian-quiroga-fusilero|Elián Quiroga]]
- [[facundo-rios-tirador|Facundo Ríos]]
- [[gaston-brizuela-zapador|Gastón Brizuela]]
- [[hernan-bordon-asalto|Hernán Bordón]]
- [[ivan-leiva-asalto|Iván Leiva]]
- [[lucas-veron-medico|Lucas Verón]]
- [[marcos-paez-fusilero|Marcos Páez]]
- [[ovidio-gauna-sargento|Ovidio Gauna]]
- [[ruben-ferreyra-cabo|Rubén Ferreyra]]
- [[tomas-aguirre-recluta|Tomás Aguirre]]

## Resistencia Subterránea · `resistencia_subterranea`

- [[anibal-painemal-comandante|Aníbal Painemal]]
- [[brian-curinanco-pandillero|Brian Curiñanco]]
- [[cosme-medico-caido|Cosme]]
- [[cristian-ledesma-barrabrava|Cristian Ledesma]]
- [[damian-figueroa-barrabrava|Damián Figueroa]]
- [[diego-maidana-barrabrava|Diego Maidana]]
- [[ezequiel-madariaga-camarada|Ezequiel Madariaga]]
- [[jonatan-coronel-barrabrava|Jonatan Coronel]]
- [[kevin-wisotzki-barrabrava|Kevin Wisotzki]]
- [[maxi-linares-pandillero|Maxi Linares]]
- [[nahuel-antieco-pandillero|Nahuel Antieco]]
- [[tobias-arce-barrabrava|Tobías Arce]]
- [[valentina-roca-camarada|Valentina Roca]]
- [[walter-cabrera-barrabrava|Walter Cabrera]]
- [[yair-conuecar-pandillero|Yair Coñuecar]]

## Iglesia / Inquisición · `iglesia`

- [[baltasar-quevedo-inquisidor|Baltasar Quevedo]]
- [[cipriano-roldan-inquisidor|Cipriano Roldán]]
- [[eulogio-sarmiento-capellan|Eulogio Sarmiento]]

## Shipibo-Conibo · `shipibo_conibo`

- [[iracema-chaman-pantano|Iracema]]

## Gremio de Pescadores · `gremio_de_pescadores`

- [[luisa-pescadora|Luisa]]

## Punteros · `punteros`

- [[ramon-sosa-puntero|Ramón Sosa]]

## Traficantes de Almas · `traficantes_de_almas`

- [[severo-tratante-de-almas|Severo]]

## Los Umbanda · `los_umbanda`

- [[yara-sacerdotisa-orixa|Yara]]
