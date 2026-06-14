---
title: Diégesis y Obsidian — El personaje como nodo del vault
tags:
  - syv/pj/diegesis
  - syv/pj/obsidian
aliases:
  - diegesis-y-obsidian
  - Convención de linkeo
  - personaje-como-nodo
---

# Diégesis y Obsidian — El personaje como nodo del vault

> [!info] El eje central
> Una hoja de personaje de SyV tiene doble naturaleza: es **dato de juego** (campos numéricos, etiquetas, historial) y es **nodo navegable del vault de Diégesis** (wikilinks a facciones, grupos, ubicaciones, otros personajes). Este documento define la convención de vinculación que hace posible esa doble naturaleza sin duplicar información.

---

## §1 — Por qué el personaje es un nodo

El vault de Diégesis es el SSOT del universo SyV: facciones, geografía, eventos históricos, personajes notables, líneas de tiempo. Una hoja de personaje que solo existe como dato de juego es una isla — se puede consultar, pero no navegar.

La convención de vinculación convierte cada hoja en un nodo conectado: desde el personaje se llega a la facción, al grupo, a la ubicación, a otros personajes; y desde esos nodos se llega de vuelta al personaje. El vault se convierte en un grafo navegable.

---

## §2 — Estructura de vinculación en la hoja de personaje

La hoja de personaje en Obsidian es un archivo `.md` con frontmatter YAML y cuerpo de prosa. Los wikilinks viven en dos lugares: en el frontmatter (como propiedades tipadas) y en el cuerpo (como vínculos en prosa o en listas).

### 2.1. Frontmatter con propiedades de vínculo

```yaml
---
title: "Sargento Walter Aguirre"
tags:
  - syv/personaje/canonizado
  - syv/faccion/confederacion_argentina
  - syv/rango/lider_de_escuadra
aliases:
  - Aguirre
  - Walter Aguirre
faccion: "[[Confederación Argentina]]"
grupo: "[[cazadores_de_ricardo|Cazadores de Ricardo]]"
ubicacion_actual: "[[Zanja de Alsina]]"
---
```

Las propiedades `faccion`, `grupo` y `ubicacion_actual` son wikilinks tipados — Obsidian las reconoce como referencias y las incluye en el grafo. Si la nota de la Confederación Argentina existe en el vault, el vínculo es navegable. Si no existe todavía, el vínculo aparece como roto pero no rompe la hoja.

### 2.2. Etiquetas de Obsidian vs. etiquetas de SyV

Son dos sistemas distintos que coexisten:

| Tipo | Dónde vive | Para qué |
|---|---|---|
| Etiquetas Obsidian (`#syv/personaje/canonizado`) | Frontmatter `tags:` | Filtrado en Obsidian, búsqueda, vistas de Bases |
| Etiquetas SyV (`faccion.confederacion_argentina`) | Campo `personaje.tags[]` en los datos de juego | Motor de reglas, generación, derivaciones |

En la hoja Obsidian, las etiquetas SyV más relevantes se replican como etiquetas Obsidian bajo la jerarquía `syv/<categoria>/<slug>`. No todas — solo las que tienen utilidad para navegar el vault.

### 2.3. Wikilinks en el cuerpo

El cuerpo de la hoja tiene tres secciones con vínculos:

**Lealtades y pertenencia** (lista breve, vínculos directos):

```markdown
## Lealtades

- Facción: [[Confederación Argentina]]
- Subfacción: [[Pelícanos]]
- Grupo táctico: [[cazadores_de_ricardo|Cazadores de Ricardo]]
- Cadena de mando: [[Mando Sur de la Zanja]]
```

**Aliados y nemesis** (proyectados desde los tags `aliado.*` / `nemesis.*`, con la prosa tomada del hito que formó cada vínculo — ver [[nemesis-y-aliados|nemesis-y-aliados.md]]):

```markdown
## Aliados

- [[K9F2H3M4|Cabo Sosa]] — segundo al mando desde la campaña del 63. Confianza ciega bajo fuego.
- [[NM4K8P2Q|Armero Pedraza]] — civil del Fortín, fuente de repuestos. Deuda pendiente.

## Némesis

- [[R7T3W1X5|Camarada Puntero Mansilla]] — enemigo directo en la Zanja desde hace dos temporadas.
```

> [!tip] Vínculos por patente o por nombre
> Dentro del vault, los vínculos a otros personajes pueden usar la patente opaca (`[[K9F2H3M4]]`) o el nombre canónico (`[[Cabo Sosa]]`). Preferir el nombre para legibilidad; la patente como alias cuando el personaje no tiene nota propia todavía.

**Ubicaciones y eventos** (en la prosa de `historia` o al pie):

```markdown
## Contexto geográfico

Desplegado en el sector norte de la [[Zanja de Alsina]], coordenadas del Fortín Seco. 
Participó en la [[Batalla del Paso Helado]] (campaña del 61).
```

---

## §3 — Convención de nombres de archivo

Los archivos de personaje en el vault siguen una convención única que los hace identificables de inmediato:

```
pj-<patente>.md
```

Ejemplos: `pj-K9F2H3M4.md`, `pj-WA3K9F2H.md`.

La patente en el nombre de archivo garantiza que dos personajes con el mismo nombre no colisionan. El `title` del frontmatter lleva el nombre legible; el nombre de archivo es el identificador técnico.

> [!note] Aliases para navegación
> El frontmatter debe incluir aliases con el nombre completo, el apellido solo y el apodo. Así `[[Aguirre]]` y `[[Sargento Aguirre]]` resuelven al mismo nodo sin necesidad de escribir la patente.

---

## §4 — Entidades del vault vinculadas al personaje

El personaje se conecta a estas entidades del vault de Diégesis. Cada una tiene su propia nota en el vault — la hoja de personaje no las define, solo las referencia.

| Entidad | Tag SyV | Wikilink en la hoja | Nota en el vault |
|---|---|---|---|
| Facción | `faccion.<slug>` | `[[Confederación Argentina]]` | `faccion-confederacion-argentina.md` |
| Subfacción | `subfaccion.<slug>` | `[[Pelícanos]]` | `subfaccion-pelicanos.md` |
| Grupo táctico | `grupo.<slug>` | `[[cazadores_de_ricardo\|Cazadores de Ricardo]]` | `grupo-cazadores-de-ricardo.md` |
| Ubicación actual | — | `[[Zanja de Alsina]]` | `ubicacion-zanja-de-alsina.md` |
| Evento histórico | — | `[[Batalla del Paso Helado]]` | `evento-batalla-paso-helado.md` |
| Otro personaje | — | `[[K9F2H3M4\|Cabo Sosa]]` | `pj-K9F2H3M4.md` |
| Sistema de tags | — | `[[sistema-tags]]` | `sistema-tags.md` (este repo) |

---

## §5 — La hoja como doble interfaz

La misma nota Obsidian es leída de dos maneras:

**Como dato de juego** — el motor de batalla, el generador de personajes y la API consumen el YAML del frontmatter y el campo `personaje.tags[]`. No les interesa el cuerpo ni los vínculos de wiki.

**Como nodo de Diégesis** — el autor narrativo, el árbitro y el lector del vault navegan el cuerpo, siguen los vínculos, leen la `historia` en prosa y consultan el `historial[]` como línea de tiempo.

Esta doble lectura es posible porque:

1. El YAML del frontmatter es la fuente de verdad de los datos estructurados.
2. El cuerpo es prosa + wikilinks — no repite los datos del frontmatter, los complementa con contexto narrativo.
3. Los wikilinks del cuerpo no necesitan validación técnica para existir — un vínculo roto es una deuda de documentación, no un error de sistema.

> [!important] No duplicar datos en el cuerpo
> El cuerpo de la hoja no repite los atributos numéricos ni la lista completa de etiquetas. Esos datos viven en el frontmatter YAML. El cuerpo es para lo que los números no capturan: contexto, relaciones con prosa, ubicación en el mundo.

---

## §6 — Personaje canonizado vs. efímero en el vault

| | Efímero | Canonizado |
|---|---|---|
| Tiene nota en el vault | No (solo existe en la API) | Sí |
| Tiene wikilinks a él desde otros nodos | No | Sí |
| Aparece en el grafo de Diégesis | No | Sí |
| `historia` está congelada | Sí (desde generación) | Sí (desde canonización) |
| `historial[]` crece | No (solo tiene entrada de creación) | Sí (de solo añadir vía hitos) |

La canonización es el momento en que el personaje pasa de dato de juego a nodo del vault. Antes de canonizar, la hoja puede existir como borrador — pero no se linkea desde otras notas del vault.

---

## §7 — Ejemplo mínimo de hoja Obsidian

```markdown
---
title: "Sargento Walter Aguirre"
tags:
  - syv/personaje/canonizado
  - syv/faccion/confederacion_argentina
  - syv/rango/lider_de_escuadra
aliases:
  - Aguirre
  - Walter Aguirre
  - Sargento Aguirre
faccion: "[[Confederación Argentina]]"
grupo: "[[cazadores_de_ricardo|Cazadores de Ricardo]]"
ubicacion_actual: "[[Zanja de Alsina]]"
---

## Lealtades

- Facción: [[Confederación Argentina]]
- Subfacción: [[Pelícanos]]
- Grupo táctico: [[cazadores_de_ricardo|Cazadores de Ricardo]]

## Aliados

- [[K9F2H3M4|Cabo Sosa]] — segundo al mando. Confianza construida en tres campañas.

## Némesis

- [[R7T3W1X5|Camarada Puntero Mansilla]] — rival directo en la Zanja desde el invierno del 63.

## Historia

Walter Aguirre nació en Ciudad Dársena en 2143. A los dieciséis se enlistó en la Confederación por convicción más que por decreto...

## Historial

- `2175-03-14` — `ascenso` — Promovido a Sargento tras la retirada del Cabo Herrera en la Campaña del Paso Helado.
- `2176-11-02` — `agregar_tag` — Incorpora `equipo.arma.fusil_confederado_mod4` tras captura en Fortín Seco.
```

---

## §8 — Navegación inversa: desde el vault al personaje

Las notas de facción, grupo y ubicación del vault deben incluir una sección con vínculos de vuelta a los personajes que las referencian. Esto no es automático — es convención editorial:

```markdown
<!-- en faccion-confederacion-argentina.md -->
## Personajes conocidos

- [[pj-K9F2H3M4|Sargento Aguirre]] — lider_de_escuadra, Cazadores de Ricardo
- [[pj-WA3K9F2H|Cabo Sosa]] — segundo_al_mando, Cazadores de Ricardo
```

Obsidian también genera backlinks automáticamente desde el panel de vínculos entrantes — esa lista es el índice vivo de personajes vinculados a cada entidad del vault.
