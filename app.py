import streamlit as st
import solver

st.set_page_config(page_title="Solver EDO Industrial", page_icon="⚙️", layout="wide")

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

st.title("🏭 Plataforma de Resolución de EDOs Industriales")

user_input = st.text_area(
    "Descripción del Problema:", 
    value=st.session_state.problem_text, 
    height=120, 
    key="textarea_problem",
    placeholder="Pegue aquí el enunciado del PDF para auto-configurar las matemáticas..."
)

case_id = detect_case(user_input)

if case_id > 0:
    st.success(f"✅ Contexto Matemático {case_id} Detectado y Vinculado.")
    st.markdown("---")
    
    with st.sidebar:
        st.header("⚙️ Entradas Dinámicas")
        
        if case_id == 1:
            T0 = st.number_input("Temp. Inicial (°C)", value=150.0)
            Ta = st.number_input("Temp. Ambiente (°C)", value=25.0)
            T1 = st.number_input("Temp. Medición 1 (°C)", value=100.0)
            t1 = st.number_input("Tiempo Medición 1 (min)", value=10.0)
            T_target = st.number_input("Temp. Objetivo (°C)", value=40.0)
            steps, figs_dict, interp = solver.solve_case_1(T0, Ta, T1, t1, T_target)
            
        elif case_id == 2:
            r = st.number_input("Radio Cilindro (m)", value=1.0)
            h0 = st.number_input("Altura Inicial (m)", value=4.0)
            a = st.number_input("Área Orificio (m²)", value=0.005, format="%.4f")
            C_factor = st.number_input("Coef. Fricción", value=0.6)
            steps, figs_dict, interp = solver.solve_case_2(r, h0, a, C_factor)
            
        elif case_id == 3:
            V = st.number_input("Volumen Tanque (L)", value=1000.0)
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
            steps, figs_dict, interp = solver.solve_case_5(H, R_top, h0)

    # --- RENDERIZADO INTERACTIVO Y LIMPIO ---
    col_math, col_graph = st.columns([1, 1.2])
    
    with col_math:
        st.subheader("📐 Rigurosidad Analítica")
        with st.container(border=True):
            for step in steps:
                if step.startswith("$$") and step.endswith("$$"):
                    st.latex(step.replace("$$", ""))
                elif "$$" in step:
                    parts = step.split("$$")
                    st.markdown(parts[0])
                    st.latex(parts[1])
                else:
                    st.markdown(step)

    with col_graph:
        st.subheader("📊 Panel de Decisión Industrial")
        # Falla 4 Corregida: Pestañas de gráficos dinámicos y sin ModeBar de Plotly
        tabs = st.tabs(list(figs_dict.keys()))
        for idx, (tab_name, fig) in enumerate(figs_dict.items()):
            with tabs[idx]:
                st.plotly_chart(
                    fig, 
                    use_container_width=True, 
                    config={'displayModeBar': False} # <- Elimina los botones inútiles de Plotly
                )
        
        # Falla 2 Corregida: Output inteligente
        st.success(f"**💡 Conclusión Ejecutiva Adaptativa:**\n\n{interp}")
else:
    st.info("Pegue el problema del PDF. Esperando parámetros térmicos, de fluidos o mecánicos...")
