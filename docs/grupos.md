---
title: Grupos — Sistema de grupos y escuadras
tags:
  - syv/pj/grupos
  - syv/pj/tactico
aliases:
  - grupos
  - Sistema de grupos
  - escuadras
---

# Grupos — Sistema de grupos y escuadras

> [!info] Alcance
> Este documento define el **grupo** como unidad táctica y organizativa en SyV: su identidad, membresía, roles internos, stats derivadas y historial. El grupo es agnóstico al tipo — una escuadra de infantería, una célula miliciana y una patrulla de exploración son variantes del mismo patrón.

---

## §1 — El grupo como entidad

Un **grupo** es un conjunto de [[hoja-personaje|personajes]] que comparten una identidad operativa, una cadena de mando interna y un historial colectivo. El grupo tiene existencia propia: puede sobrevivir la baja de cualquiera de sus integrantes, incluso la del líder.

La membresía de un personaje a un grupo se declara mediante el tag `grupo.<slug_del_grupo>` en su hoja. El grupo también lleva su propia entidad con la lista de miembros y el historial.

```yaml
grupo:
  identidad:  { slug, nombre, faccion, tipo }
  miembros:   [...]   # lista de refs con rol y metadata operativa
  historial:  [...]   # hitos del grupo, append-only
  extras:     object | null
```

---

## §2 — Identidad del grupo

| Campo | Tipo | Descripción |
|---|---|---|
| `slug` | `string` | PK del grupo. `lowercase_con_underscore`. Estable e inmutable. Ej.: `cazadores_de_ricardo`, `columna_mansilla`. Debe coincidir con el segmento final del tag `grupo.<slug>` en las hojas de sus miembros. |
| `nombre` | `string` | Nombre legible. Ej.: "Cazadores de Ricardo". |
| `faccion` | `string` | Slug de facción: `confederacion_argentina` o `ejercito_rojo`. |
| `tipo` | `string` | Tipo operativo. Enum abierto; el tipo de referencia para el MVP es `escuadra_de_infanteria`. |

> [!tip] Slug y tag en sintonía
> Si el slug del grupo es `columna_mansilla`, el tag que cada miembro lleva en su hoja es exactamente `grupo.columna_mansilla`. El slug no cambia nunca; renombrar el grupo solo cambia `nombre`.

---

## §3 — Membresía y roles internos

Cada entrada en `miembros[]` enlaza a un personaje por su patente opaca y declara su función dentro del grupo:

```yaml
miembros:
  - ref:       K9F2H3M4     # patente opaca del personaje [A-Z0-9]{8}
    pos:       int           # orden de despliegue (1 = líder, ascendente)
    rol_grupo: string        # rol dentro del grupo — ver §3.1
    puntos:    int           # costo en puntos de reclutamiento
    nombre:    string        # nombre compuesto/de guerra del personaje
    aspectos:  list[string]  # descriptores narrativos del miembro en este grupo
    activo:    bool          # false si KIA, capturado o transferido
```

### 3.1. Roles de grupo

Los roles dentro del grupo son independientes del rango del personaje. Un personaje con rango `fusilero` puede asumir el rol `lider_vigente` si los mandos superiores caen.

| `rol_grupo` | Descripción |
|---|---|
| `lider` | Mando formal del grupo. Posición `1`. |
| `segundo` | Segundo al mando; asume si el líder cae. |
| `especialista` | Función técnica específica (ametrallador, tirador, etc.). |
| `tropa` | Integrante de línea. |
| `apuntador` | Asistente de arma de apoyo. |
| `cargador` | Municionero de arma de apoyo. |

> [!note] Roles abiertos
> `rol_grupo` es un enum sugerido, no cerrado. Un grupo de reconocimiento puede tener `explorador`, `radiotelegrafista` o cualquier otro rol que tenga sentido para su tipo operativo.

### 3.2. Aspectos del miembro

`aspectos[]` es una lista mutable de frases cortas que califican al personaje dentro del marco del grupo. No afectan stats derivadas — son material narrativo y táctico para el árbitro.

Ejemplos: `"veterano del 12/15"`, `"mano firme bajo fuego"`, `"cojea por herida vieja"`.

---

## §4 — Stats derivadas del grupo

Estas estadísticas se calculan en caliente a partir de los miembros activos (`activo: true`). No se persisten.

### 4.1. Fuerza aportada total (`fza_total`)

Suma de la `fza_aportada` de cada miembro activo. La magnitud individual depende del `rol.combate` declarado en la hoja del personaje:

| `rol.combate` | `fza_aportada` |
|---|---|
| `heroe` | 3 |
| `lider` | 2 |
| cualquier otro | 1 |

### 4.2. Cohesión vigente (`cohesion_vigente`)

Promedio entero (redondeado hacia abajo) del atributo `MENTAL` de todos los miembros activos, con penalizaciones por cadena de mando rota:

- `(-2)` si el líder (`rol_grupo: lider`) está inactivo sin reemplazo.
- `(-1)` si el segundo (`rol_grupo: segundo`) asume el mando por caída del líder.

### 4.3. Moral de grupo (`moral_promedio`)

Promedio entero (redondeado hacia abajo) del atributo `MENTAL` de todos los miembros activos. Mide la cohesión psicológica media del grupo.

> [!note] Cohesión vs. Moral
> `cohesion_vigente` incorpora el factor de mando; `moral_promedio` es la psicología bruta del grupo. Un grupo con alto `moral_promedio` pero sin líder tendrá baja `cohesion_vigente`.

### 4.4. Fatiga de grupo (`fatiga_promedio`)

Promedio entero (redondeado hacia abajo) de `fatiga_max` (`fis + men`) de todos los miembros activos. Representa el desgaste físico-mental colectivo.

### 4.5. Movimiento táctico (`movimiento_tactico`)

`min(MOVIMIENTO)` entre todos los miembros activos. **El grupo marcha al ritmo de su integrante más lento.** Esta regla no tiene excepción — si un miembro está herido y su MOVIMIENTO cayó, el grupo entero se ralentiza hasta que ese miembro sea retirado o su estado cambie.

### 4.6. Puntos totales (`puntos_totales`)

Suma de `puntos` de todos los miembros del roster, incluidos inactivos. Mantiene la auditoría del costo inicial de la unidad.

### 4.7. Líder vigente (`lider_vigente`)

El personaje que ejerce la autoridad táctica efectiva, evaluado en este orden entre los miembros activos:

1. `rol_grupo: lider`
2. `rol_grupo: segundo`
3. Miembro activo de mayor edad

### 4.8. Estado del grupo (`estado_grupo`)

| Estado | Condición |
|---|---|
| `operativo` | Tiene líder o segundo activo y capacidad de combate suficiente. |
| `decapitado` | Líder y segundo inactivos. |
| `desmembrado` | `fza_total < 8` — baja operatividad, propenso a desintegración. |
| `retirado` | Unidad fuera de combate. |

---

## §5 — Historial del grupo

`historial[]` es append-only. Cada entrada registra un evento significativo para la unidad colectiva o para un integrante en el contexto del grupo.

```yaml
historial:
  - fecha:       string        # ISO-8601
    tipo:        string        # enum abierto — ver §5.1
    descripcion: string        # prosa descriptiva
    ref_miembro: string | null # patente del personaje si el hito es individual
    ref_batalla: string | null # patente de batalla si aplica
    metadata:    object        # libre
```

### 5.1. Tipos de hito sugeridos

| `tipo` | Descripción |
|---|---|
| `baja_miembro` | Un integrante pasa a estado inactivo (KIA, captura, traslado). |
| `ascenso_miembro` | Un integrante es promovido o asume mando. |
| `incorporacion_miembro` | Un nuevo integrante se suma al grupo. |
| `combate_finalizado` | Cierre de un encuentro operacional. |
| `reorganizacion` | Modificación en la composición o estructura de mando. |
| `hito_narrativo` | Evento significativo sin categoría operacional específica. |

---

## §6 — Validación de plantilla (tipo `escuadra_de_infanteria`)

Para el tipo de referencia del MVP, una escuadra de infantería debe cumplir:

1. Exactamente 1 miembro con `rol_grupo: lider` en posición `1`.
2. Mínimo 1 mando (`lider` o `segundo`) por cada 4 soldados de línea (`tropa`).
3. Exactamente 1 `especialista` con función de ametrallador, acompañado de 1 `apuntador` y 1 `cargador`.
4. Tamaño de roster: mínimo 5, máximo 21 integrantes. Óptimo: 11.

Si el grupo viola alguna condición, las derivadas exponen:

- `cumple_plantilla: false`
- `errores_validacion[]`: lista de infracciones detectadas.

> [!note] Tipos alternativos
> Otros tipos de grupo (`patrulla`, `celula_miliciana`, `columna_de_marcha`) tienen sus propias plantillas o ninguna. Un grupo sin plantilla definida siempre tiene `cumple_plantilla: true` por defecto.

---

## §7 — Relación entre hoja de personaje y grupo

El vínculo es bidireccional pero asimétrico:

- **En la hoja del personaje**: el tag `grupo.<slug>` declara la pertenencia. El tag `lealtad.<slug>` puede coexistir para vínculos más permanentes o afectivos que la membresía táctica.
- **En la entidad grupo**: `miembros[].ref` apunta a la patente del personaje.

La fuente de verdad de la **composición táctica** es la entidad grupo. La fuente de verdad del **estado del personaje** es la hoja del personaje. Ninguna replica a la otra — se consultan en conjunto cuando hace falta.

> [!warning] Estado volátil de combate
> Las variables temporales de un encuentro activo (iniciativa, posición en grilla, orden de turno) viven en la entidad grupo bajo `miembros[].iniciativa`, **no en la hoja del personaje**. La hoja queda reservada para el estado permanente que sobrevive al encuentro.
