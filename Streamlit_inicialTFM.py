import streamlit as st
import pandas as pd
import requests


# CONFIGURACIÓN DE PÁGINA

st.set_page_config(
    page_title="Modelo Predictivo de Recubrimientos",
    layout="wide"
)

st.title("Modelo Predictivo para Recubrimientos Protectores")
st.write("Sistema de apoyo para decisiones técnicas basado en datos ambientales")

# INICIO

if "temperatura" not in st.session_state:
    st.session_state.temperatura = None

if "humedad" not in st.session_state:
    st.session_state.humedad = None

if "lluvia" not in st.session_state:
    st.session_state.lluvia = None
    
if "datos_cargados" not in st.session_state:
    st.session_state.datos_cargados = False

# NUEVA CONSULTA

if st.button("🔄 Nueva consulta"):

    st.session_state.temperatura = None
    st.session_state.humedad = None
    st.session_state.lluvia = None
    st.session_state.datos_cargados = False

    st.rerun()

st.divider()

# SELECCIÓN DE FUENTE DE DATOS

modo = st.radio(
    "Seleccione fuente de datos:",
    [
        "Ingresar manualmente",
        "Consultar API",
        "Pronóstico específico",
        "Pronóstico general (16 días)"
    ]
)

# OPCIÓN 1: INGRESO MANUAL

if modo == "Ingresar manualmente":

    st.subheader("Ingreso manual de condiciones ambientales")

    col1, col2, col3 = st.columns(3)

    with col1:
        temp = st.number_input(
            "Temperatura (°C)",
            value=None,
            placeholder="Ej: 28"
        )

    with col2:
        hum = st.number_input(
            "Humedad Relativa (%)",
            value=None,
            placeholder="Ej: 85"
        )

    with col3:
        llu = st.number_input(
            "Precipitación (mm)",
            value=None,
            placeholder="Ej: 3"
        )

    if st.button("Guardar datos manuales"):

        if None in [temp, hum, llu]:
            st.warning("Debe completar todos los campos.")
            st.stop()

        st.session_state.temperatura = temp
        st.session_state.humedad = hum
        st.session_state.lluvia = llu
        st.session_state.datos_cargados = True

        st.success("Datos guardados correctamente")

    
# OPCIÓN 2: CONSULTAR API 
# ===================================

if modo == "Consultar API":

    st.subheader("Consulta automática desde Open Meteo")

    col1, col2 = st.columns(2)

    with col1:
        lat = st.number_input(
            "Latitud",
            value=None,
            placeholder="Ej: 9.93"
        )

    with col2:
        lon = st.number_input(
            "Longitud",
            value=None,
            placeholder="Ej: -84.08"
        )

    if st.button("Consultar API"):

        if lat is None or lon is None:
            st.warning("Debe ingresar latitud y longitud")
            st.stop()

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}"
                f"&longitude={lon}"
                f"&current=temperature_2m,"
                f"relative_humidity_2m,"
                f"precipitation"
            )

            response = requests.get(url)
            data = response.json()

# Guardar en session_state
            st.session_state.temperatura = data["current"]["temperature_2m"]
            st.session_state.humedad = data["current"]["relative_humidity_2m"]
            st.session_state.lluvia = data["current"]["precipitation"]

            st.session_state.datos_cargados = True
            st.success("Datos obtenidos correctamente desde Open-Meteo")

        except:
            st.error("Error al consultar la API")

# OPCIÓN 3: PRONÓSTICO ESPECÍFICO

if modo == "Pronóstico específico":

    st.subheader("Consulta de pronóstico por fecha y hora")

    col1, col2 = st.columns(2)

    with col1:
        lat_f = st.number_input(
            "Latitud",
            value=None,
            key="lat_f"
        )

    with col2:
        lon_f = st.number_input(
            "Longitud",
            value=None,
            key="lon_f"
        )

    fecha = st.date_input("Seleccione fecha")
    hora = st.selectbox("Seleccione hora", range(24))

    if st.button("Consultar pronóstico"):

        if lat_f is None or lon_f is None:
            st.warning("Debe ingresar latitud y longitud")
            st.stop()

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat_f}"
                f"&longitude={lon_f}"
                f"&hourly=temperature_2m,"
                f"relative_humidity_2m,"
                f"precipitation"
                f"&start_date={fecha}"
                f"&end_date={fecha}"
            )

            response = requests.get(url)
            data = response.json()

            idx = hora

            st.session_state.temperatura = data["hourly"]["temperature_2m"][idx]
            st.session_state.humedad = data["hourly"]["relative_humidity_2m"][idx]
            st.session_state.lluvia = data["hourly"]["precipitation"][idx]

            st.session_state.datos_cargados = True

            st.success("Pronóstico cargado correctamente")

        except:
            st.error("Error al consultar el pronóstico")

# OPCIÓN 4: PRONÓSTICO GENERAL
# ===================================

if modo == "Pronóstico general (16 días)":

    st.subheader("Pronóstico general de 16 días")

    col1, col2 = st.columns(2)

    with col1:
        lat_16 = st.number_input(
            "Latitud",
            value=None,
            key="lat16"
        )

    with col2:
        lon_16 = st.number_input(
            "Longitud",
            value=None,
            key="lon16"
        )

    if st.button("Consultar 16 días"):

        if lat_16 is None or lon_16 is None:
            st.warning("Debe ingresar latitud y longitud")
            st.stop()

        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat_16}"
                f"&longitude={lon_16}"
                f"&daily=temperature_2m_max,"
                f"temperature_2m_min,"
                f"precipitation_sum"
                f"&forecast_days=16"
            )

            response = requests.get(url)
            data = response.json()

            df_16 = pd.DataFrame({
                "Fecha": data["daily"]["time"],
                "Temp Max": data["daily"]["temperature_2m_max"],
                "Temp Min": data["daily"]["temperature_2m_min"],
                "Precipitación": data["daily"]["precipitation_sum"]
            })

            # -------------------------
            # Calcular riesgo diario
            # -------------------------
            riesgos = []
            recomendaciones = []

            for _, row in df_16.iterrows():

                # lógica simplificada
                if row["Precipitación"] > 2:
                    riesgo = "ALTO"
                    recomendacion = "No aplicar recubrimiento"

                elif row["Precipitación"] > 0:
                    riesgo = "MEDIO"
                    recomendacion = "Aplicar con monitoreo"

                else:
                    riesgo = "BAJO"
                    recomendacion = "Condición apta"

                riesgos.append(riesgo)
                recomendaciones.append(recomendacion)

            df_16["Riesgo"] = riesgos
            df_16["Recomendación"] = recomendaciones

            st.success("Pronóstico cargado")

            st.subheader("Evaluación de riesgo - próximos 16 días")
            st.dataframe(
                df_16,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Tendencia de temperatura")
            st.line_chart(
                df_16.set_index("Fecha")[["Temp Max", "Temp Min"]]
            )

        except:
            st.error("Error al consultar pronóstico")


# MOSTRAR DATOS CARGADOS

if (
    st.session_state.datos_cargados
    and modo != "Pronóstico general (16 días)"
):

    st.subheader("Datos cargados")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Temperatura",
            f"{st.session_state.temperatura} °C"
        )

    with col2:
        st.metric(
            "Humedad",
            f"{st.session_state.humedad} %"
        )

    with col3:
        st.metric(
            "Lluvia",
            f"{st.session_state.lluvia} mm"
        )

st.divider()


# EVALUACIÓN DEL RIESGO

if modo != "Pronóstico general (16 días)":

    st.divider()

    if st.button("Evaluar Riesgo"):

        # Validar datos
        if (
            not st.session_state.datos_cargados
            or st.session_state.temperatura is None
            or st.session_state.humedad is None
            or st.session_state.lluvia is None
        ):
            st.warning("Primero debe ingresar o consultar los datos.")
            st.stop()

        # Lógica del modelo
        if (
            st.session_state.humedad > 85
            or st.session_state.lluvia > 2
        ):
            riesgo = "ALTO"
            recomendacion = "No aplicar recubrimiento"

        elif st.session_state.humedad > 70:
            riesgo = "MEDIO"
            recomendacion = "Aplicar con monitoreo continuo"

        else:
            riesgo = "BAJO"
            recomendacion = "Condición apta para aplicación"

        # Mostrar resultados
        st.subheader("Resultado del Modelo")

        if riesgo == "ALTO":
            st.error(f"Nivel de riesgo: {riesgo}")

        elif riesgo == "MEDIO":
            st.warning(f"Nivel de riesgo: {riesgo}")

        else:
            st.success(f"Nivel de riesgo: {riesgo}")

        st.info(recomendacion)

        # Tabla resumen
        df = pd.DataFrame({
            "Variable": [
                "Temperatura",
                "Humedad",
                "Precipitación",
                "Nivel de Riesgo",
                "Recomendación"
            ],
            "Valor": [
                st.session_state.temperatura,
                st.session_state.humedad,
                st.session_state.lluvia,
                riesgo,
                recomendacion
            ]
        })

        st.subheader("Resumen de variables")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )