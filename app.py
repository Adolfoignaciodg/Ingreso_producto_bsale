import streamlit as st
import pandas as pd
from datetime import datetime

EXCEL_FILE = 'catalogo_productos.xlsx'

# Cargar datos
@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            'Nombre del Producto', 'Clasificación', 'Tipo de Producto', 
            '¿Posible vender en cantidad decimal?', '¿Controlarás el stock del producto?', 
            'Estado', 'Impuestos', 'Variante', '¿permitirás ventas sin stock?', 
            'Código de Barras', 'SKU', 'Marca', 'Sucursales', 'Fecha de creacion', 'Estado Variante'
        ])
    return df

df = load_data()

st.title("Ingreso y edición de productos")

# Campo para escanear o ingresar código de barras o SKU
codigo = st.text_input("Escanea o ingresa Código de Barras o SKU:")

producto_existente = None
if codigo:
    producto_existente = df[(df['Código de Barras'] == codigo) | (df['SKU'] == codigo)]
    if not producto_existente.empty:
        st.success("Producto existente encontrado, puedes editar sus datos.")
        producto_data = producto_existente.iloc[0].to_dict()
    else:
        st.info("Producto no encontrado, puedes ingresar un nuevo producto.")
        producto_data = {col: "" for col in df.columns}
        producto_data['Código de Barras'] = codigo
        producto_data['SKU'] = codigo
else:
    producto_data = {col: "" for col in df.columns}

with st.form("form_producto", clear_on_submit=False):
    nombre = st.text_input("Nombre del Producto", value=producto_data.get('Nombre del Producto', ''))
    clasificacion = st.text_input("Clasificación", value=producto_data.get('Clasificación', '')).upper()
    tipo_producto = st.text_input("Tipo de Producto", value=producto_data.get('Tipo de Producto', '')).upper()
    vender_decimal = st.selectbox("¿Posible vender en cantidad decimal?", ['Sí', 'No'], index=0 if producto_data.get('¿Posible vender en cantidad decimal?','')=='Sí' else 1)
    controlar_stock = st.selectbox("¿Controlarás el stock del producto?", ['Sí', 'No'], index=0 if producto_data.get('¿Controlarás el stock del producto?','')=='Sí' else 1)
    estado = st.text_input("Estado", value=producto_data.get('Estado', ''))
    impuestos = st.text_input("Impuestos", value=producto_data.get('Impuestos', ''))
    variante = st.text_input("Variante", value=producto_data.get('Variante', ''))
    permitir_venta_sin_stock = st.selectbox("¿permitirás ventas sin stock?", ['Sí', 'No'], index=0 if producto_data.get('¿permitirás ventas sin stock?','')=='Sí' else 1)
    codigo_barras = st.text_input("Código de Barras", value=producto_data.get('Código de Barras', ''))
    sku = st.text_input("SKU", value=producto_data.get('SKU', ''))
    marca = st.text_input("Marca", value=producto_data.get('Marca', ''))
    sucursales = st.text_input("Sucursales", value=producto_data.get('Sucursales', ''))
    fecha_creacion = producto_data.get('Fecha de creacion', '')
    if not fecha_creacion:
        fecha_creacion = datetime.now().strftime('%Y-%m-%d')
    st.write(f"Fecha de creación: {fecha_creacion}")
    estado_variante = st.text_input("Estado Variante", value=producto_data.get('Estado Variante', ''))

    submitted = st.form_submit_button("Guardar Producto")

    if submitted:
        # Crear nuevo registro o actualizar el existente
        nuevo_registro = {
            'Nombre del Producto': nombre,
            'Clasificación': clasificacion,
            'Tipo de Producto': tipo_producto,
            '¿Posible vender en cantidad decimal?': vender_decimal,
            '¿Controlarás el stock del producto?': controlar_stock,
            'Estado': estado,
            'Impuestos': impuestos,
            'Variante': variante,
            '¿permitirás ventas sin stock?': permitir_venta_sin_stock,
            'Código de Barras': codigo_barras,
            'SKU': sku,
            'Marca': marca,
            'Sucursales': sucursales,
            'Fecha de creacion': fecha_creacion,
            'Estado Variante': estado_variante,
        }

        if producto_existente.empty:
            df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
            st.success("Producto agregado correctamente.")
        else:
            idx = producto_existente.index[0]
            for key in nuevo_registro:
                df.at[idx, key] = nuevo_registro[key]
            st.success("Producto actualizado correctamente.")

        # Guardar al Excel
        df.to_excel(EXCEL_FILE, index=False)

