import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE_PATH = "catalogo_productos.xlsx"

COLUMNS = [
    "Nombre del Producto", "Clasificación", "Tipo de Producto",
    "¿Posible vender en cantidad decimal?", "¿Controlarás el stock del producto?",
    "Estado", "Impuestos", "Variante", "¿permitirás ventas sin stock?",
    "Código de Barras", "SKU", "Marca"
]

# Listas válidas para clasificaciones y tipos producto (ejemplo, ajusta según necesidad)
CLASIFICACIONES_VALIDAS = ["CERVEZA", "DESTILADOS", "VINOS", "LICORES", "SNACKS", "ABARROTES", "OTROS"]
TIPOS_PRODUCTO_VALIDOS = ["LAGER", "ALE", "STOUT", "PILSNER", "RON", "VODKA", "WHISKY", "GINEBRA", "TEQUILA", "PISCO", "OTRO"]

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

def validar_y_formatear_fila(fila):
    # Validar y forzar mayúsculas
    fila["Marca"] = str(fila["Marca"]).upper()
    fila["Clasificación"] = str(fila["Clasificación"]).upper()
    fila["Tipo de Producto"] = str(fila["Tipo de Producto"]).upper()
    fila["Nombre del Producto"] = str(fila["Nombre del Producto"]).upper()
    
    # Validar clasificacion y tipo producto
    if fila["Clasificación"] not in CLASIFICACIONES_VALIDAS:
        st.warning(f"Clasificación inválida: {fila['Clasificación']}. Se cambiará a OTROS.")
        fila["Clasificación"] = "OTROS"
    if fila["Tipo de Producto"] not in TIPOS_PRODUCTO_VALIDOS:
        st.warning(f"Tipo de Producto inválido: {fila['Tipo de Producto']}. Se cambiará a OTRO.")
        fila["Tipo de Producto"] = "OTRO"
    
    # Validar campos requeridos
    if not fila["Marca"]:
        raise ValueError("El campo 'Marca' no puede estar vacío.")
    if not fila["Nombre del Producto"]:
        raise ValueError("El campo 'Nombre del Producto' no puede estar vacío.")
    
    return fila

def ingreso_producto(df):
    st.header("Ingreso de nuevo producto")

    marca = st.text_input("Marca")
    clasificacion = st.selectbox("Clasificación", CLASIFICACIONES_VALIDAS)
    tipo_producto = st.selectbox("Tipo de Producto", TIPOS_PRODUCTO_VALIDOS)
    nombre_producto = st.text_input("Nombre del Producto")
    variante = st.text_input("Variante")
    posible_decimal = st.selectbox("¿Posible vender en cantidad decimal?", ["Sí", "No"])
    controlar_stock = st.selectbox("¿Controlarás el stock del producto?", ["Sí", "No"])
    estado = st.selectbox("Estado", ["Activo", "Inactivo"])
    impuestos = st.text_input("Impuestos", value="IVA")
    permitir_sin_stock = st.selectbox("¿Permitirás ventas sin stock?", ["Sí", "No"])
    codigo_barras = st.text_input("Código de Barras")
    sku = st.text_input("SKU")
    
    fecha_creacion = datetime.now().strftime("%Y-%m-%d")

    if st.button("Agregar producto"):
        try:
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
                "Marca": marca
            }
            nuevo = validar_y_formatear_fila(nuevo)
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
            save_data(df)
            st.success(f"Producto '{nuevo['Nombre del Producto']}' agregado correctamente.")
            st.experimental_rerun()
        except Exception as e:
            st.error(str(e))

def editar_catalogo(df):
    st.header("Catálogo de productos")
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    if st.button("Guardar cambios"):
        try:
            # Validar y formatear todas las filas antes de guardar
            for idx, fila in edited_df.iterrows():
                fila_validada = validar_y_formatear_fila(fila)
                edited_df.loc[idx] = fila_validada
            save_data(edited_df)
            st.success("Cambios guardados correctamente.")
        except Exception as e:
            st.error(f"Error al guardar: {e}")

def main():
    df = load_data()

    pestañas = st.tabs(["Ingreso", "Catálogo"])

    with pestañas[0]:
        ingreso_producto(df)

    with pestañas[1]:
        editar_catalogo(df)

if __name__ == "__main__":
    main()

