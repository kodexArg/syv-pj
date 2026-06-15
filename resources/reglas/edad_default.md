---
tags: ["regla", "regla/edad_default"]
clave: edad_default
valor:
  min: 12
  max: 70
  mediana: 26
  desvio: 10
---
Distribución de edad por defecto para la fase 2. El sorteo es una campana
truncada centrada en `mediana` (desviación `desvio`), recortada a `[min, max]`:
el grueso cae cerca de 26 y los extremos (por debajo de 16, por encima de 70)
quedan como outliers raros.
