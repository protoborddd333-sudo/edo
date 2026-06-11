import streamlit as st
import solver

# Configuracion de pagina
st.set_page_config(page_title="Solver EDO Industrial", page_icon="⚙️", layout="wide")

# --- ESTADO PARA TECLADO VIRTUAL ---
if "problem_text" not in st.session_state:
    st.session_state.problem_text = ""

def insert_symbol(sym):
    st.session_state.problem_text += sym

# --- MOTOR DE RECONOCIMIENTO DE PALABRAS CLAVE ---
def detect_case(text):
    text = text.lower()
    if not text:
        return 0
    if "enfriamiento" in text or "newton" in text:
        return 1
    elif "cilíndrico" in text or "aceite" in text and "cónico" not in text:
        return 2
    elif "mezcla" in text or "desengrasante" in text:
        return 3
    elif "actuador" in text or "hidráulico" in text:
        return 4
    elif "cónico" in text or "cono" in text or "dosing" in text:
        return 5
    return 0

# --- UI PRINCIPAL ---
st.title("🏭 Plataforma de Resolución de EDOs Industriales")
st.markdown("Pegue el problema de la Guía de Laboratorio para auto-configurar el solucionador matemático.")

# Teclado Matematico
st.write("**Teclado Matemático Rápido:**")
cols = st.columns(10)
symbols = [" d/dt ", " ∫ ", " √ ", " λ ", " e^x ", " t ", " y ", " τ ", " °C ", " π "]
for i, sym in enumerate(symbols):
    if cols[i].button(sym, key=f"btn_{i}"):
        insert_symbol(sym)

# Input del Usuario
user_input = st.text_area(
    "Descripción del Problema:", 
    value=st.session_state.problem_text, 
    height=150, 
    key="textarea_problem"
)

# Sincronizar estado (Workaround nativo de Streamlit)
if user_input != st.session_state.problem_text:
    st.session_state.problem_text = user_input

# Detectar Caso
case_id = detect_case(user_input)

if case_id > 0:
    st.success(f"✅ ¡Caso {case_id} Detectado Automáticamente!")
    st.markdown("---")
    
    # --- BARRA LATERAL: PARAMETROS DINAMICOS ---
    with st.sidebar:
        st.header(f"⚙️ Parámetros Caso {case_id}")
        
        if case_id == 1:
            st.subheader("Ley de Enfriamiento")
            T0 = st.number_input("Temp. Inicial (°C)", value=150.0)
            Ta = st.number_input("Temp. Ambiente (°C)", value=25.0)
            T1 = st.number_input("Temp. Medición 1 (°C)", value=100.0)
            t1 = st.number_input("Tiempo Medición 1 (min)", value=10.0)
            T_target = st.number_input("Temp. Objetivo Segura (°C)", value=40.0)
            steps, fig, interp = solver.solve_case_1(T0, Ta, T1, t1, T_target)
            
        elif case_id == 2:
            st.subheader("Torricelli - Cilindro")
            r = st.number_input("Radio del Tanque (m)", value=1.0)
            h0 = st.number_input("Altura Inicial (m)", value=4.0)
            a = st.number_input("Área Orificio (m²)", value=0.005, format="%.4f")
            C_factor = st.number_input("Coeficiente Fricción (C)", value=0.6)
            steps, fig, interp = solver.solve_case_2(r, h0, a, C_factor)
            
        elif case_id == 3:
            st.subheader("Mezclas Industriales")
            V = st.number_input("Volumen del Tanque (L)", value=1000.0)
            Q0 = st.number_input("Químico Inicial (kg)", value=0.0)
            cin = st.number_input("Concentración Entrada (kg/L)", value=0.2)
            rin = st.number_input("Flujo Entrada (L/min)", value=5.0)
            rout = st.number_input("Flujo Salida (L/min)", value=5.0)
            t_target = st.number_input("Tiempo a evaluar (min)", value=60.0)
            steps, fig, interp = solver.solve_case_3(V, Q0, cin, rin, rout, t_target)
            
        elif case_id == 4:
            st.subheader("Actuador Hidráulico")
            tau_ideal = st.number_input("Constante Tau Ideal (s)", value=4.0)
            t_test = st.number_input("Tiempo de Prueba (s)", value=8.0)
            y_test = st.number_input("Desplazamiento Medido (cm)", value=6.32)
            steps, fig, interp = solver.solve_case_4(t_test, y_test, tau_ideal)
            
        elif case_id == 5:
            st.subheader("Torricelli - Cono")
            H = st.number_input("Altura Total del Cono (m)", value=2.0)
            R_top = st.number_input("Radio Superior (m)", value=0.5)
            h0 = st.number_input("Altura Líquido Inicial (m)", value=2.0)
            steps, fig, interp = solver.solve_case_5(H, R_top, h0)

    # --- ZONA DE RESULTADOS ---
    col_math, col_graph = st.columns([1, 1.2])
    
    with col_math:
        st.subheader("📐 Desarrollo Matemático")
        with st.container(border=True):
            for step in steps:
                if step.startswith("$$") and step.endswith("$$"):
                    # Renderizado seguro de formulas limpias
                    st.latex(step.replace("$$", ""))
                elif "$$" in step:
                    # Para lineas que mezclan markdown con ecuaciones display
                    parts = step.split("$$")
                    st.markdown(parts[0])
                    st.latex(parts[1])
                    if len(parts) > 2:
                        st.markdown(parts[2])
                else:
                    st.markdown(step)

    with col_graph:
        st.subheader("📊 Visualización Operativa")
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"**Ejecutivo:** {interp}")

else:
    st.info("📌 Pegue o escriba el enunciado del problema arriba. El motor está esperando palabras clave (ej. 'enfriamiento', 'cilíndrico', 'mezcla', 'actuador', 'cónico').")
