
# Formato de los hallazgos

## Propósito

Definir una estructura común para los hallazgos generados por
KhazadSec OT Sentinel.

## Campos

- `id_hallazgo`: identificador único del hallazgo generado.
- `regla`: identificador de la regla que se ha activado.
- `activo_afectado`: identificador del activo o de la comunicación relacionada.
- `prioridad`: prioridad definida por el catálogo de reglas.
- `titulo`: descripción breve de la condición detectada.
- `evidencia`: dato de entrada que justifica la activación de la regla.
- `recomendacion`: acción propuesta para revisar o mitigar la condición.

## Criterios

1. Cada hallazgo debe estar asociado a una regla documentada.
2. La evidencia debe poder relacionarse con los datos de entrada.
3. La prioridad debe proceder del catálogo de reglas, no asignarse
   arbitrariamente durante la generación del informe.
4. Las recomendaciones deben ser coherentes con la condición detectada.
5. Los hallazgos no deben presentarse como prueba de un ataque
   ni como confirmación de una vulnerabilidad explotable.

## Ejemplo ilustrativo

- ID: H-001
- Regla: R-02
- Elemento afectado: OT-04
- Prioridad: Alta
- Título: Acceso OT no restringido según el escenario
- Evidencia: `acceso_restringido=no`
- Recomendación: revisar y documentar los controles de acceso previstos.

Este ejemplo representa una condición del escenario ficticio, no
un hallazgo de una auditoría real.
