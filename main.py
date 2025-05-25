import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import folium

from geopy.distance import geodesic

st.set_page_config(layout="wide")

st.title("This is our main page")

lat = st.number_input("Latitud", value=25.0, format="%.6f")
lon = st.number_input("Longitud", value=-100.0, format="%.6f")
@st.cache_data  
def load_data():
    return pd.read_csv("classi2.csv") 

df = load_data()

# Sidebar for cards
left_col, right_col = st.columns([1, 3])

with left_col:
    st.header("Top 5 Stores")
    # UI for 5 cards (static, no logic)
    for i in range(1, 6):
        st.markdown(
            f"""
            <div style="border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:10px;">
                <h4>Store: Nombre {i}</h4>
                <b>Plaza:</b> Plaza {i}<br>
                <b>Distance:</b> -- km<br>
                <i>Description: retro</i>
            </div>
            """,
            unsafe_allow_html=True
        )

with right_col:
    m = leafmap.Map(center=[lat, lon], zoom=10, layers_control=False)
    region_gdf = gpd.read_file("plazas.geojson")
    # Dummy tiendas DataFrame for UI only (remove if you have your own)
    # tiendas = pd.read_csv("tiendas.csv")
    # all_plazas = tiendas["Plaza"].astype(str).unique().tolist()
    all_plazas = ["1", "3", "4", "5", "6"]
    selected_plazas = st.multiselect("Mostrar plazas:", all_plazas, default=all_plazas)

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

    # The following is placeholder, since tiendas is not used for logic here
    # for plaza in selected_plazas:
    #     subset = tiendas[tiendas["Plaza"].astype(str) == plaza]
    #     m.add_points_from_xy(
    #         subset,
    #         x="Longitud",
    #         y="Latitud",
    #         layer_name=f"Plaza {plaza}",
    #         color_column="Plaza",
    #         marker_colors=[color_map.get(plaza, "gray")],
    #         icon_names=[icon_map.get(plaza, "star")],
    #         max_cluster_radius=40
    #     )
    avg_lat = df["LATITUD_NUM"].mean()
    avg_lon = df["LONGITUD_NUM"].mean()
    heatmap_filepath = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
    m.add_heatmap(
    data=df,
    latitude="LATITUD_NUM",
    longitude="LONGITUD_NUM",
    value="PERFORMANCE_CATEGORY",
    name="Heat map",
    radius=20,
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
# ...existing code...