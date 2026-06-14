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
> Este documento describe el sistema de etiquetas de syv-pj: qué es una etiqueta, cómo se escribe, cómo se estructura su entrada en el catálogo y cómo se extiende sin migración.
> En este documento se habla con frecuencia de [[habilidades]]. Bien: las habilidades son, en esencia, etiquetas.
> La relación entre las etiquetas y Obsidian es absolutamente lineal e intencional.
---

## §1 — Mecánica universal de la etiqueta

Una **etiqueta** es la unidad atómica del esquema. Es un identificador discreto que se aplica a un personaje y comunica una cosa concreta: una habilidad ganada, un estado de pánico, un fusil al hombro, una lealtad jurada, una cicatriz en la mejilla.

> [!tip] Regla rectora
> Todo lo que es discreto y no es identidad, atributo, prosa, auditoría o vínculo-personal-con-prosa **es etiqueta**.

Esta regla es expansiva por diseño. El sistema no predice los tipos de etiqueta que existirán; provee una notación plana y declarativa para que cualquier hecho futuro encaje sin migración.

**Lo que NO es etiqueta:**

- `identidad` — slug opaco, nombre, sobrenombre, rol, género, edad.
- `atributos` — `fis`, `tac`, `men`. Magnitudes numéricas persistidas.
- `historia` — prosa biográfica.
- `historial` — eventos temporales estructurados (append-only).
- `aliados` / `nemesis` — vínculos personales con prosa. Ver [[#§5 — Por qué aliados y némesis no son etiquetas]].
- `metadatos` — marcas de tiempo de auditoría.
- `extras` — diccionario libre para clientes externos.

**Lo que SÍ es etiqueta:**

- `habilidad.*`
- `aspecto.*`
- `entrenamiento.*`
- y muchos otros más
  
---

## §2 — Notación punto

Una etiqueta se escribe como string único: `<categoria>.<slug>`.

También es perfectamente válido `<slug>`

En raras excepciones, se recurre al tercer segmento `<categoria>.<parent>.<slug>`.

- El **primer segmento** es la categoría (eje semántico mayor):
	- `habilidad.*`
	- `aspecto.*`
	- `equipo.*`
	- ...
- Los **segmentos intermedios** son subcategorías anidadas, usualmente el segmento intermedio es el slug de la etiqueta padre.
- El **último segmento** es el slug específico.
	- `habilidad.nadar`
	- `arma.pistola_9mm`

**Reglas del slug de etiqueta:** minúsculas, guiones bajos como único separador, sin acentos, sin espacios, sin caracteres especiales. Ejemplos: `pistola`, `precision`, `ejercito_rojo`, `lider_de_escuadra`.

> [!important] Asimetría de slugs
> El slug de etiqueta es **legible por diseño**. El slug de personaje (`identidad.slug`) es la antítesis: patente opaca `^[A-Z0-9]{8}$` (ej. `K9F2H3M4`), inmutable y no semántica. No confundir.

**Prohibido multiconjunto:** `tags[]` no puede funcionar como un multiconjunto. Por ejemplo, tres `equipo.utilitario.cargador` **NO** significan tres cargadores físicos; el motor se queda con el último valor (que deberá estar en la referencia de la etiqueta, o será `vacío`).

**Huérfanos:** se invita a dejar etiquetas huérfanas con conceptos que pueden llenarse luego, cuando la etiqueta es suficientemente comunicativa, como "aspecto.cicatriz_perturbadora". Otro ejemplo más feliz de etiquetas huérfanas: `habilidad.personal.pianista`, y no sabremos qué tan bueno es hasta que creemos la referencia de la etiqueta en la historia del personaje; es decir, una etiqueta subjetiva.

**Resolución contra el catálogo:** el parser troza la etiqueta por `.` y mapea segmentos a directorios. `arma.pistola_9mm` resuelve a `tags/arma/pistola_9mm.yaml`.

---

## §3 — Categorías de referencia

Las categorías curadas a la fecha. La tabla es **ilustrativa, no exhaustiva**: por el principio [[open-close|open/close]], el universo de etiquetas es **abierto e infinito** — el sistema acepta categorías nuevas sin migración ni rupturas (ver [[#§7 — Extensibilidad]]). Son puntos de referencia, no menú restrictivo.

| Categoría | Significado |
|---|---|
| `faccion` | Pertenencia macro (bando). |
| `subfaccion` | Grupo militar o político subordinado a una facción. |
| `rango` | Designación operativa jerárquica de campo. |
| `grupo` | Asignación a un grupo o escuadra concreta. |
| `mando` | Capacidad de mando (extra al rango) dentro de la facción. |
| `estado` | Disponibilidad operativa. Exactamente uno por personaje. |
| `salud` | Estado físico actual. Acumulable. |
| `moral` | Estado anímico actual. Acumulable. |
| `mental` | Estado de concentración actual. Acumulable. |
| `rasgo` | Rasgo físico observable (cicatriz, tatuaje, constitución). |
| `aspecto` | Identidad mecánicamente activa. Ver [[habilidades]]. |
| `habilidad` | Habilitador de tirada contra atributo dominante. Ver [[habilidades]]. |
| `entrenamiento` | Adiestramiento o formación recibida (militar, sanitaria, técnica). |
| `efecto` | Bloque estructurado referenciable por otras etiquetas. |
| `equipo` | Equipo cargado. Subcategorías: `arma`, `utilitario`, `vestidura`. |
| `rol` | Roles operativos. Subcategorías: `oficio`, `jerarquia`, `narrativo`, `combate`. |
| `lealtad` | Lealtad a facción, subfacción o escuadra. Ver [[#§4 — Categoría relacional lealtad]]. |

El motor acepta etiquetas fuera del canon. La coherencia la sostiene la curaduría, no la integridad referencial.

---

## §4 — Categoría relacional: `lealtad`

`lealtad` codifica vínculos dirigidos hacia una facción, subfacción o escuadra. Su slug no es libre — es una **referencia compuesta** con prefijo que indica el tipo de entidad apuntada:

```
lealtad.faccion.{slug}      →  apunta a una facción del catálogo
lealtad.subfaccion.{slug}   →  apunta a una subfacción del catálogo
lealtad.escuadra.{slug}     →  apunta a una escuadra del catálogo
```

El prefijo es parte literal del slug compuesto. Un analizador que ve `lealtad.faccion.confederados` sabe que es una referencia a la facción de slug `confederados`.

**La categoría `lealtad` no tiene entradas propias en el catálogo.** Su semántica está en el formato de la etiqueta; la resolución apunta a los catálogos de facción, subfacción o escuadra según corresponda.

Solo lealtades **declarables y vigentes**. Las latentes, aspiracionales o secretas se manejan por sistema aparte.

---

## §5 — Por qué aliados y némesis no son etiquetas

Los vínculos personales (relaciones con otros personajes específicos) **no se expresan como etiquetas**. Viven en colecciones persistidas de primera clase sobre la [[hoja-personaje]]:

- `personaje.aliados[]` — lista de `{ref, descripcion, desde?}`.
- `personaje.nemesis[]` — lista de `{ref, descripcion, desde?}`.

**Por qué no son etiquetas:** un vínculo personal lleva prosa — la historia de ese vínculo, su textura narrativa, el momento que lo fundó. Una etiqueta puede afirmar la existencia de una relación pero no contarla. Las colecciones `aliados[]`/`nemesis[]` cargan esa textura. Una etiqueta `aliado.srg1h4f9` no diría nada; `aliados[].ref: SRG1H4F9` con su `descripcion` sí lo dice todo.

Además, las lealtades a facción o escuadra **sí son etiquetas** (`lealtad.*`): son vínculos institucionales sin prosa propia. La línea divisoria es la prosa, no la dirección del vínculo.

---

## §6 — Campos del archivo de catálogo

Cada etiqueta canónica o emergente tiene una entrada en el catálogo. Cuatro campos son siempre obligatorios; el resto es condicional u opcional y se declara solo si suma información real.

### 6.1. Campos obligatorios siempre

```yaml
slug:
  tipo: string
  regla: Último segmento de la etiqueta. Minúsculas + guion bajo, sin acentos.

nombre:
  tipo: string
  regla: Etiqueta legible, 1-3 palabras, sin slugificar.
  proposito: Lo que la vista muestra como etiqueta.

categoria:
  tipo: string
  regla: Primer segmento de la etiqueta. Solo la raíz; `subcategoria` lleva el intermedio.

descripcion:
  tipo: string
  regla: 1-3 frases canónicas sobre el significado de la etiqueta.
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
    String o lista de strings. Modificadores sobre el vocabulario canónico
    (FISICO/TACTICO/MENTAL/INICIATIVA/MORAL/FATIGA/MOVIMIENTO/ESTRESS).

equipo_arma.tipo_accion:
  obligatorio_si: subcategoria = arma
  enum: [cerrojo, semiauto, automatico, cuerpo_a_cuerpo]

equipo_arma.alcance:
  obligatorio_si: subcategoria = arma
  enum: [corto, medio, largo]

subfaccion.faccion_padre:
  obligatorio_si: categoria = subfaccion
  tipo: etiqueta faccion.*
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
  uso: Etiquetas incompatibles con esta. Simétrico al prefijo no: de requires.

etiquetas_relacionadas:
  uso: Etiquetas que típicamente acompañan a esta. Informativo, no normativo.

peso_narrativo:
  tipo: int (1..5)
  uso: Sugerencia al sorteador sobre frecuencia apropiada. No es probabilidad estricta.

metadatos:
  campos: [version_introducida, creado_en, ultima_actualizacion]
```

### 6.4. Sistema `requires`

El bloque `requires` declara cuándo una etiqueta es coherente sobre un personaje. Tiene dos subbloques combinables:

```yaml
require_all:
  semantica: El personaje debe tener TODAS estas etiquetas.

require_any:
  semantica: Basta con UNA de estas etiquetas.
```

**Modificador NOT:** prefijá cualquier entrada con `"no:"` para invertir la condición. Es un string con prefijo literal — consultable con `startswith("no:")`, obvio a la lectura humana.

```yaml
requires:
  require_all:
    - rango.sargento
    - no:estado.baja
  require_any:
    - habilidad.liderazgo_de_escuadra
    - mando.oficial_de_campo
```

> [!important] `requires` es documentación ejecutable, no validación dura
> La API acepta personajes con etiquetas incoherentes. La coherencia es responsabilidad del generador y del curador. Cualquier validador opcional puede consultar `requires`; el contrato duro no lo impone.

**Los aspectos de origen narrativo no usan `requires`.** Son recompensas otorgadas al azar (lo que antes era *ventaja*); no tienen pool por rango ni precondiciones. Ver [[habilidades]].

---

## §7 — Extensibilidad

El catálogo es **andamiaje, no jaula**. Tres ejes de extensión sin permiso ni migración:

1. **Nuevos valores dentro de una categoría existente** — `habilidad.tiro_de_precision`, `rasgo.cicatriz_quemadura`. Entran con `origen: emergente` la primera vez.
2. **Nuevas subcategorías dentro de una familia** — `equipo.montura.caballo_criollo` agrega un nivel a `equipo.*`. El día que aparezca el primer caso real, no antes.
3. **Categorías nuevas enteras** — `oficio_civil.herrero`, `vicio.fuma`, `mascota.perro_pastor`. El analizador solo necesita el primer segmento para enrutar.

**Garantía:** una etiqueta desconocida no rompe la hoja.

**Regla de espera:** no se anticipan plantillas para tipos de etiqueta que aún no existen. El catálogo crece por curaduría ante necesidades reales, no por especulación.

---

## §8 — Efectos y disparadores en el catálogo

Los efectos mecánicos de una etiqueta se declaran de dos maneras según su naturaleza:

**Efecto pasivo / permanente (inline):** mientras el personaje tenga la etiqueta, el efecto está activo. Se declara en el campo `efecto` a nivel raíz.

```yaml
efecto:
  - "(+2) INICIATIVA"
  - "(+1) MORAL"
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
> Los modificadores solo pueden apuntar a:
> - Atributos base: `FISICO`, `TACTICO`, `MENTAL`
> - Estadísticas calculadas: `INICIATIVA`, `MORAL`, `FATIGA`, `MOVIMIENTO`, `ESTRESS`
>
> Ejemplos: `"(+1) MENTAL"`, `"(-1) FATIGA"`, `"-100% MOVIMIENTO"`, `"(+2) INICIATIVA"`.
> Ver [[atributos]] para la mecánica de cada variable.
