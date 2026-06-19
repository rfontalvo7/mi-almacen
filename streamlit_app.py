import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Almacén Móvil", layout="centered")

# Conexión oficial y segura con tu Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer los datos existentes de la pestaña "Programacion"
try:
    df_existente = conn.read(worksheet="Programacion")
except Exception:
    df_existente = pd.DataFrame(columns=["Fecha", "Material", "Cantidad Esperada"])

st.title("📦 Almacén Digital Móvil")
fecha_hoy = datetime.now().strftime("%Y-%m-%d")
st.write(f"**Fecha de operación:** `{fecha_hoy}`")

tab1, tab2, tab3 = st.tabs(["📋 Programación", "📩 Registrar Entrada", "📊 Comparativo"])

with tab1:
    st.subheader("1. Cargar Programación del Día")
    
    with st.form("form_programacion", clear_on_submit=True):
        mat_prog = st.text_input("Nombre del Material esperado:")
        cant_prog = st.number_input("Cantidad total esperada:", min_value=1, step=1, value=1)
        boton_guardar = st.form_submit_button("Guardar en Programación")
        
        if boton_guardar:
            if mat_prog.strip() == "":
                st.error("⚠️ Por favor escribe el nombre del material.")
            else:
                # Crear la nueva fila de datos
                nueva_fila = pd.DataFrame([{
                    "Fecha": fecha_hoy,
                    "Material": mat_prog,
                    "Cantidad Esperada": cant_prog
                }])
                
                # Juntar datos viejos con el nuevo
                df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
                
                # Guardar directamente en Google Sheets
                conn.update(worksheet="Programacion", data=df_actualizado)
                st.success(f"✅ ¡{mat_prog} guardado correctamente en la nube!")
                st.balloons()
