---
title: "Apariencia — los tres párrafos descriptivos"
tags:
  - syv/pj/docs
  - syv/pj/apariencia
aliases:
  - Apariencia
  - apariencia
  - descriptores visuales
  - tres párrafos
---

# Apariencia

> [!info] Propósito
> Define el bloque `apariencia` de la [hoja de personaje](hoja-personaje.md): **cómo luce** el personaje, en **tres párrafos de prosa descriptiva agnóstica** — `rostro`, `figura`, `presencia`. No es un prompt, no es una lista de átomos, no es sintaxis de generador: es prosa de dominio que cualquier proyección (ComfyUI, Flux, Midjourney, una ilustración a mano, un avatar Flutter) puede leer sin reinventarla.
> Documento hermano de [sistema-tags.md](sistema-tags.md) y [contratos.md](contratos.md).

> [!warning] Sucesión — esto reemplaza a la vieja lista `apariencia`
> Hasta la revisión de esquema, `apariencia` era una **lista de descriptores atómicos** (`- ojos azul intenso`, `- rubio dorado`, `- piel trigueña`). Esa forma **queda derogada**. Ahora `apariencia` es un objeto de **tres párrafos fijos**. Todo lo que antes se atomizaba en la lista ahora se escribe como prosa dentro del párrafo que corresponda. La migración de datos (lista → tres párrafos) se hace con script determinista + test, como todo refactor de esquema (ver [hoja-personaje > §9 — Regla de refactor de esquema](hoja-personaje.md#9--regla-de-refactor-de-esquema)).

---

## §1 — Qué es

`apariencia` es un objeto con **tres párrafos obligatorios**, uno por eje estético fijo:

```yaml
apariencia:
  rostro:    "..."   # zoom a la cara
  figura:    "..."   # cuerpo entero, porte, cómo lleva lo que viste
  presencia: "..."   # cómo ocupa el espacio, luz, impresión que deja
```

Los tres ejes **no se agregan ni se quitan**: son el contrato. Un párrafo puede ser más rico o más escueto (sparse sigue valiendo, §4), pero el conjunto de ejes es fijo.

> [!tip] Regla rectora — cómo se ve, no cuánto ni qué
> Cada párrafo responde a **"¿cómo se ve el personaje?"** en lenguaje de dominio. Nunca cuánto (eso lo dicen los atributos) ni qué lleva (eso lo dicen los tags). La prosa describe la **lectura visual** de esos datos, no los datos.

---

## §2 — Los tres ejes

### 2.1. `rostro` — zoom a la cara

La cara en primer plano. Facciones, mirada, piel, pelo y vello facial, gesto habitual, marcas visibles del rostro (una cicatriz que cruza la ceja, la línea de la mandíbula). Es el eje del retrato cerrado.

> `rostro`: *"Cara ancha y curtida por el viento del sur, pómulos altos de ascendencia mapuche. Los ojos, oscuros y quietos, miran sin apuro; una cicatriz vieja le parte la ceja izquierda. Lleva el pelo negro rapado al ras y la barba de tres días que nunca termina de crecer."*

**No** describe: el cuerpo, la ropa, la escena.

### 2.2. `figura` — el cuerpo y el porte

El cuerpo entero y cómo se sostiene. Contextura, estatura relativa, cómo se para, y —clave— **cómo lleva** lo que viste: con qué actitud, no qué prenda. "Lleva el uniforme como quien nunca se lo saca" describe el porte; *qué* uniforme es un tag.

> `figura`: *"Menuda pero nervuda, se para con el peso repartido como si esperara siempre el próximo movimiento. Lleva el equipo ajustado y sin una correa suelta, con la prolijidad seca de quien confía su vida a esos detalles."*

**No** describe: **qué** prenda o arma lleva (tags `equipo/*`), ni cifras de fuerza (atributo `cuerpo`).

### 2.3. `presencia` — cómo ocupa el espacio

La impresión que deja. La luz que parece traer o robar, el aire alrededor, cómo cambia una habitación cuando entra. Es el eje más atmosférico: no da datos físicos, da **efecto**.

> `presencia`: *"Entra sin levantar la voz y aun así todos giran. Hay algo de calma tensa a su alrededor, como el silencio antes de una orden. La luz parece caerle siempre de costado, dejándole media cara en sombra."*

**No** describe: datos físicos concretos (van en `rostro`/`figura`).

---

## §3 — Anti-redundancia: la regla que gobierna los párrafos

`apariencia` **complementa** el resto de la hoja; **no re-codifica** lo que ya tiene hogar. La proyección visual lee **todo el conjunto junto** (párrafos + tags + atributos), así que la prosa no debe repetir lo que un tag o un integer ya afirma.

| Clase de dato | Dónde vive | En los párrafos |
|---|---|---|
| Cuánta potencia bruta | atributo `cuerpo` | solo su **lectura visual** ("corpulento", "nervudo") en `figura` |
| Qué arma / prenda lleva | tag `equipo/*` | solo **cómo** la lleva (el porte), nunca cuál |
| Cicatriz, tatuaje con contrato | tag `rasgo/*` / `aspecto/*` | se puede *mencionar* su lectura visual, no su efecto mecánico |
| Porte/expresión con efecto de juego | tag `aspecto/*` | su lectura visual, no su regla |

> [!important] Integers dicen cuánto · tags dicen qué · párrafos dicen cómo se ve
> Esta es la frontera de tres caras. Si un párrafo contiene un número (`fuerza 6`) o el nombre de una prenda/arma (`pistola 9mm`, `uniforme rojo`), está invadiendo el territorio de otro bloque. Reescribilo como lectura visual o borralo: el dato ya está en su lugar y el prompt-builder lo lee de ahí.

---

## §4 — Sparse por diseño: lo no dicho queda librado al azar

Los párrafos **no obligan a describirlo todo**. Se fija solo lo que el canon quiere anclar; lo omitido queda **librado al azar** del render.

- Un personaje puede tener un `rostro` detallado y una `presencia` de una sola frase.
- `apariencia: null` (los tres ausentes) deja al personaje enteramente a criterio del render.

Esto es el **azar portable** del kit SyV aplicado al eje visual: la ausencia de detalle es una **libertad explícita**, no un dato faltante.

> [!note] Raza / etnia es ascendencia visible, no dato de juego
> Coherente con el mapa étnico del lore (apellidos mapuche —Painemal, Curiñanco, Antieco, Coñuecar—, Shipibo-Conibo, sincretismo afro-umbanda). Se escribe como rasgo visual dentro de `rostro` ("pómulos altos de ascendencia mapuche"), agnóstico al generador; no modifica ninguna mecánica.

---

## §5 — La frontera del agnosticismo

Lo que **nunca** entra en un párrafo de `apariencia`:

- **Directivas de render**: iluminación técnica, cámara, lente, encuadre, aspect ratio, "quality tags". Eso lo aporta el armador de prompt **fuera de la hoja**, uniforme a todos (niveles 1 y 3 del prompt — ver [hoja-personaje > §2.6 — La hoja tiene en mente el retrato (sin parametrizarlo)](hoja-personaje.md#26--la-hoja-tiene-en-mente-el-retrato-sin-parametrizarlo)).
- **Pose momentánea** de una imagen puntual. La expresión *habitual* sí (en `rostro`); "mirando a cámara sonriendo" no.
- **Sintaxis de generador**: `masterpiece`, `8k`, `photorealistic`, nombres de modelo, sampler o LoRA. Eso es Stable-Diffusion-ismo; rompe el agnosticismo.

✓ *"los ojos oscuros miran sin apuro"* · *"se para con el peso repartido"* · *"la luz le cae de costado"*
✗ `retrato 85mm, luz dramática` · `masterpiece, 8k` · `ComicT_style, strength 0.8`

---

## §6 — Forma, largo y mutabilidad

```yaml
campo:         apariencia
tipo:          { rostro: str, figura: str, presencia: str }
default:       null              # los tres ausentes ⇒ todo librado al render
largo:         40-80 palabras por párrafo (sugerido, no duro)
idioma:        castellano rioplatense, voz descriptiva
persistencia:  persistido
mutable:       sin hito          # bajo peso narrativo, como edad; un corte de pelo lo cambia
indice:        NO entra al índice invertido de tags (no es faceta de filtrado del motor)
```

> [!info] Por qué prosa y no lista de tags (`fisico/ojos/azul_intenso`)
> La notación de [tags](sistema-tags.md) exige átomos y alimenta el índice invertido para que el **motor filtre** (facción, peso, fuerza). Nadie filtra una batalla por color de ojos: atomizar el eje visual solo pierde matiz sin ganar nada operativo. Y la lista de átomos, además, no captura el *cómo* —el porte, la impresión, la luz—: para eso hace falta prosa. `apariencia` es un **constraint suave para el render**, no una faceta de juego, y su forma natural es el párrafo.

> [!info] Por qué al final de la hoja
> Los tres párrafos son el **destilado visual** de todo lo anterior: no se pueden escribir bien sin conocer identidad, atributos y tags. Por eso cierran la hoja, justo antes de `metadatos` (ver [hoja-personaje > §0 — Estructura de la hoja](hoja-personaje.md#0--estructura-de-la-hoja)).
