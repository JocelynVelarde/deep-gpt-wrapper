import streamlit as st
import altair as alt
import pandas as pd
import plotly.express as px                                 

st.set_page_config(layout="wide")
st.title("Current Statistics")

df = pd.read_csv("data/classified.csv")
vn = pd.read_csv("data/Venta.csv")
# st.write("Preview of the data (temp for me)", df.head())

top_n = df.nlargest(10, "AVG_VENTA_TOTAL")
chart = alt.Chart(top_n).mark_bar().encode(
    x=alt.X("TIENDA_ID:N", sort="-y", title="Tienda ID"),
    y=alt.Y("AVG_VENTA_TOTAL:Q", title="Ventas Promedio (Pesos)"),
    color=alt.Color('AVG_VENTA_TOTAL:Q', scale=alt.Scale(scheme='goldorange'), legend=None),
    tooltip=["TIENDA_ID", "AVG_VENTA_TOTAL"]
).properties(
    title="Top 10 Tiendas por Venta Promedio",
    width=600
)
st.altair_chart(chart, use_container_width=True)

bottom_n = df.nsmallest(10, "AVG_VENTA_TOTAL")
chart = alt.Chart(bottom_n).mark_bar().encode(
    x=alt.X("TIENDA_ID:N", sort="-y", title="Tienda ID"),
    y=alt.Y("AVG_VENTA_TOTAL:Q", title="Ventas Promedio (Pesos)"),
    color=alt.Color('AVG_VENTA_TOTAL:Q', scale=alt.Scale(scheme='blues'), legend=None),
    tooltip=["TIENDA_ID", "AVG_VENTA_TOTAL"]
).properties(
    title="Bottom 10 Tiendas por Venta Promedio",
    width=600
)
st.altair_chart(chart, use_container_width=True)

avg_venta_nivel = df.groupby("NIVELSOCIOECONOMICO_DES")["AVG_VENTA_TOTAL"].mean().reset_index()
chart1 = alt.Chart(avg_venta_nivel).mark_bar().encode(
    y=alt.Y('NIVELSOCIOECONOMICO_DES:N', sort='-x', title='Nivel Socioeconómico'),
    x=alt.X('AVG_VENTA_TOTAL:Q', title='Venta Promedio (Pesos)'),
    color=alt.Color('AVG_VENTA_TOTAL:Q', scale=alt.Scale(scheme='greens'), legend=None),
    tooltip=['NIVELSOCIOECONOMICO_DES', 'AVG_VENTA_TOTAL']
).properties(
    title='Venta Promedio por Nivel Socioeconómico',
    width=600,
    height=400
)
st.altair_chart(chart1, use_container_width=True)

plaza_counts = df['PLAZA_CVE'].value_counts().reset_index()
plaza_counts.columns = ['Plaza', 'Num. de Tiendas']
fig = px.pie(plaza_counts, names='Plaza', values='Num. de Tiendas',
             title='Distribución de Tiendas por Plaza',
             hole=0.4)
st.plotly_chart(fig)

avg_venta_plaza = df.groupby("PLAZA_CVE")["AVG_VENTA_TOTAL"].mean().reset_index()
chart2 = alt.Chart(avg_venta_plaza).mark_bar().encode(
    x=alt.X('PLAZA_CVE:N', sort='-y', title='Plaza'),
    y=alt.Y('AVG_VENTA_TOTAL:Q', title='Venta Promedio (Pesos)'),
    color=alt.Color('AVG_VENTA_TOTAL:Q', scale=alt.Scale(scheme='purplered'), legend=None),
    tooltip=['PLAZA_CVE', 'AVG_VENTA_TOTAL']
).properties(
    title='Venta Promedio por Plaza',
    width=600,
    height=400
)
st.altair_chart(chart2, use_container_width=True)

# st.metric("Porcentaje meta cumplida", f"{(df['IS_SUCCESSFUL'].mean()*100):.2f}%")

st.title("VENTAS")

vn["MES_ID"] = pd.to_datetime(vn["MES_ID"].astype(str), format="%Y%m")
vn = vn[vn["MES_ID"] != pd.to_datetime("2024-12")]

monthly_total = vn.groupby("MES_ID")["VENTA_TOTAL"].sum().reset_index()
fig = px.line(monthly_total, x="MES_ID", y="VENTA_TOTAL", title="Ventas Totales Mensuales",
    labels={
        "MES_ID": "Mes",
        "VENTA_TOTAL": "Venta Total (Pesos)"
    })
fig.update_traces(line=dict(color='mediumturquoise'))
fig.update_layout(
    xaxis_tickformat="%b %Y",
    xaxis=dict(
        tickmode='linear',
        dtick="M1"
    ),
    xaxis_tickangle=-45
)
st.plotly_chart(fig)

store = st.selectbox("Selecciona una Tienda", sorted(vn["TIENDA_ID"].unique()))
filtered = vn[vn["TIENDA_ID"] == store].sort_values("MES_ID")

fig2 = px.line(filtered, x="MES_ID", y="VENTA_TOTAL", title=f"Ventas Mensuales - Tienda {store}",
    labels={
        "MES_ID": "Mes",
        "VENTA_TOTAL": "Venta Total (Pesos)"
    })
fig2.update_traces(line=dict(color='mediumspringgreen'))
fig2.update_layout(xaxis_tickformat="%b %Y", xaxis=dict(tickmode='linear', dtick="M1"), xaxis_tickangle=-45)
st.plotly_chart(fig2)


vn["MES_DISPLAY"] = vn["MES_ID"].dt.strftime("%b %Y")

month_options = vn[["MES_DISPLAY", "MES_ID"]].drop_duplicates().sort_values("MES_ID", ascending=False)
options = list(zip(month_options["MES_DISPLAY"], month_options["MES_ID"]))

selected_display, selected_month = st.selectbox(
    "Selecciona un mes",
    options,
    format_func=lambda x: x[0]  # show only display string
)

filtered = vn[vn["MES_ID"] == selected_month].nlargest(10, "VENTA_TOTAL")

chart = alt.Chart(filtered).mark_bar().encode(
    x=alt.X('TIENDA_ID:N', sort='-y', title='Tienda ID'),
    y=alt.Y('VENTA_TOTAL:Q', title='Venta Total (Pesos)'),
    color=alt.Color('VENTA_TOTAL:Q', scale=alt.Scale(scheme='yelloworangebrown'), legend=None),
    tooltip=['TIENDA_ID', 'VENTA_TOTAL']
).properties(
    width=600,
    height=400,
    title=f"Top 10 Tiendas - {selected_month.strftime('%b %Y')}"
)

st.altair_chart(chart, use_container_width=True)












