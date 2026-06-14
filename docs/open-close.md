---
title: Open/Closed — Extensión sin migración
tags:
  - syv/pj/arquitectura
  - syv/pj/schema
aliases:
  - open-close
  - Principio Open/Closed
---

# Open/Closed — Extensión sin migración

> [!info] Norte de este documento
> El schema de `syv-pj` es **cerrado a la modificación, abierto a la extensión**. Esta página define qué significa eso en la práctica y qué patrones lo hacen posible sin migraciones, sin romper clientes existentes y sin anticipar lo que todavía no hace falta.

---

## §1 — El principio aplicado al personaje

La [[hoja-personaje|hoja de personaje]] tiene seis bloques estructurales fijos más dos colecciones persistidas y la lista plana de tags. Esos bloques **no cambian** — son el contrato cerrado.

Lo que crece sin tocar esos bloques es todo lo demás:

- nuevas categorías de tag y nuevos slugs dentro de categorías existentes
- nuevos tipos de hito en `historial[]`
- nuevos campos dentro del escape hatch `extras`
- nuevas stats derivadas calculadas en caliente (sin tocar lo persistido)
- nuevos atributos opcionales de catálogo (descripción extendida, campos de renderizado, etc.)

Un cliente que hoy consume `personaje.atributos.fis` no necesita saber nada de una categoría de tag `psi` que se agregue mañana. El bloque `atributos` no cambió; el cliente sigue funcionando.

---

## §2 — Los tres ejes de extensión libre

### 2.1. Nuevos slugs dentro de categorías existentes

La categoría `equipo.arma` existe. Mañana aparece `equipo.arma.carabina_del_norte`. No se toca ningún schema — solo se agrega una entrada al catálogo de tags. Los personajes que tengan ese tag nuevo son leídos correctamente por cualquier cliente que itere `tags[]` sin asumir un set fijo.

```yaml
# entrada nueva en el catálogo — ningún otro archivo cambia
slug: equipo.arma.carabina_del_norte
nombre: Carabina del Norte
categoria: equipo
subcategoria: arma
descripcion: Fusil de cerrojo de fabricación confederada, culata de madera...
```

### 2.2. Nuevas subcategorías dentro de categorías existentes

La categoría `rol` tiene `rol.combate`, `rol.oficio`, `rol.jerarquia`, `rol.narrativo`. Si el proyecto necesita `rol.logistica`, se agrega sin tocar nada. Los clientes que solo leen `rol.combate` no ven `rol.logistica` a menos que lo pidan.

### 2.3. Categorías enteras nuevas

Si el universo incorpora una nueva dimensión — por ejemplo `psi` para rasgos de sensibilidad a los Poseídos — se abre una categoría nueva. Ningún personaje existente la tiene. Ningún cliente existente la conoce. Nadie se rompe.

> [!tip] Regla de curación
> Un tag desconocido **no rompe la hoja**. El catálogo es referencia y documentación, no validación dura. El campo `requires` es documentación ejecutable — avisa de dependencias, no bloquea la escritura.

---

## §3 — Extensión del historial

`historial[]` usa un enum **abierto** en `tipo`. Los tipos sugeridos de referencia (`ascenso`, `baja`, `captura`, `hito_narrativo`, `agregar_tag`, `quitar_tag`, etc.) son punto de partida, no lista cerrada.

Un consumidor downstream que no reconoce un `tipo` lo trata como `no-op` sobre los campos que conoce. La hoja no se corrompe.

Para agregar un tipo nuevo:

1. Elegir un `tipo` en `snake_case_castellano` que no colisione con los existentes.
2. Documentarlo en [[hoja-personaje#§5 — Historial|hoja-personaje §5]] bajo "Tipos sugeridos".
3. Nada más — no hay registro central que bloquee.

---

## §4 — El escape hatch `extras`

El campo `extras: object | null` en la raíz de la hoja es el válvula de extensión sin contrato:

- Un consumidor puede escribir datos propios ahí sin afectar la lectura de otros.
- `extras` nunca forma parte de ninguna derivación canónica.
- Si un dato que nació en `extras` se vuelve universal, se eleva a bloque o a tag — esa es la única migración posible, y es decisión editorial, no forzada por el schema.

> [!warning] Límite de `extras`
> `extras` es un contrato privado entre el escritor y su consumidor. Si dos consumidores distintos escriben claves distintas en `extras`, no colisionan — pero tampoco se comunican. No usar `extras` para datos que deban ser leídos por el sistema de tags o derivaciones de grupo.

---

## §5 — Stats derivadas: crecen sin persistir

Las stats (`INICIATIVA`, `MORAL`, `FATIGA`, `MOVIMIENTO`, `ESTRESS`) se calculan en caliente desde los atributos base y los efectos de los tags activos. Agregar una stat nueva sigue el mismo patrón:

1. Definir la fórmula en [[atributos-y-stats|docs/atributos-y-stats.md]].
2. Referenciarla desde los tags que la modifican.
3. Ningún dato persistido cambia.

Los atributos base (`fis`, `tac`, `men`) son el único número persistido. Ese contrato sí es cerrado.

---

## §6 — Lo que no se anticipa

El principio open/closed incluye su lado minimalista: **no se abre espacio para lo que todavía no existe**. No hay campos `reservado_futuro`, no hay categorías vacías "por si acaso", no hay `extras` pre-llenados.

Cuando algo nuevo haga falta, se extiende en ese momento. El costo de extensión es bajo por diseño; el costo de anticipar mal es alto.

> [!note] Deuda cero de anticipación
> Si una extensión requiere tocar más de dos archivos (el catálogo + la documentación de referencia), es señal de que el schema cerrado está siendo violado — revisar si el dato nuevo debería ser un tag, un hito o un campo en `extras`.
