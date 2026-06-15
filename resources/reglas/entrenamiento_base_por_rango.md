---
tags: ["regla", "regla/entrenamiento_base_por_rango"]
clave: entrenamiento_base_por_rango
valor:
  # Specialized baselines (legacy ladder keys kept verbatim).
  militante: agitacion
  recluta: instruccion_basica
  fusilero: infanteria
  apuntador: apoyo_de_fuego
  artillero: artilleria
  tirador_designado: tiro_selectivo
  segundo_al_mando: liderazgo_de_campo
  lider_de_escuadra: liderazgo_de_campo
  # Fallback baseline: any rango not specialized above still gets boot training.
  default: instruccion_basica
  # Per-rango baselines for the live ladders (the resolver keys by exact rango),
  # so no unit is left untrained. Specialized rangos keep their entry above.
  adepto: instruccion_basica
  agente_arpista: instruccion_basica
  analista_cripto: instruccion_basica
  aprendiz_gremio: instruccion_basica
  aprendiz_mason: instruccion_basica
  aprendiz_meraya: instruccion_basica
  archivista_jr: instruccion_basica
  buscavidas: instruccion_basica
  cabecilla: liderazgo_de_campo
  cabo: instruccion_basica
  canonigo: instruccion_basica
  capataz: liderazgo_de_campo
  capitan: liderazgo_de_campo
  captador: instruccion_basica
  cardenal: liderazgo_de_campo
  chamana_kuna: instruccion_basica
  cifrador: instruccion_basica
  companero_mason: instruccion_basica
  contacto: instruccion_basica
  coronel: liderazgo_de_campo
  corredor_secretos: instruccion_basica
  custodio_memoria: instruccion_basica
  filho_de_santo: instruccion_basica
  fragmento: instruccion_basica
  grumete: instruccion_basica
  guerrera_kuna: infanteria
  hermano: instruccion_basica
  iluminado: liderazgo_de_campo
  informante: instruccion_basica
  jefe_celula_arpista: liderazgo_de_campo
  lego: instruccion_basica
  madre_de_guerra: liderazgo_de_campo
  maestro_cifra: instruccion_basica
  maestro_mason: liderazgo_de_campo
  magnate: liderazgo_de_campo
  marinero: instruccion_basica
  meraya: instruccion_basica
  mercader: instruccion_basica
  militante_resistencia: agitacion
  novicio: instruccion_basica
  nucleo_consciente: instruccion_basica
  obispo: liderazgo_de_campo
  oga: instruccion_basica
  pai_de_santo: liderazgo_de_campo
  paria: instruccion_basica
  peon: instruccion_basica
  puntero: instruccion_basica
  sacerdote: instruccion_basica
  sargento: liderazgo_de_campo
  script: instruccion_basica
  simpatizante: instruccion_basica
  socio: instruccion_basica
  soldado_de_clan: infanteria
  soldado_linea: infanteria
  teniente: liderazgo_de_campo
  tratante: instruccion_basica
---
Entrenamiento base asignado a cada rango en la fase 4. El resolver indexa por
rango exacto; `default` documenta el piso (`instruccion_basica`) y las entradas
por rango lo materializan en cada escalera viva. Ver [[rangos]].
