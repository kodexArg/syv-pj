---
title: "Apariencia — la capa visual de la hoja"
tags:
  - syv/pj/docs
  - syv/pj/apariencia
aliases:
  - Apariencia
  - apariencia
  - descriptores visuales
---

# Apariencia

> [!info] Propósito
> Define el campo `apariencia` de la [[hoja-personaje|hoja de personaje]]: **cómo luce** el personaje, en una lista de descriptores visuales **agnósticos al generador de imágenes**. No es un prompt, no es prosa: es un contrato visual portable que cualquier proyección (ComfyUI, Flux, Midjourney, una ilustración a mano, un avatar Flutter) puede leer sin reinventarlo.
> Documento hermano de [[sistema-tags|sistema-tags.md]] y [[contratos|contratos.md]].

---

## §1 — Qué es

`apariencia` es una **lista de descriptores visuales libres**: frases cortas de dominio que fijan rasgos físicos del personaje.

```yaml
apariencia:
  - ojos azul intenso
  - rubio dorado
  - piel trigueña
  - mestizo
```

Se comporta como un conjunto de etiquetas —planas, discretas, enumerables— pero **admite fraseo natural** ("azul intenso", "rubio dorado") porque su consumidor es la **proyección visual**, no el índice de filtrado del motor.

> [!tip] Regla rectora — hecho visual, no directiva de render
> Cada descriptor responde a **"¿qué se ve del personaje, siempre?"**: un hecho visual intrínseco y permanente, en lenguaje de dominio. Lo que es momentáneo, lo que es instrucción para la cámara o lo que es jerga de un generador **no va acá**.

---

## §2 — Sparse por diseño: lo no dicho queda librado al azar

`apariencia` **no se completa entero**. Se declara **solo lo que el canon quiere fijar**; todo lo omitido queda **librado al azar** del generador.

- Un personaje puede fijar pelo y piel y dejar los ojos libres.
- Otro puede fijar solo la etnia.
- Otro puede fijar nada (campo ausente o `[]`) y quedar enteramente a criterio del render.

Esto es el **azar portable** del kit SyV aplicado al eje visual: la ausencia de un descriptor es una **libertad explícita**, no un dato faltante. No hay obligación de cubrir todas las clases.

---

## §3 — Qué clases cubre

El campo cubre el **residuo visual sin hogar** en el resto de la hoja:

| Clase | Ejemplos de descriptor |
|---|---|
| Ojos | `ojos azul intenso`, `ojos negros`, `mirada clara` |
| Cabello | `rubio dorado`, `pelo negro al ras`, `canoso`, `rapado` |
| Vello facial | `barba cerrada`, `bigote espeso`, `lampiño` |
| Piel | `piel trigueña`, `tez pálida`, `piel curtida` |
| Raza / etnia | `mestizo`, `mapuche`, `criollo`, `afrodescendiente`, `andino` |
| Rostro | `pómulos marcados`, `nariz quebrada`, `mandíbula ancha` |
| Contextura visible | `corpulento`, `enjuto`, `nervudo`, `menudo` |

> [!note] Raza / etnia es ascendencia visible, no dato de juego
> Coherente con el mapa étnico del lore (apellidos mapuche —Painemal, Curiñanco, Antieco, Coñuecar—, Shipibo-Conibo, sincretismo afro-umbanda). Es un rasgo visual de ascendencia, agnóstico al generador; no modifica ninguna mecánica.

---

## §4 — Regla anti-duplicación: qué NO va acá

`apariencia` **complementa** el resto de la hoja; **no re-codifica** lo que ya tiene hogar y que el armador de prompt ya puede leer:

| Si es… | Vive en… | No en `apariencia` |
|---|---|---|
| Cicatriz, tatuaje, marca de juego | `rasgo/*` (ej. `rasgo/cicatriz_perturbadora`) | no se repite |
| Prenda / vestidura | `equipo/vestidura/*` (ej. `uniforme_rojo`, `sotana`, `capucha`) | no se repite |
| Porte / expresión habitual | `aspecto/*` (ej. `aspecto/expresion_trance`) | no se repite |
| Corpulencia como capacidad | atributo `cuerpo` | solo su lectura visual (`corpulento`) |

> [!important] El prompt-builder lee el conjunto completo
> La proyección visual no consume solo `apariencia`: consume **apariencia + rasgo + vestidura + aspecto** juntos. Por eso la cicatriz no se duplica acá —ya está en `rasgo/*`— y el render igual la "ve".

---

## §5 — La frontera del agnosticismo

Lo que **nunca** entra en un descriptor de `apariencia`:

- **Directivas de render**: iluminación, cámara, lente, encuadre, pose, estilo artístico, resolución, aspect ratio, "quality tags". Eso es del **design system** + el skill que arma el prompt, aplicado **uniforme a todos** los personajes.
- **Estado momentáneo**: una pose o un gesto de una imagen puntual (la expresión *habitual* sí, pero como `aspecto/*`).
- **Sintaxis de generador**: `masterpiece`, `8k`, `photorealistic`, nombres de modelo o sampler. Eso es Stable-Diffusion-ismo; rompe el agnosticismo.

✓ `ojos azul intenso` · `piel curtida` · `mestizo`
✗ `retrato 85mm, luz dramática` · `masterpiece, 8k` · `mirando a cámara sonriendo`

---

## §6 — Forma, mutabilidad y el fork frase-vs-átomo

```yaml
campo:        apariencia
tipo:         list[str]          # frases cortas de dominio; default [] o ausente
persistencia: persistido
mutable:      sin hito           # bajo peso narrativo, como edad; un corte de pelo lo cambia
indice:       NO entra al índice invertido de tags (no es faceta de filtrado del motor)
```

> [!info] Por qué campo libre y no tags dotted (`fisico/ojos/azul_intenso`)
> La notación canónica de [[sistema-tags|tags]] exige átomos `lowercase_sin_acentos_sin_espacios` y alimenta el índice invertido para que el **motor filtre** (facción, peso, fuerza). Nadie filtra una batalla por color de ojos: atomizar "azul intenso" a `azul_intenso` solo pierde el matiz visual sin ganar nada operativo. `apariencia` es un **constraint suave para el render**, no una faceta de juego.
> **Fork abierto:** si en el futuro se quiere que estos descriptores sean filtrables/canónicos, se atomizan como tags `fisico/<slug>` dentro de `tags[]` —perdiendo el fraseo natural—. Por ahora se prefiere la frase libre por agnosticismo y naturalidad para el generador.
