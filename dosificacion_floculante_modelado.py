# calcular_dosificacion_floculante_con_grafico.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
# CONFIGURACIÓN DEL SCRIPT
# ---------------------------------------------------

input_file = "data_2024.csv"
output_file = "dosificacion_floculante_resultados.csv"

# Constantes de la ecuación ajustada
coef_carga_hidraulica = 3.89
coef_solidos = 0.00399
coef_densidad = -0.0773
intercepto = 0.0131

# Diámetro del espesador (m)
diametro_espesador = 51
area_espesador = np.pi * (diametro_espesador / 2) ** 2  # m²

# ---------------------------------------------------
# CARGAR LOS DATOS
# ---------------------------------------------------

df = pd.read_csv(input_file)
df['Fecha'] = pd.to_datetime(df['Fecha'])

# ---------------------------------------------------
# CALCULAR FLUJO TOTAL CON BOMBAS ACTIVAS (>100 m3/h)
# ---------------------------------------------------

df['flujo_total'] = df[['PP-501 Flujo de Alimentacion (m3/h)',
                        'PP-543 Flujo de Alimentacion (m3/h)',
                        'PP-544 Flujo de Alimentacion (m3/h)']].apply(
    lambda row: sum(f for f in row if f > 100), axis=1
)

# ---------------------------------------------------
# CALCULAR CARGA HIDRÁULICA
# ---------------------------------------------------

df['carga_hidraulica'] = df['flujo_total'] / area_espesador

# ---------------------------------------------------
# CALCULAR PROMEDIO DE SÓLIDOS Y DENSIDAD
# ---------------------------------------------------

df['solidos_prom'] = df[['Solidos de Alimentacion 1 (%)',
                         'Solidos de Alimentacion 2 (%)',
                         'Solidos de Alimentacion 3 (%)']].mean(axis=1)

df['densidad_prom'] = df[['PP-501 Densidad de Alimentacion (t/m3)',
                          'PP-543 Densidad de Alimentacion (t/m3)',
                          'PP-544 Densidad Alimentación (t/m3)']].mean(axis=1)

# ---------------------------------------------------
# APLICAR LA ECUACIÓN FIJA
# ---------------------------------------------------

df['dosis_modelada'] = (coef_carga_hidraulica * df['carga_hidraulica'] +
                    coef_solidos * df['solidos_prom'] +
                    coef_densidad * df['densidad_prom'] +
                    intercepto)

# ---------------------------------------------------
# GUARDAR RESULTADOS
# ---------------------------------------------------

df[['Fecha', 'flujo_total', 'carga_hidraulica', 'solidos_prom', 'densidad_prom', 'dosis_modelada']].to_csv(output_file, index=False)

# Mostrar primeras filas como verificación
print(df[['Fecha', 'flujo_total', 'carga_hidraulica', 'solidos_prom', 'densidad_prom', 'dosis_modelada']].head())
print(f"\nResultados guardados en: {output_file}")

# ---------------------------------------------------
# GENERAR GRÁFICO COMPARATIVO
# ---------------------------------------------------

plt.figure(figsize=(12, 5), dpi=300)
plt.plot(df['Fecha'], df['dosis_modelada'], label='Dosis floculante modelada', color='darkorange', linestyle='--')
plt.xlabel(' ')
plt.ylabel('Dosificación de floculante (m³/h)', fontsize=14)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.ylim(0,2)

# Guardar el gráfico
plt.savefig("dosificacion_modelada.png", facecolor='white')
plt.close()
