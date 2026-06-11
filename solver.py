# solver.py
import numpy as np
import plotly.graph_objects as go

def solve_case_1(T0, Ta, T1, t1, T_target):
    """Caso 1: Enfriamiento de Newton"""
    # Cálculos analíticos
    # T(t) = Ta + (T0 - Ta) * e^(-kt)
    k = -np.log((T1 - Ta) / (T0 - Ta)) / t1
    t_target = -np.log((T_target - Ta) / (T0 - Ta)) / k
    t_adicional = t_target - t1
    
    # Desarrollo Matemático en LaTeX
    steps = [
        r"**1. Modelo de Ley de Enfriamiento de Newton:**",
        r"$$ \frac{dT}{dt} = -k(T - T_a) $$",
        r"**2. Separación de variables e integración:**",
        r"$$ \int \frac{dT}{T - T_a} = \int -k \, dt $$",
        r"$$ \ln|T - T_a| = -kt + C \implies T(t) = T_a + C_1 e^{-kt} $$",
        r"**3. Condiciones iniciales:**",
        rf"$$ T(0) = {T0} \implies {T0} = {Ta} + C_1 e^0 \implies C_1 = {T0 - Ta} $$",
        rf"$$ T(t) = {Ta} + {T0 - Ta} e^{-kt} $$",
        r"**4. Cálculo de la constante de decaimiento $k$:**",
        rf"$$ T({t1}) = {T1} \implies {T1} = {Ta} + {T0 - Ta} e^{-{t1}k} $$",
        rf"$$ e^{-{t1}k} = \frac{{{T1 - Ta}}}{{{T0 - Ta}}} \implies k \approx {k:.5f} \text{{ min}}^{-1} $$",
        r"**5. Cálculo del tiempo para alcanzar la temperatura segura:**",
        rf"$$ {T_target} = {Ta} + {T0 - Ta} e^{-{k:.5f}t} \implies t = {t_target:.2f} \text{{ min}} $$",
        rf"**Respuesta:** El técnico debe esperar **{t_adicional:.2f} minutos adicionales**."
    ]

    # Gráfica
    t_vals = np.linspace(0, t_target + 10, 200)
    T_vals = Ta + (T0 - Ta) * np.exp(-k * t_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=T_vals, mode='lines', name='Curva de Enfriamiento', line=dict(color='#E53935', width=3)))
    fig.add_trace(go.Scatter(x=[0, t1, t_target], y=[T0, T1, T_target], mode='markers+text', 
                             text=['Inicio', 'Medición 1', 'Punto Seguro'], textposition="top right",
                             marker=dict(size=10, color='black'), name='Puntos Críticos'))
    fig.add_hline(y=Ta, line_dash="dash", line_color="blue", annotation_text="Temp. Ambiente (Asíntota)")
    fig.update_layout(title="Perfil Térmico del Rodamiento", xaxis_title="Tiempo (min)", yaxis_title="Temperatura (°C)", template="plotly_white")
    
    interpretation = (
        f"**Interpretación Técnica:** La curva térmica muestra un decaimiento exponencial asintótico hacia la temperatura ambiente ({Ta}°C). "
        f"La pendiente inicial es pronunciada, indicando una rápida pérdida de calor, pero se estabiliza con el tiempo. "
        f"Para operaciones de planta, el tiempo de inactividad total es de {t_target:.1f} minutos; planificar ventanas de mantenimiento más cortas requeriría refrigeración forzada (alterando el valor de $k$)."
    )
    
    return steps, fig, interpretation

def solve_case_2(r, h0, a, C, g=9.8):
    """Caso 2: Vaciado de Tanque de Aceite (Cilindro)"""
    A = np.pi * r**2
    K_val = (C * a * np.sqrt(2 * g)) / A
    t_end = 2 * np.sqrt(h0) / K_val
    
    steps = [
        r"**1. Modelo de Ley de Torricelli:**",
        r"$$ A \frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Separación de variables:**",
        r"$$ \frac{dh}{\sqrt{h}} = -\frac{C a \sqrt{2g}}{A} dt = -K dt $$",
        rf"Donde $ A = \pi({r})^2 = {A:.4f} \text{{ m}}^2 $",
        r"**3. Integración:**",
        r"$$ \int h^{-1/2} dh = \int -K dt \implies 2\sqrt{h} = -Kt + C_1 $$",
        r"**4. Condiciones iniciales:**",
        rf"$$ h(0) = {h0} \implies 2\sqrt{{{h0}}} = C_1 \implies C_1 = {2*np.sqrt(h0):.4f} $$",
        r"$$ h(t) = \left( \sqrt{h_0} - \frac{K}{2} t \right)^2 $$",
        r"**5. Tiempo de vaciado total ($h=0$):**",
        rf"$$ t = \frac{{2\sqrt{{h_0}}}}{{K}} = \frac{{{2*np.sqrt(h0):.4f}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{{ segundos}} $$",
        rf"**Respuesta:** El tanque tardará **{t_end/60:.2f} minutos** en vaciarse por completo."
    ]

    t_vals = np.linspace(0, t_end, 200)
    h_vals = (np.sqrt(h0) - (K_val / 2) * t_vals)**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', name='Nivel de Aceite', line=dict(color='#FFB300', width=3)))
    fig.add_trace(go.Scatter(x=[t_end/60], y=[0], mode='markers+text', text=['Tanque Vacío'], textposition="top right", marker=dict(size=10, color='black')))
    fig.update_layout(title="Curva de Vaciado Hidrodinámico", xaxis_title="Tiempo (min)", yaxis_title="Altura de líquido (m)", template="plotly_white")
    
    interpretation = (
        "**Interpretación Técnica:** El descenso del nivel de aceite no es lineal, sino parabólico. "
        "La tasa de vaciado (pendiente) es máxima al inicio debido a la mayor presión hidrostática, y disminuye paulatinamente a medida que el tanque se vacía. "
        "Esto implica que los equipos de limpieza deben prever un flujo de drenaje variable si el colector de residuos tiene restricciones de caudal máximo."
    )
    
    return steps, fig, interpretation

def solve_case_3(V, Q0, cin, rin, rout, t_target):
    """Caso 3: Control de Mezcla"""
    # EDO: dQ/dt = rin*cin - rout*(Q/V) -> dQ/dt + (rout/V)Q = rin*cin
    factor = rout / V
    inflow = rin * cin
    # Q(t) = (rin*cin*V/rout) + C * e^(-rout/V * t)
    Q_steady = (inflow * V) / rout
    C_const = Q0 - Q_steady
    Q_final = Q_steady + C_const * np.exp(-factor * t_target)
    
    steps = [
        r"**1. Modelo de Mezclas de Primer Orden:**",
        r"$$ \frac{dQ}{dt} = (\text{Tasa entrada}) - (\text{Tasa salida}) $$",
        r"$$ \frac{dQ}{dt} = r_{in} c_{in} - r_{out} \frac{Q(t)}{V(t)} $$",
        rf"**2. Sustitución de valores ($V$ es constante ya que $r_{{in}} = r_{{out}}$):**",
        rf"$$ \frac{{dQ}}{{dt}} = ({rin})({cin}) - ({rout})\frac{{Q}}{{{V}}} $$",
        rf"$$ \frac{{dQ}}{{dt}} + {factor:.4f}Q = {inflow:.2f} $$",
        r"**3. Resolución usando Factor Integrante $\mu(t) = e^{\int P(t)dt}$:**",
        rf"$$ \mu(t) = e^{{{factor:.4f}t}} $$",
        rf"$$ Q(t) = {Q_steady:.2f} + C_1 e^{-{factor:.4f}t} $$",
        r"**4. Condiciones iniciales:**",
        rf"$$ Q(0) = {Q0} \implies C_1 = {C_const:.2f} $$",
        r"**5. Cantidad de desengrasante evaluada:**",
        rf"$$ Q({t_target}) = {Q_steady:.2f} {C_const:+.2f} e^{-{factor:.4f}({t_target})} \approx {Q_final:.2f} \text{{ kg}} $$",
        rf"**Respuesta:** Después de {t_target} minutos, hay **{Q_final:.2f} kg** de desengrasante en el tanque."
    ]

    t_vals = np.linspace(0, t_target * 2, 200)
    Q_vals = Q_steady + C_const * np.exp(-factor * t_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=Q_vals, mode='lines', name='Masa de Químico', line=dict(color='#43A047', width=3)))
    fig.add_trace(go.Scatter(x=[t_target], y=[Q_final], mode='markers+text', text=[f'{Q_final:.1f} kg'], textposition="bottom right", marker=dict(size=10, color='black')))
    fig.add_hline(y=Q_steady, line_dash="dash", line_color="blue", annotation_text="Saturación Máxima (Estado Estacionario)")
    fig.update_layout(title="Cinética de Saturación del Desengrasante", xaxis_title="Tiempo (min)", yaxis_title="Cantidad de Químico (kg)", template="plotly_white")
    
    interpretation = (
        f"**Interpretación Técnica:** La masa de químico aumenta progresivamente hasta alcanzar asintóticamente su estado estacionario de saturación máxima ({Q_steady} kg). "
        "En un entorno industrial, monitorear esta curva asegura que no se desperdicie insumo químico. Si el proceso de lavado requiere una concentración específica, "
        "la gráfica indica el tiempo mínimo de homogenización necesario antes de iniciar el lavado de piezas."
    )
    
    return steps, fig, interpretation

def solve_case_4(y0, t_test, y_test, tau_ideal, force=10):
    """Caso 4: Actuador Hidráulico"""
    # tau(dy/dt) + y = force -> y(t) = force(1 - e^(-t/tau))
    # tau = -t_test / ln(1 - y_test/force)
    tau_actual = -t_test / np.log(1 - (y_test / force))
    
    steps = [
        r"**1. Modelo Lineal de Primer Orden del Actuador:**",
        rf"$$ \tau \frac{{dy}}{{dt}} + y = {force} $$",
        r"**2. Solución general (EDO Lineal no homogénea):**",
        rf"$$ y(t) = {force} + C e^{{-t/\tau}} $$",
        r"**3. Condiciones iniciales:**",
        rf"$$ y(0) = {y0} \implies {y0} = {force} + C \implies C = -{force} $$",
        rf"$$ y(t) = {force} \left(1 - e^{{-t/\tau}}\right) $$",
        r"**4. Cálculo de la Constante de Tiempo real del sistema:**",
        rf"$$ y({t_test}) = {y_test} \implies {force}\left(1 - e^{{-{t_test}/\tau}}\right) = {y_test} $$",
        rf"$$ e^{{-{t_test}/\tau}} = 1 - \frac{{{y_test}}}{{{force}}} = {1 - y_test/force:.3f} $$",
        rf"$$ -\frac{{{t_test}}}{{\tau}} = \ln({1 - y_test/force:.3f}) \implies \tau \approx {tau_actual:.2f} \text{{ segundos}} $$",
        rf"**Respuesta:** La función de posición es $y(t) = 10(1 - e^{{-t/{tau_actual:.1f}}}) $. El sistema tiene un $\tau$ real de {tau_actual:.1f}s frente al ideal de {tau_ideal}s."
    ]

    t_vals = np.linspace(0, max(t_test*2, tau_actual*4), 200)
    y_actual = force * (1 - np.exp(-t_vals / tau_actual))
    y_ideal = force * (1 - np.exp(-t_vals / tau_ideal))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=y_ideal, mode='lines', name=f'Respuesta Ideal (τ={tau_ideal}s)', line=dict(color='#81C784', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=t_vals, y=y_actual, mode='lines', name=f'Respuesta Real (τ={tau_actual:.1f}s)', line=dict(color='#D32F2F', width=3)))
    fig.add_trace(go.Scatter(x=[t_test], y=[y_test], mode='markers+text', text=['Punto de Prueba'], textposition="bottom right", marker=dict(size=10, color='black')))
    fig.update_layout(title="Respuesta Dinámica del Cilindro Hidráulico", xaxis_title="Tiempo (s)", yaxis_title="Desplazamiento y(t) [cm]", template="plotly_white")
    
    interpretation = (
        f"**Interpretación Técnica:** La constante de tiempo ($\tau$) es una medida de la inercia del sistema. El valor actual ($\tau={tau_actual:.1f}$s) es el doble del valor nominal del fabricante ($\tau={tau_ideal}$s). "
        "Físicamente, este retraso severo (la curva roja es mucho más lenta que la verde) sugiere un problema crítico de mantenimiento: "
        "posible obstrucción en las líneas hidráulicas, degradación y aumento de viscosidad del fluido, o fricción mecánica excesiva en el pistón."
    )
    
    return steps, fig, interpretation

def solve_case_5(H, R, h0, a=0.005, C=0.6, g=9.8):
    """Caso 5: Torricelli en Tanque Cónico"""
    K_val = (C * a * np.sqrt(2 * g)) / (np.pi * (R/H)**2)
    t_end = (2/5) * (h0**(5/2)) / K_val
    
    steps = [
        r"**1. Relación Geométrica (Triángulos Semejantes):**",
        rf"$$ \frac{{r}}{{h}} = \frac{{R}}{{H}} = \frac{{{R}}}{{{H}}} \implies r = {R/H} h $$",
        r"$$ A(h) = \pi r^2 = \pi \left( \frac{R}{H} h \right)^2 $$",
        r"**2. Ley de Torricelli:**",
        r"$$ A(h) \frac{dh}{dt} = -a C \sqrt{2gh} $$",
        r"**3. Ecuación Diferencial en Variables Separables:**",
        r"$$ \pi \left( \frac{R}{H} \right)^2 h^2 \frac{dh}{dt} = -a C \sqrt{2gh} $$",
        r"$$ h^{3/2} dh = -\frac{a C \sqrt{2g}}{\pi (R/H)^2} dt $$",
        r"**4. Integración para obtener la familia de curvas:**",
        r"$$ \int h^{3/2} dh = \int -K dt \implies \frac{2}{5} h^{5/2} = -Kt + C_1 $$",
        r"$$ h(t) = \left( h_0^{5/2} - \frac{5}{2} K t \right)^{2/5} $$"
    ]

    t_vals = np.linspace(0, t_end, 200)
    h_vals = (h0**(5/2) - (5/2) * K_val * t_vals)**(2/5)
    # Rellenar NaNs por precisión de punto flotante cerca de cero
    h_vals = np.nan_to_num(h_vals, nan=0.0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', name='Nivel en Cono', line=dict(color='#8E24AA', width=3)))
    fig.update_layout(title="Geometría Cónica: Vaciado Acelerado", xaxis_title="Tiempo (min)", yaxis_title="Altura Química h(t) [m]", template="plotly_white")
    
    interpretation = (
        "**Interpretación Técnica:** A diferencia de un tanque cilíndrico, la ecuación diferencial para un cono invertido presenta un exponente $h^{3/2}$. "
        "Físicamente, a medida que el nivel desciende, el área transversal se reduce cuadráticamente. Esto provoca que la velocidad de caída de la altura de la columna líquida "
        "se vuelva extremadamente rápida hacia el final del vaciado. El diseño del algoritmo de control de dosificación debe compensar esta aceleración no lineal."
    )
    
    return steps, fig, interpretation
