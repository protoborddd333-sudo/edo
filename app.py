import streamlit as st
import base64
import os
import solver

st.set_page_config(page_title="Solver EDO Industrial - TECSUP", layout="wide")

# --- FUNCIÓN PARA CARGAR EL LOGO EN BASE64 ---
def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_b64 = get_base64_image("logjitodetecsup.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 60px; float: right;">' if logo_b64 else ''

# --- INYECCIÓN DE CSS INSTITUCIONAL ---
st.markdown("""
<style>
    /* 2. Fondo General de la Pantalla (Gris Claro Neutro) */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Textos principales oscuros para contraste perfecto */
    .stMarkdown, .stText, p, label, li {
        color: #1E293B !important;
    }
    h2, h3, h4, h5, h6 {
        color: #1E293B !important;
    }
    
    /* Fondo lateral sutilmente diferenciado (Blanco puro) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    
    /* Ocultar elementos innecesarios */
    div[data-testid="stWebsocket"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. ENCABEZADO CELESTE TECSUP ---
st.markdown(f"""
<div style="background-color: #00A8E1; padding: 20px 30px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    {logo_html}
    <h1 style="color: #FFFFFF; margin: 0; padding: 0; font-family: sans-serif;">Simulador Paramétrico de EDOs</h1>
</div>
""", unsafe_allow_html=True)

if "problem_text" not in st.session_state:
    st.session_state.problem_text = ""

def detect_case(text):
    text = text.lower()
    if not text: return 0
    if "enfriamiento" in text or "newton" in text: return 1
    elif "cilíndrico" in text or "aceite" in text and "cónico" not in text: return 2
    elif "mezcla" in text or "desengrasante" in text: return 3
    elif "actuador" in text or "hidráulico" in text: return 4
    elif "cónico" in text or "cono" in text or "dosing" in text: return 5
    return 0

user_input = st.text_area(
    "Pegue el problema de ingeniería para configurar automáticamente los parámetros:", 
    value=st.session_state.problem_text, 
    height=120
)

case_id = detect_case(user_input)

if case_id > 0:
    st.info(f"Contexto Matemático {case_id} Vinculado. Sistema en línea.")
    st.markdown("---")
    
    with st.sidebar:
        st.header(f"Parámetros: Caso {case_id}")
        if case_id == 1:
            T0 = st.number_input("Temp. Inicial (C)", value=150.0)
            Ta = st.number_input("Temp. Ambiente (C)", value=25.0)
            T1 = st.number_input("Temp. Medición 1 (C)", value=100.0)
            t1 = st.number_input("Tiempo Medición 1 (min)", value=10.0)
            T_target = st.number_input("Temp. Objetivo (C)", value=40.0)
            steps, figs_dict, interp = solver.solve_case_1(T0, Ta, T1, t1, T_target)
            
        elif case_id == 2:
            r = st.number_input("Radio Cilindro (m)", value=1.0)
            h0 = st.number_input("Altura Inicial (m)", value=4.0)
            a = st.number_input("Área Orificio (m2)", value=0.005, format="%.4f")
            C_factor = st.number_input("Coef. Fricción (C)", value=0.6)
            steps, figs_dict, interp = solver.solve_case_2(r, h0, a, C_factor)
            
        elif case_id == 3:
            V = st.number_input("Volumen Tanque (L)", value=500.0)
            Q0 = st.number_input("Masa Inicial (kg)", value=0.0)
            cin = st.number_input("Concentración In (kg/L)", value=0.2)
            rin = st.number_input("Flujo In/Out (L/min)", value=5.0)
            t_target = st.number_input("Evaluar en (min)", value=60.0)
            steps, figs_dict, interp = solver.solve_case_3(V, Q0, cin, rin, rin, t_target)
            
        elif case_id == 4:
            tau_ideal = st.number_input("Tau Ideal Manual (s)", value=4.0)
            t_test = st.number_input("Tiempo Prueba (s)", value=8.0)
            y_test = st.number_input("Posición Medida (cm)", value=6.32)
            steps, figs_dict, interp = solver.solve_case_4(t_test, y_test, tau_ideal)
            
        elif case_id == 5:
            H = st.number_input("Altura Cono (m)", value=2.0)
            R_top = st.number_input("Radio Superior (m)", value=0.5)
            h0 = st.number_input("Altura Líquido Inicial (m)", value=2.0)
            a = st.number_input("Área Orificio (m2)", value=0.005, format="%.4f")
            C_factor = st.number_input("Coef. Fricción (C)", value=0.6)
            steps, figs_dict, interp = solver.solve_case_5(H, R_top, h0, a, C_factor)

    col_math, col_graph = st.columns([1, 1.2])
    
    with col_math:
        st.subheader("Desarrollo Analítico")
        with st.container(border=True):
            for step in steps:
                if step.startswith("$$") and step.endswith("$$"):
                    st.latex(step.replace("$$", "").strip())
                else:
                    st.markdown(step)

    with col_graph:
        st.subheader("Gráfica Operativa Asintótica")
        tabs = st.tabs(list(figs_dict.keys()))
        for idx, (tab_name, fig) in enumerate(figs_dict.items()):
            with tabs[idx]:
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # 3. Cuadro de Inteligencia Operativa (Azul Alerta)
        st.markdown(f"""
        <div style="background-color: #E0F2FE; color: #0369A1; padding: 18px; border-radius: 6px; border-left: 6px solid #00A8E1; font-family: sans-serif; font-size: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <strong style="font-size: 16px; text-transform: uppercase;">Inteligencia Operativa</strong><br><br>
            {interp}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #1E293B;'>Esperando contexto... Ingrese palabras clave como 'enfriamiento', 'cilíndrico', 'mezcla', 'actuador' o 'cónico'.</p>", unsafe_allow_html=True)
