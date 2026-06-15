---
title: "Sistema de Tags"
tags:
  - syv/pj/docs
  - syv/tags
aliases:
  - Sistema de Tags
  - sistema-tags
---

# Sistema de Tags

> [!info] Propósito
> Este documento describe el sistema de tags de syv-pj: qué es un tag, cómo se escribe, cómo se estructura su entrada en el catálogo y cómo se extiende sin migración.
> En este documento se habla con frecuencia de [[contratos]]. Bien: las habilidades son, en esencia, tags.
> La relación entre los tags y Obsidian es absolutamente lineal e intencional.
---

## §1 — Mecánica universal del tag

Un **tag** es la unidad atómica del esquema. Es un identificador discreto que se aplica a un personaje y comunica una cosa concreta: una habilidad ganada, un estado de pánico, un fusil al hombro, una lealtad jurada, una cicatriz en la mejilla.

> [!tip] Regla rectora
> Todo lo que es discreto y no es identidad, atributo, prosa o auditoría **es un tag**. Sin excepciones: incluso los vínculos personales —aliados y némesis— son tags. Ver [[#§5 — Categorías relacionales: `aliado` y `nemesis`]] y [[nemesis-y-aliados|nemesis-y-aliados.md]].

Esta regla es expansiva por diseño. El sistema no predice los tipos de tag que existirán; provee una notación plana y declarativa para que cualquier hecho futuro encaje sin migración.

**Lo que NO es un tag:**

- `identidad` — slug opaco, nombre, sobrenombre, rol, género, edad.
- `atributos` — `cuerpo`, `mente`, `alma`. Magnitudes numéricas persistidas.
- `historia` — prosa biográfica.
- `historial` — eventos temporales estructurados (de solo añadir).
- `metadatos` — marcas de tiempo de auditoría.
- `extras` — diccionario libre para clientes externos.

**Lo que SÍ es un tag:**

- `habilidad.*`
- `aspecto.*`
- `entrenamiento.*`
- y muchos otros más
  
---

## §2 — Notación punto

Un tag se escribe como cadena única: `<categoria>.<slug>`.

También es perfectamente válido `<slug>`

En raras excepciones, se recurre al tercer segmento `<categoria>.<parent>.<slug>`.

- El **primer segmento** es la categoría (eje semántico mayor):
	- `habilidad.*`
	- `aspecto.*`
	- `equipo.*`
	- ...
- Los **segmentos intermedios** son subcategorías anidadas, usualmente el segmento intermedio es el slug del tag padre.
- El **último segmento** es el slug específico.
	- `habilidad.nadar`
	- `arma.pistola_9mm`

**Reglas del slug de tag:** minúsculas, guiones bajos como único separador, sin acentos, sin espacios, sin caracteres especiales. Ejemplos: `pistola`, `precision`, `ejercito_rojo`, `lider_de_escuadra`.

> [!important] Asimetría de slugs
> El slug de tag es **legible por diseño**. El slug de personaje (`identidad.slug`) es la antítesis: patente opaca `^[A-Z0-9]{8}$` (ej. `K9F2H3M4`), inmutable y no semántica. No confundir.

**Prohibido multiconjunto:** `tags[]` no puede funcionar como un multiconjunto. Por ejemplo, tres `equipo.utilitario.cargador` **NO** significan tres cargadores físicos; el motor se queda con el último valor (que deberá estar en la referencia del tag, o será `vacío`).

**Huérfanos:** se invita a dejar tags huérfanos con conceptos que pueden llenarse luego, cuando el tag es suficientemente comunicativo, como "aspecto.cicatriz_perturbadora". Otro ejemplo más feliz de tags huérfanos: `habilidad.personal.pianista`, y no sabremos qué tan bueno es hasta que creemos la referencia del tag en la historia del personaje; es decir, un tag subjetivo.

**Resolución contra el catálogo:** el parser troza el tag por `.` y mapea segmentos a directorios. `arma.pistola_9mm` resuelve a `tags/arma/pistola_9mm.yaml`.

---

## §3 — Categorías de referencia

Las categorías curadas a la fecha. La tabla es **ilustrativa, no exhaustiva**: por el principio abierto/cerrado, el universo de tags es **abierto e infinito** — el sistema acepta categorías nuevas sin migración ni rupturas (ver [[#§7 — Extensibilidad]]). Son puntos de referencia, no menú restrictivo.

| Categoría | Significado |
|---|---|
| `faccion` | Pertenencia macro (bando). |
| `subfaccion` | Grupo militar o político subordinado a una facción. |
| `rango` | Designación operativa jerárquica de campo. |
| `mando` | Capacidad de mando (extra al rango) dentro de la facción. |
| `estado` | Disponibilidad operativa. Exactamente uno por personaje. |
| `salud` | Estado físico actual. Acumulable. |
| `moral` | Estado anímico actual. Acumulable. |
| `mental` | Estado de concentración actual. Acumulable. |
| `rasgo` | Rasgo físico observable y **sin efecto** (cicatriz, tatuaje, constitución). Si tiene peso mecánico es un `aspecto`, no un `rasgo` (ver [[contratos]]). |
| `aspecto` | Identidad mecánicamente activa. Ver [[contratos]]. |
| `habilidad` | Habilitador de tirada contra atributo dominante. Ver [[contratos]]. |
| `entrenamiento` | Adiestramiento o formación recibida (militar, sanitaria, técnica). |
| `efecto` | Bloque estructurado referenciable por otros tags. |
| `equipo` | Equipo cargado. Subcategorías: `arma`, `utilitario`, `vestidura`. |
| `rol` | Roles operativos. Subcategorías: `oficio`, `jerarquia`, `narrativo`, `combate`. |
| `lealtad` | Lealtad vigente. Apunta a cualquier entidad (facción, subfacción, grupo, religión, personaje…). Ver [[#§4 — Categoría relacional: `lealtad`]]. |
| `aliado` | Vínculo de alianza vigente. Apunta a personaje, facción, subfacción o grupo. Ver [[#§5 — Categorías relacionales: `aliado` y `nemesis`]]. |
| `nemesis` | Enemistad vigente. Mismo destino que `aliado`, sin restricción de bando. Ver [[#§5 — Categorías relacionales: `aliado` y `nemesis`]]. |

El motor acepta tags fuera del canon. La coherencia la sostiene la curaduría, no la integridad referencial.

---

## §4 — Categoría relacional: `lealtad`

`lealtad` codifica un vínculo de adhesión vigente, en forma **plana** `lealtad.{slug}`. El slug es una **referencia** al destino —facción, subfacción, grupo, religión o incluso otro personaje (por su patente)—, no un slug libre; sin segmento intermedio que anuncie el tipo. No tiene entradas propias en el catálogo: la resolución apunta al catálogo de la entidad referida.

Misma mecánica que `aliado` / `nemesis` (§5). Detalle en [[lealtad|lealtad.md]].

---

## §5 — Categorías relacionales: `aliado` y `nemesis`

Los vínculos personales **son tags relacionales**, de la misma familia que `lealtad` (§4). `aliado.*` codifica una alianza vigente; `nemesis.*`, una enemistad vigente. Su slug es una **referencia** al destino del vínculo:

```
aliado.{slug}     →  personaje (patente), facción, subfacción o grupo
nemesis.{slug}    →  ídem, sin restricción de bando
```

A diferencia de `lealtad` —que solo apunta a entidades de catálogo— estos pueden apuntar también a **otro personaje**, por su patente (`aliado.K9F2H3M4`). La referencia carga el identificador literal del destino: patente opaca para personajes, slug legible para entidades de catálogo (la asimetría de §2).

**La prosa del vínculo no vive en el tag.** El tag afirma la relación; la **cuenta** el hito que la formó (`formacion_lealtad` / `identificacion_nemesis`) en el [[historial|historial.md]]. Así el vínculo se cuenta y se filtra como cualquier tag, sin perder su textura narrativa.

> [!info] Detalle completo en su propio documento
> Esta sección fija solo el contrato del tag. El porqué del cambio, los tipos de destino, el ciclo de vida y la división tag/hito viven en [[nemesis-y-aliados|nemesis-y-aliados.md]].

---

## §6 — Campos del archivo de catálogo

Cada tag canónico o emergente tiene una entrada en el catálogo. Cuatro campos son siempre obligatorios; el resto es condicional u opcional y se declara solo si suma información real.

### 6.1. Campos obligatorios siempre

```yaml
slug:
  tipo: string
  regla: Último segmento del tag. Minúsculas + guion bajo, sin acentos.

nombre:
  tipo: string
  regla: Nombre legible, 1-3 palabras, sin slugificar.
  proposito: Lo que la vista muestra como tag.

categoria:
  tipo: string
  regla: Primer segmento del tag. Solo la raíz; `subcategoria` lleva el intermedio.

descripcion:
  tipo: string
  regla: 1-3 frases canónicas sobre el significado del tag.
```

### 6.2. Campos obligatorios condicionales

Obligatorios solo cuando la categoría lo demanda:

```yaml
subcategoria:
  obligatorio_si: categoria ∈ {equipo, rol}

peso:
  obligatorio_si: categoria = equipo
  tipo: int (0..50 kg)

efecto:
  obligatorio_si: >
    categoria = aspecto (salvo que declare trigger en su lugar)
    o categoria = efecto
  uso: >
    Lista de modificadores estructurados. Cada uno con `objetivo` (attr.* / stat.*),
    un valor (`mod` entero o `pct` porcentaje) y una `nota` opcional. Ver [[contratos]].

equipo_arma.tipo_accion:
  obligatorio_si: subcategoria = arma
  enum: [cerrojo, semiauto, automatico, cuerpo_a_cuerpo]

equipo_arma.alcance:
  obligatorio_si: subcategoria = arma
  enum: [corto, medio, largo]

subfaccion.faccion_padre:
  obligatorio_si: categoria = subfaccion
  tipo: tag faccion.*
```

### 6.3. Campos opcionales

Declaralos solo si aportan información real:

```yaml
origen:
  enum: [canon, emergente, custom]
  default: emergente

requires:
  uso: Precondiciones de coherencia documentada. Ver §6.4.

excluye:
  uso: Tags incompatibles con este. Simétrico al prefijo no: de requires.

tags_relacionados:
  uso: Tags que típicamente acompañan a este. Informativo, no normativo.

peso_narrativo:
  tipo: int (1..5)
  uso: Sugerencia al sorteador sobre frecuencia apropiada. No es probabilidad estricta.

metadatos:
  campos: [version_introducida, creado_en, ultima_actualizacion]
```

### 6.4. Sistema `requires`

El bloque `requires` declara cuándo un tag es coherente sobre un personaje. Tiene dos subbloques combinables:

```yaml
require_all:
  semantica: El personaje debe tener TODOS estos tags.

require_any:
  semantica: Basta con UNO de estos tags.
```

**Modificador NOT:** prefijá cualquier entrada con `"no:"` para invertir la condición. Es una cadena con prefijo literal — consultable con `startswith("no:")`, obvio a la lectura humana.

```yaml
requires:
  require_all:
    - rango.sargento
    - no:estado.baja
  require_any:
    - habilidad.liderazgo
    - mando.oficial_de_campo
```

> [!important] `requires` es documentación ejecutable, no validación dura
> La API acepta personajes con tags incoherentes. La coherencia es responsabilidad del generador y del curador. Cualquier validador opcional puede consultar `requires`; el contrato duro no lo impone.

**Los aspectos de origen narrativo no usan `requires`.** Son recompensas otorgadas al azar (lo que antes era *ventaja*); no tienen depósito por rango ni precondiciones. Ver [[contratos]].

---

## §7 — Extensibilidad

El catálogo es **andamiaje, no jaula**. Tres ejes de extensión sin permiso ni migración:

1. **Nuevos valores dentro de una categoría existente** — `habilidad.tiro_de_precision`, `rasgo.cicatriz_quemadura`. Entran con `origen: emergente` la primera vez.
2. **Nuevas subcategorías dentro de una familia** — `equipo.montura.caballo_criollo` agrega un nivel a `equipo.*`. El día que aparezca el primer caso real, no antes.
3. **Categorías nuevas enteras** — `oficio_civil.herrero`, `vicio.fuma`, `mascota.perro_pastor`. El analizador solo necesita el primer segmento para enrutar.

**Garantía:** un tag desconocido no rompe la hoja.

**Regla de espera:** no se anticipan plantillas para tipos de tag que aún no existen. El catálogo crece por curaduría ante necesidades reales, no por especulación.

---

## §8 — Efectos y disparadores en el catálogo

Los efectos mecánicos de un tag se declaran de dos maneras según su naturaleza:

**Efecto pasivo / permanente (inline):** mientras el personaje tenga el tag, el efecto está activo. Se declara en el campo `efecto` a nivel raíz, como lista de modificadores estructurados.

```yaml
efecto:
  - objetivo: stat.iniciativa
    mod: +2
  - objetivo: stat.moral
    mod: +1
```

**Efecto reactivo / disparado (trigger):** el efecto se aplica ante un evento en partida. Se declara en un bloque `trigger` con `trigger-action` apuntando a entradas del catálogo `efecto.*`.

```yaml
trigger:
  evento: chequeo_moral
  condicion: fallado
  probabilidad: "50%"
  trigger-action:
    - efecto.panico_momentaneo
```

> [!tip] Vocabulario canónico de efectos
> El campo `objetivo` de cada modificador apunta a una variable en notación punto:
> - Atributos base: `attr.cuerpo`, `attr.mente`, `attr.alma`
> - Estadísticas calculadas: `stat.iniciativa`, `stat.moral`, `stat.fatiga`, `stat.movimiento`, `stat.estress`, `stat.sanar`, `stat.percepcion`
>
> El valor va en `mod` (delta entero) o `pct` (porcentaje). Un campo opcional `condicion` (palabra clave) restringe cuándo cuenta el modificador; `nota` es opcional.
> Ver [[contratos]] para la forma completa y [[atributos]] para la mecánica de cada variable.
