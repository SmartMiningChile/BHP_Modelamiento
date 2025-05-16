# ---------------------------------------------------
# Script para calcular y graficar la Carga Hidráulica
# en un Espesador de 51 metros de diámetro
# ---------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# 1. Definir los archivos de entrada y salida
# ---------------------------------------------------
input_file = "data_2024.csv"  # Archivo CSV con datos operacionales
output_file = "carga_hidraulica_resultados.csv"  # Archivo donde se guardarán los resultados

# ---------------------------------------------------
# 2. Definir las características del espesador
# ---------------------------------------------------
diametro_espesador = 51  # Diámetro del espesador en metros
area_espesador = np.pi * (diametro_espesador / 2) ** 2  # Cálculo del área en m²

# ---------------------------------------------------
# 3. Cargar los datos operacionales
# ---------------------------------------------------
df = pd.read_csv(input_file)

# Asegurar que la columna 'Fecha' esté en formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# ---------------------------------------------------
# 4. Calcular el flujo total de alimentación
# ---------------------------------------------------
# Solo se consideran bombas activas que entregan más de 100 m³/h
df['flujo_total'] = df[['PP-501 Flujo de Alimentacion (m3/h)',
                        'PP-543 Flujo de Alimentacion (m3/h)',
                        'PP-544 Flujo de Alimentacion (m3/h)']].apply(
    lambda row: sum(f for f in row if f > 100), axis=1
)

# ---------------------------------------------------
# 5. Calcular la carga hidráulica
# ---------------------------------------------------
# Carga hidráulica = Flujo total / Área del espesador
df['carga_hidraulica'] = df['flujo_total'] / area_espesador

# ---------------------------------------------------
# 6. Guardar los resultados en un nuevo archivo CSV
# ---------------------------------------------------
df[['Fecha', 'flujo_total', 'carga_hidraulica']].to_csv(output_file, index=False)

# ---------------------------------------------------
# 7. Generar gráfico de la evolución de la carga hidráulica
# ---------------------------------------------------
plt.figure(figsize=(10, 5), dpi=300)
plt.plot(df['Fecha'], df['carga_hidraulica'], marker='o', linestyle='-', color='blue', alpha=0.7)
plt.title('Evolución de la Carga Hidráulica en el Espesador')
plt.xlabel(' ')  # Etiqueta vacía para simplificar
plt.ylabel('Carga Hidráulica (m³/h/m²)')
plt.xticks(rotation=45)  # Rotar etiquetas de fechas
plt.tight_layout()
plt.grid(True)

# ---------------------------------------------------
# 8. Guardar el gráfico como imagen PNG
# ---------------------------------------------------
plt.savefig("carga_hidraulica.png", facecolor='white')
plt.close()