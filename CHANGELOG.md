# Changelog

## [Unreleased]

- group: mocs-discoverable
  priority: high
  commit: 221a405
  changes:
    - docs(resources): MOCs de descubribilidad — índice maestro `_moc-resources` + 12 MOCs por categoría (aspectos, entrenamientos, equipos, facciones, habilidades, rasgos, roles, subfacciones, nombres, rangos, atributos, personajes)
    - docs(resources): 381 recursos catalogados, cada uno enlazado vía wikilinks desde su MOC; path-qualified donde el basename es ambiguo (p.ej. 126 links en roles con path)
    - docs(SPINE.md): enlazado desde SPINE.md; ningún recurso queda huérfano
- group: resources-adoption
  priority: critical
  commit: 7294bee
  changes:
    - feat(resources): adoptado `resources/` (catálogos, rangos, personajes) como **SSOT de datos del universo**, externalizado desde syv-pj-api
    - feat(resources/catalogos): aspectos, entrenamientos, equipo, habilidades, rasgos — estructura markdown con frontmatter per-entity en subfolders
    - feat(resources/rangos): 20 tablas de atributos base, rúbrica de alma (líderes/clero alto, rasos bajo)
    - feat(resources/personajes): 34 fichas de ejemplo — ejército rojo (29), iniciados inquisidores (2), capellán de batalla (1), 2 prueba (severo, yara)
    - feat(resources): depósitos de nombres (nombres_mujeres.yaml, nombres_varones.yaml con apodos_patrones)
    - feat(resources): nuevo `resources/reglas/` — per-key markdown (clave, valor) migrado desde YAML monolítico
    - docs: repo hecho PÚBLICO en GitHub; datos universales ya accesibles vía submodule desde syv-pj-api
- group: attributes-refactor-cuerpo-mente-alma
  priority: critical
  commit: 8e33613
  changes:
    - feat(docs/atributos.md): Físico/Mental/Táctico → Cuerpo/Mente/Alma; nombres deterministas en yaml/json (cuerpo, mente, alma); mapeo (fisico→cuerpo, tactico→mente, mental→descartado)
    - feat(docs/atributos.md): Nueva derivada fatiga_max = cuerpo + alma; moral_max = alma; iniciativa = max(cuerpo, mente, alma)
    - feat(docs/contratos.md): Nuevo campo condicion en entradas de efecto; keywords: calcular_encuentros, tiradas_activas, chequeo_miedo
    - feat(docs/contratos.md): Táctico deja de ser atributo, pasa a ser aspecto; 4 aspectos definidos (tactico, religioso, tecnico, primeros_auxilios)
    - refactor(docs): Nombres populares en prosa: Cuerpo/Mente/Alma (o Espíritu); se elimina abreviatura de 3 chars (fis/tac/men)
    - docs(SPINE.md): Atualizado con nueva nomenclatura y derivadas
    - docs(MODEL.md): Atualizado con nueva nomenclatura y derivadas
- group: initial-release
  priority: high
  commit: 903d4a1
  changes:
    - feat(root): PRD.md — especificación de producto; alcance, usuarios, valor, restricciones
    - feat(root): MODEL.md — modelo conceptual; relaciones entidad/atributo, cardinales, notación
    - feat(root): API.md — contratos de interfaz; tipos de datos, esquemas, patrones de extensión
    - feat(root): AGENTS.md — contexto de agentes y herramientas; roles, responsabilidades, herramientas
    - feat(root): README.md — punto de entrada; instrucciones de cómo usar syv-pj
    - feat(docs): hoja-personaje.md — núcleo del módulo; anatomía, campos, invariantes, ejemplos
    - feat(docs): sistema-tags.md — ontología de tags; jerarquía, reglas, casos de uso
    - feat(docs): contratos.md — contratos nombre→paquete; mecánica, registro, propiedades dinámicas
    - feat(docs): atributos-y-habilidades.md — estadísticas y atributos; rango, fórmulas, efectos
    - feat(docs): generacion-procedural.md — algoritmo de generación; distribución, siembra, ejemplos
    - feat(docs): open-close.md — principios SOLID para extensión sin modificación; patrones
    - feat(docs): grupos.md — escuadra→grupo universalizado; jerarquía, composición, alcance
    - feat(docs): diegesis-y-obsidian.md — convención de linkeo al vault; integración, queries
    - feat(docs): casos-de-uso.md — narrativas de punta a punta; personaje, diégesis, estrategia, rol, visual
