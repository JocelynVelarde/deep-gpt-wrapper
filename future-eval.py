import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import folium
from geopy.distance import geodesic

# OpenAI SDK (nuevo cliente)
from openai import OpenAI

# Inicializa cliente de OpenAI con tu clave secreta desde Streamlit
client = OpenAI(api_key=st.secrets["OPEN_AI"])

st.set_page_config(layout="wide")
st.title("Modelo Predictivo")

lat = st.number_input("Latitud", value=25.0, format="%.6f")
lon = st.number_input("Longitud", value=-100.0, format="%.6f")

@st.cache_data
def load_data():
    return pd.read_csv("classi2.csv")

df = load_data()

# GPT function using new OpenAI SDK
def gpt_comment(nombre, plaza, distancia):
    prompt = (
        f"Genera un breve comentario para una tienda llamada '{nombre}' ubicada en la plaza '{plaza}', "
        f"a {distancia:.2f} km del punto seleccionado. El comentario debe ser útil y relevante para una decisión de negocio."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de ubicaciones comerciales."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=40,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error con OpenAI: {e}")
        return "Comentario no disponible."

# Sidebar para las tiendas más cercanas
left_col, right_col = st.columns([1, 3])

with left_col:
    st.header("Top 3 Stores")
    
    # Calcular distancias
    df["distance"] = df.apply(
        lambda row: geodesic((lat, lon), (row["LATITUD_NUM"], row["LONGITUD_NUM"])).km, axis=1
    )
    top5 = df.nsmallest(3, "distance")
    
    # Scroll de tarjetas
    st.markdown(
        """
        <div style="max-height:400px; overflow-y:auto;">
        """,
        unsafe_allow_html=True
    )

    for idx, row in top5.iterrows():
        comment = gpt_comment(
            row.get("NOMBRE", f"Nombre {idx+1}"),
            row.get("PLAZA", f"Plaza {idx+1}"),
            row["distance"]
        )
        st.markdown(
            f"""
            <div style="border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:10px;">
                <h4>Store: {row.get('NOMBRE', f'Nombre {idx+1}')}</h4>
                <b>Plaza:</b> {row.get('PLAZA', f'Plaza {idx+1}')}<br>
                <b>Distance:</b> {row['distance']:.2f} km<br>
                <i>Description: {comment}</i>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    m = leafmap.Map(center=[lat, lon], zoom=10, layers_control=False)
    region_gdf = gpd.read_file("plazas.geojson")
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

    m.add_heatmap(
        df,
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
