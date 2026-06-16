---
title: atributos
tags:
  - syv/pj/atributos
aliases:
  - atributos-y-habilidades
---
# Atributos

_Ver [[hoja-personaje]], [[sistema-tags]], [[contratos]]._

---

## 1. Atributos base (persistidos)

Las **únicas** magnitudes numéricas de capacidad que se guardan en la hoja. Todo otro número se calcula en tiempo real para evitar divergencia.

| Clave | Nombre | Semántica | Escala |
| :--- | :--- | :--- | :---: |
| `cuerpo` | **CUERPO** | Fuerza, resistencia orgánica, potencia muscular. En prosa también **Físico**. | 2..7 |
| `mente` | **MENTE** | Puntería, coordinación, reflejos, lectura táctica, destreza técnica. | 2..7 |
| `alma` | **ALMA** | Aura, liderazgo, voluntad, temple ante el miedo. En prosa también **Espíritu**. | 2..7 |

> [!info] Nombre determinista vs. nombre popular
> En `yaml`/`json`/estadísticas la clave es **siempre** `cuerpo`, `mente`, `alma` —sin reducción a tres caracteres—. En prosa el trío se nombra **"Cuerpo, Mente y Alma"** (o **Espíritu** por Alma); **Físico ≡ Cuerpo** y **Espíritu ≡ Alma**. No existen más las claves `fis`/`tac`/`men`.

> [!info] Escala unificada
> La escala 2..7 es la misma para los tres atributos. Estos son los valores que un personaje puede alcanzar en creación (ver [[generacion-procedural#fase-3-atributos|Fase 3]]); el uno o el tope solo se alcanza vía hito narrativo. 


### 1.1. Mutabilidad

Los atributos quedan **fijos al rango de creación**. Un ascenso posterior cambia el tag `rango/*` pero no los atributos: el progreso real es el equipo, los aspectos y los vínculos ganados en campaña.

Mutación permitida únicamente vía hito de tipo `triple_cero` o `mejora_atributo` — eventos narrativos costosos, no la norma.

### 1.2. Conjunto abierto

El sistema de atributos es **abierto**: se puede introducir un cuarto atributo (ej. `sigilo`) sin migración. Basta definirlo en el catálogo canónico y referenciar su clave en las fórmulas que lo usen. Mientras no exista en la hoja, las fórmulas lo ignoran o lo tratan como `0`. No hay cambios que rompan compatibilidad.

---

## 2. Estadísticas calculadas (en tiempo real)

No se persisten en la hoja. El motor las computa al servir: toma los atributos base de la hoja, aplica los modificadores de tags activos y devuelve el valor final. Si la hoja cambia (nuevo tag, hito), la estadística se recalcula sola.

### 2.1. INICIATIVA

Capacidad para actuar primero en un encuentro. **Determinística, sin tiradas.**

**Fórmula:**

```
base = max(CUERPO, MENTE, ALMA)
INICIATIVA = clamp(base + Σ modificadores_tags, 0, 5)
```

- `Σ modificadores_tags`: suma algebraica de todos los `efecto` sobre `INICIATIVA` de los tags activos (ej. modificadores con `objetivo: stat.iniciativa`).
- `clamp(x, 0, 5)`: el resultado no puede caer por debajo de 0 ni superar 5.

La iniciativa alta actúa primero en la grilla de combate, pero también queda expuesta antes. Actuar primero no es ventaja por sí sola: una ficha mal armada o sin cobertura adelanta su turno sin sacar provecho.

### 2.2. MORAL

Estado de ánimo, voluntad de lucha y cohesión psicológica individual. **`ALMA` es el atributo de los chequeos de miedo y voluntad.**

**Fórmula:**

```
MORAL = ALMA + Σ modificadores_tags
```

- Valor de referencia inicial: igual a `ALMA`.
- Cada fallo en tirada de moral resta 1 punto (fuera de esta fórmula — es consumo, no modificador de tag).

> [!warning] Caída de moral
> La caída progresiva puede llevar a **Desesperación** / **Pánico** (pérdida de control), **Furia** (ataques descontrolados) o **Locura** (inutilización permanente para el combate del personaje).

### 2.3. FATIGA

Recurso físico-mental que limita las acciones continuas. Principal eje de desgaste sostenido.

**Fórmula:**

```
FATIGA_max = CUERPO + ALMA + Σ modificadores_tags
```

- Depósito inicial igual a `FATIGA_max`.
- Los puntos de `CUERPO` se consumen primero. Al agotarse: el personaje gana `salud/cansado`.
- Luego se consumen los de `ALMA`. Al agotarse: gana `salud/exhausto` y queda inmovilizado.
- Cada turno con orden ejecutada, o evento ambiental/mecánico, consume puntos del depósito.

### 2.4. MOVIMIENTO

Velocidad y capacidad de desplazamiento táctico en el tablero.

**Fórmula:**

```
MOVIMIENTO = CUERPO × factor_orden + Σ modificadores_tags
```

- `factor_orden`: multiplicador entero definido por la orden táctica del turno (caminar, correr, reptar, etc.). Lo define el motor de batalla, no esta hoja.

### 2.5. ESTRESS

Tensión acumulada a corto plazo. Actúa como amortiguador antes del colapso mental.

**Fórmula:**

```
ESTRESS_max = ALMA + Σ modificadores_tags   (mínimo 1)
```

- Odómetro descendente: arranca en `ESTRESS_max` (valor típico: 3 para `alma = 3`).
- Cada evento estresante resta 1.
- Al llegar a 0: el personaje recibe un tag mental negativo permanente por lo que resta del combate; el odómetro se reinicia a `ESTRESS_max`.

### 2.6. SANAR

Capacidad de estabilizar y atender heridas (propias o ajenas). No deriva de un atributo base: es una estadística **puramente aditiva**, sin valor de origen — su magnitud nace de los modificadores de tags activos.

**Fórmula:**

```
SANAR = Σ modificadores_tags   (base 0)
```

- Sin contratos que la modifiquen, vale `0`: el personaje no sabe atender heridas.
- La aportan aspectos y habilidades de competencia sanitaria (ver `primeros_auxilios`, `religioso` en [[contratos]]).

### 2.7. PERCEPCION

Agudeza para detectar lo que otros no ven —amenazas, emboscadas, detalles del terreno—. También **puramente aditiva**, base 0.

**Fórmula:**

```
PERCEPCION = Σ modificadores_tags   (base 0)
```

- Es el blanco habitual de los modificadores **condicionales** (ver §3.5): un `+1 percepcion` siempre activo no es lo mismo que un `+1 percepcion` que solo cuenta al calcular encuentros.

---

## 3. Sistema de efectos: cómo los tags modifican atributos y estadísticas

Un `efecto` es un paquete declarativo dentro de un contrato (`aspecto/*`, `efecto.*`) que apunta al vocabulario canónico de esta sección. Cada modificador es un objeto con datos **separados y extraíbles**: el **objetivo** (la variable), el **valor** y una **nota** opcional. La forma completa del contrato vive en [[contratos]].

### 3.1. Objetivo en notación punto

El campo `objetivo` nombra la variable afectada con prefijo:

- `attr.*` — atributos base: `attr.cuerpo`, `attr.mente`, `attr.alma`.
- `stat.*` — estadísticas calculadas: `stat.iniciativa`, `stat.moral`, `stat.fatiga`, `stat.movimiento`, `stat.estress`, `stat.sanar`, `stat.percepcion`.

### 3.2. Delta entero (`mod`)

Suma o resta un valor fijo a la variable objetivo.

```yaml
- objetivo: stat.iniciativa
  mod: +2            # +2 al cálculo de INICIATIVA
- objetivo: stat.fatiga
  mod: -1            # -1 al depósito máximo de FATIGA
- objetivo: attr.alma
  mod: +1            # +1 a ALMA (solo para derivar estadísticas; no altera el atributo persistido salvo hito)
```

`mod` es un entero con signo.

### 3.3. Porcentaje (`pct`)

Multiplica (o reduce) la variable por un porcentaje del valor base calculado en ese momento.

```yaml
- objetivo: stat.movimiento
  pct: -100          # inmoviliza al personaje (MOVIMIENTO × 0)
- objetivo: stat.fatiga
  pct: +50           # aumenta el depósito máximo en 50% del valor base
```

`pct` es un entero con signo, sin el símbolo `%`. Cada modificador lleva `mod` **o** `pct`, nunca ambos. Los porcentajes se aplican **después** de sumar los deltas enteros.

### 3.4. Portabilidad

Tanto los deltas como los porcentajes son **portables**: el mismo formato funciona para cualquier variable del vocabulario canónico presente o futuro. Si se agrega un nuevo atributo o estadística, basta nombrarlo con su prefijo (`attr.*` / `stat.*`) y el sistema de efectos ya sabe cómo procesarlo.

### 3.5. Bonificador condicional (`condicion`)

Un modificador de `efecto` puede llevar un campo **opcional** `condicion: <keyword_slug>`. La `condicion` es una **palabra clave persistente** —un slug— que nombra el momento de juego en el que ese modificador cuenta. **Sin `condicion`, el modificador siempre está activo**; con ella, solo se suma cuando el motor evalúa esa palabra clave.

```yaml
efecto:
  - objetivo: stat.percepcion
    mod: +1                      # SIEMPRE activo: +1 percepción en todo momento
  - objetivo: stat.percepcion
    mod: +1
    condicion: calcular_encuentros   # SOLO al calcular encuentros
```

> [!important] Por qué "+1 percepción" ≠ "+1 percepción para calcular encuentros"
> El primero es un bono permanente: el personaje ve mejor siempre. El segundo es un bono **situacional**: solo pesa cuando el motor resuelve si hay un encuentro (una emboscada, un avistaje), y es invisible el resto del tiempo. Mismo número, alcance distinto. La `condicion` separa "es más perceptivo" de "es más perceptivo *para esto*".

**Palabras clave iniciales** (catálogo abierto, igual que el resto):

| `condicion` | Cuándo cuenta el modificador |
| :--- | :--- |
| `calcular_encuentros` | Al resolver si se produce un encuentro (avistaje, emboscada, detección). |
| `tiradas_activas` | En tiradas que el personaje inicia activamente (acciones deliberadas). |
| `chequeo_miedo` | En chequeos de miedo / voluntad (resueltos por `ALMA`). |

Un modificador sin `condicion` es el caso por defecto y el más común. La palabra clave es un slug legible (minúsculas, guion bajo); el motor decide qué condiciones evalúa en cada momento de juego. Agregar una palabra clave nueva no rompe nada: un modificador con una `condicion` que el motor aún no evalúa simplemente no se aplica todavía.

> [!tip] Acumulación
> Varios tags activos con efectos sobre la misma variable se acumulan algebraicamente. No existe límite de acumulación salvo el que imponga el `clamp` de cada estadística (donde corresponda).
