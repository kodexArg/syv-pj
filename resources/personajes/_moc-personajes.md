---
slug: _moc-personajes
nombre: Personajes de ejemplo
description: Catálogo de los personajes canónicos de ejemplo, agrupados por facción. Referencia para el motor generador y guía de estilo/contenido para el LLM.
tipo: moc
---

# Personajes de ejemplo — catálogo

Estos son los personajes canónicos de ejemplo del universo *Subordinación y Valor*. Cada uno es una instancia real de la [[hoja-de-personaje|hoja de personaje]] y funciona como referencia concreta para el motor generador y como guía de estilo/contenido para el LLM.

Las secciones se agrupan por el átomo de `faccion` que carga cada ficha: el título de cada `##` lleva ese valor canónico entre código, de modo que el índice sea verificable 1:1 contra el dato.

> [!important] Convención de autoría — campos dedicados, no el espejo de tags planos
> Estas fichas son la **proyección Obsidian** de la hoja: cada dimensión controlada vive en **su propio campo** (`faccion`, `rango`, `especialidad`, `estado`, `lealtad`, `aspectos`, `rasgos`, `equipo`, `apariencia`) y las relaciones son **wikilinks** —conforme a `.claude/rules/tags-taxonomy.md` y `.claude/rules/wikilinks-relations.md`—. **No** se duplica la serialización plana `tags/<categoria>/<slug>` del motor: ese espejo redundante era un anti-patrón (dos fuentes de verdad en un archivo a mano) y fue retirado; `tags` queda como **vivero** (`[]`). El motor (`syv-pj-api`) conserva su forma canónica de `tags[]` planos intacta: es su formato de cable/persistencia, separado de cómo se autora una ficha-ejemplo.
> Todo nuevo campo visual va en `apariencia` (sparse, agnóstico al generador) — ver [[apariencia|docs/apariencia.md]].

## Fuerzas Armadas · `fuerzas_armadas`

- [[dario-sandoval-interrogador|Darío Sandoval]]
- [[elian-quiroga-fusilero|Elián Quiroga]]
- [[facundo-rios-tirador|Facundo Ríos]]
- [[gaston-brizuela-zapador|Gastón Brizuela]]
- [[hernan-bordon-asalto|Hernán Bordón]]
- [[ivan-leiva-asalto|Iván Leiva]]
- [[lucas-veron-medico|Lucas Verón]]
- [[marcos-paez-fusilero|Marcos Páez]]
- [[ovidio-gauna-sargento|Ovidio Gauna]]
- [[ruben-ferreyra-cabo|Rubén Ferreyra]]
- [[tomas-aguirre-recluta|Tomás Aguirre]]

## Resistencia Subterránea · `resistencia_subterranea`

- [[anibal-painemal-comandante|Aníbal Painemal]]
- [[brian-curinanco-pandillero|Brian Curiñanco]]
- [[cosme-medico-caido|Cosme]]
- [[cristian-ledesma-barrabrava|Cristian Ledesma]]
- [[damian-figueroa-barrabrava|Damián Figueroa]]
- [[diego-maidana-barrabrava|Diego Maidana]]
- [[ezequiel-madariaga-camarada|Ezequiel Madariaga]]
- [[jonatan-coronel-barrabrava|Jonatan Coronel]]
- [[kevin-wisotzki-barrabrava|Kevin Wisotzki]]
- [[maxi-linares-pandillero|Maxi Linares]]
- [[nahuel-antieco-pandillero|Nahuel Antieco]]
- [[tobias-arce-barrabrava|Tobías Arce]]
- [[valentina-roca-camarada|Valentina Roca]]
- [[walter-cabrera-barrabrava|Walter Cabrera]]
- [[yair-conuecar-pandillero|Yair Coñuecar]]

## Iglesia / Inquisición · `iglesia`

- [[baltasar-quevedo-inquisidor|Baltasar Quevedo]]
- [[cipriano-roldan-inquisidor|Cipriano Roldán]]
- [[eulogio-sarmiento-capellan|Eulogio Sarmiento]]

## Shipibo-Conibo · `shipibo_conibo`

- [[iracema-chaman-pantano|Iracema]]

## Gremio de Pescadores · `gremio_de_pescadores`

- [[luisa-pescadora|Luisa]]

## Punteros · `punteros`

- [[ramon-sosa-puntero|Ramón Sosa]]

## Traficantes de Almas · `traficantes_de_almas`

- [[severo-tratante-de-almas|Severo]]

## Los Umbanda · `los_umbanda`

- [[yara-sacerdotisa-orixa|Yara]]
