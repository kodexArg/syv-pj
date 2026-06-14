---
title: "Historial — el registro de hitos del personaje"
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

> [!info] Qué es este documento
> El contrato detallado de `personaje.historial[]`: el **registro de hitos** de un personaje canonizado. Es el documento hermano que expande [[hoja-personaje#§5 — Historial|hoja-personaje.md §5]]; el núcleo da el resumen, acá vive la letra chica de cómo se escribe un hito.
>
> **Documentos hermanos**:
> - [[hoja-personaje|hoja-personaje.md]] — el esquema núcleo que referencia este registro.
> - [[contratos|contratos.md]] — los tipos de hito de mutación de etiquetas (`agregar_tag` / `quitar_tag`) tocan contratos.
> - [[diegesis-y-obsidian|diegesis-y-obsidian.md]] — cómo `actores[]` y `encuentro` se vuelven wikilinks navegables.
> - [[MODEL|MODEL.md]] / [[API|API.md]] — tipado del hito y las operaciones que lo escriben y lo leen.

---

## §0 — Qué es el historial

`historial[]` es un **array de hitos**: la línea de tiempo del personaje **ya canonizado**. Cada entrada describe un evento temporal sobre la ficha. Es un **registro de eventos de solo añadir** — nunca se reescribe ni se borra.

- Un personaje recién creado arranca con `historial: []`.
- Un efímero (sin canonizar) **no tiene historial**: el registro se abre recién al canonizar, cuando la `historia` se congela (ver [[hoja-personaje#§4 — Historia|hoja-personaje.md §4]]).
- Doble naturaleza: es **dato de juego** (la ficha cambia vía hitos) y es **línea de tiempo navegable** del vault de Diégesis.

> [!note] El historial es la bitácora de la mutabilidad
> Casi todo cambio de peso narrativo sobre la ficha deja rastro acá. La pregunta que decide si algo es un hito es: ==¿esto es parte de la historia del personaje?== La matriz completa de qué muta vía hito vive en [[hoja-personaje#§8 — Matriz de mutabilidad|hoja-personaje.md §8]].

---

## §1 — El hito, campo por campo

```yaml
fecha:       ISO-8601        # cuándo ocurrió el evento
tipo:        string          # catálogo sugerido, abierto (ver §2)
actores:     [string]        # patentes de personajes involucrados; [] válido, normalmente varios
descripcion: string          # obligatorio — la prosa del evento
encuentro:   slug | null     # patente de batalla/encuentro externo, opcional
metadata:    object          # libre (a futuro puede portar adjuntos)
```

### 1.1. `fecha`

Marca temporal del evento en formato ISO-8601. Es la **fecha diegética del hecho**, no la de registro (esa vive en `metadatos.ultima_actualizacion` de la ficha). La línea de tiempo se ordena por este campo.

### 1.2. `tipo`

Clasifica el evento. El catálogo es **sugerido, no cerrado** (ver §2): un tipo personalizado es legítimo y no rompe la ficha. La mitigación es curaduría, no validación. Algunos tipos disparan efectos sobre la ficha vigente (ver [[API#post-personajeslugevento|API.md §POST /evento]]); los demás solo se registran.

### 1.3. `actores`

Lista de **patentes** (`^[A-Z0-9]{8}$`) de los personajes involucrados en el evento. El propio personaje dueño de la ficha es implícito —no hace falta listarse a sí mismo— y la lista enumera a los **demás** que participaron.

```yaml
actores:
  tipo:    list[string]     # cada elemento es la patente de otro personaje
  default: []
  forma:   "^[A-Z0-9]{8}$"  # misma patente opaca que identidad.slug
```

- `[]` es válido: un hito puede no involucrar a nadie más (un ascenso administrativo, una herida en solitario).
- Pero **en general un evento lleva varios actores enlazados**: un combate, una traición, una promoción ocurren entre personajes. Poblarlos teje el grafo de Diégesis sin prosa adicional.
- Sin integridad referencial: igual que `aliados[]`/`nemesis[]`, se aceptan patentes colgadas (ver [[MODEL#5. invariantes-globales|MODEL.md §5]]). Una refactorización narrativa no invalida el registro.

> [!tip] `actores[]` ≠ `aliados[]` / `nemesis[]`
> `actores[]` **lista quién estuvo** en un evento puntual: patentes sueltas, sin prosa, congeladas en ese hito. `aliados[]` / `nemesis[]` son **vínculos persistentes y vigentes** con prosa que cuenta cómo se formó la relación (ver [[hoja-personaje#§3.4 — Aliados y némesis|hoja-personaje.md §3.4]]).
> Se complementan: un hito `formacion_lealtad` puede registrar en `actores[]` al personaje con quien se forjó el vínculo, mientras la entrada correspondiente en `aliados[]` guarda la descripción duradera. El hito es el **cuándo**; la colección es el **vínculo vigente**.

### 1.4. `descripcion`

Prosa breve del evento. **Obligatorio.** Es lo que un hito tiene y una etiqueta no puede tener: la textura narrativa de qué pasó. Castellano rioplatense, voz narrativa, consistente con el resto de la ficha.

### 1.5. `encuentro`

Patente opaca (`^[A-Z0-9]{8}$`) de una **batalla o encuentro externo**, o `null` si el hito no nace de un encuentro. La patente se obtiene de [[API#61-get-metaencuentronuevo|`GET /meta/encuentro/nuevo`]]. `syv-pj` **no persiste el encuentro como entidad** — solo guarda la referencia; modelarlo es responsabilidad del motor de batalla que consume la API.

> [!note] Por qué `encuentro` y no `ref_batalla`
> El campo se llama `encuentro` en todo el modelo (núcleo, MODEL, grupos). El nombre evoca la entidad implícita de combate —el encuentro— y no presume que todo evento referenciado sea una "batalla" formal: una emboscada, una deserción o una negociación armada también son encuentros.

### 1.6. `metadata`

Objeto libre para datos estructurados que acompañan al hito. El motor no lo inspecciona. Convenciones útiles (no obligatorias):

- `{ atributo, delta, valor_anterior, valor_nuevo }` para `mejora_atributo` / `triple_cero`.
- `{ categoria, valor }` para `agregar_tag` / `quitar_tag`.

> [!warning] Adjuntos a futuro
> `metadata` es la válvula prevista para **adjuntos** (imágenes, documentos, recortes de bitácora) en versiones futuras. Por ahora es texto/estructura libre; el contrato deja la puerta abierta sin comprometer hoy una forma de adjunto.

---

## §2 — Catálogo de tipos (sugerido, abierto)

Tipos de referencia, agrupados por lo que tocan. **No es una enumeración cerrada**: el cliente puede usar tipos fuera de esta lista, y el servidor los acepta. Se expone también vía [[API#53-get-metatipos_hito|`GET /meta/tipos_hito`]].

| Familia | Tipos |
|---|---|
| Atributos | `triple_cero`, `mejora_atributo` |
| Etiquetas | `agregar_tag`, `quitar_tag` |
| Rol / rango / mando | `ascenso`, `cambio_rol`, `cambio_rango`, `cambio_mando` |
| Estado | `herida`, `recuperacion`, `cambio_estado`, `cambio_salud`, `cambio_mental` |
| Grupo / traslado | `asignacion_escuadra`, `asignacion_grupo`, `traslado` |
| Vínculos | `formacion_lealtad`, `identificacion_nemesis`, `ruptura_lealtad` |
| Combate / vida | `combate`, `condecoracion`, `licencia`, `desercion`, `muerte` |

> [!info] Curaduría, no validación
> Que el catálogo sea abierto no significa que sea libre de criterio: la coherencia se cuida por proceso editorial, no por constraint. Un tipo desconocido se persiste tal cual y no rompe la ficha.

---

## §3 — De solo añadir

No hay reverso de hito. Un error **no se borra**: se corrige con un **hito compensatorio nuevo**. La línea de tiempo es íntegra por construcción — refleja lo que se creyó en cada momento, incluidos los errores y sus enmiendas.

- `metadatos.ultima_actualizacion` de la ficha se actualiza con cada hito.
- Solo se escribe vía [[API#post-personajeslugevento|`POST /personaje/{slug}/evento`]]; el cuerpo de esa operación **es un hito** con la forma de §1.
- Se lee completo vía [[API#get-personajesluhistorial|`GET /personaje/{slug}/historial`]].

---

## §4 — Proyección en Diégesis

Cuando la ficha se mira como nodo del vault, los campos de referencia del hito se renderizan como **wikilinks** (ver [[diegesis-y-obsidian|diegesis-y-obsidian.md]]):

- cada patente de `actores[]` → `[[slug|Nombre Visible]]` al personaje involucrado;
- `encuentro` → enlace a la batalla/encuentro si el vault lo modela.

Así el `historial[]` deja de ser una bitácora aislada y se vuelve una línea de tiempo navegable: desde un hito se llega a los otros personajes que estuvieron ahí, y desde ellos de vuelta al evento. La persistencia guarda **patentes**; la vista de Diégesis las muestra como vínculos. No se duplica información.
