---
title: "Némesis y Aliados — vínculos como etiquetas"
tags:
  - syv/pj/esquema
  - syv/pj/vinculos
aliases:
  - Némesis y Aliados
  - nemesis-y-aliados
  - aliado
  - nemesis
  - némesis
---

# Némesis y Aliados

> [!info] Qué es este documento
> Los vínculos de un personaje —sus **aliados** y sus **némesis**— son **etiquetas**. Nada más. Este documento existe para decir exactamente eso y nada que [[sistema-tags|sistema-tags.md]] no diga ya: un aliado es un tag `aliado.*`, un némesis es un tag `nemesis.*`, y se comportan como cualquier otra etiqueta relacional. La prosa del vínculo —cómo se formó, qué lo sostiene— vive en su **hito** de [[historial|historial.md]], no acá.

---

## §1 — Son etiquetas

Un aliado y un némesis se anotan como cualquier otra cosa discreta del personaje: una entrada en `tags[]`, en notación punto. Todo lo que dice [[sistema-tags|sistema-tags.md §1]] sobre un tag vale acá sin excepción.

```yaml
aliado.<slug>
nemesis.<slug>
```

- `aliado.K9F2H3M4` — aliado: apunta a otro personaje por su patente.
- `nemesis.ejercito_rojo` — némesis: apunta a una facción por su slug de catálogo.

Son etiquetas **relacionales**, de la misma familia que [[lealtad|lealtad.md]]: su slug no es libre, es una **referencia** al destino del vínculo (ver [[sistema-tags|sistema-tags.md §4]]). El motor las enruta por el primer segmento —`aliado` / `nemesis`— igual que enruta cualquier tag.

---

## §2 — A qué apuntan

El último segmento es la referencia. A diferencia de `lealtad.*` —que solo apunta a entidades de catálogo— un aliado o un némesis puede apuntar también a **otro personaje**:

| El slug es… | Referencia | Ejemplo |
|---|---|---|
| Un personaje | su patente `^[A-Z0-9]{8}$` | `aliado.K9F2H3M4` |
| Una facción | slug de catálogo | `nemesis.ejercito_rojo` |
| Una subfacción | slug de catálogo | `aliado.pelicanos` |
| Un grupo / escuadra | slug de catálogo | `nemesis.columna_mansilla` |

> [!important] El slug es una referencia, no un slug libre
> Cuando el vínculo apunta a un personaje, el slug es su **patente opaca** (mayúsculas, `^[A-Z0-9]{8}$`) — la misma asimetría que [[sistema-tags|sistema-tags.md §2]] documenta para los slugs relacionales: la referencia carga el identificador literal de su destino, no se "slugifica". Para entidades de catálogo (facción, subfacción, grupo) el slug es legible, como en cualquier tag. No hay integridad referencial: una patente colgada es legal, igual que en `actores[]` (ver [[historial|historial.md]]).

> [!note] Sin restricción de bando
> Un némesis del propio bando es legítimo (traición personal, vieja deuda). El vínculo no mira la facción; la mira el `lealtad.*`.

---

## §3 — Por qué etiquetas y no colecciones

Antes los vínculos vivían en colecciones aparte (`aliados[]`, `nemesis[]`) con su prosa adentro. Se deshizo esa decisión **desde la raíz**. La razón es simple y es la del principio rector del esquema: **todo lo discreto es etiqueta** (ver [[sistema-tags|sistema-tags.md §1]]). Un vínculo es discreto. No hay motivo para sacarlo del único lugar donde vive todo lo discreto.

Lo que se gana al volverlos etiquetas:

- **Agregados gratis.** "¿Cuántos aliados tiene?" es contar `aliado.*`. "¿Cuántos némesis?" es contar `nemesis.*`. Una colección aparte no se cuenta junto al resto; una etiqueta sí.
- **Filtrables.** `?tag=aliado.K9F2H3M4` devuelve a todos los que lo tienen por aliado. Un campo aparte no entra en el filtro de tags.
- **Una sola regla.** No hay un mecanismo especial para vínculos: se agregan y se quitan con `agregar_tag` / `quitar_tag` como cualquier etiqueta, o con sus hitos dedicados (§4).

KISS: un solo lugar para lo discreto, una sola notación, una sola forma de contar.

---

## §4 — Dónde vive la prosa

La objeción vieja era que un vínculo "lleva prosa" —la historia de cómo se formó— y una etiqueta no puede contarla. Cierto: la etiqueta no la cuenta. **El hito sí.**

La prosa del vínculo vive en el [[historial|historial.md]], en el hito que lo introdujo:

- `formacion_lealtad` → agrega un `aliado.*` y su `descripcion` cuenta cómo nació la alianza.
- `identificacion_nemesis` → agrega un `nemesis.*` y su `descripcion` cuenta el origen de la enemistad.
- `ruptura_lealtad` → quita el tag cuando el vínculo se rompe.

```yaml
historial:
  - fecha: 2024-05-01
    tipo: formacion_lealtad
    actores: [K9F2H3M4]
    descripcion: "Cabo Sosa lo saca a rastras de la Zanja bajo fuego. Desde entonces, confianza ciega."
    encuentro: NMC8H5P9
    metadata: { tag: aliado.K9F2H3M4 }
```

La división del trabajo es limpia: la **etiqueta** afirma el vínculo vigente (y se cuenta, se filtra, se agrega); el **hito** lo narra y lo fecha. El antiguo campo `desde` de la colección es, simplemente, la `fecha` del hito.

> [!tip] La hoja no define esto
> La [[hoja-personaje|hoja-personaje.md]] solo dice **dónde** se anotan (en `tags[]`) y **qué valor** esperan (un `aliado.*` / `nemesis.*` con su referencia). El contrato del tag está en [[sistema-tags|sistema-tags.md]]; la prosa, en [[historial|historial.md]]; la definición del vínculo, acá. DRY: cada cosa se explica una sola vez.

---

## §5 — Ciclo de vida

- Un personaje recién canonizado **no tiene** tags `aliado.*` ni `nemesis.*` — los vínculos se ganan en campaña.
- Se pueblan en caliente vía hito (`formacion_lealtad` / `identificacion_nemesis`) o por curaduría directa sobre `tags[]`.
- Se rompen quitando el tag (`ruptura_lealtad` u `quitar_tag`); como todo en el historial, la ruptura **se agrega**, no borra el hito que formó el vínculo. La línea de tiempo queda íntegra (ver [[historial|historial.md]]).

---

En Diégesis, los tags `aliado.*` / `nemesis.*` se proyectan como secciones **Aliados** y **Némesis** de la nota del personaje, con la prosa tomada del hito correspondiente (ver [[diegesis-y-obsidian|diegesis-y-obsidian.md]]).
