# Changelog

## [Unreleased]

- group: attributes-refactor-cuerpo-mente-alma
  priority: critical
  commit: pending
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
