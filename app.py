# app.py

import streamlit as st
import solver


st.set_page_config(
    page_title="Resolución de EDO",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #EAF3F8;
        color: #111111;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        padding-bottom: 1rem;
        max-width: 1250px;
    }

    section[data-testid="stSidebar"] {
        background-color: #F5F7FA;
        border-right: 1px solid #D8E1E8;
    }

    h1, h2, h3, h4, p, label, div, span {
        color: #111111;
    }

    h1 {
        font-size: 28px !important;
        margin-bottom: 0.2rem !important;
    }

    h2 {
        font-size: 22px !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-size: 18px !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.3rem !important;
    }

    p {
        font-size: 15px !important;
        line-height: 1.35 !important;
    }

    .main-card {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.9rem;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
    }

    .small-card {
        background-color: #FFFFFF;
        border: 1px solid #D8E1E8;
        border-radius: 12px;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    .result-card {
        background-color: #F5FAFD;
        border: 1px solid #D8E1E8;
        border-radius: 10px;
        padding: 0.65rem;
        text-align: center;
        min-height: 65px;
    }

    .result-title {
        font-size: 13px;
        color: #444444;
        margin-bottom: 0.2rem;
    }

    .result-value {
        font-size: 20px;
        font-weight: 700;
        color: #111111;
    }

    .footer {
        text-align: center;
        font-size: 13px;
        color: #111111;
        margin-top: 0.6rem;
        padding-bottom: 0.3rem;
    }

    div[data-testid="stNumberInput"] input {
        height: 32px;
        font-size: 14px;
    }

    div[data-testid="stSelectbox"] {
        margin-bottom: 0.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def case_name(case_id):
    names = {
        1: "Caso 1 - Enfriamiento de Newton",
        2: "Caso 2 - Vaciado de tanque cilíndrico",
        3: "Caso 3 - Mezcla de desengrasante",
        4: "Caso 4 - Actuador hidráulico",
        5: "Caso 5 - Tanque cónico",
    }
    return names[case_id]


def render_steps(steps):
    for step in steps:
        clean = str(step).strip()

        if clean.startswith("###"):
            st.markdown(clean)

        elif clean.startswith("$$") and clean.endswith("$$"):
            st.latex(clean.replace("$$", ""))

        else:
            st.markdown(clean)


def graph_interpretation(case_id):
    if case_id == 1:
        return (
            "La gráfica muestra un enfriamiento exponencial. "
            "La temperatura baja rápido al inicio y luego disminuye más lentamente al acercarse a la temperatura ambiente."
        )

    if case_id == 2:
        return (
            "La gráfica muestra que la altura del líquido disminuye de forma no lineal. "
            "El vaciado es más rápido al inicio porque la presión hidrostática es mayor."
        )

    if case_id == 3:
        return (
            "La gráfica muestra una aproximación progresiva al estado estacionario. "
            "La cantidad de desengrasante aumenta con rapidez al inicio y luego tiende a estabilizarse."
        )

    if case_id == 4:
        return (
            "La gráfica compara la respuesta real con la respuesta ideal del actuador. "
            "Una curva real más lenta indica mayor constante de tiempo y posible retraso hidráulico."
        )

    if case_id == 5:
        return (
            "La gráfica muestra un vaciado no lineal debido a la geometría cónica. "
            "El área transversal cambia con la altura, por eso el comportamiento no es igual al de un tanque cilíndrico."
        )

    return "La gráfica representa el comportamiento del modelo diferencial seleccionado."


def extract_results(case_id, values, interpretation):
    if case_id == 1:
        return [
            ("Temperatura inicial", f"{values['T0']:.2f} °C"),
            ("Temperatura objetivo", f"{values['T_obj']:.2f} °C"),
            ("Tiempo medición", f"{values['t1']:.2f} min"),
        ]

    if case_id == 2:
        return [
            ("Radio", f"{values['r']:.2f} m"),
            ("Altura inicial", f"{values['h0']:.2f} m"),
            ("Área orificio", f"{values['a']:.6f} m²"),
        ]

    if case_id == 3:
        return [
            ("Volumen", f"{values['V']:.2f} L"),
            ("Concentración", f"{values['cin']:.2f} kg/L"),
            ("Tiempo evaluado", f"{values['t_target']:.2f} min"),
        ]

    if case_id == 4:
        return [
            ("Tiempo prueba", f"{values['t_test']:.2f} s"),
            ("Posición medida", f"{values['y_test']:.2f} cm"),
            ("Tau ideal", f"{values['tau_ideal']:.2f} s"),
        ]

    return [
        ("Altura cono", f"{values['H']:.2f} m"),
        ("Radio superior", f"{values['R_top']:.2f} m"),
        ("Altura inicial", f"{values['h0']:.2f} m"),
    ]


st.markdown(
    """
    <div class="main-card">
        <h1>Resolución de Ecuaciones Diferenciales Ordinarias</h1>
        <p>Aplicación para resolver casos industriales mediante modelos de EDO, mostrando cálculo, gráfica e interpretación técnica.</p>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="small-card">', unsafe_allow_html=True)

selected_case = st.selectbox(
    "Elige el caso a resolver",
    options=[1, 2, 3, 4, 5],
    format_func=case_name
)

st.markdown("</div>", unsafe_allow_html=True)


st.sidebar.title("Parámetros")

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


left_col, right_col = st.columns([1, 1], gap="medium")

with left_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## Resultados principales")

    result_items = extract_results(selected_case, values, interpretation)
    kpi_cols = st.columns(3)

    for col, item in zip(kpi_cols, result_items):
        with col:
            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-title">{item[0]}</div>
                    <div class="result-value">{item[1]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## Cálculos ordenados")
    render_steps(steps)
    st.markdown("</div>", unsafe_allow_html=True)


with right_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## Gráfico")

    for _, fig in figures.items():
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("## Interpretaciones")

    st.markdown("### Interpretación de la gráfica")
    st.markdown(f"- {graph_interpretation(selected_case)}")

    st.markdown("### Interpretación de la respuesta")
    st.markdown(f"- {interpretation}")

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer">
        Usuario: Jenifer U.
    </div>
    """,
    unsafe_allow_html=True
)
