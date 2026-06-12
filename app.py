# app.py

import streamlit as st
from PIL import Image
import solver


st.set_page_config(
    page_title="Solver Industrial de EDO",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #F4F7FA;
    }

    section[data-testid="stSidebar"] {
        background-color: #E8EEF5;
    }

    .main-card {
        background-color: white;
        padding: 1.4rem;
        border-radius: 14px;
        border: 1px solid #D9E2EC;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .header-title {
        font-size: 34px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 0px;
    }

    .header-subtitle {
        font-size: 17px;
        color: #475569;
        margin-top: 4px;
    }

    .metric-card {
        background-color: #EDF4FB;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #D6E4F0;
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #64748B;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0F172A;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def detect_case(text):
    text = text.lower()

    if "newton" in text or "enfriamiento" in text or "rodamiento" in text:
        return 1

    if (
        "mezcla" in text
        or "desengrasante" in text
        or "concentracion" in text
        or "concentración" in text
    ):
        return 3

    if (
        "actuador" in text
        or "hidraulico" in text
        or "hidráulico" in text
        or "piston" in text
        or "pistón" in text
        or "tau" in text
    ):
        return 4

    if "cono" in text or "conico" in text or "cónico" in text or "dosing" in text:
        return 5

    if (
        "torricelli" in text
        or "cilindrico" in text
        or "cilíndrico" in text
        or "aceite" in text
        or "tanque" in text
    ):
        return 2

    return 0


def render_steps(steps):
    for item in steps:
        if isinstance(item, str):
            clean = item.strip()
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
        0: "Seleccionar manualmente",
        1: "Caso 1 - Enfriamiento de Newton",
        2: "Caso 2 - Vaciado de tanque cilíndrico",
        3: "Caso 3 - Mezcla de desengrasante",
        4: "Caso 4 - Actuador hidráulico",
        5: "Caso 5 - Tanque cónico",
    }
    return names.get(case_id, "Seleccionar manualmente")


def result_summary(case_id, values):
    if case_id == 1:
        return [
            ("Temperatura inicial", f"{values['T0']:.2f} °C"),
            ("Temperatura objetivo", f"{values['T_obj']:.2f} °C"),
            ("Tiempo de medición", f"{values['t1']:.2f} min"),
        ]

    if case_id == 2:
        return [
            ("Radio del tanque", f"{values['r']:.2f} m"),
            ("Altura inicial", f"{values['h0']:.2f} m"),
            ("Área del orificio", f"{values['a']:.6f} m²"),
        ]

    if case_id == 3:
        return [
            ("Volumen", f"{values['V']:.2f} L"),
            ("Concentración entrada", f"{values['cin']:.2f} kg/L"),
            ("Tiempo evaluado", f"{values['t_target']:.2f} min"),
        ]

    if case_id == 4:
        return [
            ("Tiempo de prueba", f"{values['t_test']:.2f} s"),
            ("Posición medida", f"{values['y_test']:.2f} cm"),
            ("Tau ideal", f"{values['tau_ideal']:.2f} s"),
        ]

    if case_id == 5:
        return [
            ("Altura del cono", f"{values['H']:.2f} m"),
            ("Radio superior", f"{values['R_top']:.2f} m"),
            ("Altura inicial", f"{values['h0']:.2f} m"),
        ]

    return []


logo = load_logo()

header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    if logo is not None:
        st.image(logo, width=150)
    else:
        st.markdown("**TECSUP**")

with header_col2:
    st.markdown(
        """
        <div class="header-title">Solver Industrial de Ecuaciones Diferenciales Ordinarias</div>
        <div class="header-subtitle">
        Plataforma interactiva para resolver modelos EDO aplicados a procesos industriales.
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")


with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.subheader("Ingreso del problema")

    problem_text = st.text_area(
        "Pega aquí el enunciado del problema:",
        height=150,
        placeholder="Ejemplo: Enfriamiento de un rodamiento por Ley de Newton..."
    )

    detected_case = detect_case(problem_text)

    case_options = [0, 1, 2, 3, 4, 5]

    if detected_case != 0:
        st.success(f"Caso detectado automáticamente: {case_name(detected_case)}")
        default_index = case_options.index(detected_case)
    else:
        st.info("El sistema no detectó un caso automáticamente. Puedes seleccionarlo manualmente.")
        default_index = 0

    selected_case = st.selectbox(
        "Caso a resolver:",
        options=case_options,
        index=default_index,
        format_func=case_name
    )

    st.markdown('</div>', unsafe_allow_html=True)


if selected_case == 0:
    st.warning("Selecciona un caso para resolver.")
    st.stop()


st.sidebar.title("Parámetros del modelo")
st.sidebar.write("Modifica los valores y la aplicación recalculará automáticamente.")


values = {}

if selected_case == 1:
    st.sidebar.subheader("Caso 1: Enfriamiento de Newton")

    values["T0"] = st.sidebar.number_input("Temperatura inicial T0 (°C)", value=150.0)
    values["Ta"] = st.sidebar.number_input("Temperatura ambiente Ta (°C)", value=25.0)
    values["T1"] = st.sidebar.number_input("Temperatura medida T1 (°C)", value=100.0)
    values["t1"] = st.sidebar.number_input("Tiempo de medición t1 (min)", value=10.0, min_value=0.01)
    values["T_obj"] = st.sidebar.number_input("Temperatura objetivo (°C)", value=40.0)

    steps, figures, interpretation = solver.solve_case_1(
        T0=values["T0"],
        Ta=values["Ta"],
        T1=values["T1"],
        t1=values["t1"],
        T_obj=values["T_obj"]
    )

elif selected_case == 2:
    st.sidebar.subheader("Caso 2: Vaciado de tanque cilíndrico")

    values["r"] = st.sidebar.number_input("Radio del tanque r (m)", value=1.0, min_value=0.01)
    values["h0"] = st.sidebar.number_input("Altura inicial h0 (m)", value=4.0, min_value=0.01)
    values["a"] = st.sidebar.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
    values["C_factor"] = st.sidebar.number_input("Coeficiente C", value=0.6, min_value=0.01)
    values["g"] = st.sidebar.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_2(
        r=values["r"],
        h0=values["h0"],
        a=values["a"],
        C_factor=values["C_factor"],
        g=values["g"]
    )

elif selected_case == 3:
    st.sidebar.subheader("Caso 3: Mezcla de desengrasante")

    values["V"] = st.sidebar.number_input("Volumen V (L)", value=500.0, min_value=0.01)
    values["Q0"] = st.sidebar.number_input("Cantidad inicial Q0 (kg)", value=0.0)
    values["cin"] = st.sidebar.number_input("Concentración de entrada cin (kg/L)", value=0.2, min_value=0.0)
    values["rin"] = st.sidebar.number_input("Caudal de entrada rin (L/min)", value=5.0, min_value=0.01)
    values["rout"] = st.sidebar.number_input("Caudal de salida rout (L/min)", value=5.0, min_value=0.01)
    values["t_target"] = st.sidebar.number_input("Tiempo a evaluar (min)", value=60.0, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_3(
        V=values["V"],
        Q0=values["Q0"],
        cin=values["cin"],
        rin=values["rin"],
        rout=values["rout"],
        t_target=values["t_target"]
    )

elif selected_case == 4:
    st.sidebar.subheader("Caso 4: Actuador hidráulico")

    values["t_test"] = st.sidebar.number_input("Tiempo de prueba (s)", value=8.0, min_value=0.01)
    values["y_test"] = st.sidebar.number_input("Posición medida y (cm)", value=6.32, min_value=0.01)
    values["tau_ideal"] = st.sidebar.number_input("Tau ideal (s)", value=4.0, min_value=0.01)
    values["recorrido"] = st.sidebar.number_input("Recorrido máximo (cm)", value=10.0, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_4(
        t_test=values["t_test"],
        y_test=values["y_test"],
        tau_ideal=values["tau_ideal"],
        recorrido=values["recorrido"]
    )

elif selected_case == 5:
    st.sidebar.subheader("Caso 5: Tanque cónico")

    values["H"] = st.sidebar.number_input("Altura total H (m)", value=2.0, min_value=0.01)
    values["R_top"] = st.sidebar.number_input("Radio superior R (m)", value=0.5, min_value=0.01)
    values["h0"] = st.sidebar.number_input("Altura inicial h0 (m)", value=2.0, min_value=0.01)
    values["a"] = st.sidebar.number_input("Área del orificio a (m²)", value=0.005, min_value=0.000001, format="%.6f")
    values["C_factor"] = st.sidebar.number_input("Coeficiente C", value=0.6, min_value=0.01)
    values["g"] = st.sidebar.number_input("Gravedad g (m/s²)", value=9.8, min_value=0.01)

    steps, figures, interpretation = solver.solve_case_5(
        H=values["H"],
        R_top=values["R_top"],
        h0=values["h0"],
        a=values["a"],
        C_factor=values["C_factor"],
        g=values["g"]
    )


st.markdown("## Panel de resultados")

summary_items = result_summary(selected_case, values)
summary_cols = st.columns(3)

for col, item in zip(summary_cols, summary_items):
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

st.markdown("")


left_col, right_col = st.columns([1, 1.25])

with left_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Desarrollo matemático paso a paso")
    render_steps(steps)
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Gráfica del modelo")

    for figure_title, fig in figures.items():
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretación técnica")
    st.info(interpretation)

    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")
st.caption("TECSUP - Aplicación académica para análisis de Ecuaciones Diferenciales Ordinarias.")
