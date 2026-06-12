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
        font-family: "Times New Roman", Times, serif !important;
    }

    .stApp {
        background-color: #F5F7FA;
    }

    .block-container {
        padding-top: 0.45rem !important;
        padding-bottom: 0.2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #EAF0F4;
        border-right: 1px solid #D8E1E8;
        width: 25% !important;
        min-width: 25% !important;
        padding-top: 0.4rem;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.4rem !important;
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
        margin-bottom: 0.2rem !important;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-size: 15px !important;
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }

    section[data-testid="stSidebar"] label {
        font-size: 12px !important;
        margin-bottom: 0px !important;
        color: #1F2937;
    }

    section[data-testid="stSidebar"] div[data-testid="stNumberInput"] {
        margin-bottom: -0.55rem !important;
    }

    section[data-testid="stSidebar"] input {
        height: 30px !important;
        font-size: 12px !important;
        border-radius: 8px !important;
        border: 1px solid #C8D4DC !important;
        background-color: #FFFFFF !important;
    }

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.04);
        margin-bottom: 0.5rem;
    }

    div[data-testid="stExpander"] summary {
        font-size: 13px !important;
        font-weight: bold;
    }

    .top-header {
        height: 78px;
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.06);
        display: flex;
        align-items: center;
        padding: 0.35rem 0.8rem;
        margin-bottom: 0.45rem;
    }

    .header-title {
        text-align: center;
        font-size: 23px;
        font-weight: bold;
        color: #111827;
        line-height: 1.05;
        margin: 0px;
    }

    .header-subtitle {
        text-align: center;
        font-size: 13px;
        color: #475569;
        margin-top: 2px;
    }

    .control-card {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        padding: 0.55rem 0.75rem;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.05);
        margin-bottom: 0.45rem;
    }

    .kpi-card {
        height: 72px;
        background: linear-gradient(180deg, #FFFFFF 0%, #DCEEF8 100%);
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        box-shadow: 0px 3px 10px rgba(15, 23, 42, 0.06);
        padding: 0.45rem 0.5rem;
        text-align: center;
    }

    .kpi-title {
        font-size: 12px;
        color: #64748B;
        margin-bottom: 3px;
        line-height: 1;
    }

    .kpi-value {
        font-size: 17px;
        color: #111827;
        font-weight: bold;
        line-height: 1.1;
    }

    .content-card {
        height: 610px;
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 16px;
        box-shadow: 0px 3px 12px rgba(15, 23, 42, 0.06);
        padding: 0.6rem 0.7rem;
        overflow: hidden;
    }

    .content-card-scroll {
        height: 535px;
        overflow-y: auto;
        padding-right: 0.35rem;
    }

    .footer {
        text-align: center;
        color: #475569;
        font-size: 12px;
        padding-top: 0.25rem;
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span {
        font-family: "Times New Roman", Times, serif !important;
    }

    h2 {
        font-size: 18px !important;
        margin-top: 0rem !important;
        margin-bottom: 0.35rem !important;
        color: #111827 !important;
    }

    h3 {
        font-size: 15px !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.15rem !important;
        color: #1F2937 !important;
    }

    p {
        margin-bottom: 0.25rem !important;
        font-size: 13px !important;
    }

    .stMarkdown {
        margin-bottom: 0.05rem !important;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label {
        font-size: 13px !important;
        font-weight: bold;
        color: #1F2937;
    }

    div[data-testid="stSelectbox"] {
        margin-bottom: -0.25rem !important;
    }

    div[data-testid="stTextArea"] textarea {
        height: 45px !important;
        min-height: 45px !important;
        font-size: 12px !important;
        border-radius: 10px !important;
        border: 1px solid #D8E1E8 !important;
    }

    div[data-testid="stAlert"] {
        padding: 0.4rem 0.6rem !important;
        border-radius: 12px !important;
        font-size: 12px !important;
        margin-top: 0.2rem !important;
    }

    div[data-testid="stPlotlyChart"] {
        height: 515px !important;
        border-radius: 14px;
        border: 1px solid #E5EAF0;
        background-color: #FFFFFF;
        padding: 0.2rem;
    }

    div[data-testid="stTabs"] button {
        font-size: 12px !important;
        padding: 0.25rem 0.55rem !important;
    }

    .katex {
        font-size: 0.88em !important;
    }

    hr {
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def detect_case(text):
    text = text.lower()

    if "newton" in text or "enfriamiento" in text or "rodamiento" in text:
        return 1

    if "mezcla" in text or "desengrasante" in text or "concentracion" in text or "concentración" in text:
        return 3

    if "actuador" in text or "hidraulico" in text or "hidráulico" in text or "piston" in text or "pistón" in text or "tau" in text:
        return 4

    if "cono" in text or "conico" in text or "cónico" in text or "dosing" in text:
        return 5

    if "torricelli" in text or "cilindrico" in text or "cilíndrico" in text or "aceite" in text or "tanque" in text:
        return 2

    return 0


def render_steps_tabs(steps):
    grupos = []
    actual_titulo = "Desarrollo"
    actual_items = []

    for item in steps:
        clean = str(item).strip()
        if clean.startswith("###"):
            if actual_items:
                grupos.append((actual_titulo, actual_items))
            actual_titulo = clean.replace("###", "").strip()
            actual_items = []
        else:
            actual_items.append(clean)

    if actual_items:
        grupos.append((actual_titulo, actual_items))

    if not grupos:
        grupos = [("Desarrollo", steps)]

    tabs = st.tabs([g[0][:22] for g in grupos])

    for tab, (_, items) in zip(tabs, grupos):
        with tab:
            for clean in items:
                if str(clean).startswith("$$") and str(clean).endswith("$$"):
                    st.latex(str(clean).replace("$$", ""))
                else:
                    st.markdown(str(clean))


def load_logo():
    try:
        return Image.open("logjitodetecsup.png")
    except Exception:
        return None


def case_name(case_id):
    names = {
        0: "Selección manual",
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
            ("T ambiente", f"{values['Ta']:.2f} °C"),
            ("T objetivo", f"{values['T_obj']:.2f} °C"),
            ("Tiempo medición", f"{values['t1']:.2f} min"),
        ]

    if case_id == 2:
        return [
            ("Radio", f"{values['r']:.2f} m"),
            ("Altura inicial", f"{values['h0']:.2f} m"),
            ("Orificio", f"{values['a']:.6f} m²"),
            ("Coeficiente", f"{values['C_factor']:.2f}"),
        ]

    if case_id == 3:
        return [
            ("Volumen", f"{values['V']:.2f} L"),
            ("Concentración", f"{values['cin']:.2f} kg/L"),
            ("Entrada", f"{values['rin']:.2f} L/min"),
            ("Tiempo", f"{values['t_target']:.2f} min"),
        ]

    if case_id == 4:
        return [
            ("Tiempo prueba", f"{values['t_test']:.2f} s"),
            ("Posición", f"{values['y_test']:.2f} cm"),
            ("Tau ideal", f"{values['tau_ideal']:.2f} s"),
            ("Recorrido", f"{values['recorrido']:.2f} cm"),
        ]

    return [
        ("Altura cono", f"{values['H']:.2f} m"),
        ("Radio superior", f"{values['R_top']:.2f} m"),
        ("Altura inicial", f"{values['h0']:.2f} m"),
        ("Orificio", f"{values['a']:.6f} m²"),
    ]


logo = load_logo()

st.markdown('<div class="top-header">', unsafe_allow_html=True)
hcol1, hcol2, hcol3 = st.columns([1, 6, 1])

with hcol1:
    if logo is not None:
        st.image(logo, width=68)
    else:
        st.markdown("**TECSUP**")

with hcol2:
    st.markdown(
        """
        <div class="header-title">Resolución de Ecuaciones Diferenciales Ordinarias</div>
        <div class="header-subtitle">Dashboard científico para modelos industriales con gráfica, desarrollo e interpretación técnica</div>
        """,
        unsafe_allow_html=True
    )

with hcol3:
    st.markdown("")

st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="control-card">', unsafe_allow_html=True)

control_col1, control_col2 = st.columns([1.1, 1.6])

with control_col1:
    problem_text = st.text_area(
        "Detección automática",
        height=45,
        placeholder="Pega palabras clave: Newton, Torricelli, mezcla, actuador, cono..."
    )

detected_case = detect_case(problem_text)

case_options = [1, 2, 3, 4, 5]
default_case = detected_case if detected_case != 0 else 1
default_index = case_options.index(default_case)

with control_col2:
    selected_case = st.selectbox(
        "Selección manual del caso",
        options=case_options,
        index=default_index,
        format_func=case_name
    )

st.markdown("</div>", unsafe_allow_html=True)


st.sidebar.title("Parámetros")
st.sidebar.markdown("Datos de entrada compactos.")


values = {}

if selected_case == 1:
    with st.sidebar.expander("Caso 1: Enfriamiento", expanded=True):
        values["T0"] = st.number_input("Temperatura inicial T0 (°C)", value=150.0)
        values["Ta"] = st.number_input("Temperatura ambiente Ta (°C)", value=25.0)
        values["T1"] = st.number_input("Temperatura medida T1 (°C)", value=100.0)
        values["t1"] = st.number_input("Tiempo de medición t1 (min)", value=10.0, min_value=0.01)
        values["T_obj"] = st.number_input("Temperatura objetivo (°C)", value=40.0)
    steps, figures, interpretation = solver.solve_case_1(**values)

elif selected_case == 2:
    with st.sidebar.expander("Caso 2: Tanque cilíndrico", expanded=True):
        values["r"] = st.number_input("Radio del tanque r (m)", value=1.0, min_value=0.01)
        values["h0"] = st.number_input("Altura inicial h0 (m)", value=4.0, min_value=0.01)
        values["a"] = st.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
        values["C_factor"] = st.number_input("Coeficiente C", value=0.6, min_value=0.01)
        values["g"] = st.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)
    steps, figures, interpretation = solver.solve_case_2(**values)

elif selected_case == 3:
    with st.sidebar.expander("Caso 3: Mezclas", expanded=True):
        values["V"] = st.number_input("Volumen V (L)", value=500.0, min_value=0.01)
        values["Q0"] = st.number_input("Cantidad inicial Q0 (kg)", value=0.0)
        values["cin"] = st.number_input("Concentración entrada cin (kg/L)", value=0.2, min_value=0.0)
        values["rin"] = st.number_input("Caudal entrada rin (L/min)", value=5.0, min_value=0.01)
        values["rout"] = st.number_input("Caudal salida rout (L/min)", value=5.0, min_value=0.01)
        values["t_target"] = st.number_input("Tiempo a evaluar (min)", value=60.0, min_value=0.01)
    steps, figures, interpretation = solver.solve_case_3(**values)

elif selected_case == 4:
    with st.sidebar.expander("Caso 4: Actuador", expanded=True):
        values["t_test"] = st.number_input("Tiempo de prueba (s)", value=8.0, min_value=0.01)
        values["y_test"] = st.number_input("Posición medida y (cm)", value=6.32, min_value=0.01)
        values["tau_ideal"] = st.number_input("Tau ideal (s)", value=4.0, min_value=0.01)
        values["recorrido"] = st.number_input("Recorrido máximo (cm)", value=10.0, min_value=0.01)
    steps, figures, interpretation = solver.solve_case_4(**values)

else:
    with st.sidebar.expander("Caso 5: Tanque cónico", expanded=True):
        values["H"] = st.number_input("Altura total H (m)", value=2.0, min_value=0.01)
        values["R_top"] = st.number_input("Radio superior R (m)", value=0.5, min_value=0.01)
        values["h0"] = st.number_input("Altura inicial h0 (m)", value=2.0, min_value=0.01)
        values["a"] = st.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
        values["C_factor"] = st.number_input("Coeficiente C", value=0.6, min_value=0.01)
        values["g"] = st.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)
    steps, figures, interpretation = solver.solve_case_5(**values)


kpi_cols = st.columns(4)

for col, item in zip(kpi_cols, result_summary(selected_case, values)):
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


main_left, main_right = st.columns([1, 1])

with main_left:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("## Desarrollo matemático")
    st.markdown('<div class="content-card-scroll">', unsafe_allow_html=True)
    render_steps_tabs(steps)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with main_right:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("## Gráfica del modelo")

    for _, fig in figures.items():
        fig.update_layout(
            height=485,
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Times New Roman", size=12, color="#111827"),
            margin=dict(l=28, r=15, t=35, b=28),
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
