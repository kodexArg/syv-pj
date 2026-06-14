---
title: atributos
tags:
  - syv/pj/atributos
aliases:
  - stats
  - atributos-y-stats
---
# Atributos

_Ver [[hoja-personaje]], [[sistema-tags]], [[habilidades]]._

---

## 1. Atributos base (persistidos)

Las **únicas** magnitudes numéricas de capacidad que se guardan en la hoja. Todo otro número se calcula en tiempo real para evitar divergencia.

| Clave | Nombre | Semántica | Escala |
| :--- | :--- | :--- | :---: |
| `fis` | **FÍSICO** | Fuerza, resistencia orgánica, potencia muscular. | 2..7 |
| `tac` | **TÁCTICO** | Puntería, coordinación, reflejos, destreza técnica. | 2..7 |
| `men` | **MENTAL** | Fortaleza psicológica, moral base, resistencia al estrés, liderazgo. | 2..7 |

> [!info] Escala unificada
> La escala 2..7 es la misma para los tres atributos. Estos son los valores que un rol puede alcanzar en creación (ver [[generacion-procedural#fase-3-atributos|Fase 3]]); el uno o el tope solo se alcanza vía hito narrativo. 


### 1.1. Mutabilidad

Los atributos quedan **fijos al rango de creación**. Un ascenso posterior cambia el tag `rango.*` pero no los atributos: el progreso real es el equipo, los aspectos y los vínculos ganados en campaña.

Mutación permitida únicamente vía hito de tipo `triple_cero` o `mejora_atributo` — eventos narrativos costosos, no la norma.

### 1.2. Conjunto abierto

El sistema de atributos es **abierto**: se puede introducir un cuarto atributo (ej. `liderazgo`, `sigilo`) sin migración. Basta definirlo en el catálogo canónico y referenciar su clave en las fórmulas que lo usen. Mientras no exista en la hoja, las fórmulas lo ignoran o lo tratan como `0`. No hay cambios que rompan compatibilidad.

---

## 2. Estadísticas calculadas (en tiempo real)

No se persisten en la hoja. El motor las computa al servir: toma los atributos base de la hoja, aplica los modificadores de tags activos y devuelve el valor final. Si la hoja cambia (nuevo tag, hito), la estadística se recalcula sola.

### 2.1. INICIATIVA

Capacidad para actuar primero en un encuentro. **Determinística, sin tiradas.**

**Fórmula:**

```
base = max(FISICO, TACTICO, MENTAL)
INICIATIVA = clamp(base + Σ modificadores_tags, 0, 5)
```

- `Σ modificadores_tags`: suma algebraica de todos los `efecto` sobre `INICIATIVA` de los tags activos (ej. `(+2) INICIATIVA`, `(-1) INICIATIVA`).
- `clamp(x, 0, 5)`: el resultado no puede caer por debajo de 0 ni superar 5.

La iniciativa alta actúa primero en la grilla de combate, pero también queda expuesta antes. Actuar primero no es ventaja por sí sola: una ficha mal armada o sin cobertura adelanta su turno sin sacar provecho.

### 2.2. MORAL

Estado de ánimo, voluntad de lucha y cohesión psicológica individual.

**Fórmula:**

```
MORAL = MENTAL + Σ modificadores_tags
```

- Valor de referencia inicial: igual a `MENTAL`.
- Cada fallo en tirada de moral resta 1 punto (fuera de esta fórmula — es consumo, no modificador de tag).

> [!warning] Caída de moral
> La caída progresiva puede llevar a **Desesperación** / **Pánico** (pérdida de control), **Furia** (ataques descontrolados) o **Locura** (inutilización permanente para el combate del personaje).

### 2.3. FATIGA

Recurso físico-mental que limita las acciones continuas. Principal eje de desgaste sostenido.

**Fórmula:**

```
FATIGA_max = FISICO + MENTAL + Σ modificadores_tags
```

- Pool inicial igual a `FATIGA_max`.
- Los puntos de `FISICO` se consumen primero. Al agotarse: el personaje gana `salud.cansado`.
- Luego se consumen los de `MENTAL`. Al agotarse: gana `salud.exhausto` y queda inmovilizado.
- Cada turno con orden ejecutada, o evento ambiental/mecánico, consume puntos del pool.

### 2.4. MOVIMIENTO

Velocidad y capacidad de desplazamiento táctico en el tablero.

**Fórmula:**

```
MOVIMIENTO = FISICO × factor_orden + Σ modificadores_tags
```

- `factor_orden`: multiplicador entero definido por la orden táctica del turno (caminar, correr, reptar, etc.). Lo define el motor de batalla, no esta hoja.
- Si el personaje integra una escuadra, la velocidad grupal queda limitada por el menor `MOVIMIENTO` individual entre los miembros activos.

### 2.5. ESTRESS

Tensión acumulada a corto plazo. Actúa como amortiguador antes del colapso mental.

**Fórmula:**

```
ESTRESS_max = MENTAL + Σ modificadores_tags   (mínimo 1)
```

- Odómetro descendente: arranca en `ESTRESS_max` (valor típico: 3 para `men = 3`).
- Cada evento estresante resta 1.
- Al llegar a 0: el personaje recibe un tag mental negativo permanente por lo que resta del combate; el odómetro se reinicia a `ESTRESS_max`.

---

## 3. Sistema de efectos: cómo los tags modifican atributos y estadísticas

Un `efecto` es un paquete declarativo dentro de un tag (`aspecto.*`, `efecto.*`) que apunta al vocabulario canónico de esta sección. Dos formatos:

### 3.1. Delta entero

Suma o resta un valor fijo a la variable objetivo.

```
"(+2) INICIATIVA"    → +2 al cálculo de INICIATIVA
"(-1) FATIGA"        → -1 al pool máximo de FATIGA
"(+1) MENTAL"        → +1 al atributo MENTAL (solo para derivar estadísticas; no altera el atributo persistido salvo hito)
```

Notación: `(+N)` o `(-N)` seguido del nombre en mayúsculas.

### 3.2. Porcentaje

Multiplica (o reduce) la variable por un porcentaje del valor base calculado en ese momento.

```
"-100% MOVIMIENTO"   → inmoviliza al personaje (MOVIMIENTO × 0)
"+50% FATIGA"        → aumenta el pool máximo en 50% del valor base
```

Notación: `+N%` o `-N%` seguido del nombre en mayúsculas. Los porcentajes se aplican **después** de sumar los deltas enteros.

### 3.3. Portabilidad

Tanto los deltas como los porcentajes son **portables**: el mismo formato funciona para cualquier variable del vocabulario canónico presente o futuro. Si se agrega un nuevo atributo o estadística, basta nombrarlo en mayúsculas y el sistema de efectos ya sabe cómo procesarlo.

> [!tip] Acumulación
> Varios tags activos con efectos sobre la misma variable se acumulan algebraicamente. No existe límite de acumulación salvo el que imponga el `clamp` de cada estadística (donde corresponda).
