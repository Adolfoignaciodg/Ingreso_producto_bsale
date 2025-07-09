import streamlit as st
import pandas as pd
import os

ARCHIVO_EXCEL = "catalogo_productos.xlsx"

# Función para cargar o crear archivo Excel con hojas
def cargar_datos():
    if os.path.exists(ARCHIVO_EXCEL):
        xls = pd.ExcelFile(ARCHIVO_EXCEL)
        hojas = {hoja: xls.parse(hoja) for hoja in xls.sheet_names}
    else:
        # Crear estructura vacía si no existe
        columnas = [
            "Nombre del Producto", "Clasificación", "Tipo de Producto", "¿Posible vender en cantidad decimal?",
            "¿Controlarás el stock del producto?", "Estado", "Impuestos", "Variante", "¿permitirás ventas sin stock?",
            "Código de Barras", "SKU", "Marca", "Sucursales", "Fecha de creacion", "Estado Variante"
        ]
        hojas = {
            "Ingreso": pd.DataFrame(columns=columnas),
            "Catálogo": pd.DataFrame(columns=columnas),
            "Edición": pd.DataFrame(columns=columnas)
        }
        guardar_datos(hojas)
    return hojas

def guardar_datos(hojas):
    with pd.ExcelWriter(ARCHIVO_EXCEL, engine='openpyxl', mode='w') as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre, index=False)

# --- App Streamlit ---
st.set_page_config("🛒 Catálogo de Productos", layout="wide")
st.title("🛍️ Catálogo de Productos Supermercado")

# Cargar los datos del archivo
hojas = cargar_datos()

# Menú de navegación
menu = st.sidebar.radio("Menú", ["Ingreso", "Catálogo", "Editar"])

# --- Pestaña Ingreso ---
if menu == "Ingreso":
    st.header("➕ Ingreso de Nuevo Producto")
    
    with st.form("form_ingreso"):
        marca = st.text_input("Marca", "").strip().upper()
        tipo_envase = st.selectbox("Tipo de envase", ["BOTELLÍN", "BOTELLA", "LATA", "PACK", "BARRIL", "CAJA", "SOBRE"])
        variante = st.text_input("Estilo / Variante", "").strip().upper()
        volumen = st.text_input("Volumen (ej: 330cc, 1L)", "").strip().upper()
        clasificacion = st.selectbox("Clasificación", sorted([
            "CERVEZA", "BEBIDA", "DESTILADO", "LICOR", "VINO", "MINI COCTEL", "AGUA", "ENERGÉTICA", "ABARROTES",
            "CHOCOLATE", "SNACK", "TABAQUERIA", "LÁCTEOS", "FIAMBRES", "CAFÉ"
        ]))
        tipo_producto = st.text_input("Tipo de producto (ej: IPA, LAGER, TINTO)", "").strip().upper()
        codigo_barras = st.text_input("Código de barras (opcional)").strip()
        sku = st.text_input("SKU (opcional)").strip().upper()
        
        nombre_producto = f"{marca.title()} {tipo_envase.title()} {variante.title()} {volumen}".strip()
        
        submit = st.form_submit_button("Guardar")

        if submit:
            nuevo = {
                "Nombre del Producto": nombre_producto,
                "Clasificación": clasificacion,
                "Tipo de Producto": tipo_producto,
                "¿Posible vender en cantidad decimal?": "NO",
                "¿Controlarás el stock del producto?": "SÍ",
                "Estado": "ACTIVO",
                "Impuestos": "IVA",
                "Variante": variante,
                "¿permitirás ventas sin stock?": "NO",
                "Código de Barras": codigo_barras,
                "SKU": sku,
                "Marca": marca,
                "Sucursales": "PRINCIPAL",
                "Fecha de creacion": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "Estado Variante": "ACTIVO"
            }

            hojas["Ingreso"] = pd.concat([hojas["Ingreso"], pd.DataFrame([nuevo])], ignore_index=True)
            hojas["Catálogo"] = pd.concat([hojas["Catálogo"], pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(hojas)
            st.success("✅ Producto agregado correctamente.")

# --- Pestaña Catálogo ---
elif menu == "Catálogo":
    st.header("📦 Catálogo de Productos")
    df = hojas["Catálogo"]

    col1, col2 = st.columns(2)
    with col1:
        filtro_categoria = st.selectbox("Filtrar por Clasificación", ["TODOS"] + sorted(df["Clasificación"].dropna().unique()))
    with col2:
        busqueda = st.text_input("🔍 Buscar por nombre de producto o marca").upper()

    df_filtrado = df.copy()
    if filtro_categoria != "TODOS":
        df_filtrado = df_filtrado[df_filtrado["Clasificación"] == filtro_categoria]
    if busqueda:
        df_filtrado = df_filtrado[
            df_filtrado["Nombre del Producto"].str.upper().str.contains(busqueda) |
            df_filtrado["Marca"].str.upper().str.contains(busqueda)
        ]

    st.dataframe(df_filtrado, use_container_width=True)

# --- Pestaña Edición ---
elif menu == "Editar":
    st.header("✏️ Editar Catálogo")
    df = hojas["Catálogo"].copy()

    producto_buscar = st.text_input("🔎 Buscar producto por nombre")
    df_filtrado = df[df["Nombre del Producto"].str.contains(producto_buscar, case=False)] if producto_buscar else df

    if not df_filtrado.empty:
        index_edit = st.selectbox("Selecciona el producto a editar", df_filtrado["Nombre del Producto"].tolist())
        idx = df[df["Nombre del Producto"] == index_edit].index[0]
        producto = df.loc[idx]

        with st.form("editar_producto"):
            marca = st.text_input("Marca", producto["Marca"])
            clasificacion = st.text_input("Clasificación", producto["Clasificación"])
            tipo = st.text_input("Tipo de Producto", producto["Tipo de Producto"])
            variante = st.text_input("Variante", producto["Variante"])
            estado = st.selectbox("Estado", ["ACTIVO", "INACTIVO"], index=["ACTIVO", "INACTIVO"].index(producto["Estado"]))

            guardar = st.form_submit_button("Actualizar")

            if guardar:
                df.at[idx, "Marca"] = marca
                df.at[idx, "Clasificación"] = clasificacion
                df.at[idx, "Tipo de Producto"] = tipo
                df.at[idx, "Variante"] = variante
                df.at[idx, "Estado"] = estado
                hojas["Catálogo"] = df
                guardar_datos(hojas)
                st.success("✅ Producto actualizado.")

    else:
        st.warning("No se encontraron coincidencias.")

