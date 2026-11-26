---
title: "Lealtad — adhesión como etiqueta"
tags:
  - syv/pj/esquema
  - syv/pj/vinculos
aliases:
  - Lealtad
  - lealtad
---

# Lealtad

> [!NOTE]
> **En una línea**
>
> Una lealtad es una **etiqueta relacional**: `lealtad.{slug}`. El slug apunta a lo que sea —una facción, una subfacción, un grupo, una religión, incluso otro personaje—. Misma mecánica que [aliados y némesis](nemesis-y-aliados.md); acá va solo lo que cambia.

`lealtad` es de la familia de etiquetas relacionales de [sistema-tags.md §4](sistema-tags.md). Todo lo que vale para `aliado/*` / `nemesis/*` vale acá (ver [nemesis-y-aliados.md](nemesis-y-aliados.md)): es un tag, se cuenta, se filtra y se enruta por su primer segmento.

```yaml
lealtad.{slug}
```

- `lealtad/ejercito_rojo` — a una facción.
- `lealtad/pelicanos` — a una subfacción.
- `lealtad/K9F2H3M4` — a un comandante, por su patente.

**Plano, sin segmento intermedio.** No existe `lealtad/faccion/*` ni `lealtad/subfaccion/*`: el destino no anuncia su tipo en el tag —el slug se resuelve contra el catálogo que corresponda—. Como en `aliado` y `nemesis`, el slug es una **referencia**, no un slug libre: patente para personajes, slug legible para entidades de catálogo (la asimetría de [sistema-tags.md §2](sistema-tags.md)). No tiene entradas propias en el catálogo.

> [!NOTE]
> **Qué la distingue de aliado/nemesis**
>
> La diferencia es **semántica, no estructural**: `lealtad` es adhesión vigente; `aliado`/`nemesis`, el signo de un vínculo personal. Solo se declaran lealtades **vigentes** —las latentes, aspiracionales o secretas se manejan aparte—. Su prosa, si la hay, vive en el hito que la formó (`formacion_lealtad` / `ruptura_lealtad`) del [historial.md](historial.md).
