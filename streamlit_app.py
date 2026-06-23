import streamlit as st
import pandas as pd
from datetime import datetime
import requests

st.set_page_config(page_title="Almacén Móvil", layout="centered")

st.title("📦 Almacén Digital Móvil")
fecha_hoy = datetime.now().strftime("%Y-%m-%d")
st.write(f"**Fecha de operación:** `{fecha_hoy}`")

tab1, tab2, tab3 = st.tabs(["📋 Programación", "📩 Registrar Entrada", "📊 Comparativo"])

# Tu enlace de Apps Script oficial para guardar sin bloqueos de Google
URL_CONEXION = "https://script.google.com/macros/s/AKfycbymjnkcyUxBCvkDyeHLav38mSQ1SY3reZ2QrAptSJGJ9YAtbw3ZrY0DSr_f5qItXIVH/exec"

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
                # Paquete de datos estructurado para enviar a tu Google Sheets
                datos = {
                    "fecha": fecha_hoy,
                    "material": mat_prog,
                    "cantidad": int(cant_prog)
                }
                
                try:
                    # Envío directo por internet
                    respuesta = requests.post(URL_CONEXION, json=datos)
                    if respuesta.status_code == 200:
                        st.success(f"✅ ¡{mat_prog} guardado correctamente en tu Google Sheets!")
                        st.balloons()
                    else:
                        st.error("⚠️ La hoja no respondió correctamente. Verifica el Apps Script.")
                except Exception as e:
                    st.error(f"Error de comunicación: {e}")
