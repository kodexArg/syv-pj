---
title: "Generación Procedural de Personajes"
tags:
  - syv/pj/generacion
  - syv/pj/procedural
aliases:
  - generacion-procedural
  - flujo-de-creacion
---

# Generación Procedural de Personajes

Flujo canónico para construir un personaje de *Subordinación y Valor*. El orden **no sigue la hoja terminada**: la afiliación operativa va primero porque determina qué es válido en cada fase siguiente. Todo está config-driven; ningún valor está hardcodeado en el generador.

Ver [[hoja-personaje]], [[sistema-tags]], [[atributos-y-stats]].

---

## Principios rectores

- **Determinismo de stats**: los atributos base (`fis`, `tac`, `men`) se leen de tablas de configuración por `(rol, rango)`. Cero azar en esa fase.
- **Azar portable**: toda probabilidad se expresa en porcentaje; todo modificador como delta entero o porcentaje. Nunca un número mágico embebido en código.
- **Reproducibilidad por seed**: `(seed, faccion, rol)` reproduce el mismo personaje efímero. El canonizado pierde esa propiedad tras el primer hito (la historia narrada ya es irrepetible).
- **Config-driven**: pesos de sorteo, tablas de atributos, restricciones cruzadas, pools de nombres — todo vive en archivos de configuración externos al generador. Cambiar una regla es editar config, no código.

---

## Orden de fases

```
Fase 1 — Afiliación    → rango, facción, subfacción, escuadra
Fase 2 — Identidad     → nombre, sobrenombre, edad, género
Fase 3 — Atributos     → fis, tac, men  (determinísticos por rango)
Fase 4 — Tags          → tags adicionales sorteados ponderados
Fase 5 — Prosa         → historia por LLM (congela al canonizar)
Fase 6 — Relaciones    → aliados y nemesis sembrados
```

Cada fase depende de la anterior. Las restricciones cruzadas (ej. rango → edad mínima) viajan como tabla de reglas consultada antes de sortear.

---

## Fase 1 — Afiliación

Tres campos en orden estricto: **rango → facción → subfacción**. Si no se provee, cada uno se sortea según su tabla de pesos. El sistema solicita el campo y sortea como fallback.

### 1.1. Rango

Cada personaje arranca con exactamente un tag `rango.*`. El sorteo ponderado refleja la escasez operativa real:

| Rango | Peso |
| :--- | ---: |
| `recluta` | 30% |
| `fusilero` | 20% |
| `militante` | 18% |
| `apuntador` | 10% |
| `artillero` | 10% |
| `segundo_al_mando` | 7% |
| `lider_de_escuadra` | 3% |
| `tirador_designado` | 2% |

`ciudadano` se asigna solo explícitamente (NPC civil); no entra al sorteo de combatientes.

### 1.2. Facción

Exactamente un tag `faccion.*`. Sorteo uniforme 50/50 por defecto; override por contexto de campaña.

- `confederados`
- `ejercito_rojo`

### 1.3. Subfacción

Exactamente un tag `subfaccion.*`. Se sortea entre las subfacciones **compatibles con la facción** de §1.2 (cada subfacción declara su `faccion_padre` en el catálogo).

### 1.4. Escuadra

Exactamente un tag `escuadra.*`. Si la escuadra nombrada no existe en el almacenamiento, se crea al vuelo: slug heredado del tag, facción heredada del personaje, tipo inicializado a `escuadra_de_infanteria`, historial con hito `reorganizacion`.

### 1.5. Restricciones que esta fase puede imponer

Esta fase puede acotar el rango de edad o el conjunto de géneros válidos en Fase 2. Ejemplos:

- `lider_de_escuadra` → `edad ≥ 25`
- `recluta` → `edad ≤ 22`

Las reglas concretas viven en la tabla de reglas del proyecto (scope separado). El generador la consulta antes de sortear cada campo de Fase 2 y recorta el pool o rango al subconjunto válido.

---

## Fase 2 — Identidad personal

Genera el bloque `personaje.identidad` respetando las restricciones de Fase 1.

### 2.1. Género

Sorteo ponderado:

| Resultado | Peso |
| :--- | ---: |
| `masculino` | 45% |
| `femenino` | 45% |
| `no_binario` | 5% |
| `desconocido` | 5% |

Si Fase 1 restringe el set, se re-sortea hasta caer dentro del set permitido (no se sesga la tabla base).

### 2.2. Edad

Rango por defecto: **12–70 años**, entero, uniforme. Si Fase 1 estrecha el rango, se re-sortea hasta caer dentro.

### 2.3. Nombre

Sorteo desde pools curados (`resources/nombres/`):

- `nombres_m.txt` — nombres masculinos, formato `Nombre|Apodo`
- `nombres_f.txt` — nombres femeninos, formato `Nombre|Apodo`
- `apellidos.txt` — apellidos (mix hispano + inmigración argentina)

Composición: `{nombre} {apellido}`. Selección uniforme dentro del pool del género. La estructura admite pools alternativos por facción (`nombres_m_<faccion>.txt`) sin tocar el generador.

### 2.4. Sobrenombre

Probabilidad de emitir sobrenombre: **50%** por personaje. El apodo está curado en el pool junto al nombre (`Francisco|Pancho`). Si no se emite, el campo queda `null`.

### 2.5. `slug` y `rol`

- `slug`: deferido al servidor al persistir (patente `^[A-Z0-9]{8}$`); en memoria volátil queda `null`.
- `rol`: arranca `"ciudadano"` (default narrativo); el rol operativo emerge como tag `rol.*` en Fase 4.

---

## Fase 3 — Atributos

**Cero aleatoriedad.** Lookup determinístico sobre el tag `rango.*` de Fase 1:

| Rango | `fis` | `tac` | `men` |
| :--- | :---: | :---: | :---: |
| `ciudadano` | 2 | 2 | 2 |
| `militante` | 2 | 2 | 3 |
| `recluta` | 3 | 2 | 3 |
| `fusilero` | 3 | 3 | 3 |
| `apuntador` | 3 | 4 | 4 |
| `artillero` | 4 | 4 | 3 |
| `tirador_designado` | 4 | 5 | 3 |
| `segundo_al_mando` | 3 | 4 | 5 |
| `lider_de_escuadra` | 3 | 5 | 6 |

Topes absolutos de la escala: `fis 7`, `tac 7`, `men 7`. Los valores de creación quedan por debajo; el tope solo se alcanza vía hito narrativo.

Esta tabla vive en config (no en código). Cambiar un valor de rango es editar la tabla; el generador la lee en tiempo de ejecución.

> [!info] Inmutabilidad práctica
> Un ascenso posterior cambia el tag `rango.*` pero no los atributos. El progreso real es el equipo, los perks y los vínculos ganados en campaña. Mutación solo vía hito `triple_cero` o `mejora_atributo`.

---

## Fase 4 — Tags adicionales

Con rango, facción, subfacción y escuadra ya fijados, el generador sortea **tags adicionales ponderados** desde el catálogo.

### 4.1. Procedimiento

1. El catálogo filtra los tags válidos para el rango y facción del personaje (respetando `requires` de cada entrada).
2. Cada tag elegible tiene un `peso` declarado en el catálogo (entero; ausente = 1).
3. Se sortea sin reemplazo hasta completar la cantidad de tags configurada para el rango (o hasta agotar elegibles sin conflicto).
4. Tags mutuamente excluyentes (`requires` con prefijo `no:`) se eliminan del pool antes de cada sorteo.

### 4.2. Tags de rol operativo

En esta fase se asigna el tag `rol.*` que corresponda al rango, si existe mapping directo (ej. `lider_de_escuadra` → `rol.jerarquia.lider`). Este tag no se sortea: es determinístico.

> [!tip] Extensibilidad
> Agregar una nueva categoría de tag no requiere cambios en el generador: basta incluir los nuevos slugs en el catálogo con sus pesos y restricciones. El generador los levanta automáticamente.

---

## Fase 5 — Prosa por LLM

El generador compone un prompt con los datos ya fijados (rango, facción, atributos, tags) y lo envía a un LLM para generar el campo `personaje.historia`.

- La prosa se trata como **borrador volátil** hasta la canonización.
- Al canonizar: `historia` se congela (se persiste tal cual, inmutable a partir de ese momento). No se regenera ante cambios de tags o atributos.
- La reproducibilidad por seed **no aplica a la prosa**: dos llamadas con el mismo seed pueden producir textos distintos por variabilidad del modelo. El seed controla las fases 1–4; la prosa es inherentemente no determinística.

> [!warning] Congelado canónico
> Una vez que `canonizado_en` está presente en los metadatos, `historia` no se toca. Cualquier evolución posterior va al `historial[]` como hito narrativo.

---

## Fase 6 — Relaciones sembradas

Siembra inicial de `aliados[]` y `nemesis[]`.

- En la generación procedural pura las colecciones arrancan **vacías** (listas vacías, no null).
- En el autofill de escuadra (cuando se generan varios personajes en lote), el generador puede sembrar vínculos de alianza entre miembros de la misma escuadra: un hito `formacion_vinculo` en el historial de cada uno y la entrada correspondiente en `aliados[]`.
- Los vínculos de nemesis se siembran solo si el contexto de campaña lo requiere explícitamente.

---

## Reproducibilidad por seed

```
(seed, faccion, rol) → personaje efímero determinístico
```

- Las fases 1–4 son reproducibles: dado el mismo `seed`, `faccion` y rol de entrada, la secuencia de sorteos ponderados produce idéntico resultado.
- El `seed` se guarda en `metadatos.extras.seed` durante la vida efímera.
- **Al canonizar**: el personaje gana identidad permanente (slug asignado, historia congelada, primer hito registrado). A partir del primer hito la reproducibilidad se pierde: el historial es append-only y la historia no se regenera.

> [!info] Propósito del seed
> El seed sirve para regenerar el mismo borrador (ej. previsualizar antes de canonizar, o revertir una edición no confirmada). No es un identificador permanente; no se expone en la API pública.

---

## Autofill de escuadra

Cuando una escuadra no alcanza el mínimo reglamentario, el sistema ofrece completarla automáticamente:

1. Lee el template de la escuadra para saber qué roles faltan.
2. Para cada rol faltante, ejecuta las fases 1–4 con `faccion` y `escuadra` fijados, `rango` determinado por el rol requerido, y un seed nuevo.
3. La prosa (Fase 5) puede omitirse en el autofill rápido; el campo `historia` queda vacío hasta que el usuario canonice cada personaje.
4. Los personajes generados se persisten como efímeros hasta canonización individual.

---

## Resumen del flujo

```
seed + (faccion, rol)
        │
        ▼
[Fase 1] rango → facción → subfacción → escuadra
        │  (tablas de pesos en config)
        ▼
[Fase 2] género → edad → nombre → sobrenombre
        │  (pools en resources/nombres/, restricciones de Fase 1)
        ▼
[Fase 3] fis, tac, men
        │  (tabla config rango → atributos, cero azar)
        ▼
[Fase 4] tags adicionales sorteados ponderados
        │  (catálogo filtrado por rango/facción)
        ▼
[Fase 5] historia — LLM con prompt compuesto de fases 1-4
        │  (volátil hasta canonización)
        ▼
[Fase 6] aliados[], nemesis[] sembrados
        │
        ▼
   personaje efímero
        │
   canonización
        │
        ▼
   personaje canónico (slug asignado, historia congelada, seed descartado)
```
