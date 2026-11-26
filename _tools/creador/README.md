# Creador de personajes

Página HTML autónoma que arma un personaje por las ocho fases de [generacion-procedural.md](../../docs/generacion-procedural.md), con los catálogos de `resources/` incrustados. Muestra la ficha viva con las estadísticas derivadas y exporta la hoja canónica `personaje:` en YAML.

- `plantilla.html`: la página, con el marcador `__DATA__` donde van los catálogos. Está escrita para publicarse como artefacto de claude.ai.
- `build_creador.py`: lee `resources/` y escribe `creador-personajes.html` como documento completo, listo para abrir en el navegador.
- `creador-personajes.html`: la salida. Se regenera; no se edita a mano.

```sh
python3 _tools/creador/build_creador.py
```

Hay que regenerarla cada vez que cambia un catálogo, una regla o un depósito de nombres.

## Qué hace

- **Semilla reproducible**: la misma semilla con los mismos campos fijados da el mismo personaje. La prosa queda afuera.
- **Campos fijables**: cada campo tiene candado. Editar un campo lo fija y vuelve a sortear lo que depende de él.
- **Notación de tags**: punto por defecto, con selector para barra.
- **Prosa con Claude**: los botones de historia y apariencia, y las descargas `.md` y `.json`, solo aparecen publicada como artefacto en claude.ai. Abierta como archivo local, el resto funciona igual.

## Decisiones de sorteo que no están en los docs

- La facción se pondera por el campo `probabilidad` del catálogo; una facción con `0` solo sale elegida a mano.
- Las especialidades de combate siempre llevan arma; el resto, con 60% si su facción tiene especialidades de combate y 35% si no.
- `sesgo_faccion`, `sesgo_especialidad` y `sesgo_rango` multiplican el peso de sorteo: no excluyen.
- Hay 25% de sumar un segundo entrenamiento, ponderado por `peso_narrativo`.
