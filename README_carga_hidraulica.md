
# Cálculo de Carga Hidráulica en Espesador

## Descripción

Este script permite el cálculo físico-matemático de la carga hidráulica en un espesador de concentrado a partir del flujo volumétrico de alimentación y las dimensiones del equipo. El cálculo permite monitorear la carga hidráulica en el tiempo y generar un gráfico de su evolución para apoyar la operación estable del espesador y evitar condiciones de sobrecarga.

## Dependencias

El modelo requiere Python y las siguientes bibliotecas:
- pandas
- numpy
- matplotlib

## Parámetros de Entrada

El cálculo requiere la siguiente información:

### Tabla `data_2024.csv`
- `Fecha`: Fecha y hora del registro (YYYY-MM-DD HH:MM:SS)
- `PP-501 Flujo de Alimentacion (m3/h)`: Caudal desde bomba 501 (float, >0) ----> en BD CAMPO: solidos_bomba_este
- `PP-543 Flujo de Alimentacion (m3/h)`: Caudal desde bomba 543 (float, >0) ----> en BD CAMPO: solidos_bomba_sur
- `PP-544 Flujo de Alimentacion (m3/h)`: Caudal desde bomba 544 (float, >0) ----> en BD CAMPO: solidos_bomba_oeste
- `Diametro (m)`: Diametro de espesador E3 (int, 50) ----> en BD CAMPO: diametro_espesador
## Ecuación del Cálculo

El cálculo utiliza la siguiente ecuación basada en principios hidráulicos:

\[
\text{Carga Hidráulica} = \frac{\text{Flujo Total de Alimentación}}{\text{Área del Espesador}}
\]

Donde:
- **Flujo Total**: Suma de los caudales de las bombas activas (mayores a 100 m³/h).
- **Área del Espesador**: Calculada como \( \pi \times (D/2)^2 \), D es el diametro del espesador E3

## Rangos Operativos Recomendados

Con base en el análisis de datos históricos del espesador, se recomienda mantener la carga hidráulica dentro de rangos que aseguren una sedimentación eficiente, evitando tanto subutilización como sobrecarga. Estos rangos deben ser validados según las condiciones específicas de cada planta.

## Parámetros de Salida

- `Fecha`: Fecha y hora del registro (YYYY-MM-DD HH:MM:SS)
- `flujo_total`: Flujo combinado de las bombas activas (m³/h, float)
- `carga_hidraulica`: Carga hidráulica calculada (m³/h/m², float)

Los resultados se exportan en:
- Archivo CSV: `carga_hidraulica_resultados.csv`

## Ejemplo de Resultados

```json
{
  "Fecha": "2024-01-01 00:00:00",
  "flujo_total": 420.5,
  "carga_hidraulica": 0.206
}
```
