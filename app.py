import streamlit as st
import pandas as pd
import os

ARCHIVO_EXCEL = "catalogo_productos.xlsx"

# Columnas base
COLUMNAS = [
    "Nombre del Producto", "Clasificación", "Tipo de Producto", "¿Posible vender en cantidad decimal?",
    "¿Controlarás el stock del producto?", "Estado", "Impuestos", "Variante", "¿permitirás ventas sin stock?",
    "Código de Barras", "SKU", "Marca", "Sucursales", "Fecha de creacion", "Estado Variante"
]

def cargar_datos():
    if os.path.exists(ARCHIVO_EXCEL):
        xls = pd.ExcelFile(ARCHIVO_EXCEL)
        st.write(f"Hojas encontradas en el archivo: {xls.sheet_names}")
        hojas = {}
        for hoja_nombre in ["Ingreso", "Catálogo", "Edición"]:
            if hoja_nombre in xls.sheet_names:
                df = xls.parse(hoja_nombre)
                # Validar columnas, si faltan agregar vacías
                for col in COLUMNAS:
                    if col not in df.columns:
                        df[col] = ""
                # Reordenar columnas para evitar problemas
                df = df[COLUMNAS]
                hojas[hoja_nombre] = df
            else:
                hojas[hoja_nombre] = pd.DataFrame(columns=COLUMNAS)
        return hojas
    else:
        hojas = {h: pd.DataFrame(columns=COLUMNAS) for h in ["Ingreso", "Catálogo", "Edición"]}
        guardar_datos(hojas)
        return hojas

def guardar_datos(hojas):
    with pd.ExcelWriter(ARCHIVO_EXCEL, engine="openpyxl", mode="w") as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre, index=False)

# Configuración de la app
st.set_page_config("🛒 Catálogo de Productos", layout="wide")
st.title("🛍️ Catálogo de Productos Supermercado")

# Cargar hojas
hojas = cargar_datos()

# Menú lateral
menu = st.sidebar.radio("Menú", ["Ingreso", "Catálogo", "Editar"])

# --- Ingreso de productos ---
if menu == "Ingreso":
    st.header("➕ Ingreso de Nuevo Producto")

    with st.form("form_ingreso"):
        marca = st.text_input("Marca").strip().upper()
        tipo_envase = st.selectbox("Tipo de envase", ["BOTELLÍN", "BOTELLA", "LATA", "PACK", "BARRIL", "CAJA", "SOBRE"])
        variante = st.text_input("Estilo / Variante").strip().upper()
        volumen = st.text_input("Volumen (ej: 330cc, 1L)").strip().upper()
        clasificacion = st.selectbox("Clasificación", sorted([
            "CERVEZA", "BEBIDA", "DESTILADO", "LICOR", "VINO", "MINI COCTEL", "AGUA", "ENERGÉTICA",
            "ABARROTES", "CHOCOLATE", "SNACK", "TABAQUERIA", "LÁCTEOS", "FIAMBRES", "CAFÉ"
        ]))
        tipo_producto = st.text_input("Tipo de producto (ej: IPA, TINTO, ENERGY)").strip().upper()
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

            for h in ["Ingreso", "Catálogo"]:
                hojas[h] = pd.concat([hojas[h], pd.DataFrame([nuevo])], ignore_index=True)

            guardar_datos(hojas)
            st.success("✅ Producto agregado correctamente.")

# --- Catálogo ---
elif menu == "Catálogo":
    st.header("📦 Catálogo de Productos")
    df = hojas["Catálogo"].copy()

    if df.empty:
        st.warning("⚠️ No hay productos cargados en el catálogo.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            filtro_categoria = st.selectbox("Filtrar por Clasificación", ["TODOS"] + sorted(df["Clasificación"].dropna().unique()))
        with col2:
            busqueda = st.text_input("🔍 Buscar por nombre o marca").strip().upper()

        df_filtrado = df.copy()
        if filtro_categoria != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["Clasificación"] == filtro_categoria]
        if busqueda:
            df_filtrado = df_filtrado[
                df_filtrado["Nombre del Producto"].str.upper().str.contains(busqueda) |
                df_filtrado["Marca"].str.upper().str.contains(busqueda)
            ]

        st.dataframe(df_filtrado, use_container_width=True)

# --- Edición ---
elif menu == "Editar":
    st.header("✏️ Editar Producto Existente")
    df = hojas["Catálogo"].copy()

    busqueda = st.text_input("🔎 Buscar por nombre")
    df_filtrado = df[df["Nombre del Producto"].str.contains(busqueda, case=False)] if busqueda else df

    if not df_filtrado.empty:
        seleccionado = st.selectbox("Selecciona un producto", df_filtrado["Nombre del Producto"].tolist())
        idx = df[df["Nombre del Producto"] == seleccionado].index[0]
        producto = df.loc[idx]

        with st.form("editar_producto"):
            marca = st.text_input("Marca", producto["Marca"])
            clasificacion = st.text_input("Clasificación", producto["Clasificación"])
            tipo = st.text_input("Tipo de Producto", producto["Tipo de Producto"])
            variante = st.text_input("Variante", producto["Variante"])
            estado = st.selectbox("Estado", ["ACTIVO", "INACTIVO"], index=0 if producto["Estado"] == "ACTIVO" else 1)

            guardar = st.form_submit_button("Actualizar")

            if guardar:
                df.at[idx, "Marca"] = marca.strip().upper()
                df.at[idx, "Clasificación"] = clasificacion.strip().upper()
                df.at[idx, "Tipo de Producto"] = tipo.strip().upper()
                df.at[idx, "Variante"] = variante.strip().upper()
                df.at[idx, "Estado"] = estado
                hojas["Catálogo"] = df
                guardar_datos(hojas)
                st.success("✅ Producto actualizado.")
    else:
        st.warning("No se encontraron productos con ese nombre.")


