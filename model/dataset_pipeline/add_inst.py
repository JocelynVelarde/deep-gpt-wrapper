import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# -----------------------------
# 1. Cargar los datasets
# -----------------------------
df_tiendas = pd.read_csv("reportes.csv")  # Sin TIENDA_ID, pero con LATITUD_NUM y LONGITUD_NUM
df_escuelas = pd.read_csv("entidades_educativas.csv")  # columnas lat, lon, nivel_educativo, sostenimiento
# Drop rows with NA values in both dataframes
df_escuelas = df_escuelas.dropna()

# -----------------------------
# 2. Convertir coordenadas a radianes
# -----------------------------
tiendas_coords = np.radians(df_tiendas[["LATITUD_NUM", "LONGITUD_NUM"]].values)
escuelas_coords = np.radians(df_escuelas[["lat", "lon"]].values)

# -----------------------------
# 3. Crear BallTree para escuelas
# -----------------------------
tree_escuelas = BallTree(escuelas_coords, metric="haversine")

# -----------------------------
# 4. Calcular escuelas en radio de 0.5 km
# -----------------------------
radio_km = 0.5
radio_rad = radio_km / 6371.0  # Convertir radio a radianes

# Obtener índices de escuelas cercanas para cada tienda
indices = tree_escuelas.query_radius(tiendas_coords, r=radio_rad)

# -----------------------------
# 5. Calcular métricas por tienda
# -----------------------------
def calcular_metricas(indices_escuelas):
    escuelas_cercanas = df_escuelas.iloc[indices_escuelas]
    return {
        "num_escuelas": len(escuelas_cercanas),
        # "num_esc_primaria": escuelas_cercanas["nivel_educativo"].str.contains("PRIMARIA", case=False).sum(),
        # "num_esc_secundaria": escuelas_cercanas["nivel_educativo"].str.contains("SECUNDARIA", case=False).sum(),
        # "num_esc_media_sup": escuelas_cercanas["nivel_educativo"].str.contains("MEDIA", case=False).sum(),
        # "num_esc_publicas": (escuelas_cercanas["sostenimiento"].str.upper() == "PÚBLICO").sum(),
        # "num_esc_privadas": (escuelas_cercanas["sostenimiento"].str.upper() == "PRIVADO").sum()
    }

# Aplicar la función a todos los índices
metricas = [calcular_metricas(idx) for idx in indices]

# -----------------------------
# 6. Agregar métricas al DataFrame original
# -----------------------------
df_metricas = pd.DataFrame(metricas)
df_tiendas_enriquecido = pd.concat([df_tiendas, df_metricas], axis=1)

# -----------------------------
# 7. Guardar resultado
# -----------------------------
df_tiendas_enriquecido.to_csv("god.csv", index=False)