import streamlit as st
import pandas as pd
import os

ARCHIVO_EXCEL = "catalogo_productos.xlsx"

COLUMNAS = [
    "Clasificación", "Tipo de Producto", "¿Posible vender en cantidad decimal?",
    "¿Controlarás el stock del producto?", "Estado", "Impuestos", "Variante",
    "¿permitirás ventas sin stock?", "Código de Barras", "SKU", "Marca",
    "Sucursales", "Fecha de creacion", "Estado Variante"
]

# Cargar archivo o crear
def cargar_datos():
    if os.path.exists(ARCHIVO_EXCEL):
        xls = pd.ExcelFile(ARCHIVO_EXCEL)
        hojas = {hoja: xls.parse(hoja) for hoja in xls.sheet_names}
        for h in ["Ingreso", "Catálogo", "Edición"]:
            if h not in hojas:
                hojas[h] = pd.DataFrame(columns=COLUMNAS)
    else:
        hojas = {h: pd.DataFrame(columns=COLUMNAS) for h in ["Ingreso", "Catálogo", "Edición"]}
        guardar_datos(hojas)
    return hojas

def guardar_datos(hojas):
    with pd.ExcelWriter(ARCHIVO_EXCEL, engine="openpyxl", mode="w") as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre, index=False)

st.set_page_config("🛒 Catálogo de Productos", layout="wide")
st.title("🛍️ Catálogo de Productos Supermercado")

hojas = cargar_datos()
menu = st.sidebar.radio("Menú", ["Ingreso", "Catálogo", "Editar"])

if menu == "Ingreso":
    st.header("➕ Ingreso de Producto")

    with st.form("form_ingreso"):
        clasificacion = st.selectbox("Clasificación", sorted([
            "CERVEZA", "BEBIDA", "DESTILADO", "LICOR", "VINO", "MINI COCTEL", "AGUA", "ENERGÉTICA",
            "ABARROTES", "CHOCOLATE", "SNACK", "TABAQUERIA", "LÁCTEOS", "FIAMBRES", "CAFÉ"
        ]))

        tipo_producto = st.text_input("Tipo de Producto").strip().upper()
        variante = st.text_input("Variante").strip().upper()
        marca = st.text_input("Marca").strip().upper()
        codigo_barras = st.text_input("Código de Barras").strip()
        sku = st.text_input("SKU").strip().upper()

        posible_decimal = st.radio("¿Se puede vender en cantidad decimal?", ["NO", "SÍ"], index=0)
        controlar_stock = st.radio("¿Controlarás el stock?", ["SÍ", "NO"], index=0)
        estado = st.radio("Estado del producto", ["ACTIVO", "INACTIVO"], index=0)
        impuestos = st.selectbox("Impuestos", ["IVA", "EXENTO"])
        permitir_sin_stock = st.radio("¿Permitir ventas sin stock?", ["NO", "SÍ"], index=0)
        sucursal = "PRINCIPAL"

        fecha_creacion = pd.Timestamp.now().strftime("%Y-%m-%d")
        estado_variante = estado

        submit = st.form_submit_button("Guardar")

        if submit:
            nuevo = {
                "Clasificación": clasificacion.upper(),
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
                "Sucursales": sucursal,
                "Fecha de creacion": fecha_creacion,
                "Estado Variante": estado_variante
            }

            for h in ["Ingreso", "Catálogo"]:
                hojas[h] = pd.concat([hojas[h], pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(hojas)
            st.success("✅ Producto guardado correctamente.")

# Visualización
elif menu == "Catálogo":
    st.header("📦 Catálogo de Productos")
    df = hojas["Catálogo"]

    col1, col2 = st.columns(2)
    with col1:
        filtro = st.selectbox("Filtrar por Clasificación", ["TODOS"] + sorted(df["Clasificación"].dropna().unique()))
    with col2:
        busqueda = st.text_input("Buscar por marca o SKU").upper().strip()

    df_filtrado = df.copy()
    if filtro != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["Clasificación"] == filtro]
    if busqueda:
        df_filtrado = df_filtrado[
            df_filtrado["Marca"].str.contains(busqueda, case=False) |
            df_filtrado["SKU"].str.contains(busqueda, case=False)
        ]

    st.dataframe(df_filtrado, use_container_width=True)

# Edición
elif menu == "Editar":
    st.header("✏️ Editar Producto")
    df = hojas["Catálogo"]

    busqueda = st.text_input("Buscar por SKU").strip().upper()
    df_filtrado = df[df["SKU"] == busqueda] if busqueda else df.head(0)

    if not df_filtrado.empty:
        seleccionado = df_filtrado.iloc[0]
        idx = df[df["SKU"] == seleccionado["SKU"]].index[0]

        with st.form("editar_producto"):
            tipo_producto = st.text_input("Tipo de Producto", seleccionado["Tipo de Producto"])
            variante = st.text_input("Variante", seleccionado["Variante"])
            estado = st.radio("Estado", ["ACTIVO", "INACTIVO"], index=0 if seleccionado["Estado"] == "ACTIVO" else 1)

            guardar = st.form_submit_button("Actualizar")

            if guardar:
                df.at[idx, "Tipo de Producto"] = tipo_producto
                df.at[idx, "Variante"] = variante
                df.at[idx, "Estado"] = estado
                hojas["Catálogo"] = df
                guardar_datos(hojas)
                st.success("✅ Producto actualizado.")
    else:
        st.info("Busca un producto por SKU para editar.")

