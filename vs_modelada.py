# Script de Modelado de Velocidad de Sedimentación
# ------------------------------------------------
# Este script calcula la velocidad de sedimentación en un espesador
# utilizando un modelo físico-matemático basado en el porcentaje de sólidos.
# Además, genera un gráfico con zonas de alerta y guarda el resultado en un archivo PNG.

import pandas as pd
import matplotlib
# Configura Matplotlib para entornos sin interfaz gráfica (evita errores en servidores o terminales)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ------------------------------------------------
# 1. Cargar los datos desde archivos CSV
# ------------------------------------------------
torque = pd.read_csv("Torque.csv")              # Datos de torque del espesador
nivel_cama = pd.read_csv("Nivel_de_cama_m.csv") # Datos del nivel de cama
data_2024 = pd.read_csv("data_2024.csv")        # Datos operacionales con % de sólidos

# ------------------------------------------------
# 2. Convertir columnas de texto a fechas para procesar correctamente las series de tiempo
# ------------------------------------------------
torque['fecha'] = pd.to_datetime(torque['fecha'])
nivel_cama['fecha'] = pd.to_datetime(nivel_cama['fecha'])
data_2024['Fecha'] = pd.to_datetime(data_2024['Fecha'])

# ------------------------------------------------
# 3. Une los datos en un único DataFrame según la columna Fecha
# ------------------------------------------------
df = pd.merge(data_2024, torque, left_on='Fecha', right_on='fecha', how='inner')
df = pd.merge(df, nivel_cama, left_on='Fecha', right_on='fecha', how='inner')

# ------------------------------------------------
# 4. Calcula la fracción promedio de sólidos (de porcentaje a fracción [0, 1])
# ------------------------------------------------
df['C'] = df[['Solidos de Alimentacion 1 (%)',
              'Solidos de Alimentacion 2 (%)',
              'Solidos de Alimentacion 3 (%)']].mean(axis=1) / 100

# ------------------------------------------------
# 5. Aplicar el modelo físico-matemático de velocidad de sedimentación
#    v_s = K * C^n
# ------------------------------------------------
K = 3.84  # Constante empírica
n = 0.13  # Exponente empírico
df['vs_ajustada'] = K * (df['C'] ** n)

# ------------------------------------------------
# 6. Calcula el promedio diario de la velocidad ajustada
# ------------------------------------------------
vs_ajustada_diaria = df.resample('D', on='Fecha')['vs_ajustada'].mean().reset_index()

# ------------------------------------------------
# 7. Establece el rango de fechas para limitar el eje X en el gráfico
# ------------------------------------------------
fecha_min = vs_ajustada_diaria['Fecha'].min()
fecha_max = vs_ajustada_diaria['Fecha'].max()

# ------------------------------------------------
# 8. Crea el gráfico con las zonas de alerta y la serie calculada
# ------------------------------------------------
plt.figure(figsize=(10, 5))

# Zonas de alerta operacionales
plt.axhspan(0, 2.0, color='red', alpha=0.1, label='Riesgo de embancamiento (<2.0 cm/min)')
plt.axhspan(2.0, 4.0, color='green', alpha=0.1, label='Operación estable (2.0–4.0 cm/min)')
plt.axhspan(4.0, 10.0, color='orange', alpha=0.1, label='Riesgo de arrastre (>4.0 cm/min)')

# Serie de velocidad ajustada
plt.plot(vs_ajustada_diaria['Fecha'], vs_ajustada_diaria['vs_ajustada'],
         label='Velocidad modelada', color='k')

plt.xlabel(' ')  
plt.ylabel('Velocidad de sedimentación (cm/min)')
plt.title('Velocidad de sedimentación con zonas de alerta (modelo calibrado)')
plt.legend()
plt.grid(False)
plt.xlim([fecha_min, fecha_max])  
plt.ylim(0, 6)                    
plt.tight_layout()

# ------------------------------------------------
# 9. Guarda el gráfico en un archivo PNG
# ------------------------------------------------
plt.savefig("vs_modelada.png", dpi=300)
plt.close()  # Cierra el gráfico para liberar recursos
