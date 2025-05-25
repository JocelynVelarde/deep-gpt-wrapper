import pandas as pd
import numpy as np
from tqdm import tqdm

# -----------------------------
# 1. Load datasets
# -----------------------------
df_tiendas = pd.read_csv("knn.csv")  # LATITUD_NUM, LONGITUD_NUM, TIENDA_ID
df_locales = pd.read_excel("seven_locales.xlsx")  # LATITUD, LONGITUD, NOMBRE, CATEGORIA (or whatever columns exist)

# -----------------------------
# 2. Haversine distance
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    d_phi = np.radians(lat2 - lat1)
    d_lambda = np.radians(lon2 - lon1)
    a = np.sin(d_phi / 2)*2 + np.cos(phi1) * np.cos(phi2) * np.sin(d_lambda / 2)*2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# -----------------------------
# 3. Distance-based feature creation
# -----------------------------
locales_cercanos = []
radio_km = 0.5

for idx, tienda in tqdm(df_tiendas.iterrows(), total=len(df_tiendas)):
    lat_t, lon_t = tienda['LATITUD_NUM'], tienda['LONGITUD_NUM']
    dist = haversine(lat_t, lon_t, df_locales['Latitud'].values, df_locales['Longitud'].values)
    cerca = df_locales[dist <= radio_km]

    resumen = {
        'TIENDA_ID': tienda['TIENDA_ID'],
        'num_locales_cercanos': len(cerca),
        # Add specific filters if needed, for example:
        # 'num_cafeterias': (cerca['CATEGORIA'] == "Cafetería").sum(),
        # 'num_bancos': (cerca['CATEGORIA'] == "Banco").sum(),
    }
    locales_cercanos.append(resumen)

df_features_locales = pd.DataFrame(locales_cercanos)

# -----------------------------
# 4. Merge with stores
# -----------------------------
df_final = df_tiendas.merge(df_features_locales, on='TIENDA_ID', how='left')

# -----------------------------
# 5. Save result
# -----------------------------
df_final.to_csv("locales.csv", index=False)