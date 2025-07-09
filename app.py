import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE_PATH = "catalogo_productos.xlsx"

COLUMNS = [
    "Nombre del Producto", "Clasificación", "Tipo de Producto",
    "¿Posible vender en cantidad decimal?", "¿Controlarás el stock del producto?",
    "Estado", "Impuestos", "Variante", "¿permitirás ventas sin stock?",
    "Código de Barras", "SKU", "Marca", "Sucursales",
    "Fecha de creacion", "Estado Variante"
]

@st.cache_data
def load_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    else:
        return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    df.to_excel(FILE_PATH, index=False)

def ingreso_producto(df):
    st.header("Ingreso de nuevo producto")

    marca = st.text_input("Marca")
    clasificacion = st.selectbox("Clasificación", ["CERVEZA", "DESTILADOS", "VINOS", "LICORES", "SNACKS", "ABARROTES", "OTROS"])
    tipo_producto = st.text_input("Tipo de Producto")
    nombre_producto = st.text_input("Nombre del Producto")
    variante = st.text_input("Variante")
    posible_decimal = st.selectbox("¿Posible vender en cantidad decimal?", ["Sí", "No"])
    controlar_stock = st.selectbox("¿Controlarás el stock del producto?", ["Sí", "No"])
    estado = st.selectbox("Estado", ["Activo", "Inactivo"])
    impuestos = st.text_input("Impuestos", value="IVA")  # o desplegable si tienes opciones
    permitir_sin_stock = st.selectbox("¿Permitirás ventas sin stock?", ["Sí", "No"])
    codigo_barras = st.text_input("Código de Barras")
    sku = st.text_input("SKU")
    sucursales = st.text_input("Sucursales")
    estado_variante = st.text_input("Estado Variante")
    fecha_creacion = datetime.now().strftime("%Y-%m-%d")

    if st.button("Agregar producto"):
        if nombre_producto and marca:
            nuevo = {
                "Nombre del Producto": nombre_producto,
                "Clasificación": clasificacion,
                "Tipo de Producto": tipo_producto,
                "¿Posible vender en cantidad decimal?": posible_decimal,
                "¿Controlarás el stock del producto?": controlar_stock,
                "Estado": estado,
                "Impuestos": impuestos,
                "Variante": variante,
                "¿permitirás ventas sin stock?": permitir_sin_stock,
                "Código de Barras": codigo_barras,
                "SKU": sku,
                "Marca": marca,
                "Sucursales": sucursales,
                "Fecha de creacion": fecha_creacion,
                "Estado Variante": estado_variante
            }
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            save_data(df)
            st.success(f"Producto '{nombre_producto}' agregado correctamente.")
            st.experimental_rerun()
        else:
            st.error("Debe ingresar al menos Marca y Nombre del Producto.")

def editar_catalogo(df):
    st.header("Catálogo de productos")
    edited_df = st.data_editor(df, num_rows="dynamic")
    if st.button("Guardar cambios"):
        save_data(edited_df)
        st.success("Cambios guardados.")

def main():
    df = load_data()

    pestañas = st.tabs(["Ingreso", "Catálogo"])

    with pestañas[0]:
        ingreso_producto(df)

    with pestañas[1]:
        editar_catalogo(df)

if __name__ == "__main__":
    main()
