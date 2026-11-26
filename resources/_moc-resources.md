---
title: MOC — Recursos (índice maestro)
folder: resources
description: Índice umbrella de todos los MOCs de categoría en resources/. Cada categoría agrupa los datos/mock templates que el motor usa para generar personajes y sirven como guías de estilo y contenido para el LLM.
tags:
  - entidad/guia
aliases:
  - Catálogo de recursos
  - MOC Resources
---

# Recursos — índice maestro

`resources/` contiene los **datos canónicos de referencia** del motor `syv-pj`: catálogos, templates, ejemplos y mock data. Todo lo que aquí vive es de solo lectura para el motor en tiempo de generación; el LLM los consume como contexto y guía.

## Categorías

| MOC | Qué contiene |
|---|---|
| [_moc-especialidades](especialidades/_moc-especialidades.md) | Roles de personaje (`especialidad/oficio`, `especialidad/combate`, `especialidad/jerarquia`, `especialidad/narrativo`). Determinan atributos base y pool de tags disponibles en creación. |
| [_moc-equipo](catalogos/equipo/_moc-equipo.md) | Ítems de equipo (`equipo/arma`, `equipo/utilitario`, `equipo/vestidura`). Cada ítem es un tag equipable con sus efectos declarados. |
| [_moc-rasgos](catalogos/rasgo/_moc-rasgos.md) | Rasgos físicos observables (`rasgo/*`): cicatrices, tatuajes, marcas. Puramente descriptivos, sin efecto mecánico directo. |
| [_moc-entrenamiento](catalogos/entrenamiento/_moc-entrenamiento.md) | Entrenamientos (`entrenamiento/*`): disciplinas aprendidas que habilitan ciertas habilidades o modifican atributos al crearlas. |
| [_moc-habilidades](catalogos/habilidad/_moc-habilidades.md) | Habilidades (`habilidad/*`): habilitadores de tirada contra un `atributo_dominante`. Nunca aplican modificador directo. |
| [_moc-facciones](facciones/_moc-facciones.md) | Facciones del universo (`faccion/*`): los bloques de poder dentro de *Subordinación y Valor*. Cada facción define el pool de rangos, subfacciones y especialidades disponibles. |
| [_moc-subfacciones](subfacciones/_moc-subfacciones.md) | Subfacciones (`subfaccion/*`): ramas, órdenes o células dentro de una facción mayor. |
| [_moc-rangos](rangos/_moc-rangos.md) | Rangos (`rango/*`): jerarquía interna de cada facción. Determinan atributos base y peso de mando. |
| [_moc-aspectos](catalogos/aspecto/_moc-aspectos.md) | Aspectos (`aspecto/*`): identidad mecánicamente activa (carácter, condición, marca con peso mecánico). Declaran efectos pasivos o reactivos. |
| [_moc-reglas](reglas/_moc-reglas.md) | Reglas del sistema: glosario de mecánicas, vocabulario canónico de atributos/estadísticas, contratos aspecto/habilidad/efecto. |
| [_moc-nombres](nombres/_moc-nombres.md) | Depósitos de nombres para generación procedural: nombres de varón, de mujer, por origen cultural o facción. |
| [_moc-personajes](personajes/_moc-personajes.md) | Personajes canónicos de ejemplo (34 instancias reales). Referencia concreta para el motor y guía de estilo para el LLM. |
