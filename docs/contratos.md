---
title: Aspectos, Habilidades y Efectos como Contratos
tags:
  - syv/pj/docs
  - syv/contratos
  - syv/habilidades
  - syv/atributos
aliases:
  - Contratos
  - Habilidades
  - Rasgos y Ventajas
  - rasgos-y-ventajas
---
# Aspectos, Habilidades y Efectos como Contratos

> [!info] Concepto central
> Un **contrato** es la información que vive **detrás** de ciertos tags. El [[sistema-tags|tag]] es el **link** —un puntero que puede o no llevar algo detrás—; el contrato es ese algo: un **paquete declarado** de modificadores numéricos, habilitadores de tirada y/o efectos referenciables. El nombre es la cara legible; el paquete es la letra chica. Tres categorías traen contrato siempre: **`aspecto`**, **`habilidad`** y **`efecto`**.

> [!warning] Vocabulario unificado
> *ventaja* y *destreza* **ya no existen como categorías**: *ventaja* → **`aspecto`** de origen narrativo (§5.4), *destreza* → **`habilidad`**. De *rasgo*, lo que tenía **peso mecánico** (identidad con efecto) pasó a **`aspecto`**; el *rasgo* **puramente cosmético** —cicatriz, tatuaje, constitución, sin efecto— sigue siendo categoría propia, un tag sin contrato (ver [[sistema-tags#§3 — Categorías de referencia|sistema-tags §3]]). Si encontrás `ventaja.*` o `destreza.*` en una hoja vieja, son legado a migrar.

---

## §1 — Tag y contrato: el link y la información

Un [[sistema-tags|tag]] es un **link**: un identificador discreto que se posa sobre el personaje y apunta a algo. Como todo link, puede llevar información detrás **o no llevarla** — un tag huérfano como `habilidad.personal.pianista` afirma el hecho sin describir su alcance hasta que alguien escriba su referencia en el catálogo.

Un **contrato** es esa información: la entrada de catálogo (`tags/<categoria>/<slug>.yaml`) que vive detrás del link. **No todos los tags tienen contrato.** `rango.sargento`, `faccion.confederados`, `lealtad.ejercito_rojo` o `aliado.K9F2H3M4` son tags puros —clasificatorios o relacionales—, sin paquete mecánico. Pero los tags de tres categorías traen contrato **siempre**:

| | Tag | Contrato |
|---|---|---|
| Qué es | un link discreto sobre el personaje | la información detrás del link |
| ¿Siempre presente? | sí — es la unidad atómica del esquema | no — solo bajo `aspecto.*`, `habilidad.*`, `efecto.*` |
| Dónde vive | en `tags[]` de la [[hoja-personaje\|hoja]] | en el catálogo `tags/<categoria>/<slug>.yaml` |
| Qué entrega | la afirmación de un hecho | un **paquete**: modificadores, habilitadores, efectos |

> [!tip] Lo que no trae contrato sigue siendo tag
> `rango.*`, `faccion.*`, `lealtad.*`, `aliado.*`, `nemesis.*` no declaran paquete mecánico: son links puros (ver [[sistema-tags]], [[nemesis-y-aliados|nemesis-y-aliados.md]], [[lealtad|lealtad.md]]). Y un contrato puede, además del paquete, **referenciar información adicional** —incluso prosa: quién sabe lo que el contrato escriba detrás del tag.

---

## §2 — Por qué "contrato": misma data, no importa quién lo active

Se llaman **contratos** porque cumplen una promesa fija: entregan **siempre los mismos datos**, sin importar quién los porte. Si `efecto.inmune_al_miedo` vuelve inmune al miedo, lo hace idéntico tanto si el portador es un **dron de guerra** como un **inquisidor**. El contrato no negocia con el personaje: declara un paquete y lo cumple igual sobre toda hoja.

De ahí se sigue lo central: **aspecto, habilidad y efecto son mecánicamente la misma clase de objeto.** No tienen diferencia funcional — los tres son contratos que entregan datos extraíbles. Lo que los separa es el **rol semántico**, no el motor:

| Tipo | Rol semántico | Qué entrega |
|---|---|---|
| `aspecto` | identidad mecánicamente activa | modificadores (pasivos) o un disparador |
| `habilidad` | habilitador de tirada | acceso binario a un chequeo |
| `efecto` | bloque referenciable | modificadores, aplicados por referencia o inline |

> [!important] Agnóstico al sistema
> No sabemos —ni nos importa todavía— cómo se implementará el motor. El contrato vive en la capa de **dominio**: promete data portable. Cómo cada cliente la consume (motor de juego, motor de batalla, generador visual) es problema del cliente, no del contrato. Ver [[casos-de-uso|casos-de-uso.md]].

---

## §3 — El contrato como entidad: sin relación, un pool que crece

El contrato es una **entidad** de relación **varios-a-varios** con los personajes — es decir, en la práctica, **sin relación**. Cualquier contrato puede posarse sobre cualquier personaje; no hay tabla de pertenencia ni dueño. Un `aspecto.veterano_de_campo` no "pertenece" a nadie: está definido una vez y queda disponible para todas las hojas.

Los contratos definidos se acumulan en un **pool** del que el generador y el curador van tirando (ver [[generacion-procedural#Fase 4 — Tags adicionales|Fase 4]]). El pool crece **abierto/cerrado, incrementalmente**: agregar un contrato nuevo nunca rompe los existentes ni exige migración. Un `aspecto.*` más en el catálogo es, simplemente, una opción más en el sorteo.

---

## §4 — El patrón-contrato

Todo contrato sigue la misma estructura lógica:

```
nombre legible  →  paquete declarado
```

El **nombre** es el identificador humano del contrato — la etiqueta que el motor, el narrador y el jugador ven. Corto, evocador y estable.

El **paquete** es lo que ese nombre promete mecánicamente: modificadores sobre el vocabulario canónico, habilitadores de tirada o efectos referenciables. Puede ser positivo, negativo o mixto.

Este patrón tiene tres variantes según el **tipo de contrato:**

| Tipo | Naturaleza | Efecto | `requires` | Polaridad |
|---|---|---|---|---|
| `aspecto` | Identidad mecánicamente activa | pasivo o disparado | condicional (salvo origen narrativo) | mixta |
| `habilidad` | Habilitador de tirada | ninguno directo | condicional | neutra |
| `efecto` | Bloque referenciable | pasivo o externo | no aplica | mixta |

La categoría en el tag sigue el mismo patrón: `aspecto.vanguardia`, `habilidad.tiro_de_precision`, `efecto.panico_momentaneo`.

### 4.1. El paquete: `efecto[]` estructurado

El paquete de modificadores es una **lista**. Cada modificador es un objeto con tres datos **separados y extraíbles**: qué variable afecta, cuánto, y opcionalmente por qué.

```yaml
efecto:
  - objetivo: stat.iniciativa          # QUÉ variable afecta (notación punto)
    mod: +2                            # CUÁNTO (delta entero, con signo)
  - objetivo: stat.moral
    mod: +1
    nota: "Su sola presencia levanta a los de al lado."   # opcional: el porqué
```

- **`objetivo`** — la variable canónica afectada, en notación punto (ver §4.2). `attr.*` para atributos base, `stat.*` para estadísticas calculadas.
- **`mod`** — modificador como **delta entero** con signo (`+2`, `-1`).
- **`pct`** — modificador como **porcentaje** con signo, sin el símbolo `%` (`-100` = ×0). Para magnitudes continuas:

```yaml
efecto:
  - objetivo: stat.movimiento
    pct: -100                          # inmoviliza (MOVIMIENTO × 0)
```

  Cada modificador lleva `mod` **o** `pct`, nunca ambos.
- **`nota`** — opcional. Descripción subjetiva de *este* modificador. No confundir con la `descripcion` del contrato, que describe el contrato entero.

> [!warning] Por qué estructurado y no string
> La forma vieja `"(+2) INICIATIVA"` empaquetaba valor y objetivo en una sola cadena: no era extraíble sin parsear. La forma estructurada **separa el valor (`mod`/`pct`) del objetivo (`objetivo`) y de la nota (`nota`)** — cada dato sale directo, sin regex. Si encontrás `"(+N) VARIABLE"` en una hoja vieja, es legado a migrar.

### 4.2. Vocabulario canónico de objetivos

`objetivo` solo apunta a estas variables. La mecánica de cada una vive en [[atributos]].

**Atributos base** (`attr.*`, persistidos):

| `objetivo` | Variable | Clave de hoja |
|---|---|---|
| `attr.fisico` | FÍSICO | `fis` |
| `attr.tactico` | TÁCTICO | `tac` |
| `attr.mental` | MENTAL | `men` |

**Estadísticas calculadas** (`stat.*`, derivadas al servir):

| `objetivo` | Variable |
|---|---|
| `stat.iniciativa` | INICIATIVA |
| `stat.moral` | MORAL |
| `stat.fatiga` | FATIGA |
| `stat.movimiento` | MOVIMIENTO |
| `stat.estress` | ESTRESS |

El conjunto es **abierto**: si [[atributos]] suma una variable nueva, basta nombrarla con su prefijo (`attr.*` / `stat.*`) y el sistema de efectos la procesa sin migración.

---

## §5 — Aspecto: identidad mecánicamente activa

Un **aspecto** es un rasgo de carácter, condición física, marca de comportamiento o ventaja ganada que tiene peso mecánico. No es solo sabor narrativo — declara un efecto que el motor aplica mientras el personaje lo lleve. Absorbe lo que antes se partía en *rasgo con peso mecánico* (identidad con efecto) y *ventaja* (recompensa narrativa): la diferencia ya no es de categoría, sino de **origen** (ver §5.4). El *rasgo* puramente cosmético —sin efecto— no es un aspecto: sigue siendo un tag `rasgo.*` sin contrato.

### 5.1. Estructura

Un aspecto pasivo declara `efecto` a nivel raíz:

```yaml
slug: vanguardia
nombre: "Vanguardia"
categoria: aspecto
descripcion: >
  Siempre va al frente. Empuja la línea sin que nadie lo pida.
  El rasgo más valioso en un punto de asalto.
efecto:
  - objetivo: stat.iniciativa
    mod: +2
  - objetivo: stat.moral
    mod: +1
    nota: "Empujar la línea arrastra a los de atrás."
```

Un aspecto reactivo declara `trigger` en lugar de `efecto` directo:

```yaml
slug: panico_al_fuego
nombre: "Pánico al fuego"
categoria: aspecto
descripcion: >
  El ruido de los disparos cercanos le dispara el instinto de huida.
  Funciona bajo presión normal, pero falla ante el caos.
trigger:
  evento: bajo_fuego
  condicion: primera_vez
  probabilidad: "60%"
  trigger-action:
    - efecto.huida_instintiva
```

### 5.2. Polaridad mixta

Los aspectos admiten positivos, negativos y combinados en la misma bolsa. No hay jerarquía de deseabilidad: `cobarde` y `veterano` son contratos del mismo tipo, con paquetes opuestos.

```yaml
# Aspecto negativo
slug: cobarde
nombre: "Cobarde"
categoria: aspecto
descripcion: >
  Evita el combate directo siempre que puede. Se paraliza ante la presión.
efecto:
  - objetivo: stat.moral
    mod: -2
  - objetivo: stat.iniciativa
    mod: -1

# Aspecto mixto
slug: terco
nombre: "Terco"
categoria: aspecto
descripcion: >
  No cede. Esa firmeza le salva la moral en situaciones extremas,
  pero lo hace lento para adaptarse a órdenes cambiantes.
efecto:
  - objetivo: stat.moral
    mod: +2
  - objetivo: stat.iniciativa
    mod: -1
```

### 5.3. `requires` en aspectos estructurales

Un aspecto puede declarar `requires` cuando asume una condición previa en la hoja:

```yaml
slug: tirador_experto
nombre: "Tirador experto"
categoria: aspecto
descripcion: >
  Años de práctica le dan una calma que los reclutas no pueden fingir.
efecto:
  - objetivo: attr.tactico
    mod: +2
requires:
  require_any:
    - habilidad.tiro_de_precision
    - rango.tirador_designado
```

Esto es documentación ejecutable. El motor no lo impone; el generador y el curador lo respetan. Ver [[sistema-tags#6.4. Sistema requires|§6.4 de sistema-tags]].

### 5.4. Origen narrativo (lo que antes era *ventaja*)

Un aspecto de **origen narrativo** es una ventaja otorgada al azar como sorpresa — un hito en campo, una jugada extraordinaria, un momento de suerte. Es la antigua noción de *ventaja*, ahora un aspecto con tres marcas características:

- **`origen: narrativo`** en el catálogo (frente a `canon`/`emergente`/`custom`).
- **Sin `requires` nunca.** Cualquier aspecto narrativo puede aparecer sobre cualquier personaje; la sorpresa es parte de su naturaleza.
- **Siempre positivo.** Su paquete es siempre una ventaja. Las penalizaciones van a aspectos estructurales.

```yaml
slug: ojo_de_aguila
nombre: "Ojo de águila"
categoria: aspecto
origen: narrativo
descripcion: >
  Ve lo que otros se pierden. Alcance visual y percepción táctica fuera
  de lo común — el tipo que avisa antes de que nadie más escuche nada.
efecto:
  - objetivo: attr.tactico
    mod: +2
  - objetivo: stat.iniciativa
    mod: +1
```

La vía canónica para ganar un aspecto narrativo es el `historial[]`: un hito `agregar_tag` registra el evento (con `metadata: { categoria: aspecto, valor: <slug> }`) y el tag se agrega a la hoja. El hito es de solo añadir; el aspecto persiste. Ver [[historial|historial.md]]. Mecánicamente, en tiempo de ejecución, un aspecto narrativo se aplica igual que cualquier aspecto pasivo — la diferencia es de **origen y semántica**, no de motor.

---

## §6 — Habilidad: habilitador de tirada

Una **habilidad** (lo que antes era *destreza*) no modifica atributos ni estadísticas directamente. Su función es binaria: **habilitar un chequeo** contra el `atributo_dominante` declarado en su entrada de catálogo.

El motor pregunta: ¿el personaje tiene `habilidad.X`? Si sí, puede hacer la tirada. Si no, la acción no es posible (o se resuelve con penalización según regla del motor).

### 6.1. Estructura

```yaml
slug: primeros_auxilios
nombre: "Primeros auxilios"
categoria: habilidad
descripcion: >
  Sabe estabilizar una herida bajo presión. No es médico — pero mantiene
  al compañero con vida hasta que llegue alguien que lo sea.
atributo_dominante: men
```

```yaml
slug: tiro_de_precision
nombre: "Tiro de precisión"
categoria: habilidad
descripcion: >
  Disparo deliberado a distancia con arma larga. Necesita tiempo,
  posición y visión — pero cuando conecta, conecta bien.
atributo_dominante: tac
```

### 6.2. Por qué la habilidad no modifica estadísticas

Una habilidad habilitada no te hace mejor en el atributo; te da acceso a aplicarlo. La diferencia importa: un personaje con `TACTICO 3` y `habilidad.tiro_de_precision` puede intentar ese disparo. Uno con `TACTICO 5` sin la habilidad no puede. El nivel del atributo determina qué tan bien saldrá la tirada; la habilidad determina si puede hacerse.

Esto evita inflación de estadísticas por acumulación de habilidades y mantiene limpia la separación entre **capacidad** (atributos) y **conocimiento** (habilidades).

---

## §7 — Efecto: bloque estructurado referenciable

Un **efecto** (`efecto.*`) es un bloque de consecuencias mecánicas que puede ser aplicado por referencia desde otras etiquetas — principalmente desde los `trigger-action` de aspectos reactivos, pero también inline en cualquier etiqueta que declare efectos permanentes.

### 7.1. Efecto externo (archivo propio)

Vive en `tags/efecto/{slug}.yaml`. Es el destino de un `trigger-action`:

```yaml
slug: panico_momentaneo
nombre: "Pánico momentáneo"
categoria: efecto
descripcion: >
  El personaje pierde un turno completo bajo fuego y agacha la cabeza.
  Aplica por un turno, luego se disipa.
efecto:
  - objetivo: stat.moral
    mod: -2
  - objetivo: stat.movimiento
    pct: -100
```

```yaml
slug: furia_de_combate
nombre: "Furia de combate"
categoria: efecto
descripcion: >
  Entra en un estado de ataque descontrolado. Sube la agresividad pero
  ignora la cobertura — potente y peligroso para él mismo.
efecto:
  - objetivo: attr.fisico
    mod: +2
  - objetivo: attr.tactico
    mod: -2
  - objetivo: stat.estress
    mod: -1
```

### 7.2. Efecto inline

Cuando el modificador es permanente y simple, no necesita archivo propio. Se declara directamente en la etiqueta que lo aplica (típicamente un `aspecto` pasivo). Ver [[#§5 — Aspecto identidad mecánicamente activa]].

### 7.3. Vocabulario canónico

Los modificadores de cualquier efecto —externo o inline— solo pueden apuntar al vocabulario canónico de objetivos (`attr.*` / `stat.*`). La tabla completa está en §4.2; la mecánica de cada variable, en [[atributos]].

---

## §8 — El patrón en práctica: lectura de una hoja

Cuando el motor sirve un personaje, recorre sus etiquetas y aplica contratos:

1. **Aspectos pasivos** — suma sus `efecto` al cálculo de estadísticas en caliente (incluye los de origen narrativo: sin diferencia mecánica en tiempo de ejecución).
2. **Aspectos reactivos** — registra sus `trigger` para evaluarlos ante eventos de partida.
3. **Habilidades** — marca el habilitador binario. El motor lo consulta cuando una acción requiere la habilidad.
4. **Efectos activos** — aplicados directamente o referenciados vía `trigger-action`.

Ningún contrato modifica la hoja persistida. Todo cálculo es **en caliente** sobre los atributos base `fis`, `tac`, `men`. Las estadísticas (`INICIATIVA`, `MORAL`, etc.) no se guardan — se derivan al servir. Ver [[hoja-personaje]] para la estructura de la hoja y [[atributos]] para las fórmulas de derivación.

---

## §9 — Ejemplos de contratos SyV

### Aspecto de veterano (pasivo, positivo)

```yaml
slug: veterano_de_campo
nombre: "Veterano de campo"
categoria: aspecto
descripcion: >
  Lo ha visto todo. No se sorprende, no se paraliza, no abandona el puesto.
  Su presencia sola eleva a los que tiene al lado.
efecto:
  - objetivo: attr.mental
    mod: +1
  - objetivo: stat.moral
    mod: +1
  - objetivo: stat.iniciativa
    mod: +1
```

### Aspecto de herida antigua (pasivo, negativo)

```yaml
slug: rodilla_vencida
nombre: "Rodilla vencida"
categoria: aspecto
descripcion: >
  Una lesión vieja que nunca cerró del todo. Aguanta en combate,
  pero no corre como antes.
efecto:
  - objetivo: attr.fisico
    mod: -1
  - objetivo: stat.movimiento
    pct: -30
```

### Aspecto reactivo de cólera

```yaml
slug: colera_ciega
nombre: "Cólera ciega"
categoria: aspecto
descripcion: >
  Cuando ve caer a un compañero, pierde el control táctico.
  Feroz y peligroso — para todos.
trigger:
  evento: baja_aliada
  condicion: presenciada
  probabilidad: "70%"
  trigger-action:
    - efecto.furia_de_combate
```

### Aspecto narrativo de suerte (origen narrativo, positivo, sin requires)

```yaml
slug: instinto_de_supervivencia
nombre: "Instinto de supervivencia"
categoria: aspecto
origen: narrativo
descripcion: >
  Esquiva por reflejo puro. Ningún entrenamiento lo explica —
  el cuerpo actúa antes de que la cabeza procese la amenaza.
efecto:
  - objetivo: stat.iniciativa
    mod: +1
  - objetivo: attr.fisico
    mod: +1
```

### Habilidad de demolición

```yaml
slug: manejo_de_explosivos
nombre: "Manejo de explosivos"
categoria: habilidad
descripcion: >
  Sabe preparar, colocar y detonar cargas. También sabe cuándo
  no hacerlo — que es la mitad del oficio.
atributo_dominante: tac
```

---

## §10 — Extensión del catálogo de contratos

Los contratos se extienden igual que cualquier etiqueta — sin migración, sin permiso (es el pool de §3 creciendo):

- **Nuevo aspecto:** agregar `tags/aspecto/{slug}.yaml` con los cuatro campos obligatorios y el campo `efecto` (o `trigger`). Marcá `origen: narrativo` si es una recompensa de hito (sin `requires`, positivo).
- **Nueva habilidad:** agregar `tags/habilidad/{slug}.yaml` con `atributo_dominante`.
- **Nuevo efecto:** agregar `tags/efecto/{slug}.yaml` con la lista de modificadores estructurados.

Un contrato desconocido no rompe la hoja. La coherencia la garantiza la curaduría del catálogo, no la validación de esquema. Detalle de los campos de catálogo en [[sistema-tags#§6 — Campos del archivo de catálogo|§6 de sistema-tags]].
