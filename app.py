# app.py

import streamlit as st
from PIL import Image
import solver


st.set_page_config(
    page_title="Resolución de Ecuaciones Diferenciales Ordinarias",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #F4FAFD;
    }

    section[data-testid="stSidebar"] {
        background-color: #DFF4FC;
    }

    .header-box {
        background-color: #00A3E0;
        padding: 1.2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1rem;
    }

    .header-title {
        font-size: 32px;
        font-weight: 800;
        color: white;
        margin-bottom: 0px;
    }

    .header-subtitle {
        font-size: 16px;
        color: white;
        margin-top: 4px;
    }

    .main-card {
        background-color: white;
        padding: 1.3rem;
        border-radius: 14px;
        border: 1px solid #CDEAF5;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .metric-card {
        background-color: #E9F8FD;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #BEE8F7;
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #475569;
    }

    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #0F172A;
    }

    .footer {
        text-align: center;
        color: #475569;
        font-size: 14px;
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def render_steps(steps):
    for item in steps:
        clean = str(item).strip()
        if clean.startswith("$$") and clean.endswith("$$"):
            st.latex(clean.replace("$$", ""))
        else:
            st.markdown(clean)


def load_logo():
    try:
        return Image.open("logjitodetecsup.png")
    except Exception:
        return None


def case_name(case_id):
    names = {
        1: "Caso 1 - Enfriamiento de Newton",
        2: "Caso 2 - Vaciado de tanque cilíndrico",
        3: "Caso 3 - Mezcla de desengrasante",
        4: "Caso 4 - Actuador hidráulico",
        5: "Caso 5 - Tanque cónico",
    }
    return names[case_id]


def result_summary(case_id, values):
    if case_id == 1:
        return [
            ("T inicial", f"{values['T0']:.2f} °C"),
            ("T objetivo", f"{values['T_obj']:.2f} °C"),
            ("Tiempo medición", f"{values['t1']:.2f} min"),
        ]

    if case_id == 2:
        return [
            ("Radio", f"{values['r']:.2f} m"),
            ("Altura inicial", f"{values['h0']:.2f} m"),
            ("Orificio", f"{values['a']:.6f} m²"),
        ]

    if case_id == 3:
        return [
            ("Volumen", f"{values['V']:.2f} L"),
            ("Concentración", f"{values['cin']:.2f} kg/L"),
            ("Tiempo", f"{values['t_target']:.2f} min"),
        ]

    if case_id == 4:
        return [
            ("Tiempo prueba", f"{values['t_test']:.2f} s"),
            ("Posición", f"{values['y_test']:.2f} cm"),
            ("Tau ideal", f"{values['tau_ideal']:.2f} s"),
        ]

    return [
        ("Altura cono", f"{values['H']:.2f} m"),
        ("Radio superior", f"{values['R_top']:.2f} m"),
        ("Altura inicial", f"{values['h0']:.2f} m"),
    ]


logo = load_logo()

st.markdown('<div class="header-box">', unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 5])

with col_logo:
    if logo is not None:
        st.image(logo, width=140)
    else:
        st.markdown("TECSUP")

with col_title:
    st.markdown(
        """
        <div class="header-title">
        Resolución de Ecuaciones Diferenciales Ordinarias
        </div>
        <div class="header-subtitle">
        Aplicación interactiva para modelos industriales con desarrollo matemático, gráfica e interpretación técnica.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="main-card">', unsafe_allow_html=True)

selected_case = st.selectbox(
    "Selecciona manualmente el caso a resolver:",
    options=[1, 2, 3, 4, 5],
    format_func=case_name
)

st.markdown("</div>", unsafe_allow_html=True)


st.sidebar.title("Parámetros")
st.sidebar.write("Modifica los datos del caso seleccionado.")


values = {}

if selected_case == 1:
    st.sidebar.subheader("Caso 1")
    values["T0"] = st.sidebar.number_input("Temperatura inicial T0 (°C)", value=150.0)
    values["Ta"] = st.sidebar.number_input("Temperatura ambiente Ta (°C)", value=25.0)
    values["T1"] = st.sidebar.number_input("Temperatura medida T1 (°C)", value=100.0)
    values["t1"] = st.sidebar.number_input("Tiempo de medición t1 (min)", value=10.0, min_value=0.01)
    values["T_obj"] = st.sidebar.number_input("Temperatura objetivo (°C)", value=40.0)

    steps, figures, interpretation = solver.solve_case_1(**values)

elif selected_case == 2:
    st.sidebar.subheader("Caso 2")
    values["r"] = st.sidebar.number_input("Radio del tanque r (m)", value=1.0, min_value=0.01)
    values["h0"] = st.sidebar.number_input("Altura inicial h0 (m)", value=4.0, min_value=0.01)
    values["a"] = st.sidebar.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
    values["C_factor"] = st.sidebar.number_input("Coeficiente C", value=0.6, min_value=0.01)
    values["g"] = st.sidebar.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_2(**values)

elif selected_case == 3:
    st.sidebar.subheader("Caso 3")
    values["V"] = st.sidebar.number_input("Volumen V (L)", value=500.0, min_value=0.01)
    values["Q0"] = st.sidebar.number_input("Cantidad inicial Q0 (kg)", value=0.0)
    values["cin"] = st.sidebar.number_input("Concentración entrada cin (kg/L)", value=0.2, min_value=0.0)
    values["rin"] = st.sidebar.number_input("Caudal entrada rin (L/min)", value=5.0, min_value=0.01)
    values["rout"] = st.sidebar.number_input("Caudal salida rout (L/min)", value=5.0, min_value=0.01)
    values["t_target"] = st.sidebar.number_input("Tiempo a evaluar (min)", value=60.0, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_3(**values)

elif selected_case == 4:
    st.sidebar.subheader("Caso 4")
    values["t_test"] = st.sidebar.number_input("Tiempo de prueba (s)", value=8.0, min_value=0.01)
    values["y_test"] = st.sidebar.number_input("Posición medida y (cm)", value=6.32, min_value=0.01)
    values["tau_ideal"] = st.sidebar.number_input("Tau ideal (s)", value=4.0, min_value=0.01)
    values["recorrido"] = st.sidebar.number_input("Recorrido máximo (cm)", value=10.0, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_4(**values)

else:
    st.sidebar.subheader("Caso 5")
    values["H"] = st.sidebar.number_input("Altura total H (m)", value=2.0, min_value=0.01)
    values["R_top"] = st.sidebar.number_input("Radio superior R (m)", value=0.5, min_value=0.01)
    values["h0"] = st.sidebar.number_input("Altura inicial h0 (m)", value=2.0, min_value=0.01)
    values["a"] = st.sidebar.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
    values["C_factor"] = st.sidebar.number_input("Coeficiente C", value=0.6, min_value=0.01)
    values["g"] = st.sidebar.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_5(**values)


st.markdown("## Panel de resultados")

summary_cols = st.columns(3)

for col, item in zip(summary_cols, result_summary(selected_case, values)):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{item[0]}</div>
                <div class="metric-value">{item[1]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

left_col, right_col = st.columns([1, 1.25])

with left_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Desarrollo matemático paso a paso")
    render_steps(steps)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Gráfica del modelo")

    for _, fig in figures.items():
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretación técnica")
    st.info(interpretation)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer">
        Usuario: Jenifer U.
    </div>
    """,
    unsafe_allow_html=True
)
