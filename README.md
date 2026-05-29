TFM-2026-G4 · Modelo Predictivo para Recubrimientos Protectores
> **Asignatura 5 — Fuentes y Obtención de Datos**  
> Máster en Big Data & Business Intelligence · Online Feb 26/27  
> Equipo: Esteban Sanchez Huertas · Ana Contreras Benavides · Alan Santiago García Rodríguez · Javier Enoc Ramírez Zamarripa · Grupo 04
---
Descripción
Este proyecto desarrolla un modelo predictivo basado en datos ambientales para apoyar la toma de decisiones técnicas en la selección, aplicación y mantenimiento de recubrimientos protectores industriales.
Los datos meteorológicos se obtienen a través de la API de Open-Meteo, extrayendo variables como temperatura, humedad relativa, punto de rocío, radiación solar y precipitación, con el objetivo de identificar condiciones óptimas y de riesgo para la aplicación de recubrimientos.
---
Estructura del repositorio
```
TFM-2026-G4/
│
├── datos/                          # Datos extraídos de la API
│   ├── datos_diarios.csv           # 30 registros diarios
│   └── variables_por_hora.csv      # 720 registros horarios
│
├── api_weatherOpenM.ipynb          # Extracción, limpieza y EDA
├── requirements.txt                # Dependencias del proyecto
└── README.md
```
---
Fuente de datos
Fuente	Tipo	Variables principales
Open-Meteo API	API REST (abierta)	Temperatura, humedad relativa, punto de rocío, precipitación, radiación solar, velocidad del viento, índice UV
---
Requisitos
Python 3.10 o superior
Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/JaviercloudGR14/TFM-2026-G4.git
cd TFM-2026-G4

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el notebook
jupyter lab api_weatherOpenM.ipynb
```
Para lanzar la aplicación Streamlit:
```bash
streamlit run app.py
```
---
Variables extraídas
Diarias: temperatura máxima y mínima, duración de luz solar, índice UV, precipitación y lluvia acumulada.
Por hora: temperatura, humedad relativa, probabilidad de precipitación, velocidad y dirección del viento, punto de rocío, radiación solar, lluvia y chubascos.
---
Hallazgos del EDA
558 horas con condiciones óptimas para aplicación (77.5% del período)
74 horas con humedad superior al 85% → riesgo alto de adhesión deficiente
82 horas con diferencia temperatura–punto de rocío < 3°C → riesgo de condensación
Índice UV promedio de 9.30 (clasificado como muy alto en 25 de 30 días)
---
Equipo
Nombre	Responsabilidad
Alan Santiago García Rodríguez	Obtención de datos
Esteban Sanchez Huertas	Eliminación de duplicados
Javier Enoc Ramírez Zamarripa	Tratamiento de valores faltantes y EDA
Ana Contreras Benavides	Estandarización de formatos y Streamlit
---
Máster
Big Data & Business Intelligence · Online Feb 26/27 · 2025–2026
