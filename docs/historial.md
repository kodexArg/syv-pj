---
title: "Historial — la hoja de ruta del personaje"
tags:
  - syv/pj/esquema
  - syv/pj/historial
aliases:
  - Historial
  - historial
  - registro de hitos
  - hito
---

# Historial

El `historial[]` es la **hoja de ruta** que acompaña al personaje: una lista de **hitos** en orden temporal donde queda asentado todo lo que le fue pasando. Cada vez que gana una etiqueta, una habilidad, un entrenamiento, un ascenso o una herida, eso es un hito. La ficha dice **quién es hoy**; el historial cuenta **cómo llegó hasta acá**.

Arranca vacío. Un personaje recién canonizado se entrega con `historial: []` — el momento inicial se da por sentado y no se registra; el historial solo guarda lo que viene después. (Un efímero, sin canonizar, ni siquiera tiene historial: se abre al canonizar, cuando la `historia` se congela.)

## Un historial de ejemplo

```yaml
historial:
  - fecha: 2024-03-12
    tipo: agregar_tag
    actores: []
    descripcion: "Aprueba el curso de tirador; suma la habilidad de francotirador."
    encuentro: null
    metadata: { categoria: habilidad, valor: francotirador }

  - fecha: 2024-05-01
    tipo: combate
    actores: [K9F2H3M4, SLG3D7K2]
    descripcion: "Defiende la Zanja de Alsina y cae herido cubriendo la retirada."
    encuentro: NMC8H5P9
    metadata: {}
```

Se lee de arriba hacia abajo como una línea de tiempo: primero el entrenamiento, después el combate.

## Los campos

| Campo | Tipo | Qué guarda |
|---|---|---|
| `fecha` | `ISO-8601` | Cuándo ocurrió (fecha diegética, no la de registro). Ordena la línea de tiempo. |
| `tipo` | `string` | Qué clase de evento. Catálogo sugerido y abierto (ver abajo). |
| `actores` | `[string]` | Patentes de los **otros** personajes involucrados; `[]` válido, normalmente varios. |
| `descripcion` | `string` | **Obligatorio.** La prosa del evento, en voz narrativa. |
| `encuentro` | `slug \| null` | Patente de la batalla/encuentro externo, si lo hubo (de `GET /meta/encuentro/nuevo`). |
| `metadata` | `object` | Libre. Datos estructurados del hito (ej. `{ atributo, delta }`). |

**Tipos sugeridos:** `agregar_tag`, `quitar_tag`, `mejora_atributo`, `triple_cero`, `ascenso`, `cambio_rol`, `herida`, `recuperacion`, `traslado`, `condecoracion`, `formacion_lealtad`, `identificacion_nemesis`, `combate`, `licencia`, `desercion`, `muerte`. La lista es **abierta**: un tipo nuevo se acepta y se persiste igual. Algunos mutan la ficha al registrarse (ver [[API|API.md]]); el resto solo deja constancia.

## Advertencias

> [!warning] De solo añadir
> El historial no se reescribe ni se borra. Un error no se arregla tocando el hito viejo, sino **agregando un hito nuevo** que lo enmienda. La línea de tiempo es íntegra por construcción.

- **`actores` no es lo mismo que los tags `aliado/*`/`nemesis/*`.** `actores` solo lista quién estuvo en *ese* evento; los aliados y némesis son **vínculos vigentes** del personaje, anotados como etiquetas (ver [[nemesis-y-aliados|nemesis-y-aliados.md]]). De hecho, la prosa de ese vínculo vive justamente en el hito que lo formó (`formacion_lealtad` / `identificacion_nemesis`): el tag afirma el lazo, el hito lo cuenta. `actores` tampoco impone integridad referencial: se aceptan patentes colgadas, como en aquellos (ver [[MODEL|MODEL.md §4]]).
- **`metadata` podría portar adjuntos a futuro** (imágenes, documentos). Hoy es estructura libre; el contrato deja la puerta abierta sin comprometer una forma todavía.
- **En Diégesis, `actores` y `encuentro` se muestran como wikilinks** `[[slug]]`, volviendo el historial una línea de tiempo navegable (ver [[diegesis|diegesis.md]]). La persistencia guarda patentes; la vista las enlaza.

---

Tipado formal del hito en [[MODEL|MODEL.md §1.1]]; resumen en el núcleo, [[hoja-personaje|hoja-personaje.md §5]].
