---
tags: ["regla", "regla/habilidad_por_rol"]
clave: habilidad_por_rol
valor:
  # The resolver keys by EXACT rol slug; only the 5 existing habilidad slugs are
  # used (combate_cuerpo_a_cuerpo · liderazgo · manejo_de_explosivos ·
  # primeros_auxilios · tiro_de_precision). Map only where a skill is genuinely
  # implied by the role.

  # Combat family → close-quarters fighting (designated shooters and demolition
  # specialists are the exceptions).
  rol/combate/tirador: tiro_de_precision
  rol/combate/asalto: combate_cuerpo_a_cuerpo
  rol/combate/cazadora: combate_cuerpo_a_cuerpo
  rol/combate/cruzado: combate_cuerpo_a_cuerpo
  rol/combate/fusilero: combate_cuerpo_a_cuerpo
  rol/combate/guerrera: combate_cuerpo_a_cuerpo
  rol/combate/maton: combate_cuerpo_a_cuerpo
  rol/combate/vigilante: combate_cuerpo_a_cuerpo
  rol/combate/saboteador: manejo_de_explosivos
  rol/combate/zapador: manejo_de_explosivos
  rol/combate/heroe: liderazgo
  rol/combate/lider: liderazgo
  rol/oficio/medico: primeros_auxilios
  rol/oficio/enfermero: primeros_auxilios
  rol/oficio/cirujano: primeros_auxilios
  rol/oficio/ciruja: primeros_auxilios
  rol/oficio/curandero: primeros_auxilios
  rol/paranormal/sanador: primeros_auxilios
  rol/paranormal/sanadora: primeros_auxilios
  rol/paranormal/curandero: primeros_auxilios
  rol/paranormal/exorcista_medico: primeros_auxilios
---
Habilidad especial otorgada según el rol táctico del personaje en la fase 4. El
resolver indexa por rol exacto. Ver [[roles]].
