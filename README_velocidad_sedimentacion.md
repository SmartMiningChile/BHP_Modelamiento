
# Modelo de Velocidad de Sedimentación en Espesador

## Descripción

Este proyecto implementa un modelo físico-matemático para estimar la velocidad de sedimentación en un espesador de concentrado a partir de variables operacionales como el porcentaje de sólidos en alimentación, torque y nivel de cama. El modelo permite comparar la velocidad estimada con las mediciones reales de laboratorio y generar un gráfico con zonas de alerta operativas.

## Dependencias

El modelo requiere Python y las siguientes bibliotecas:
- pandas
- matplotlib

## Parámetros de Entrada

El modelo requiere la siguiente información:

### Tabla `sm_operaciones_e3`
- `Fecha`: Fecha y hora del registro (YYYY-MM-DD HH:MM:SS)
- `Solidos de Alimentacion 1 (%)`: Porcentaje de sólidos en alimentación 1 (float, [0,100]) ----> en BD CAMPO: solidos_bomba_este
- `Solidos de Alimentacion 2 (%)`: Porcentaje de sólidos en alimentación 2 (float, [0,100]) ----> en BD CAMPO: solidos_bomba_sur
- `Solidos de Alimentacion 3 (%)`: Porcentaje de sólidos en alimentación 3 (float, [0,100]) ----> en BD CAMPO: solidos_bomba_oeste
- `Torque (mNm)`: Torque del motor (float, >0) 						    ----> en BD CAMPO: torque
- `Nivel de cama (m)`: Nivel de cama en metros (float, >0) 				    ----> en BD CAMPO: nivel_cama

## Ecuación del Modelo

El modelo utiliza la siguiente ecuación basada en una ley de potencia:

\[ v_s = K \times C^n \]

Donde:
- `v_s`: Velocidad de sedimentación ajustada (cm/min)
- `C`: Fracción de sólidos (adimensional, [0,1])
- `K`: Constante empírica (3.84)
- `n`: Exponente empírico (0.13)


## Rangos Operativos Recomendados

Con base en el análisis de datos históricos del espesador, se establecen los siguientes rangos operativos para maximizar la estabilidad y mantener la velocidad de sedimentación dentro del rango óptimo (2.0 – 4.0 cm/min):

- **Porcentaje de Sólidos en Alimentación: 50% a 70%**
- **Nivel de Cama: 0 m a 4 m**
- **Torque del Motor: 5 Nm a 15 Nm**


## Parámetros de Salida

- `timestamp`: Fecha de cálculo (YYYY-MM-DD)
- `vs_ajustada`: Velocidad estimada por el modelo (cm/min, float)

Los resultados se grafican en el archivo `zonas_alerta_vs_ajustada.png`, que incluye:
- Línea de velocidad modelada
- Zonas de alerta:
  - Rojo (<2.0 cm/min): Riesgo de embancamiento
  - Verde (2.0–4.0 cm/min): Operación estable
  - Naranjo (>4.0 cm/min): Riesgo de arrastre

## Ejemplo de Resultados

```json
{
  "timestamp": "2024-01-01",
  "vs_ajustada": 3.12
}
```
