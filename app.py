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
    html, body, [class*="css"] {
        font-family: "Times New Roman", Times, serif;
    }

    .stApp {
        background: linear-gradient(135deg, #EAF7FC 0%, #F7FAFC 45%, #EEF2F6 100%);
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1.2rem;
        max-width: 1180px;
    }

    section[data-testid="stSidebar"] {
        background-color: #EEF6FA;
        border-right: 1px solid #D5E4EC;
        box-shadow: 2px 0px 10px rgba(15, 23, 42, 0.05);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1F2937;
        font-weight: bold;
    }

    section[data-testid="stSidebar"] label {
        color: #334155;
        font-size: 14px;
    }

    .top-panel {
        background: rgba(255, 255, 255, 0.92);
        padding: 0.75rem 1rem;
        border-radius: 16px;
        border: 1px solid #D7E7EF;
        box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.08);
        margin-bottom: 0.9rem;
    }

    .header-title {
        font-size: 24px;
        font-weight: bold;
        color: #111827;
        margin-bottom: 2px;
        line-height: 1.15;
    }

    .header-subtitle {
        font-size: 14px;
        color: #475569;
        margin-top: 2px;
    }

    .main-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #D7E7EF;
        box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.07);
        margin-bottom: 0.9rem;
    }

    .metric-card {
        background: linear-gradient(180deg, #F8FCFE 0%, #EAF7FC 100%);
        padding: 0.75rem;
        border-radius: 14px;
        border: 1px solid #CFE3ED;
        text-align: center;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.06);
    }

    .metric-title {
        font-size: 12.5px;
        color: #64748B;
        margin-bottom: 4px;
    }

    .metric-value {
        font-size: 18px;
        font-weight: bold;
        color: #111827;
    }

    div[data-testid="stSelectbox"] {
        background-color: #FFFFFF;
        border-radius: 12px;
    }

    div[data-testid="stNumberInput"] input {
        background-color: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #CBDDE7;
        color: #111827;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 0.4rem;
        border: 1px solid #E2E8F0;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid #D7E7EF;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span {
        font-family: "Times New Roman", Times, serif !important;
    }

    h2 {
        font-size: 23px !important;
        color: #111827;
        font-weight: bold;
    }

    h3 {
        font-size: 18px !important;
        color: #1F2937;
        font-weight: bold;
    }

    .footer {
        text-align: center;
        color: #475569;
        font-size: 13px;
        padding-top: 0.6rem;
        padding-bottom: 0.2rem;
    }

    hr {
        border: none;
        border-top: 1px solid #D7E7EF;
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

st.markdown('<div class="top-panel">', unsafe_allow_html=True)

col_logo, col_title = st.columns([0.8, 5.2])

with col_logo:
    if logo is not None:
        st.image(logo, width=85)
    else:
        st.markdown("**TECSUP**")

with col_title:
    st.markdown(
        """
        <div class="header-title">
        Resolución de Ecuaciones Diferenciales Ordinarias
        </div>
        <div class="header-subtitle">
        Modelos matemáticos aplicados a procesos industriales
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
st.sidebar.markdown("Datos de entrada del modelo seleccionado.")


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

left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Desarrollo matemático")
    render_steps(steps)
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Gráfica del modelo")

    for _, fig in figures.items():
        fig.update_layout(
            height=430,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Times New Roman", size=13, color="#111827"),
            margin=dict(l=35, r=25, t=45, b=35),
        )
        fig.update_xaxes(showgrid=True, gridcolor="#E5EEF3")
        fig.update_yaxes(showgrid=True, gridcolor="#E5EEF3")
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
