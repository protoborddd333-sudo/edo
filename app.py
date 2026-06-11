# app.py
import streamlit as st
import solver

st.set_page_config(page_title="Solver Industrial EDO", layout="wide")

# --- LÓGICA DE TECLADO VIRTUAL ---
if "problem_text" not in st.session_state:
    st.session_state["problem_text"] = ""

def insert_symbol(sym):
    st.session_state["problem_text"] += sym

# --- MOTOR DE FILTRO DE PALABRAS CLAVE ---
def detect_case(text):
    text = text.lower()
    if "enfriamiento" in text or "newton" in text: return 1
    if "cilíndrico" in text or ("radio de 1 metro" in text and "torricelli" in text): return 2
    if "desengrasante" in text or "mezcla" in text: return 3
    if "actuador" in text or "cilindro hidráulico" in text: return 4
    if "cónico" in text or "cono" in text: return 5
    return 0

# --- INTERFAZ PRINCIPAL ---
st.title("🏭 Plataforma de Resolución de EDOs Industriales")
st.markdown("Pegue el problema de ingeniería para detectar automáticamente el modelo matemático correspondiente, generar la solución paso a paso y graficar las curvas operativas.")

# Panel Calculadora Matemática
st.write("**Teclado Matemático Rápido:**")
cols = st.columns(10)
symbols = [" d/dt ", " ∫ ", " √ ", " λ ", " e^x ", " t ", " y ", " τ ", " °C ", " \pi "]
for i, sym in enumerate(symbols):
    cols[i].button(sym, on_click=insert_symbol, args=(sym,))

# Área de Texto Principal
user_input = st.text_area("Descripción del Problema:", value=st.session_state["problem_text"], height=150, key="problem_text")

case_id = detect_case(user_input)

if case_id > 0:
    st.success(f"✅ ¡Caso {case_id} Detectado Automáticamente!")
    st.markdown("---")
    
    # --- FORMULARIOS DINÁMICOS POR CASO ---
    with st.sidebar:
        st.header(f"Parámetros: Caso {case_id}")
        
        if case_id == 1:
            T0 = st.number_input("Temp Inicial (T0)", value=150.0)
            Ta = st.number_input("Temp Ambiente (Ta)", value=25.0)
            T1 = st.number_input("Temp Medida (T1)", value=100.0)
            t1 = st.number_input("Tiempo Medida (t1 min)", value=10.0)
            T_target = st.number_input("Temp Objetivo", value=40.0)
            
        elif case_id == 2:
            r = st.number_input("Radio tanque (m)", value=1.0)
            h0 = st.number_input("Altura inicial (m)", value=4.0)
            a = st.number_input("Área orificio (m²)", value=0.005, format="%.4f")
            C = st.number_input("Coef. Fricción (C)", value=0.6)
            
        elif case_id == 3:
            V = st.number_input("Volumen mezcla (L)", value=500.0)
            Q0 = st.number_input("Químico Inicial (kg)", value=0.0)
            cin = st.number_input("Concentración Entrada (kg/L)", value=0.2)
            rin = st.number_input("Flujo Entrada (L/min)", value=5.0)
            rout = st.number_input("Flujo Salida (L/min)", value=5.0)
            t_target = st.number_input("Tiempo a evaluar (min)", value=60.0)
            
        elif case_id == 4:
            tau_ideal = st.number_input("Tau Ideal Manual (s)", value=4.0)
            t_test = st.number_input("Tiempo Prueba (s)", value=8.0)
            y_test = st.number_input("Desplazamiento Prueba (cm)", value=6.32)
            
        elif case_id == 5:
            H = st.number_input("Altura Cono (m)", value=2.0)
            R = st.number_input("Radio Superior (m)", value=0.5)
            h0 = st.number_input("Altura Líquido Inicial (m)", value=2.0)

    # --- RENDERIZADO DE RESULTADOS ---
    col1, col2 = st.columns([1, 1.2])
    
    # Calcular según caso
    if case_id == 1: steps, fig, interp = solver.solve_case_1(T0, Ta, T1, t1, T_target)
    elif case_id == 2: steps, fig, interp = solver.solve_case_2(r, h0, a, C)
    elif case_id == 3: steps, fig, interp = solver.solve_case_3(V, Q0, cin, rin, rout, t_target)
    elif case_id == 4: steps, fig, interp = solver.solve_case_4(0, t_test, y_test, tau_ideal)
    elif case_id == 5: steps, fig, interp = solver.solve_case_5(H, R, h0)

    # Columna Izquierda: Matemática
    with col1:
        st.subheader("Desarrollo Matemático")
        with st.container(border=True):
            for step in steps:
                if step.startswith("$$"):
                    st.latex(step.replace("$$", ""))
                else:
                    st.markdown(step)

    # Columna Derecha: Gráficas e Interpretación
    with col2:
        st.plotly_chart(fig, use_container_width=True)
        st.info(interp)

elif user_input != "":
    st.warning("Escriba o pegue el enunciado del problema. Esperando palabras clave...")
