import streamlit as st
import pandas as pd
from datetime import datetime

# Listas de ejemplo (puedes ampliar)
marcas = ['Royal Guard', 'Becker', 'Cusqueña', 'Budweiser', 'Heineken', 'Kunstmann', 'Sol']
clasificaciones = ['Cerveza', 'Vino', 'Destilado', 'Bebida', 'Licores']
tipos_producto = ['Lager', 'IPA', 'Stout', 'Cabernet Sauvignon', 'Whisky', 'Vodka', 'Ron']
variante_posible_decimal = ['Sí', 'No']
estado_lista = ['Activo', 'Inactivo']
impuestos_lista = ['IVA 19%', 'Exento', 'Otro']
permiso_venta_sin_stock = ['Sí', 'No']
tipo_envase = ['Botellín', 'Lata', 'Botella', 'Barril', 'Pack', 'Otros']

st.title("Ingreso de Productos Supermercado")

# Inputs
marca = st.selectbox("Marca", marcas)
clasificacion = st.selectbox("Clasificación", clasificaciones)
tipo_producto = st.selectbox("Tipo de Producto", tipos_producto)
variante = st.text_input("Variante (ej: Botellín, Lager, Rojo...)")
volumen = st.text_input("Volumen (ej: 355cc, 750ml)")
posible_decimal = st.selectbox("¿Posible vender en cantidad decimal?", variante_posible_decimal)
control_stock = st.selectbox("¿Controlarás el stock?", variante_posible_decimal)
estado = st.selectbox("Estado", estado_lista)
impuestos = st.selectbox("Impuestos", impuestos_lista)
permitir_sin_stock = st.selectbox("¿Permitir ventas sin stock?", permiso_venta_sin_stock)
codigo_barras = st.text_input("Código de Barras")
sku = st.text_input("SKU")
sucursales = st.text_area("Sucursales (separar con comas)")
fecha_creacion = datetime.today().strftime('%Y-%m-%d')
estado_variante = st.selectbox("Estado Variante", estado_lista)

# Construcción Nombre del Producto (concatenar)
nombre_producto = f"{marca} {tipo_producto} {variante} {volumen}".strip()

# Mostrar resumen
st.markdown("### Resumen del Producto")
producto = {
    "Nombre del Producto": nombre_producto,
    "Clasificación": clasificacion,
    "Tipo de Producto": tipo_producto,
    "¿Posible vender en cantidad decimal?": posible_decimal,
    "¿Controlarás el stock?": control_stock,
    "Estado": estado,
    "Impuestos": impuestos,
    "Variante": variante,
    "¿Permitirás ventas sin stock?": permitir_sin_stock,
    "Código de Barras": codigo_barras,
    "SKU": sku,
    "Marca": marca,
    "Sucursales": sucursales,
    "Fecha de creación": fecha_creacion,
    "Estado Variante": estado_variante,
}

df = pd.DataFrame([producto])
st.dataframe(df)

# Guardar en CSV
if st.button("Guardar producto"):
    try:
        df.to_csv("productos.csv", mode='a', header=False, index=False)
        st.success("Producto guardado en productos.csv")
    except Exception as e:
        st.error(f"Error al guardar: {e}")
