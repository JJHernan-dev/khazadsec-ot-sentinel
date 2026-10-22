# KhazadSec OT Sentinel — Escenario industrial

## 1. Descripción de la instalación

Erebor Energy es una instalación energética ficticia dedicada a la supervisión de equipos de distribución eléctrica.

El escenario representa una arquitectura industrial simplificada que combina sistemas de tecnología de la información (IT) y sistemas de tecnología operacional (OT).

La instalación se utilizará como entorno didáctico para estudiar el inventario de activos industriales, la segmentación de redes y la identificación de posibles condiciones de riesgo.

## 2. Objetivo del laboratorio

OT Sentinel Lab es un laboratorio didáctico de ciberseguridad industrial desarrollado bajo la identidad KhazadSec.

Su herramienta principal, KhazadSec OT Sentinel, tendrá como objetivo analizar un inventario de activos ficticios, identificar posibles condiciones de riesgo mediante reglas explícitas y generar un informe técnico con hallazgos, prioridades y recomendaciones.

El proyecto también pretende demostrar conocimientos iniciales de Python, análisis de riesgos, documentación técnica y fundamentos de ciberseguridad IT/OT.

## 3. Activos previstos

La instalación contará inicialmente con los siguientes activos ficticios:

- Equipo de administración IT.
- Cortafuegos para controlar las comunicaciones entre las zonas IT y OT.
- Servidor SCADA para la supervisión del proceso.
- Estación HMI para la visualización y operación del sistema.
- Controlador lógico programable (PLC).
- Equipo de adquisición de datos.

Las funciones concretas, la criticidad, las propiedades de seguridad y las comunicaciones de cada activo se definirán durante el diseño de la arquitectura y del inventario.

## 4. Arquitectura IT/OT

La arquitectura se dividirá conceptualmente en dos zonas:

- **Zona IT:** representa los sistemas corporativos y los equipos de administración.
- **Zona OT:** contiene los sistemas industriales de control y supervisión.

Un cortafuegos representará el punto de control entre ambas zonas. Las comunicaciones necesarias y las medidas de segmentación se definirán durante el diseño técnico.

Esta arquitectura es un modelo didáctico inicial y no representa una instalación real ni una configuración validada para su uso en producción.

## 5. Alcance del análisis

KhazadSec OT Sentinel será una aplicación de consola desarrollada en Python que leerá un inventario en formato CSV.

La aplicación tendrá como objetivos:

1. Leer y validar los datos del inventario.
2. Analizar las características de seguridad declaradas para cada activo.
3. Aplicar reglas documentadas para identificar posibles condiciones de riesgo.
4. Asignar prioridades según criterios explícitos.
5. Generar un informe técnico con los activos analizados, los hallazgos y las medidas correctoras propuestas.

Las reglas, los criterios de priorización y el formato definitivo del informe se concretarán durante el desarrollo.

## 6. Tecnologías previstas

- Python para la lógica de análisis.
- CSV para el inventario de activos.
- Markdown para la documentación técnica.
- Git y GitHub para el control de versiones y la publicación del proyecto.
- Una herramienta de diagramación para representar la arquitectura IT/OT.

El alcance inicial no contempla una interfaz gráfica ni una base de datos.

## 7. Seguridad y limitaciones

Todos los activos, direcciones, configuraciones y datos utilizados en el laboratorio serán ficticios.

No se realizarán pruebas contra redes industriales reales, PLC reales, sistemas de terceros ni infraestructuras de producción.

El análisis se basará exclusivamente en los datos disponibles en el inventario y en reglas didácticas documentadas.

Los resultados representarán indicios o condiciones que requieren atención, no pruebas concluyentes de compromiso ni una evaluación exhaustiva del riesgo real.

El laboratorio no constituye una auditoría profesional ni certifica el cumplimiento de normas o marcos regulatorios.

## 8. Supuestos pendientes de definir

Antes de implementar el analizador, se deberán concretar:

- La función y la zona de cada activo.
- Las comunicaciones necesarias entre los equipos.
- La criticidad asignada a cada activo y su justificación.
- Las características de seguridad que se registrarán en el inventario.
- Las reglas de detección y sus justificaciones.
- Los criterios para asignar prioridades.
- Las medidas correctoras asociadas a los hallazgos.

## 9. Identidad y organización del proyecto

- **Identidad del proyecto:** KhazadSec.
- **Laboratorio:** OT Sentinel Lab.
- **Herramienta:** KhazadSec OT Sentinel.
- **Instalación ficticia:** Erebor Energy.
- **Repositorio previsto:** `khazadsec-ot-sentinel`.

La identidad visual podrá incorporar referencias discretas a la fantasía y a la Tierra Media, manteniendo una nomenclatura técnica clara y una documentación profesional.