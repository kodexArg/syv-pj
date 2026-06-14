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
> Un **contrato** es una palabra o frase corta que, al aplicarse a un personaje, entrega un **paquete declarado**: modificadores numéricos, habilitadores de tirada y/o efectos referenciables. El nombre es la cara legible; el efecto es la letra chica. Todo contrato es, en esencia, una [[sistema-tags|etiqueta]].

> [!warning] Vocabulario unificado
> *rasgo*, *ventaja* y *destreza* **ya no existen como categorías.** Quedaron fundidos en tres: **`aspecto`** (lo que era *rasgo* **y** *ventaja*), **`habilidad`** (lo que era *destreza*) y **`efecto`**. Si encontrás `rasgo.*`, `ventaja.*` o `destreza.*` en una hoja vieja, son legado a migrar.

---

## §1 — El patrón-contrato

Todo contrato sigue la misma estructura lógica:

```
nombre legible  →  paquete declarado
```

El **nombre** es el identificador humano del contrato — la etiqueta que el motor, el narrador y el jugador ven. Corto, evocador y estable.

El **paquete** es lo que ese nombre promete mecánicamente: modificadores sobre el vocabulario canónico (`FISICO`, `TACTICO`, `MENTAL`, `INICIATIVA`, `MORAL`, `FATIGA`, `MOVIMIENTO`, `ESTRESS`), habilitadores de tirada, o efectos referenciables. El paquete puede ser positivo, negativo o mixto.

Este patrón tiene tres variantes según el **tipo de contrato:**

| Tipo | Naturaleza | Efecto | `requires` | Polaridad |
|---|---|---|---|---|
| `aspecto` | Identidad mecánicamente activa | pasivo o disparado | condicional (salvo origen narrativo) | mixta |
| `habilidad` | Habilitador de tirada | ninguno directo | condicional | neutra |
| `efecto` | Bloque referenciable | pasivo o externo | no aplica | mixta |

La categoría en el tag sigue el mismo patrón: `aspecto.vanguardia`, `habilidad.tiro_de_precision`, `efecto.panico_momentaneo`.

---

## §2 — Aspecto: identidad mecánicamente activa

Un **aspecto** es un rasgo de carácter, condición física, marca de comportamiento o ventaja ganada que tiene peso mecánico. No es solo sabor narrativo — declara un efecto que el motor aplica mientras el personaje lo lleve. Absorbe lo que antes se partía en *rasgo* (identidad con peso) y *ventaja* (recompensa narrativa): la diferencia ya no es de categoría, sino de **origen** (ver §2.4).

### 2.1. Estructura

Un aspecto pasivo declara `efecto` a nivel raíz:

```yaml
slug: vanguardia
nombre: "Vanguardia"
categoria: aspecto
descripcion: >
  Siempre va al frente. Empuja la línea sin que nadie lo pida.
  El rasgo más valioso en un punto de asalto.
efecto:
  - "(+2) INICIATIVA"
  - "(+1) MORAL"
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

### 2.2. Polaridad mixta

Los aspectos admiten positivos, negativos y combinados en la misma bolsa. No hay jerarquía de deseabilidad: `cobarde` y `veterano` son contratos del mismo tipo, con paquetes opuestos.

```yaml
# Aspecto negativo
slug: cobarde
nombre: "Cobarde"
categoria: aspecto
descripcion: >
  Evita el combate directo siempre que puede. Se paraliza ante la presión.
efecto:
  - "(-2) MORAL"
  - "(-1) INICIATIVA"

# Aspecto mixto
slug: terco
nombre: "Terco"
categoria: aspecto
descripcion: >
  No cede. Esa firmeza le salva la moral en situaciones extremas,
  pero lo hace lento para adaptarse a órdenes cambiantes.
efecto:
  - "(+2) MORAL"
  - "(-1) INICIATIVA"
```

### 2.3. `requires` en aspectos estructurales

Un aspecto puede declarar `requires` cuando asume una condición previa en la hoja:

```yaml
slug: tirador_experto
nombre: "Tirador experto"
categoria: aspecto
descripcion: >
  Años de práctica le dan una calma que los reclutas no pueden fingir.
efecto:
  - "(+2) TACTICO"
requires:
  require_any:
    - habilidad.tiro_de_precision
    - rango.tirador_designado
```

Esto es documentación ejecutable. El motor no lo impone; el generador y el curador lo respetan. Ver [[sistema-tags#§6.4 Sistema requires|§6.4 de sistema-tags]].

### 2.4. Origen narrativo (lo que antes era *ventaja*)

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
  - "(+2) TACTICO"
  - "(+1) INICIATIVA"
```

La vía canónica para ganar un aspecto narrativo es el `historial[]`: un hito (p. ej. `aspecto_obtenido`) registra el evento y el tag se agrega a la hoja. El hito es de solo añadir; el aspecto persiste. Mecánicamente, en tiempo de ejecución, un aspecto narrativo se aplica igual que cualquier aspecto pasivo — la diferencia es de **origen y semántica**, no de motor.

---

## §3 — Habilidad: habilitador de tirada

Una **habilidad** (lo que antes era *destreza*) no modifica atributos ni estadísticas directamente. Su función es binaria: **habilitar un chequeo** contra el `atributo_dominante` declarado en su entrada de catálogo.

El motor pregunta: ¿el personaje tiene `habilidad.X`? Si sí, puede hacer la tirada. Si no, la acción no es posible (o se resuelve con penalización según regla del motor).

### 3.1. Estructura

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

### 3.2. Por qué la habilidad no modifica estadísticas

Una habilidad habilitada no te hace mejor en el atributo; te da acceso a aplicarlo. La diferencia importa: un personaje con `TACTICO 3` y `habilidad.tiro_de_precision` puede intentar ese disparo. Uno con `TACTICO 5` sin la habilidad no puede. El nivel del atributo determina qué tan bien saldrá la tirada; la habilidad determina si puede hacerse.

Esto evita inflación de estadísticas por acumulación de habilidades y mantiene limpia la separación entre **capacidad** (atributos) y **conocimiento** (habilidades).

---

## §4 — Efecto: bloque estructurado referenciable

Un **efecto** (`efecto.*`) es un bloque de consecuencias mecánicas que puede ser aplicado por referencia desde otras etiquetas — principalmente desde los `trigger-action` de aspectos reactivos, pero también inline en cualquier etiqueta que declare efectos permanentes.

### 4.1. Efecto externo (archivo propio)

Vive en `tags/efecto/{slug}.yaml`. Es el destino de un `trigger-action`:

```yaml
slug: panico_momentaneo
nombre: "Pánico momentáneo"
categoria: efecto
descripcion: >
  El personaje pierde un turno completo bajo fuego y agacha la cabeza.
  Aplica por un turno, luego se disipa.
efecto:
  - "(-2) MORAL"
  - "-100% MOVIMIENTO"
```

```yaml
slug: furia_de_combate
nombre: "Furia de combate"
categoria: efecto
descripcion: >
  Entra en un estado de ataque descontrolado. Sube la agresividad pero
  ignora la cobertura — potente y peligroso para él mismo.
efecto:
  - "(+2) FISICO"
  - "(-2) TACTICO"
  - "(-1) ESTRESS"
```

### 4.2. Efecto inline

Cuando el modificador es permanente y simple, no necesita archivo propio. Se declara directamente en la etiqueta que lo aplica (típicamente un `aspecto` pasivo). Ver [[#§2 — Aspecto identidad mecánicamente activa]].

### 4.3. Vocabulario canónico

Los modificadores de cualquier efecto — externo o inline — solo pueden apuntar a las siguientes variables:

- **Atributos base:** `FISICO`, `TACTICO`, `MENTAL`
- **Estadísticas calculadas:** `INICIATIVA`, `MORAL`, `FATIGA`, `MOVIMIENTO`, `ESTRESS`

Formatos válidos: `"(+1) MENTAL"`, `"(-2) MORAL"`, `"-100% MOVIMIENTO"`, `"(+2) INICIATIVA"`. Ver [[atributos]] para la mecánica de cada variable.

---

## §5 — El patrón en práctica: lectura de una hoja

Cuando el motor sirve un personaje, recorre sus etiquetas y aplica contratos:

1. **Aspectos pasivos** — suma sus `efecto` al cálculo de estadísticas en caliente (incluye los de origen narrativo: sin diferencia mecánica en tiempo de ejecución).
2. **Aspectos reactivos** — registra sus `trigger` para evaluarlos ante eventos de partida.
3. **Habilidades** — marca el habilitador binario. El motor lo consulta cuando una acción requiere la habilidad.
4. **Efectos activos** — aplicados directamente o referenciados vía `trigger-action`.

Ningún contrato modifica la hoja persistida. Todo cálculo es **en caliente** sobre los atributos base `fis`, `tac`, `men`. Las estadísticas (`INICIATIVA`, `MORAL`, etc.) no se guardan — se derivan al servir. Ver [[hoja-personaje]] para la estructura de la hoja y [[atributos]] para las fórmulas de derivación.

---

## §6 — Ejemplos de contratos SyV

### Aspecto de veterano (pasivo, positivo)

```yaml
slug: veterano_de_campo
nombre: "Veterano de campo"
categoria: aspecto
descripcion: >
  Lo ha visto todo. No se sorprende, no se paraliza, no abandona el puesto.
  Su presencia sola eleva a los que tiene al lado.
efecto:
  - "(+1) MENTAL"
  - "(+1) MORAL"
  - "(+1) INICIATIVA"
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
  - "(-1) FISICO"
  - "-30% MOVIMIENTO"
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
  - "(+1) INICIATIVA"
  - "(+1) FISICO"
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

## §7 — Extensión del catálogo de contratos

Los contratos se extienden igual que cualquier etiqueta — sin migración, sin permiso:

- **Nuevo aspecto:** agregar `tags/aspecto/{slug}.yaml` con los cuatro campos obligatorios y el campo `efecto` (o `trigger`). Marcá `origen: narrativo` si es una recompensa de hito (sin `requires`, positivo).
- **Nueva habilidad:** agregar `tags/habilidad/{slug}.yaml` con `atributo_dominante`.
- **Nuevo efecto:** agregar `tags/efecto/{slug}.yaml` con la lista de instrucciones.

Un contrato desconocido no rompe la hoja. La coherencia la garantiza la curaduría del catálogo, no la validación de esquema.
