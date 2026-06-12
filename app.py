# app.py

import re
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
        font-family: "Times New Roman", Times, serif !important;
        color: #111111 !important;
    }

    .stApp {
        background-color: #00A3E0;
    }

    .block-container {
        padding-top: 0.55rem !important;
        padding-bottom: 0.35rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        max-width: 1220px !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #EAF3F8 !important;
        border-right: 1px solid #D8E1E8;
        box-shadow: 2px 0px 10px rgba(0, 0, 0, 0.06);
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
        color: #111111 !important;
        margin-bottom: 0.25rem !important;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-size: 15px !important;
        color: #111111 !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.2rem !important;
    }

    section[data-testid="stSidebar"] label {
        font-size: 12.5px !important;
        color: #111111 !important;
        margin-bottom: 0px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
        margin-bottom: -0.55rem !important;
    }

    section[data-testid="stSidebar"] input {
        height: 29px !important;
        font-size: 12.5px !important;
        border-radius: 8px !important;
        border: 1px solid #D8E1E8 !important;
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }

    div[data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #D8E1E8 !important;
        border-radius: 16px !important;
        box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.06);
        margin-bottom: 0.45rem !important;
    }

    div[data-testid="stExpander"] summary {
        font-size: 13px !important;
        font-weight: bold !important;
        color: #111111 !important;
    }

    .header-card {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.10);
        padding: 0.45rem 0.75rem;
        height: 78px;
        margin-bottom: 0.55rem;
        display: flex;
        align-items: center;
    }

    .title-text {
        font-size: 23px;
        font-weight: bold;
        color: #111111;
        line-height: 1.05;
        margin: 0px;
        text-align: left;
    }

    .subtitle-text {
        font-size: 13.5px;
        color: #333333;
        margin-top: 2px;
        line-height: 1.05;
        text-align: left;
    }

    .white-card {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.10);
        padding: 0.75rem;
        margin-bottom: 0.6rem;
    }

    .compact-card {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.10);
        padding: 0.6rem 0.75rem;
        margin-bottom: 0.55rem;
    }

    .section-title {
        font-size: 20px;
        font-weight: bold;
        color: #111111;
        margin-bottom: 0.4rem;
        line-height: 1.1;
    }

    .kpi-card {
        background-color: #F5FAFD;
        border: 1px solid #D8E1E8;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.05);
        padding: 0.45rem 0.5rem;
        min-height: 58px;
        text-align: center;
    }

    .kpi-title {
        font-size: 12px;
        color: #444444;
        margin-bottom: 2px;
        line-height: 1.05;
    }

    .kpi-value {
        font-size: 19px;
        color: #111111;
        font-weight: bold;
        line-height: 1.1;
    }

    .mini-list {
        font-size: 14px;
        color: #111111;
        margin-top: -0.15rem;
    }

    .mini-list ul {
        margin-top: 0.15rem;
        margin-bottom: 0rem;
        padding-left: 1.1rem;
    }

    .mini-list li {
        margin-bottom: 0.15rem;
        line-height: 1.15;
    }

    div[data-testid="stSelectbox"] label {
        font-size: 14px !important;
        font-weight: bold !important;
        color: #111111 !important;
    }

    div[data-testid="stSelectbox"] {
        margin-bottom: -0.35rem !important;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #D8E1E8;
        padding: 0.15rem;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stAlert"] {
        padding: 0.45rem 0.6rem !important;
        border-radius: 12px !important;
        border: 1px solid #D8E1E8 !important;
        font-size: 13px !important;
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span {
        font-family: "Times New Roman", Times, serif !important;
        color: #111111;
    }

    h2 {
        font-size: 20px !important;
        margin-top: 0rem !important;
        margin-bottom: 0.35rem !important;
    }

    h3 {
        font-size: 16px !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.15rem !important;
    }

    p {
        font-size: 14px !important;
        margin-bottom: 0.25rem !important;
        line-height: 1.2 !important;
    }

    .stMarkdown {
        margin-bottom: 0.08rem !important;
    }

    .katex {
        font-size: 0.86em !important;
    }

    .math-scroll {
        max-height: 245px;
        overflow-y: auto;
        padding-right: 0.35rem;
    }

    .footer {
        text-align: center;
        color: #FFFFFF;
        font-size: 13px;
        margin-top: 0.1rem;
        padding-bottom: 0rem;
    }

    hr {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
        border-top: 1px solid #D8E1E8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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


def render_steps_compact(steps):
    for item in steps:
        clean = str(item).strip()

        if clean.startswith("###"):
            st.markdown(f"**{clean.replace('###', '').strip()}**")
        elif clean.startswith("$$") and clean.endswith("$$"):
            st.latex(clean.replace("$$", ""))
        else:
            st.markdown(clean)


def split_interpretation(text):
    parts = re.split(r"(?<=[.!?])\\s+", text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) == 0:
        return ["No se generó interpretación."]
    return parts[:3]


def make_result_kpis(case_id, values, interpretation):
    nums = re.findall(r"-?\\d+(?:\\.\\d+)?", interpretation)

    if case_id == 1:
        return [
            ("T inicial", f"{values['T0']:.1f} °C"),
            ("T objetivo", f"{values['T_obj']:.1f} °C"),
            ("Espera adicional", f"{nums[3] if len(nums) > 3 else '---'} min"),
        ]

    if case_id == 2:
        return [
            ("Radio", f"{values['r']:.2f} m"),
            ("Altura inicial", f"{values['h0']:.2f} m"),
            ("Vaciado", f"{nums[0] if len(nums) > 0 else '---'} min"),
        ]

    if case_id == 3:
        return [
            ("Volumen", f"{values['V']:.0f} L"),
            ("Tiempo", f"{values['t_target']:.0f} min"),
            ("Cantidad final", f"{nums[1] if len(nums) > 1 else '---'} kg"),
        ]

    if case_id == 4:
        return [
            ("Tiempo prueba", f"{values['t_test']:.1f} s"),
            ("Posición", f"{values['y_test']:.2f} cm"),
            ("Tau ideal", f"{values['tau_ideal']:.1f} s"),
        ]

    return [
        ("Altura cono", f"{values['H']:.2f} m"),
        ("Radio superior", f"{values['R_top']:.2f} m"),
        ("Vaciado", f"{nums[0] if len(nums) > 0 else '---'} min"),
    ]


def graph_interpretation(case_id):
    if case_id == 1:
        return [
            "La curva presenta decaimiento exponencial.",
            "La pendiente es mayor al inicio y disminuye con el tiempo.",
            "El comportamiento se aproxima a la temperatura ambiente.",
        ]

    if case_id == 2:
        return [
            "El nivel del líquido disminuye de forma no lineal.",
            "La presión hidrostática inicial produce mayor velocidad de salida.",
            "El punto final indica el tiempo total de vaciado.",
        ]

    if case_id == 3:
        return [
            "La masa de desengrasante aumenta con tendencia asintótica.",
            "El estado estacionario representa el límite de concentración.",
            "La gráfica ayuda a definir el tiempo operativo del proceso.",
        ]

    if case_id == 4:
        return [
            "La curva real se compara con la respuesta ideal.",
            "Un incremento de tau indica respuesta más lenta.",
            "La desviación puede asociarse a fallas hidráulicas o fricción.",
        ]

    return [
        "La altura disminuye de forma no lineal por el área variable.",
        "El área transversal cambia con la altura del cono.",
        "El modelo permite estimar el tiempo de vaciado.",
    ]


def answer_interpretation(interpretation):
    points = split_interpretation(interpretation)
    clean_points = []
    for p in points:
        clean_points.append(p)
    return clean_points[:3]


logo = load_logo()

st.markdown('<div class="header-card">', unsafe_allow_html=True)

header_col1, header_col2 = st.columns([0.75, 5.25])

with header_col1:
    if logo is not None:
        st.image(logo, width=62)
    else:
        st.markdown("**TECSUP**")

with header_col2:
    st.markdown(
        """
        <div class="title-text">Resolución de Ecuaciones Diferenciales Ordinarias</div>
        <div class="subtitle-text">Dashboard académico para modelos industriales, gráfica e interpretación técnica</div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="compact-card">', unsafe_allow_html=True)

selected_case = st.selectbox(
    "Selecciona el caso a resolver",
    options=[1, 2, 3, 4, 5],
    format_func=case_name
)

st.markdown("</div>", unsafe_allow_html=True)


st.sidebar.title("Parámetros")


values = {}

if selected_case == 1:
    with st.sidebar.expander("Caso 1", expanded=True):
        values["T0"] = st.number_input("Temperatura inicial T0 (°C)", value=150.0)
        values["Ta"] = st.number_input("Temperatura ambiente Ta (°C)", value=25.0)
        values["T1"] = st.number_input("Temperatura medida T1 (°C)", value=100.0)
        values["t1"] = st.number_input("Tiempo de medición t1 (min)", value=10.0, min_value=0.01)
        values["T_obj"] = st.number_input("Temperatura objetivo (°C)", value=40.0)

    steps, figures, interpretation = solver.solve_case_1(**values)

elif selected_case == 2:
    with st.sidebar.expander("Caso 2", expanded=True):
        values["r"] = st.number_input("Radio del tanque r (m)", value=1.0, min_value=0.01)
        values["h0"] = st.number_input("Altura inicial h0 (m)", value=4.0, min_value=0.01)
        values["a"] = st.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
        values["C_factor"] = st.number_input("Coeficiente C", value=0.6, min_value=0.01)
        values["g"] = st.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_2(**values)

elif selected_case == 3:
    with st.sidebar.expander("Caso 3", expanded=True):
        values["V"] = st.number_input("Volumen V (L)", value=500.0, min_value=0.01)
        values["Q0"] = st.number_input("Cantidad inicial Q0 (kg)", value=0.0)
        values["cin"] = st.number_input("Concentración entrada cin (kg/L)", value=0.2, min_value=0.0)
        values["rin"] = st.number_input("Caudal entrada rin (L/min)", value=5.0, min_value=0.01)
        values["rout"] = st.number_input("Caudal salida rout (L/min)", value=5.0, min_value=0.01)
        values["t_target"] = st.number_input("Tiempo a evaluar (min)", value=60.0, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_3(**values)

elif selected_case == 4:
    with st.sidebar.expander("Caso 4", expanded=True):
        values["t_test"] = st.number_input("Tiempo de prueba (s)", value=8.0, min_value=0.01)
        values["y_test"] = st.number_input("Posición medida y (cm)", value=6.32, min_value=0.01)
        values["tau_ideal"] = st.number_input("Tau ideal (s)", value=4.0, min_value=0.01)
        values["recorrido"] = st.number_input("Recorrido máximo (cm)", value=10.0, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_4(**values)

else:
    with st.sidebar.expander("Caso 5", expanded=True):
        values["H"] = st.number_input("Altura total H (m)", value=2.0, min_value=0.01)
        values["R_top"] = st.number_input("Radio superior R (m)", value=0.5, min_value=0.01)
        values["h0"] = st.number_input("Altura inicial h0 (m)", value=2.0, min_value=0.01)
        values["a"] = st.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
        values["C_factor"] = st.number_input("Coeficiente C", value=0.6, min_value=0.01)
        values["g"] = st.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_5(**values)


left_col, right_col = st.columns([1, 1], gap="small")


with left_col:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Resolución</div>', unsafe_allow_html=True)

    kpis = make_result_kpis(selected_case, values, interpretation)
    kpi_cols = st.columns(3)

    for col, item in zip(kpi_cols, kpis):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">{item[0]}</div>
                    <div class="kpi-value">{item[1]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interpretación de la respuesta</div>', unsafe_allow_html=True)

    bullets = answer_interpretation(interpretation)
    st.markdown('<div class="mini-list"><ul>', unsafe_allow_html=True)
    for bullet in bullets:
        st.markdown(f"<li>{bullet}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


with right_col:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Gráfica del modelo</div>', unsafe_allow_html=True)

    for _, fig in figures.items():
        fig.update_layout(
            height=330,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Times New Roman", size=12, color="#111111"),
            margin=dict(l=30, r=18, t=35, b=28),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(255,255,255,0)"
            )
        )
        fig.update_xaxes(showgrid=True, gridcolor="#E5EEF3", zeroline=False)
        fig.update_yaxes(showgrid=True, gridcolor="#E5EEF3", zeroline=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interpretación de la gráfica</div>', unsafe_allow_html=True)

    st.markdown('<div class="mini-list"><ul>', unsafe_allow_html=True)
    for bullet in graph_interpretation(selected_case):
        st.markdown(f"<li>{bullet}</li>", unsafe_allow_html=True)
    st.markdown("</ul></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="white-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Procedimiento matemático</div>', unsafe_allow_html=True)

with st.expander("Ver desarrollo matemático", expanded=False):
    st.markdown('<div class="math-scroll">', unsafe_allow_html=True)
    render_steps_compact(steps)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer">
        Usuario: Jenifer U.
    </div>
    """,
    unsafe_allow_html=True
)
