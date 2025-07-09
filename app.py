# app.py
import streamlit as st
import pandas as pd
import os

FILE_PATH = "catalogo_productos.xlsx"

st.title("Gestor de Catálogo de Productos")

# Columnas esperadas
COLUMNS = [
    "Nombre del Producto", "Clasificación", "Tipo de Producto",
    "¿Posible vender en cantidad decimal?", "¿Controlarás el stock del producto?",
    "Estado", "Impuestos", "Variante", "¿permitirás ventas sin stock?",
    "Código de Barras", "SKU", "Marca", "Sucursales",
    "Fecha de creacion", "Estado Variante"
]

# Función para cargar o crear df
@st.cache_data
def load_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        # Asegurar columnas
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    else:
        # Crear df vacío con columnas
        df = pd.DataFrame(columns=COLUMNS)
        return df

df = load_data()

st.write("Catálogo actual:")

edited_df = st.data_editor(df, num_rows="dynamic")

if st.button("Guardar cambios"):
    edited_df.to_excel(FILE_PATH, index=False)
    st.success("Datos guardados en catalogo_productos.xlsx")

