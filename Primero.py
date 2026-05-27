
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Portal de Aprobaciones", layout="wide")

# -------------------------
# DATOS DE PRUEBA
# -------------------------
if "documentos" not in st.session_state:
    st.session_state.documentos = [
        {
            "numero": "OC-2025-001",
            "empresa": "Codegasco",
            "tipo": "Orden de Compra",
            "estado": "Pendiente Filtro 1",
            "responsable": "Sebastián Pinzón",
            "fecha_creacion": datetime(2025, 5, 20, 8, 30),
            "fecha_actualizacion": datetime(2025, 5, 20, 8, 30),
            "observacion": "Compra de herramientas"
        },
        {
            "numero": "REQ-2025-002",
            "empresa": "Transpcargas",
            "tipo": "Requisición",
            "estado": "Pendiente Filtro 2",
            "responsable": "Yhon Pinzón",
            "fecha_creacion": datetime(2025, 5, 21, 10, 0),
            "fecha_actualizacion": datetime(2025, 5, 21, 12, 0),
            "observacion": "Servicio de mantenimiento"
        }
    ]

# -------------------------
# ENCABEZADO
# -------------------------
st.title("🚀 Portal Empresarial de Aprobaciones")
st.caption("Codegasco / Transpcargas — Órdenes de Compra y Requisiciones")

menu = st.sidebar.radio(
    "Menú",
    ["Dashboard", "Nueva solicitud", "Aprobaciones", "Base de datos"]
)

usuario = st.sidebar.selectbox(
    "Usuario actual",
    ["Solicitante", "Sebastián Pinzón", "Yhon Pinzón", "Adriana Porras"]
)

# -------------------------
# DASHBOARD
# -------------------------
if menu == "Dashboard":
    docs = st.session_state.documentos

    total = len(docs)
    proceso = len([d for d in docs if "Pendiente" in d["estado"]])
    aprobados = len([d for d in docs if d["estado"] == "Aprobado Final"])
    rechazados = len([d for d in docs if d["estado"] == "Rechazado"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total documentos", total)
    col2.metric("En proceso", proceso)
    col3.metric("Aprobados", aprobados)
    col4.metric("Rechazados", rechazados)

    st.subheader("📌 Seguimiento actual")

    df = pd.DataFrame(docs)
    st.dataframe(df, use_container_width=True)

# -------------------------
# NUEVA SOLICITUD
# -------------------------
elif menu == "Nueva solicitud":
    st.subheader("➕ Crear nueva solicitud")

    with st.form("form_solicitud"):
        empresa = st.selectbox("Empresa", ["Codegasco", "Transpcargas"])
        tipo = st.selectbox("Tipo de documento", ["Orden de Compra", "Requisición"])
        numero = st.text_input("Número de documento")
        observacion = st.text_area("Observaciones")
        pdf = st.file_uploader("Cargar PDF", type=["pdf"])

        enviar = st.form_submit_button("Enviar a Filtro 1")

        if enviar:
            nuevo = {
                "numero": numero,
                "empresa": empresa,
                "tipo": tipo,
                "estado": "Pendiente Filtro 1",
                "responsable": "Sebastián Pinzón",
                "fecha_creacion": datetime.now(),
                "fecha_actualizacion": datetime.now(),
                "observacion": observacion
            }

            st.session_state.documentos.append(nuevo)
            st.success("Solicitud creada y enviada a Sebastián Pinzón.")

# -------------------------
# APROBACIONES
# -------------------------
elif menu == "Aprobaciones":
    st.subheader("✅ Mis aprobaciones pendientes")

    pendientes = [
        d for d in st.session_state.documentos
        if d["responsable"] == usuario and "Pendiente" in d["estado"]
    ]

    if not pendientes:
        st.info("No tienes documentos pendientes.")
    else:
        for doc in pendientes:
            with st.expander(f"{doc['numero']} - {doc['tipo']}"):
                st.write(f"**Empresa:** {doc['empresa']}")
                st.write(f"**Estado actual:** {doc['estado']}")
                st.write(f"**Observación:** {doc['observacion']}")
                st.write(f"**Fecha creación:** {doc['fecha_creacion']}")

                col1, col2 = st.columns(2)

                if col1.button(f"Aprobar {doc['numero']}"):
                    if usuario == "Sebastián Pinzón":
                        doc["estado"] = "Pendiente Filtro 2"
                        doc["responsable"] = "Yhon Pinzón"

                    elif usuario == "Yhon Pinzón":
                        doc["estado"] = "Pendiente Filtro 3"
                        doc["responsable"] = "Adriana Porras"

                    elif usuario == "Adriana Porras":
                        doc["estado"] = "Aprobado Final"
                        doc["responsable"] = "Finalizado"

                    doc["fecha_actualizacion"] = datetime.now()
                    st.success("Documento aprobado correctamente.")
                    st.rerun()

                if col2.button(f"Rechazar {doc['numero']}"):
                    doc["estado"] = "Rechazado"
                    doc["responsable"] = "Finalizado"
                    doc["fecha_actualizacion"] = datetime.now()
                    st.error("Documento rechazado.")
                    st.rerun()

# -------------------------
# BASE DE DATOS
# -------------------------
elif menu == "Base de datos":
    st.subheader("🗄️ Base de datos de solicitudes")

    df = pd.DataFrame(st.session_state.documentos)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Descargar Excel",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="base_aprobaciones.csv",
        mime="text/csv"
    )










