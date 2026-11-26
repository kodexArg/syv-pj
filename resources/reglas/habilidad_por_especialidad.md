---
tags: ["regla", "regla/habilidad_por_especialidad"]
clave: habilidad_por_especialidad
valor:
  # The resolver keys by EXACT especialidad slug; only the 5 existing habilidad slugs are
  # used (combate_cuerpo_a_cuerpo · liderazgo · manejo_de_explosivos ·
  # primeros_auxilios · tiro_de_precision). Map only where a skill is genuinely
  # implied by the role.

  # Combat family → close-quarters fighting (designated shooters and demolition
  # specialists are the exceptions).
  especialidad/combate/tirador: tiro_de_precision
  especialidad/combate/asalto: combate_cuerpo_a_cuerpo
  especialidad/combate/cazadora: combate_cuerpo_a_cuerpo
  especialidad/combate/cruzado: combate_cuerpo_a_cuerpo
  especialidad/combate/fusilero: combate_cuerpo_a_cuerpo
  especialidad/combate/guerrera: combate_cuerpo_a_cuerpo
  especialidad/combate/maton: combate_cuerpo_a_cuerpo
  especialidad/combate/vigilante: combate_cuerpo_a_cuerpo
  especialidad/combate/saboteador: manejo_de_explosivos
  especialidad/combate/zapador: manejo_de_explosivos
  especialidad/combate/heroe: liderazgo
  especialidad/combate/lider: liderazgo
  especialidad/oficio/medico: primeros_auxilios
  especialidad/oficio/enfermero: primeros_auxilios
  especialidad/oficio/cirujano: primeros_auxilios
  especialidad/oficio/ciruja: primeros_auxilios
  especialidad/oficio/curandero: primeros_auxilios
  especialidad/paranormal/sanador: primeros_auxilios
  especialidad/paranormal/sanadora: primeros_auxilios
  especialidad/paranormal/curandero: primeros_auxilios
  especialidad/paranormal/exorcista_medico: primeros_auxilios
---
Habilidad especial otorgada según la especialidad táctica del personaje en la fase 4. El
resolver indexa por especialidad exacta. Ver especialidades.
