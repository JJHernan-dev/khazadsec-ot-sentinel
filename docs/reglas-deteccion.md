
# Catálogo de reglas de detección

## Propósito

Definir las reglas que utilizará KhazadSec OT Sentinel para identificar
condiciones de riesgo en los datos ficticios del laboratorio Erebor Energy.

Los hallazgos describen discrepancias con las condiciones definidas
en el escenario. No constituyen evidencia de compromiso ni una auditoría
de una instalación real.

## R-01 — Comunicación no autorizada

- Fuente: `data/comunicaciones.csv`
- Condición: `estado=no_autorizada`
- Prioridad propuesta: alta
- Recomendación: revisar la necesidad de la comunicación y aplicar
  los controles de bloqueo previstos en el diseño.

## R-02 — Acceso OT no restringido

- Fuente: `data/inventario.csv`
- Condición: `zona=OT` y `acceso_restringido=no`
- Prioridad propuesta: alta
- Recomendación: revisar y documentar los controles de acceso previstos.

## R-03 — Política de actualizaciones no definida

- Fuente: `data/inventario.csv`
- Condición: `actualizaciones_definidas=no`
- Prioridad propuesta: media
- Recomendación: definir y documentar una política de gestión de
  actualizaciones adecuada al entorno.

## R-04 — Comunicación condicional sin control previsto

- Fuente: `data/comunicaciones.csv`
- Condición: `estado=condicional` y `control_previsto` vacío
- Prioridad propuesta: media
- Recomendación: documentar el control que debe hacer cumplir
  la condición de la comunicación.

## Resultados esperados con los datos de ejemplo

- R-01: `COM-06`
- R-02: `OT-04`
- R-03: `OT-01`, `OT-03` y `OT-04`
- R-04: ningún hallazgo

## Limitaciones

Las prioridades son decisiones iniciales del laboratorio. Los resultados
dependen de los datos de entrada y de las reglas implementadas.
El analizador no verifica la configuración real de la red ni demuestra
que una comunicación haya sido observada.
