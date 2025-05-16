
# Modelo de Dosificación de Floculante con Ecuación Fija

## Descripción

Este documento contiene la implementación de la ecuación ajustada para estimar la dosificación requerida de floculante en un espesador de concentrado. La ecuación se basa en datos operacionales históricos y permite su aplicación directa en caso de no contar con datos en tiempo real.

## Dependencias

El script requiere Python y las siguientes bibliotecas:
- pandas
- numpy
- matplotlib

## Ecuación del Modelo

La dosificación se calcula según la siguiente ecuación ajustada:

\[
F = 3.89 \times \text{Carga Hidráulica} + 0.00399 \times \% \text{Sólidos} - 0.0773 \times \text{Densidad} + 0.0131
\]

Donde:
- **F**: Dosificación de floculante estimada (m³/h).
- **Carga Hidráulica**: Flujo total dividido por el área del espesador (m³/h/m²).
- **% Sólidos**: Promedio de los sólidos en alimentación (%).
- **Densidad**: Densidad promedio de alimentación (t/m³).

## Parámetros de Entrada

El modelo puede operar tanto con datos de archivos como con valores ingresados manualmente. Se requiere:

### Desde datos operacionales`
- `Fecha`: Fecha y hora del registro (YYYY-MM-DD HH:MM:SS)
- `PP-501 Densidad de Alimentacion (t/m3)`: Densidad de alimentación bomba este (float, [0,100]) ----> en BD CAMPO: flujo_bomba_este
- `PP-543 Densidad de Alimentacion (t/m3)`: Densidad de alimentación bomba sur (float, [0,100]) ----> en BD CAMPO: flujo_bomba_aur
- `PP-544 Densidad de Alimentacion (t/m3)`: Densidad de alimentación bomba oeste (float, [0,100]) ----> en BD CAMPO: flujo_bomba_oeste
- `Solidos de Alimentacion 1 (%)`: Porcentaje de sólidos en alimentación bomba este (float, [0,100]) ----> en BD CAMPO: solidos_bomba_este
- `Solidos de Alimentacion 2 (%)`: Porcentaje de sólidos en alimentación bomba sur (float, [0,100]) ----> en BD CAMPO: solidos_bomba_sur
- `Solidos de Alimentacion 3 (%)`: Porcentaje de sólidos en alimentación bomba oeste (float, [0,100]) ----> en BD CAMPO: solidos_bomba_oeste

### Ingreso de rangos en caso de no contar con valores en tiempo real
- **Flujo Total de Alimentación (m³/h)**: Rango sugerido 300 - 600
- **% Sólidos en Alimentación (%)**: Rango sugerido 50 - 70
- **Densidad de Alimentación (t/m³)**: Rango sugerido 1.3 - 2.5

## Parámetros de Salida

- `dosis_floculante_modeladad`: Dosificación de floculante estimada (m³/h, float)

## Ejemplo de Resultados

```json
{
  "Fecha": "2024-01-01 00:00:00",
  "flujo_total": 420.5,
  "carga_hidraulica": 0.206,
  "solidos_prom": 60.5,
  "densidad_prom": 2.1,
  "dosis_fija": 3.12
}
```
