import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import folium

st.title("This is our main page")

lat = st.number_input("Latitud", value=25.0, format="%.6f")
lon = st.number_input("Longitud", value=-100.0, format="%.6f")

m = leafmap.Map(center=[40, -100], zoom=6, layers_control=False)
# # tiendas = "tiendas.csv"
# # regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

# # m.add_geojson(regions, layer_name="US Regions")
tiendas = pd.read_csv("tiendas.csv")

# gdf = gpd.GeoDataFrame(
#     tiendas,
#     geometry=gpd.points_from_xy(tiendas.Longitud, tiendas.Latitud),
#     crs="EPSG:4326"
# )

# polygons = []
# for plaza, group in gdf.groupby("Plaza"):
#     merged = group.unary_union.convex_hull # make region shape
#     polygons.append({"plaza": plaza, "geometry": merged})

# region_gdf = gpd.GeoDataFrame(polygons, crs="EPSG:4326")
# region_gdf.to_file("plazas.geojson", driver="GeoJSON")

region_gdf = gpd.read_file("plazas.geojson")

all_plazas = tiendas["Plaza"].astype(str).unique().tolist()
selected_plazas = st.multiselect("Mostrar plazas:", all_plazas, default=all_plazas)

# m.add_geojson("plazas.geojson", layer_name="Bordes de Región")
# m.add_points_from_xy(
#     tiendas,
#     x="Longitud",
#     y="Latitud",
#     color_column="Plaza",
#     icon_names=["gear", "map", "leaf", "globe", "heart"],
#     spin=True,
#     add_legend=True,
#     max_cluster_radius=80
# )

color_map = {
    "1": "red",
    "3": "blue",
    "4": "green",
    "5": "purple",
    "6": "orange",
}

icon_map = {
    "1": "map",
    "3": "gear",
    "4": "leaf",
    "5": "globe",
    "6": "heart",
}

for plaza in selected_plazas:
    plaza_region = region_gdf[region_gdf["plaza"].astype(str) == plaza]
    if not plaza_region.empty:
        m.add_geojson(plaza_region, layer_name=f"Región Plaza {plaza}")

for plaza in selected_plazas:
    subset = tiendas[tiendas["Plaza"].astype(str) == plaza]
    m.add_points_from_xy(
        subset,
        x="Longitud",
        y="Latitud",
        layer_name=f"Plaza {plaza}",
        color_column="Plaza",
        marker_colors=[color_map.get(plaza, "gray")],
        icon_names=[icon_map.get(plaza, "star")], # fallback rocket
        max_cluster_radius=40
    )
m.add_legend(title="Plazas", legend_dict=color_map)

if st.button('Seleccionar Punto'):
    pop = f"Latitud: {lat}\nLongitud: {lon}"
    folium.Marker(
        location=[lat, lon],
        popup=pop,
        icon=folium.Icon(color="black", icon="info-sign")
    ).add_to(m)

m.to_streamlit()