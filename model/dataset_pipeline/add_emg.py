import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

# Cargar datos
df_tiendas = pd.read_csv("locales.csv")
df_reportes = pd.read_csv("incidentes_911.csv")

# Filtrar reportes válidos
df_reportes = df_reportes[df_reportes["descripcion_cierre"] != "Solo verificacion"]

# Convertir coordenadas a radianes
tienda_coords = np.radians(df_tiendas[["LATITUD_NUM", "LONGITUD_NUM"]].to_numpy())
reporte_coords = np.radians(df_reportes[["latitud", "longitud"]].to_numpy())

# Crear BallTree con los reportes
tree = BallTree(reporte_coords, metric="haversine")

# Definir radio (en kilómetros)
radio_km = 1.0
radio_rad = radio_km / 6371.0  # Convertir a radianes

# Buscar cuántos reportes hay dentro del radio para cada tienda
counts = tree.query_radius(tienda_coords, r=radio_rad, count_only=True)

# Agregar la nueva columna
df_tiendas["reportes_cercanos"] = counts

# Guardar resultado
df_tiendas.to_csv("reportes.csv", index=False)
