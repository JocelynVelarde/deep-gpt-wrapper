import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union

st.title("This is our main page")

m = leafmap.Map(center=[40, -100], zoom=6, draw_control=True)
# # tiendas = "tiendas.csv"
# # regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"

# # m.add_geojson(regions, layer_name="US Regions")
tiendas = pd.read_csv("tiendas.csv")

gdf = gpd.GeoDataFrame(
    tiendas,
    geometry=gpd.points_from_xy(tiendas.Longitud, tiendas.Latitud),
    crs="EPSG:4326"
)

polygons = []
for plaza, group in gdf.groupby("Plaza"):
    merged = group.unary_union.convex_hull # make region shape
    polygons.append({"plaza": plaza, "geometry": merged})

region_gdf = gpd.GeoDataFrame(polygons, crs="EPSG:4326")
region_gdf.to_file("plazas.geojson", driver="GeoJSON")

m.add_geojson("plazas.geojson", layer_name="Bordes de Región")
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

unique_plazas = tiendas["Plaza"].astype(str).unique()
for plaza in unique_plazas:
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
m.to_streamlit()