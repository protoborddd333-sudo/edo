import numpy as np
import plotly.graph_objects as go

def solve_case_1(T0, Ta, T1, t1, T_target):
    """Ley de Enfriamiento de Newton"""
    t1 = max(t1, 1e-5)
    T0 = max(T0, Ta + 0.1)
    T1 = max(min(T1, T0 - 0.1), Ta + 0.1)
    T_target = max(T_target, Ta + 0.1)

    k = -np.log((T1 - Ta) / (T0 - Ta)) / t1
    k = max(k, 1e-5)
    t_target_calc = -np.log((T_target - Ta) / (T0 - Ta)) / k
    t_adicional = max(t_target_calc - t1, 0)
    
    # Falla 1 y 3 Corregidas: Simbólico -> Numérico -> Cierre Analítico
    steps = [
        r"**1. Modelo Simbólico:** $$\frac{dT}{dt}=-k(T-T_a)$$",
        r"**2. Solución General:** $$T(t)=T_a+C_1 e^{-kt}$$",
        rf"**3. Condición Inicial ($t=0$):** $$T(0)=T_0 \implies {T0} = {Ta} + C_1 \implies C_1 = {T0 - Ta:.2f}$$",
        rf"**4. Constante $k$:** $$k=-\frac{{\ln((T_1-T_a)/(T_0-T_a))}}{{t_1}} \implies k = {k:.4f}$$",
        rf"**5. Ecuación Horaria:** $$T(t)={Ta} + {T0 - Ta:.2f} e^{{-{k:.4f}t}}$$",
        rf"**6. Cálculo del tiempo:** $$t=\frac{{-\ln(({T_target}-{Ta})/({T0}-{Ta}))}}{{{k:.4f}}} \approx {t_target_calc:.2f} \text{{ min}}$$"
    ]

    t_vals = np.linspace(0, t_target_calc + 10, 200)
    T_vals = Ta + (T0 - Ta) * np.exp(-k * t_vals)
    dT_dt = -k * (T0 - Ta) * np.exp(-k * t_vals)
    
    # Falla 4 Corregida: Múltiples curvas operativas
    fig_T = go.Figure(go.Scatter(x=t_vals, y=T_vals, mode='lines', line=dict(color='red', width=3)))
    fig_T.add_hline(y=Ta, line_dash="dash", line_color="blue", annotation_text=f"Temp. Ambiente ({Ta}°C)")
    fig_T.update_layout(title="Perfil Térmico T(t)", xaxis_title="Tiempo (min)", yaxis_title="Temperatura (°C)", template="plotly_white")
    
    fig_rate = go.Figure(go.Scatter(x=t_vals, y=dT_dt, mode='lines', line=dict(color='orange', width=3)))
    fig_rate.update_layout(title="Tasa de Enfriamiento dT/dt", xaxis_title="Tiempo (min)", yaxis_title="Tasa (°C/min)", template="plotly_white")

    # Falla 2 Corregida: Análisis dinámico
    if t_adicional > 0:
        interp = f"Dado que el tiempo total de enfriamiento es de {t_target_calc:.1f} min, el operador DEBE ESPERAR {t_adicional:.1f} minutos adicionales. La tasa de pérdida de calor arranca bruscamente en {abs(dT_dt[0]):.1f} °C/min y decae rápidamente."
    else:
        interp = f"El rodamiento ya ha alcanzado la temperatura segura de {T_target}°C. Es seguro que los técnicos inicien el mantenimiento inmediatamente."

    return steps, {"T(t)": fig_T, "Tasa Pérdida Calor": fig_rate}, interp


def solve_case_2(r, h0, a, C_factor, g=9.8):
    """Ley de Torricelli - Tanque Cilíndrico"""
    r = max(r, 1e-5)
    h0 = max(h0, 0.0)
    
    A = np.pi * r**2
    K_val = (C_factor * a * np.sqrt(2 * g)) / A
    t_end = 2 * np.sqrt(h0) / max(K_val, 1e-8)
    
    steps = [
        r"**1. Modelo Simbólico:** $$A_0\frac{dh}{dt}=-C a \sqrt{2gh}$$",
        r"**2. Separación de Variables:** $$\int h^{-1/2} dh = -\frac{C a \sqrt{2g}}{A_0} \int dt = -K \int dt$$",
        rf"**3. Evaluación de Constantes:** $$A_0 = \pi({r})^2 = {A:.4f} \text{{ m}}^2 \implies K = {K_val:.5f}$$",
        r"**4. Integración y Despeje:** $$2\sqrt{h} = -Kt + C_1$$",
        rf"**5. Condición Inicial ($t=0$):** $$h(0)={h0} \implies C_1 = 2\sqrt{{{h0}}} = {2*np.sqrt(h0):.4f}$$",
        rf"**6. Ecuación Horaria:** $$h(t) = \left( \sqrt{{{h0}}} - \frac{{{K_val:.5f}}}{{2}} t \right)^2$$"
    ]

    t_vals = np.linspace(0, t_end, 200)
    h_vals = np.maximum(0, np.sqrt(h0) - (K_val / 2) * t_vals)**2
    Q_vals = C_factor * a * np.sqrt(2 * g * h_vals) * 1000 # Caudal en L/s
    
    fig_h = go.Figure(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', line=dict(color='#FFB300', width=3)))
    fig_h.update_layout(title="Vaciado Hidrodinámico h(t)", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)", template="plotly_white")
    
    fig_q = go.Figure(go.Scatter(x=t_vals/60, y=Q_vals, mode='lines', line=dict(color='#1E88E5', width=3)))
    fig_q.update_layout(title="Caudal de Drenaje Q(t)", xaxis_title="Tiempo (min)", yaxis_title="Caudal (L/s)", template="plotly_white")
    
    t_min = t_end/60
    interp = f"El tiempo total para el drenaje del aceite es de {t_min:.1f} minutos. El caudal de salida es máximo al inicio ({Q_vals[0]:.1f} L/s) y decrece linealmente. Esto asegura que la presión sobre las válvulas de desfogue disminuya conforme avanza el proceso."

    return steps, {"Altura vs Tiempo": fig_h, "Caudal vs Tiempo": fig_q}, interp


def solve_case_3(V, Q0, cin, rin, rout, t_target):
    """Mezclas - Volumen Constante"""
    V = max(V, 1e-5)
    factor = rout / V
    inflow = rin * cin
    Q_steady = (inflow * V) / rout if rout > 0 else 0
    C_1 = Q0 - Q_steady
    Q_final = Q_steady + C_1 * np.exp(-factor * t_target)
    
    steps = [
        r"**1. Modelo Simbólico:** $$\frac{dQ}{dt}=r_{in}c_{in} - r_{out}\frac{Q}{V}$$",
        rf"**2. EDO Lineal Numérica:** $$\frac{{dQ}}{{dt}} + \left(\frac{{{rout}}}{{{V}}}\right)Q = {inflow:.2f}$$",
        rf"**3. Solución General:** $$Q(t) = {Q_steady:.1f} + C_1 e^{{-{factor:.4f}t}}$$",
        rf"**4. Condición Inicial ($t=0$):** $$Q(0)={Q0} \implies C_1 = {Q0} - {Q_steady:.1f} = {C_1:.1f}$$",
        rf"**5. Ecuación Horaria:** $$Q(t)={Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}t}}$$"
    ]

    t_vals = np.linspace(0, max(t_target * 1.5, 60), 200)
    Q_vals = Q_steady + C_1 * np.exp(-factor * t_vals)
    Conc_vals = Q_vals / V
    
    fig_q = go.Figure(go.Scatter(x=t_vals, y=Q_vals, mode='lines', line=dict(color='green', width=3)))
    fig_q.add_hline(y=Q_steady, line_dash="dash", line_color="black")
    fig_q.update_layout(title="Masa Químico Q(t)", xaxis_title="Tiempo (min)", yaxis_title="Cantidad (kg)", template="plotly_white")
    
    fig_c = go.Figure(go.Scatter(x=t_vals, y=Conc_vals, mode='lines', line=dict(color='purple', width=3)))
    fig_c.update_layout(title="Concentración en Tanque c(t)", xaxis_title="Tiempo (min)", yaxis_title="Concentración (kg/L)", template="plotly_white")
    
    c_final = Q_final / V
    if c_final >= (cin * 0.95):
        interp = f"A los {t_target} min, la mezcla ha alcanzado un estado casi estacionario con {Q_final:.1f} kg. La concentración actual es de {c_final:.3f} kg/L, óptima para el proceso de lavado."
    else:
        interp = f"A los {t_target} min, la mezcla contiene {Q_final:.1f} kg y una concentración de {c_final:.3f} kg/L. El proceso AÚN SE ENCUENTRA EN ESTADO TRANSITORIO; no iniciar el lavado hasta alcanzar la saturación de {cin} kg/L."

    return steps, {"Masa Química": fig_q, "Concentración": fig_c}, interp


def solve_case_4(t_test, y_test, tau_ideal, force=10.0):
    """Actuador Hidráulico"""
    t_test = max(t_test, 1e-5)
    y_test_safe = min(y_test, force * 0.999) 
    tau_actual = max(-t_test / np.log(1 - (y_test_safe / force)), 1e-5)
    
    steps = [
        rf"**1. Modelo Simbólico:** $$\tau\frac{{dy}}{{dt}}+y = F_0$$",
        r"**2. Solución General:** $$y(t) = F_0 + C_1 e^{-t/\tau}$$",
        rf"**3. Condición Inicial ($t=0$):** $$y(0)=0 \implies 0 = {force} + C_1 \implies C_1 = -{force}$$",
        rf"**4. Ecuación Posición:** $$y(t)={force}(1-e^{{-t/\tau}})$$",
        rf"**5. Despeje de $\tau$ real:** $${y_test} = {force}(1-e^{{-{t_test}/\tau}}) \implies \tau \approx {tau_actual:.2f} \text{{ s}}$$"
    ]

    t_vals = np.linspace(0, max(t_test * 2, tau_actual * 4), 200)
    y_actual = force * (1 - np.exp(-t_vals / tau_actual))
    v_actual = (force / tau_actual) * np.exp(-t_vals / tau_actual)
    
    fig_y = go.Figure(go.Scatter(x=t_vals, y=y_actual, mode='lines', name=f'Real', line=dict(color='red', width=3)))
    fig_y.update_layout(title="Desplazamiento del Vástago y(t)", xaxis_title="Tiempo (s)", yaxis_title="Posición (cm)", template="plotly_white")

    fig_v = go.Figure(go.Scatter(x=t_vals, y=v_actual, mode='lines', line=dict(color='teal', width=3)))
    fig_v.update_layout(title="Velocidad del Pistón v(t)", xaxis_title="Tiempo (s)", yaxis_title="Velocidad (cm/s)", template="plotly_white")
    
    ratio = tau_actual / tau_ideal
    if ratio > 1.5:
        interp = f"¡ALERTA DE MANTENIMIENTO! El $\\tau$ real es de {tau_actual:.1f}s frente a un ideal de {tau_ideal}s (Desviación del {(ratio-1)*100:.0f}%). El retraso crítico sugiere desgaste severo, fricción excesiva del pistón o fluido hidráulico degradado."
    else:
        interp = f"El $\\tau$ real del cilindro es de {tau_actual:.1f}s. Se encuentra dentro de márgenes operativos aceptables respecto al ideal de {tau_ideal}s. El actuador responde con normalidad."

    return steps, {"Desplazamiento": fig_y, "Velocidad Interna": fig_v}, interp


def solve_case_5(H, R_top, h0, a=0.005, C_factor=0.6, g=9.8):
    """Torricelli - Tanque Cónico"""
    H = max(H, 1e-5)
    R_top = max(R_top, 1e-5)
    h0 = max(h0, 0.0)
    
    K_val = (C_factor * a * np.sqrt(2 * g)) / (np.pi * (R_top/H)**2)
    t_end = (2/5) * (h0**(5/2)) / max(K_val, 1e-8)
    C_1 = (2/5) * (h0**(5/2))
    
    steps = [
        rf"**1. Simetría Cónica:** $$\frac{{r}}{{h}}=\frac{{R}}{{H}} \implies r(h) = \left(\frac{{{R_top}}}{{{H}}}\right)h = {R_top/H:.2f}h$$",
        rf"**2. Área Variables:** $$A(h) = \pi r^2 = \pi \left(\frac{{{R_top}}}{{{H}}}\right)^2 h^2 = {np.pi*(R_top/H)**2:.4f} h^2$$",
        r"**3. EDO Torricelli:** $$A(h)\frac{dh}{dt} = -C a \sqrt{2gh}$$",
        rf"**4. Separación:** $$h^{{3/2}} dh = -\frac{{C a \sqrt{{2g}}}}{{\pi (R/H)^2}} dt = -{K_val:.5f} dt$$",
        r"**5. Integración:** $$\frac{2}{5}h^{5/2} = -Kt + C_1$$",
        rf"**6. Condición Inicial:** $$h(0)={h0} \implies C_1 = \frac{{2}}{{5}}({h0})^{{5/2}} = {C_1:.4f}$$",
        rf"**7. Ecuación Horaria:** $$h(t) = \left( {h0**(5/2):.3f} - \frac{{5}}{{2}}({K_val:.5f})t \right)^{{2/5}}$$"
    ]

    t_vals = np.linspace(0, t_end, 200)
    base_vals = np.maximum(0, h0**(5/2) - (5/2) * K_val * t_vals)
    h_vals = base_vals**(2/5)
    
    # Calcular velocidad de descenso de altura dh/dt = -Ca_sqrt(2gh)/A(h)
    A_h_vals = np.maximum(np.pi * (R_top/H)**2 * h_vals**2, 1e-5)
    dh_dt = - (C_factor * a * np.sqrt(2 * g * h_vals)) / A_h_vals
    
    fig_h = go.Figure(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', line=dict(color='purple', width=3)))
    fig_h.update_layout(title="Nivel en Cono h(t)", xaxis_title="Tiempo (min)", yaxis_title="Altura Química (m)", template="plotly_white")
    
    fig_dh = go.Figure(go.Scatter(x=t_vals/60, y=abs(dh_dt), mode='lines', line=dict(color='red', width=3)))
    fig_dh.update_layout(title="Tasa de Caída de Nivel |dh/dt|", xaxis_title="Tiempo (min)", yaxis_title="Velocidad Nivel (m/s)", template="plotly_white")
    
    interp = f"Tiempo de vaciado: {t_end/60:.2f} min. Dado que el radio disminuye junto con la altura (Perfil Cónico), el sistema presenta una no-linealidad extrema: al inicio el nivel cae a {abs(dh_dt[0]):.4f} m/s, pero hacia el final del proceso, la contracción del área acelera violentamente la caída del líquido."

    return steps, {"Altura vs Tiempo": fig_h, "Aceleración Vaciado": fig_dh}, interp
