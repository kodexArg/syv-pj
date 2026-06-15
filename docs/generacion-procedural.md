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

Flujo canónico para construir un personaje de *Subordinación y Valor* desde la nada: una secuencia de fases ordenadas que parte sin ningún dato y termina con una hoja completa —situada, equipada, con vínculos y con una historia propia.

Ver [[hoja-personaje]].

---

## Cómo leer este flujo

El flujo es una **secuencia de fases en orden estricto**: cada una depende de lo que fijó la anterior y le pasa restricciones a la siguiente. Esa es la columna vertebral, y no cambia. Lo que sí cambia es **cuánto se llena**: no todo personaje pasa por todas las fases con la misma profundidad.

El orden no es arbitrario: la **prosa es siempre la última fase**, porque el modelo de lenguaje necesita todo lo demás ya resuelto para escribir una historia coherente. Y el **equipo es la última capa antes de la prosa**: lo que el personaje carga se decide cuando ya sabemos quién es, qué sabe y a quién es leal.

> [!info] El flujo es un esqueleto, no una jaula
> El esquema es **abierto** (ver [[sistema-tags|sistema-tags.md §7]]). Se pueden crear personajes con campos que **no figuran en este flujo**, por tres vías especiales:
>
> 1. **Campo provisto como entrada.** Cualquier campo que el flujo sortearía puede entregarse ya fijado. El generador lo respeta y no lo sortea — así se dirigen personajes concretos sin salirse del flujo.
> 2. **Catálogo abierto.** Un personaje puede portar etiquetas de categorías que este flujo ni nombra (`oficio_civil.herrero`, `vicio.fuma`, `credo.anatema`). Entran sin migración; el flujo no necesita conocerlas de antemano.
> 3. **`extras`.** Lo que no encaja en ningún bloque de la hoja viaja en la válvula de escape (ver [[hoja-personaje|hoja-personaje.md §7]]).
>
> Y a la inversa: un personaje puede **omitir fases enteras**. Un civil no pasa por rango ni por equipo militar; un personaje de Diégesis puede entrar directo a la prosa con todo lo demás provisto a mano.

---

## Principios rectores

- **Determinismo de estadísticas**: los atributos base (`cuerpo`, `mente`, `alma`) se leen de tablas de configuración por rango. Cero azar en esa fase.
- **Azar portable**: toda probabilidad se expresa en porcentaje; todo modificador como delta entero o porcentaje. Nunca un número mágico insertado en código.
- **Reproducibilidad por semilla**: la misma semilla reproduce el mismo personaje efímero. El canonizado pierde esa propiedad tras el primer hito (la historia narrada ya es irrepetible).
- **Basado en configuración**: pesos de sorteo, tablas de atributos, restricciones cruzadas, depósitos de nombres — todo vive en archivos de configuración externos al generador. Cambiar una regla es editar la configuración, no código.

---

## Orden de fases

```
Fase 1 — Afiliación   → facción, subfacción, rango, mando, rol operativo
Fase 2 — Identidad    → género, edad, nombre, sobrenombre
Fase 3 — Atributos    → cuerpo, mente, alma
Fase 4 — Formación    → entrenamiento, habilidades
Fase 5 — Aspectos     → aspecto.* (carácter mecánicamente activo)
Fase 6 — Vínculos     → lealtad.*, aliado.*, nemesis.*
Fase 7 — Equipo       → arma, utilitario, vestidura
Fase 8 — Prosa        → historia por LLM (congela al canonizar)
```

Cada fase depende de la anterior. Las restricciones cruzadas (p. ej. rango → edad mínima) viajan como tabla de reglas consultada antes de sortear.

> [!danger] De acá en adelante: el flujo de ejemplo de un combatiente
> Todo lo que sigue —Afiliación, Identidad, Atributos, Formación, Aspectos, Vínculos, Equipo— es **un recorrido de ejemplo: el de un combatiente**. Se elige un combatiente a propósito, porque es el caso que ejercita el flujo **completo** y los dos ejes del universo: la **subordinación** (facción, subfacción, rango, mando, lealtad — la cadena de obediencia) y el **valor** (atributos, equipo y aspectos en combate).
>
> Para un **no-combatiente** el esqueleto es el mismo, pero se llena distinto: un civil no tiene rango ni mando, puede no tener facción, y varias fases se omiten o se relajan. Donde abajo se lee "el combatiente", entendé "el ejemplo que recorre todas las fases"; no es una obligación del esquema.

---

## Fase 1 — Afiliación

La **afiliación** sitúa al personaje dentro de la estructura de subordinación del universo. En el ejemplo del combatiente se llena **completa**: pertenece a un bando, a una subfacción, tiene un rango, una capacidad de mando definida y un rol operativo derivado.

> [!info] Por qué acá facción y subfacción **no** son opcionales
> En el caso general la afiliación puede quedar vacía (ver el esqueleto de arriba). Pero hemos definido un **combatiente**: un combatiente pelea **por** algo y **dentro** de algo. Por eso, en este recorrido, facción y subfacción se fijan siempre — es lo que permite hacer el recorrido completo.

### 1.1. Facción

Exactamente un tag `faccion.*`. Las facciones disponibles no se fijan en este flujo: salen de la documentación de *Subordinación y Valor* (ver [[diegesis|diegesis.md]]). Cuando no se provee, se sortea **uniforme** entre las facciones que el contexto habilite.

Las facciones canónicas vigentes del universo:

- `confederados`
- `ejercito_rojo`

### 1.2. Subfacción

Al menos un tag `subfaccion.*`, y puede tener varios. Se sortean entre las subfacciones **compatibles con la facción** de §1.1 que la documentación defina (cada subfacción declara su `faccion_padre` en el catálogo). La subfacción afina de qué tropa específica viene el combatiente, y más adelante sesga su formación y su equipo.

### 1.3. Rango

El combatiente recibe un rango: exactamente un tag `rango.*`. El catálogo de rangos sale de la documentación del universo; algunos rangos de ejemplo:

- `recluta`
- `fusilero`
- `militante`
- `apuntador`
- `artillero`
- `segundo_al_mando`
- `lider_de_escuadra`
- `tirador_designado`

La frecuencia relativa de cada rango (la escasez operativa: muchos reclutas, pocos líderes) es una **decisión de balance que vive en configuración**, no en este documento. Acá se fija qué rangos existen, no con qué probabilidad salen. El rango alimenta los atributos (Fase 3) y el rol operativo (§1.5).

### 1.4. Mando — ¿puede liderar?

> [!tip] Decisión de diseño: el mando se decide en la Afiliación
> El **mando** —la capacidad de liderar— es un eje **separado del rango** (ver [[sistema-tags|sistema-tags.md §3]]: `mando` es "capacidad de mando, extra al rango"). Por eso se decide acá, en Fase 1: es parte de la estructura de subordinación, debe quedar fijado antes de Identidad (un líder puede exigir edad mínima) y de él se deriva el rol operativo.

El software produce un booleano explícito:

```yaml
puede_liderar: true | false
```

- `puede_liderar: true` → se agrega un tag `mando.*` acorde (el grado de mando que la documentación defina para ese rango).
- `puede_liderar: false` → ningún tag `mando.*`.

Algunos rangos **implican** mando (`lider_de_escuadra`, `segundo_al_mando` ⇒ `true` por defecto); en el resto el defecto es `false`, pero el contexto puede elevarlo. La regla rango → mando vive en configuración.

### 1.5. Rol operativo (determinístico)

Cerrada la cadena de subordinación, el rol operativo se deriva **sin azar**: mapeo directo desde rango (y mando). P. ej. `lider_de_escuadra` → `rol.jerarquia.lider`. No se sortea: es determinístico. (Este es el `rol.*` operativo de la hoja; no confundir con `identidad.rol`, que es narrativo — ver [[hoja-personaje|hoja-personaje.md §1.2]].)

La **lealtad de base** del combatiente a su facción se siembra más adelante, en la fase de Vínculos (§6) — el hogar único de todas las etiquetas relacionales.

### 1.6. Restricciones que esta fase impone a Fase 2

La afiliación elegida **puede** acotar el rango de edad o el conjunto de géneros válidos en Fase 2. Por ejemplo:

- `lider_de_escuadra` → `edad ≥ 25`
- `recluta` → `edad ≤ 22`

Esas reglas viven en la tabla de reglas del contexto (ámbito separado), no en el flujo. El generador la consulta antes de sortear cada campo de Fase 2 y recorta el depósito o el rango al subconjunto válido.

---

## Fase 2 — Identidad personal

Genera el bloque `personaje.identidad` respetando las restricciones de Fase 1.

### 2.1. Género

Sorteo ponderado (pesos de ejemplo, ajustables en configuración):

| Resultado | Peso |
| :--- | ---: |
| `masculino` | 45% |
| `femenino` | 45% |
| `no_binario` | 5% |
| `desconocido` | 5% |

Si Fase 1 restringe el conjunto, se re-sortea hasta caer dentro del conjunto permitido (no se sesga la tabla base).

### 2.2. Edad

Rango por defecto: **12–70 años**, entero, uniforme. Si Fase 1 estrecha el rango, se re-sortea hasta caer dentro del intervalo permitido.

### 2.3. Nombre

Sorteo desde depósitos curados (`resources/nombres/`):

- `nombres_m.txt` — nombres masculinos, formato `Nombre|Apodo`
- `nombres_f.txt` — nombres femeninos, formato `Nombre|Apodo`
- `apellidos.txt` — apellidos (mezcla hispana + inmigración argentina)

Composición: `{nombre} {apellido}`. Selección uniforme dentro del depósito del género. La estructura admite depósitos alternativos por facción (`nombres_m_<faccion>.txt`) sin tocar el generador.

### 2.4. Sobrenombre

Probabilidad de emitir sobrenombre: **50%** por personaje. El apodo está curado en el depósito junto al nombre (`Francisco|Pancho`). Si no se emite, el campo queda `null`.

### 2.5. `slug` y `rol`

- `slug`: diferido al servidor al persistir (patente `^[A-Z0-9]{8}$`); en memoria volátil queda `null`.
- `rol`: arranca `"ciudadano"` (defecto narrativo de identidad). El rol **operativo** ya se fijó como tag `rol.*` en la Afiliación (§1.5).

---

## Fase 3 — Atributos

**Cero aleatoriedad.** Lookup determinístico sobre el tag `rango.*` de Fase 1:

| Rango | `cuerpo` | `mente` | `alma` |
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

> [!note] `cuerpo` ← viejo `fis`, `mente` ← viejo `tac`, `alma` es nuevo
> El renombre es lineal en dos columnas: `cuerpo` toma los valores del viejo `fis` y `mente` los del viejo `tac`. El tercer atributo viejo —`men` (mental)— se **descarta**: no tiene columna heredera. `alma` (Aura, liderazgo, voluntad, temple) es un atributo **nuevo**, **reasignado por clase** según rúbrica —no heredado de `men`—: altísimo en alto clero, chamanismo y líderes de escuadra; alto en militantes y fanáticos; bajo (2–3) en el resto.

Topes absolutos de la escala: `cuerpo 7`, `mente 7`, `alma 7`. Los valores de creación quedan por debajo; el tope solo se alcanza vía hito narrativo. Si el personaje no tiene rango, los atributos caen a la línea base `ciudadano`.

Esta tabla vive en configuración (no en código). Cambiar un valor de rango es editar la tabla; el generador la lee en tiempo de ejecución.

> [!info] Inmutabilidad práctica
> Un ascenso posterior cambia el tag `rango.*` pero no los atributos. El progreso real es el equipo, los aspectos y los vínculos ganados en campaña. Mutación solo vía hito `triple_cero` o `mejora_atributo`.

---

## Fase 4 — Formación

Lo que el combatiente **sabe hacer**: el adiestramiento recibido (`entrenamiento.*`) y las habilidades que habilita (`habilidad.*`). Es la primera capa de etiquetas sorteadas; define la competencia antes de que la prosa y el equipo la luzcan.

> **Entrada:** rango, rol, subfacción (Fase 1). · **Salida:** etiquetas `entrenamiento.*` y `habilidad.*`.

### 4.1. Entrenamiento (`entrenamiento.*`)

Adiestramiento o formación recibida (militar, sanitaria, técnica). Parte es **determinista** —un rango trae una base de entrenamiento implícita— y parte se **sortea** ponderado por la subfacción (una subfacción de zapadores sesga hacia `entrenamiento.demolicion`; una sanitaria, hacia `entrenamiento.medico_de_campo`).

### 4.2. Habilidades (`habilidad.*`)

Una **habilidad** habilita una tirada contra su `atributo_dominante`; no modifica atributos (ver [[contratos|contratos.md §6]]). Se asignan coherentes con el rango, el rol y el entrenamiento:

- `tirador_designado` → `habilidad.tiro_de_precision`.
- formación sanitaria → `habilidad.primeros_auxilios`.

Algunas son determinísticas (el rol las implica), otras se sortean ponderado. Sus `requires` se anclan al rango, el rol y el entrenamiento —todo ya fijado—; el arma que las haga lucir se elige después, en Equipo (Fase 7), de forma coherente con ellas.

---

## Fase 5 — Aspectos

Quién **es** el combatiente bajo presión: su carácter mecánicamente activo. Un **aspecto** declara un paquete de efectos que el motor aplica mientras el personaje lo lleve (ver [[contratos|contratos.md §5]]). Es la fase que le da textura: el veterano que no se quiebra, el cobarde, el terco, el de cólera ciega.

> **Entrada:** afiliación, atributos, formación, edad. · **Salida:** etiquetas `aspecto.*` y `rasgo.*`.

### 5.1. Sorteo de aspectos (`aspecto.*`)

1. Cuota típica: **0–3** aspectos, según configuración por rango.
2. Cada aspecto elegible se pondera por su `peso_narrativo` (1..5) — sugerencia de frecuencia, no probabilidad estricta (ver [[sistema-tags|sistema-tags.md §6.3]]).
3. Se respetan `requires` y `excluye`: por eso esta fase va **después** de Formación — sus precondiciones (habilidades, rango, entrenamiento) ya están en la hoja. Y se evita lo incoherente (no se sortea `cobarde` junto a `vanguardia`).
4. **Coherencia con la identidad**: la edad sesga el depósito. Un combatiente de 19 años no saca `aspecto.veterano_de_campo`; uno de 55, sí lo tiene a tiro.
5. **Sorpresa narrativa**: con baja probabilidad puede caer un aspecto de `origen: narrativo` (siempre positivo, sin `requires`) — el golpe de suerte, el `ojo_de_aguila` (ver [[contratos|contratos.md §5.4]]).

### 5.2. Rasgos físicos (`rasgo.*`)

Marcas observables —cicatrices, tatuajes, constitución— sorteadas con baja cuota. Admiten **huérfanos**: `rasgo.cicatriz_perturbadora` afirma la marca sin explicarla; su origen lo salda la prosa (Fase 8).

### 5.3. Lo que **no** se sortea al nacer

> [!warning] Estados de campaña, no de creación
> Estas categorías **no** entran a ningún sorteo de creación — son estados volátiles que se ganan en partida, no se nace con ellos:
> - `salud.*`, `moral.*`, `mental.*` — arrancan limpios (depósitos llenos, sin condiciones).
> - `estado.*` — se fija determinístico a `disponible`.

---

## Fase 6 — Vínculos

Los lazos del personaje: a quién es **leal**, quién es su **aliado**, quién su **némesis**. En *Subordinación y Valor* esto no es decoración: la subordinación —por quién pelea, a quién obedece, a quién traicionaría— es la mitad del nombre del universo. La prosa no puede contar a un combatiente sin saber sus vínculos, por eso esta fase va **antes** del equipo y de la historia.

Las tres son etiquetas **relacionales** de la misma familia: su slug referencia el destino del vínculo (ver [[sistema-tags|sistema-tags.md §4]], [[nemesis-y-aliados|nemesis-y-aliados.md]], [[lealtad|lealtad.md]]). Por eso viven juntas en una sola fase.

> **Entrada:** afiliación (Fase 1), identidad, aspectos. · **Salida:** etiquetas `lealtad.*`, `aliado.*`, `nemesis.*`.

### 6.1. Lealtades (`lealtad.*`)

- **Lealtad de base**: todo combatiente arranca leal a su bando — `lealtad.<faccion>`, determinística desde la facción de Fase 1. Es el piso de la subordinación.
- **Lealtades finas**: el contexto puede sembrar adhesiones más específicas — a un líder (`lealtad.<patente>`), a una subfacción o a un credo (`lealtad.<slug>`). Son opcionales, pero cuando existen pesan más que la lealtad de bando y abren conflicto narrativo (¿obedezco al credo o a la facción?).

### 6.2. Aliados y némesis (`aliado.*` / `nemesis.*`)

- En la generación procedural pura el personaje arranca **sin** `aliado.*` / `nemesis.*` — se ganan en campaña.
- Cuando se siembra un vínculo, se agrega su tag (`aliado.<patente>` / `nemesis.<slug>`) y se registra el hito que lo funda (`formacion_lealtad` / `identificacion_nemesis`), cuya `descripcion` carga la prosa del lazo (ver [[historial|historial.md]]).
- Un némesis del **propio bando** es legítimo (traición personal, vieja deuda): el vínculo no mira la facción, la mira la lealtad. Los vínculos de némesis se siembran solo si el contexto de campaña lo requiere explícitamente.

---

## Fase 7 — Equipo

La **última capa material** antes de la prosa: lo que el combatiente carga. Se decide al final —cuando ya sabemos su rango, su formación y sus vínculos— para que el kit sea coherente con todo lo anterior (al `tirador_designado` con `habilidad.tiro_de_precision` le toca un arma de alcance largo, no un fusil de recluta).

> **Entrada:** afiliación (Fase 1) y formación (Fase 4). · **Salida:** etiquetas `equipo.*`.

### 7.1. Ejes del equipo

El equipo se sortea **por eje**, con una cuota por eje definida en configuración — no como una bolsa indiferenciada. Así se garantiza un kit coherente (no tres armas y cero munición):

| Eje | Subcategoría | Cuota típica | Regla |
| :--- | :--- | :--- | :--- |
| Arma principal | `equipo.arma.*` | exactamente 1 | acorde al rango/rol/formación (alcance largo para el tirador; fusil básico para el recluta) |
| Utilitario | `equipo.utilitario.*` | 0–N | granadas, botiquín, radio, prismáticos… según rol y cuota |
| Vestidura | `equipo.vestidura.*` | 0–1 | uniforme o protección de la subfacción |

### 7.2. Procedimiento

1. Para cada eje, el catálogo filtra el equipo elegible para el rango, facción, subfacción y formación del personaje (respetando `requires`).
2. Cada entrada elegible tiene un `peso` de sorteo declarado (entero; ausente = 1).
3. Se sortea sin reemplazo hasta cubrir la cuota del eje, o hasta agotar elegibles sin conflicto.
4. Las armas declaran `tipo_accion` y `alcance` en el catálogo; el sorteo respeta lo que el rol y la habilidad exigen. El `peso` físico (kg) de cada ítem es informativo en creación.

> [!note] El equipo es progreso, no nacimiento fijo
> El equipo cargado al crear es el punto de partida; en campaña se gana, se pierde y se cambia. Por eso vive en `tags[]` como cualquier etiqueta, no en un bloque aparte.

---

## Fase 8 — Prosa por modelo de lenguaje

La **fase final**, y por eso la última: el modelo de lenguaje necesita **todo lo anterior** —afiliación, atributos, formación, aspectos, vínculos, equipo— para escribir una historia que cierre. Con todo fijado, el generador compone un aviso y genera el campo `personaje.historia`. La prosa es donde el personaje **se vuelve alguien**: no repite las etiquetas, las **explica y las ancla**.

> [!important] La prosa carga los datos personales — incluida la procedencia
> `historia` es un string estático, pero generado con un aviso muy específico. Todo el dato personal que no es etiqueta vive acá: de **dónde viene** el personaje (su lugar, su procedencia), por qué tiene la cicatriz, en qué guerra se hizo veterano, cómo aprendió a tirar, qué lo ata a sus lealtades. El aviso obliga a que la prosa **salde la referencia** de los tags subjetivos y huérfanos (ver [[sistema-tags|sistema-tags.md §2]]): el lugar y el pasado quedan en la historia, no en un campo aparte.

- El aviso se compone con todos los datos ya fijados en las fases 1–7.
- La prosa se trata como **borrador volátil** hasta la canonización.
- Al canonizar: `historia` se congela (se persiste tal cual, inmutable desde ese momento). No se regenera ante cambios de etiquetas o atributos.
- La reproducibilidad por semilla **no aplica a la prosa**: dos llamadas con la misma semilla pueden producir textos distintos por variabilidad del modelo. La semilla controla las fases 1–7; la prosa es inherentemente no determinística.

> [!warning] Congelado canónico
> Una vez que `canonizado_en` está presente en los metadatos, `historia` no se toca. Cualquier evolución posterior va al `historial[]` como hito narrativo.

---

## Reproducibilidad por semilla

```
semilla → personaje efímero determinístico
```

- Las fases **1–7** son reproducibles: dada la misma `semilla` (y los campos provistos como entrada), la secuencia de sorteos ponderados produce idéntico resultado.
- La `semilla` se guarda en `metadatos.extras.semilla` durante la vida efímera.
- La **Fase 8 (prosa)** queda fuera: es no determinística por naturaleza del modelo.
- **Al canonizar**: el personaje gana identidad permanente (slug asignado, historia congelada, primer hito registrado). A partir del primer hito la reproducibilidad se pierde: el historial es de solo añadir y la historia no se regenera.

> [!info] Propósito de la semilla
> La semilla sirve para regenerar el mismo borrador (p. ej. previsualizar antes de canonizar, o revertir una edición no confirmada). No es un identificador permanente; no se expone en la API pública.

---

## Resumen del flujo

```
semilla  (+ campos provistos como entrada)
        │
        ▼
[Fase 1] Afiliación   facción → subfacción → rango → mando → rol operativo
        │  (catálogo de la documentación SyV; subordinación)
        ▼
[Fase 2] Identidad    género → edad → nombre → sobrenombre
        │  (depósitos en resources/nombres/, restricciones de Fase 1)
        ▼
[Fase 3] Atributos    cuerpo, mente, alma
        │  (tabla rango → atributos, cero azar)
        ▼
[Fase 4] Formación    entrenamiento → habilidades
        │  (determinista + ponderado por subfacción)
        ▼
[Fase 5] Aspectos     aspecto.* (+ rasgo.*)   ·   estados de campaña NO se sortean
        │  (ponderado por peso_narrativo, sesgado por edad)
        ▼
[Fase 6] Vínculos     lealtad.* (base + finas) → aliado.* → nemesis.*
        │  (etiquetas relacionales; la subordinación del universo)
        ▼
[Fase 7] Equipo       arma → utilitario → vestidura
        │  (última capa material; sorteo por eje, coherente con formación)
        ▼
[Fase 8] Prosa        historia — el LLM ancla lugar, pasado, vínculos y referencias
        │  (usa las fases 1–7; volátil hasta canonización, no determinística)
        ▼
   personaje efímero
        │
   canonización
        │
        ▼
   personaje canónico (slug asignado, historia congelada, semilla descartada)
```
