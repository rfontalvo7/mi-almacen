import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Almacén Móvil", layout="centered")

# Enlace directo para leer el Google Sheets exportado en CSV de forma pública
SHEET_URL = "https://docs.google.com/spreadsheets/d/1c9zMN1SCtCxUtnrFl96-jVDtANQeDkACB5kihRuQuKs/edit?gid=154374785#gid=154374785"

fecha_hoy = datetime.now().strftime("%Y-%m-%d")

st.title("📦 Almacén Digital Móvil (Nube)")
st.write(f"📅 Fecha de operación: **{fecha_hoy}**")

tab1, tab2, tab3 = st.tabs(["📝 Programación", "📥 Registrar Entrada", "📊 Comparativo"])

with tab1:
    st.subheader("1. Cargar Programación del Día")
    with st.form("form_programacion", clear_on_submit=True):
        mat_prog = st.text_input("Nombre del Material esperado:")
        cant_prog = st.number_input("Cantidad total esperada:", min_value=1, step=1, value=1)
        btn_prog = st.form_submit_button("Guardar en Programación")
        
        if btn_prog and mat_prog:
            st.info("Para guardar en la nube de forma definitiva, subiremos el proyecto a Streamlit Cloud.")

    try:
        # Leer la pestaña 'Programacion' desde internet de forma directa
        df_prog_actual = pd.read_csv(SHEET_URL + "Programacion")
        df_prog_hoy = df_prog_actual[df_prog_actual["Fecha"] == fecha_hoy]
        st.write("**Materiales esperados hoy (Desde la Nube):**")
        st.dataframe(df_prog_hoy[["Material", "Cantidad Esperada"]], width=2000, hide_index=True)
    except Exception as e:
        st.info("Conectando con Google Sheets...")

with tab2:
    st.subheader("2. Formato de Entrada de Material")
    try:
        df_prog_actual = pd.read_csv(SHEET_URL + "Programacion")
        materiales_hoy = df_prog_actual[df_prog_actual["Fecha"] == fecha_hoy]["Material"].unique().tolist()
    except:
        materiales_hoy = []
    
    if len(materiales_hoy) == 0:
        st.warning("Agrega materiales en la pestaña 'Programación'.")
    else:
        with st.form("form_entradas", clear_on_submit=True):
            material_sel = st.selectbox("Selecciona el Material:", materiales_hoy)
            cant_entrada = st.number_input("Cantidad:", min_value=1, step=1, value=1)
            btn_entrada = st.form_submit_button("Registrar Ingreso")

        try:
            df_ent_actual = pd.read_csv(SHEET_URL + "Entradas")
            df_ent_hoy = df_ent_actual[df_ent_actual["Fecha"] == fecha_hoy]
            st.write("**Historial de ingresos de hoy (Desde la Nube):**")
            st.dataframe(df_ent_hoy[["Hora", "Material", "Cantidad Recibida"]], width=2000, hide_index=True)
        except:
            pass

with tab3:
    st.subheader("3. Consolidado y Validación")
    try:
        df_p = pd.read_csv(SHEET_URL + "Programacion")
        df_e = pd.read_csv(SHEET_URL + "Entradas")
        p_hoy = df_p[df_p["Fecha"] == fecha_hoy]
        e_hoy = df_e[df_e["Fecha"] == fecha_hoy]
        
        if p_hoy.empty:
            st.info("No hay datos de programación en la nube.")
        else:
            e_agrupado = e_hoy.groupby("Material")["Cantidad Recibida"].sum().reset_index()
            comparativo = pd.merge(p_hoy[["Material", "Cantidad Esperada"]], e_agrupado, on="Material", how="left")
            comparativo["Cantidad Recibida"] = comparativo["Cantidad Recibida"].fillna(0).astype(int)
            comparativo["Diferencia"] = comparativo["Cantidad Recibida"] - comparativo["Cantidad Esperada"]
            
            st.write("**Resumen de cumplimiento del día:**")
            st.dataframe(comparativo, width=2000, hide_index=True)
    except:
        st.warning("Esperando datos para procesar la conciliación.")
