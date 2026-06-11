import streamlit as st
import base64
import os
import solver

st.set_page_config(page_title="Solver EDO Industrial - TECSUP", layout="wide")

def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_b64 = get_base64_image("logjitodetecsup.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 60px; float: right;">' if logo_b64 else ''

# --- INYECCIÓN DE CSS INSTITUCIONAL (GRIS Y CELESTE EN SIDEBAR) ---
st.markdown("""
<style>
    /* Fondo General de la Pantalla */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Textos principales */
    .stMarkdown, .stText, p, li {
        color: #1E293B !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #00A8E1 !important;
    }
    
    /* DISENO DE BARRA LATERAL (GRIS CON ACENTOS CELESTES) */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9 !important; /* Gris muy elegante */
        border-right: 2px solid #00A8E1;
    }
    
    /* Encabezados dentro de la barra lateral en Celeste */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        background-color: #00A8E1 !important;
        color: #FFFFFF !important;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 15px;
    }

    /* Etiquetas de los inputs de la barra lateral en Celeste oscuro */
    [data-testid="stSidebar"] label {
        color: #0369A1 !important;
        font-weight: 600;
    }

    /* Ocultar elementos innecesarios */
    div[data-testid="stWebsocket"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO CELESTE TECSUP ---
st.markdown(f"""
<div style="background-color: #00A8E1; padding: 20px 30px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    {logo_html}
    <h1 style="color: #FFFFFF !important; margin: 0; padding: 0; font-family: sans-serif;">Simulador Parametrico de EDOs</h1>
</div>
""", unsafe_allow_html=True)

if "problem_text" not in st.session_state:
    st.session_state.problem_text = ""

def detect_case(text):
    text = text.lower()
    if not text: return 0
    if "enfriamiento" in text or "newton" in text or "temperatura" in text: return 1
    elif "cilindro" in text or "cilindrico" in text: return 2
    elif "mezcla" in text or "concentracion" in text or "salmuera" in text: return 3
    elif "actuador" in text or "hidraulico" in text or "piston" in text: return 4
    elif "conico" in text or "cono" in text or "embudo" in text: return 5
    return 0

user_input = st.text_area(
    "Pegue el problema de ingenieria o deje en blanco y seleccione el modelo en el menu lateral:", 
    value=st.session_state.problem_text, 
    height=100
)

# --- SELECTOR MANUAL UNIVERSAL ---
detected_case = detect_case(user_input)

opciones_modelos = {
    0: "Seleccione un modelo matematico...",
    1: "Ley de Enfriamiento de Newton",
    2: "Ley de Torricelli (Tanque Cilindrico)",
    3: "Dinamica de Mezclas (Volumen Constante)",
    4: "Sistemas Lineales de Primer Orden (Actuadores)",
    5: "Ley de Torricelli (Tanque Conico)"
}

with st.sidebar:
    st.markdown("### Seleccion de Modelo")
    case_id = st.selectbox(
        "Tipo de EDO a resolver:", 
        options=list(opciones_modelos.keys()), 
        format_func=lambda x: opciones_modelos[x],
        index=detected_case if detected_case in opciones_modelos else 0
    )

if case_id > 0:
    st.markdown("---")
    
    with st.sidebar:
        st.markdown("### Parametros de Entrada")
        if case_id == 1:
            T0 = st.number_input("Temp. Inicial", value=150.0, step=1.0)
            Ta = st.number_input("Temp. Ambiente", value=25.0, step=1.0)
            T1 = st.number_input("Temp. en t1", value=100.0, step=1.0)
            t1 = st.number_input("Tiempo de medicion t1", value=10.0, step=1.0)
            T_target = st.number_input("Temp. Objetivo Final", value=40.0, step=1.0)
            steps, figs_dict, interp = solver.solve_case_1(T0, Ta, T1, t1, T_target)
            
        elif case_id == 2:
            r = st.number_input("Radio Cilindro (m)", value=1.0, step=0.1)
            h0 = st.number_input("Altura Inicial (m)", value=4.0, step=0.1)
            a = st.number_input("Area Orificio (m2)", value=0.005, format="%.4f", step=0.001)
            C_factor = st.number_input("Coef. Descarga (C)", value=0.6, step=0.1)
            steps, figs_dict, interp = solver.solve_case_2(r, h0, a, C_factor)
            
        elif case_id == 3:
            V = st.number_input("Volumen Tanque (L)", value=500.0, step=10.0)
            Q0 = st.number_input("Masa Inicial (kg)", value=0.0, step=1.0)
            cin = st.number_input("Concentracion Entrada (kg/L)", value=0.2, step=0.05)
            rin = st.number_input("Flujo Entrada/Salida (L/min)", value=5.0, step=1.0)
            t_target = st.number_input("Tiempo a evaluar (min)", value=60.0, step=5.0)
            steps, figs_dict, interp = solver.solve_case_3(V, Q0, cin, rin, rin, t_target)
            
        elif case_id == 4:
            tau_ideal = st.number_input("Tau Ideal Teorico (s)", value=4.0, step=0.5)
            t_test = st.number_input("Tiempo de Prueba (s)", value=8.0, step=0.5)
            y_test = st.number_input("Posicion Medida (cm)", value=6.32, step=0.1)
            force = st.number_input("Valor Asintotico / Fuerza (cm)", value=10.0, step=1.0)
            steps, figs_dict, interp = solver.solve_case_4(t_test, y_test, tau_ideal, force)
            
        elif case_id == 5:
            H = st.number_input("Altura Total Cono (m)", value=2.0, step=0.1)
            R_top = st.number_input("Radio Superior (m)", value=0.5, step=0.1)
            h0 = st.number_input("Altura Liquido Inicial (m)", value=2.0, step=0.1)
            a = st.number_input("Area Orificio (m2)", value=0.005, format="%.4f", step=0.001)
            C_factor = st.number_input("Coef. Descarga (C)", value=0.6, step=0.1)
            steps, figs_dict, interp = solver.solve_case_5(H, R_top, h0, a, C_factor)

    col_math, col_graph = st.columns([1, 1.2])
    
    with col_math:
        st.markdown("### Desarrollo Analitico Riguroso")
        with st.container(border=True):
            for step in steps:
                if step.startswith("$$") and step.endswith("$$"):
                    st.latex(step.replace("$$", "").strip())
                else:
                    st.markdown(step)

    with col_graph:
        st.markdown("### Comportamiento del Sistema")
        tabs = st.tabs(list(figs_dict.keys()))
        for idx, (tab_name, fig) in enumerate(figs_dict.items()):
            with tabs[idx]:
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown(f"""
        <div style="background-color: #E0F2FE; color: #0369A1; padding: 18px; border-radius: 6px; border-left: 6px solid #00A8E1; font-family: sans-serif; font-size: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <strong style="font-size: 16px; text-transform: uppercase;">Conclusion Tecnica Computada</strong><br><br>
            {interp}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #64748B; font-size: 18px;'>Seleccione un modelo matematico en la barra lateral izquierda para iniciar la simulacion.</p>", unsafe_allow_html=True)
