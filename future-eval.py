import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import folium
from geopy.distance import geodesic
from model.create_model import safe_predict
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPEN_AI"])

st.set_page_config(layout="wide")
st.title("Modelo Predictivo")

lat = st.number_input("Latitud", value=25.0, format="%.6f")
lon = st.number_input("Longitud", value=-100.0, format="%.6f")

predicted_sales = None
predicted_category = None

if st.button("Predecir ventas para esta ubicación"):
    try:
        predicted_category, predicted_sales, predicted_proba = safe_predict(lat, lon)
    except Exception as e:
        st.error(f"Error en la predicción: {e}")
        predicted_sales = None

if predicted_sales is not None:
    st.success(f"**Ventas predichas para esta ubicación:** ${predicted_sales:,.2f} (Categoría: {predicted_category})")

@st.cache_data
def load_data():
    return pd.read_csv("data/classi2.csv")

df = load_data()

# GPT function using additional data
def gpt_comment(tienda_row):
    nombre = tienda_row.get("NOMBRE", f"Tienda {tienda_row['TIENDA_ID']}")
    plaza = tienda_row.get("PLAZA", f"Plaza {tienda_row['PLAZA_CVE']}")
    distancia = tienda_row["distance"]

    prompt = (
        f"Genera un breve comentario para una tienda llamada '{nombre}' ubicada en la plaza '{plaza}', "
        f"a {distancia:.2f} km del punto seleccionado. "
        f"Tiene un entorno '{tienda_row['ENTORNO_DES']}', con un nivel socioeconómico '{tienda_row['NIVELSOCIOECONOMICO_DES']}', "
        f"{tienda_row['MTS2VENTAS_NUM']} m² de ventas, {tienda_row['PUERTASREFRIG_NUM']} puertas de refrigeración, "
        f"{tienda_row['CAJONESESTACIONAMIENTO_NUM']} cajones de estacionamiento. Segmento: {tienda_row['SEGMENTO_MAESTRO_DESC']}. "
        f"Meta de venta: ${tienda_row['Meta_venta']}, desempeño actual: {tienda_row['PERFORMANCE_LABEL']}."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de ubicaciones comerciales."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error con OpenAI: {e}")
        return "Comentario no disponible."

left_col, right_col = st.columns([1, 3])

with left_col:
    st.header("Top 3 sucursales cercanas al punto")

    # Calcular distancias
    df["distance"] = df.apply(
        lambda row: geodesic((lat, lon), (row["LATITUD_NUM"], row["LONGITUD_NUM"])).km, axis=1
    )
    top3 = df.nsmallest(3, "distance")

    st.markdown("<div style='max-height:400px; overflow-y:auto;'>", unsafe_allow_html=True)

    for idx, row in top3.iterrows():
        comment = gpt_comment(row)
        st.markdown(
            f"""
            <div style="border:1px solid #ccc; border-radius:8px; padding:10px; margin-bottom:10px;">
                <h4>Tienda: {row.get('NOMBRE', f'Tienda {row["TIENDA_ID"]}')}</h4>
                <b>Plaza:</b> {row.get('PLAZA', f'Plaza {row["PLAZA_CVE"]}')}<br>
                <b>Distancia:</b> {row['distance']:.2f} km<br>
                <i>Descripción: {comment}</i>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    m = leafmap.Map(center=[lat, lon], zoom=10, layers_control=False)
    region_gdf = gpd.read_file("data/plazas.geojson")
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
