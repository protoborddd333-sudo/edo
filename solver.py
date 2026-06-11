import numpy as np
import plotly.graph_objects as go

def solve_case_1(T0, Ta, T1, t1, T_target):
    """Ley de Enfriamiento de Newton"""
    # Protecciones matematicas para evitar log(<=0) o div/0
    t1 = max(t1, 1e-5)
    T0 = max(T0, Ta + 0.1)
    T1 = max(min(T1, T0 - 0.1), Ta + 0.1)
    T_target = max(T_target, Ta + 0.1)

    # Calculo analitico
    k = -np.log((T1 - Ta) / (T0 - Ta)) / t1
    k = max(k, 1e-5) # Evitar division por cero posterior
    t_target_calc = -np.log((T_target - Ta) / (T0 - Ta)) / k
    t_adicional = max(t_target_calc - t1, 0)
    
    steps = [
        r"**1. Modelo:** $$\frac{dT}{dt}=-k(T-T_a)$$",
        r"**2. Solucion general:** $$T(t)=T_a+(T_0-T_a)e^{-kt}$$",
        rf"**3. Calculo de k:** $$k=-\frac{{\ln({T1-Ta:.1f}/{T0-Ta:.1f})}}{{{t1:.1f}}} \approx {k:.4f}$$",
        rf"**4. Tiempo final ($40^\circ C$):** $$t=\frac{{-\ln({T_target-Ta:.1f}/{T0-Ta:.1f})}}{{{k:.4f}}} \approx {t_target_calc:.2f} \text{{ min}}$$",
        rf"**Respuesta:** El tecnico debe esperar **{t_adicional:.2f} min** extra."
    ]

    t_vals = np.linspace(0, t_target_calc + 10, 200)
    T_vals = Ta + (T0 - Ta) * np.exp(-k * t_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=T_vals, mode='lines', name='Enfriamiento', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=[0, t1, t_target_calc], y=[T0, T1, T_target], mode='markers+text', 
                             text=['Inicio', 'Medicion 1', 'Punto Seguro'], textposition="top right", marker=dict(size=10, color='black')))
    fig.add_hline(y=Ta, line_dash="dash", line_color="blue", annotation_text="Temp. Ambiente")
    fig.update_layout(title="Perfil Termico", xaxis_title="Tiempo (min)", yaxis_title="Temperatura (C)", template="plotly_white")
    
    interpretation = "Interpretacion: Decaimiento exponencial. El enfriamiento inicial es rapido pero se ralentiza al acercarse a la temperatura ambiente asintoticamente."
    return steps, fig, interpretation


def solve_case_2(r, h0, a, C_factor, g=9.8):
    """Ley de Torricelli - Tanque Cilindrico"""
    # Proteccion division por cero
    r = max(r, 1e-5)
    h0 = max(h0, 0.0)
    
    A = np.pi * r**2
    K_val = (C_factor * a * np.sqrt(2 * g)) / A
    t_end = 2 * np.sqrt(h0) / max(K_val, 1e-8)
    
    steps = [
        r"**1. Modelo:** $$A\frac{dh}{dt}=-Ca\sqrt{2gh}$$",
        r"**2. Variables separables:** $$\int h^{-1/2} dh = \int -K dt$$",
        rf"**3. Constante K:** $$K=\frac{{{C_factor} \times {a} \times \sqrt{{19.6}}}}{{\pi({r:.1f})^2}} \approx {K_val:.5f}$$",
        rf"**4. Tiempo vaciado total:** $$t=\frac{{2\sqrt{{{h0}}}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{{ s}}$$",
        rf"**Respuesta:** El tanque tardara **{t_end/60:.2f} minutos** en vaciarse."
    ]

    t_vals = np.linspace(0, t_end, 200)
    h_vals = np.maximum(0, np.sqrt(h0) - (K_val / 2) * t_vals)**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', name='Nivel', line=dict(color='#FFB300', width=3)))
    fig.update_layout(title="Vaciado Hidrodinamico", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)", template="plotly_white")
    
    interpretation = "Interpretacion: El descenso no es lineal, forma una curva parabolica. La mayor presion hidrostatica inicial genera un drenaje mas veloz al comienzo."
    return steps, fig, interpretation


def solve_case_3(V, Q0, cin, rin, rout, t_target):
    """Mezclas - Volumen Constante"""
    V = max(V, 1e-5) # Evitar div/0
    factor = rout / V
    inflow = rin * cin
    Q_steady = (inflow * V) / rout if rout > 0 else 0
    Q_final = Q_steady + (Q0 - Q_steady) * np.exp(-factor * t_target)
    
    steps = [
        r"**1. Modelo:** $$\frac{dQ}{dt}=r_{in}c_{in} - r_{out}\frac{Q}{V}$$",
        rf"**2. Sustitucion:** $$\frac{dQ}{dt}=({rin})({cin}) - ({rout})\frac{{Q}}{{{V:.1f}}}$$",
        rf"**3. EDO Lineal:** $$\frac{dQ}{dt} + {factor:.4f}Q = {inflow:.2f}$$",
        rf"**4. Solucion general:** $$Q(t)={Q_steady:.1f} + ({Q0 - Q_steady:.1f})e^{{-{factor:.4f}t}}$$",
        rf"**Respuesta:** A los {t_target} min, habra **{Q_final:.2f} kg** de desengrasante."
    ]

    t_vals = np.linspace(0, max(t_target + 30, 100), 200)
    Q_vals = Q_steady + (Q0 - Q_steady) * np.exp(-factor * t_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=Q_vals, mode='lines', name='Desengrasante (kg)', line=dict(color='green', width=3)))
    fig.add_trace(go.Scatter(x=[t_target], y=[Q_final], mode='markers+text', text=[f'{Q_final:.2f} kg'], textposition="bottom right", marker=dict(size=10, color='black')))
    fig.add_hline(y=Q_steady, line_dash="dash", line_color="blue", annotation_text="Saturacion (Estacionario)")
    fig.update_layout(title="Cinetica de Mezcla", xaxis_title="Tiempo (min)", yaxis_title="Cantidad (kg)", template="plotly_white")
    
    interpretation = "Interpretacion: Saturacion asintotica. Util para asegurar que el proceso de lavado comience cuando la mezcla alcance la concentracion homogenea esperada."
    return steps, fig, interpretation


def solve_case_4(t_test, y_test, tau_ideal, force=10.0):
    """Actuador Hidraulico"""
    t_test = max(t_test, 1e-5)
    # Limitar y_test para evitar math domain error en log(<=0)
    y_test_safe = min(y_test, force * 0.999) 
    
    tau_actual = -t_test / np.log(1 - (y_test_safe / force))
    tau_actual = max(tau_actual, 1e-5)
    
    steps = [
        rf"**1. Modelo Lineal:** $$\tau\frac{{dy}}{{dt}}+y={force}$$",
        rf"**2. Solucion:** $$y(t)={force}(1-e^{{-t/\tau}})$$",
        rf"**3. Despeje de tau:** $${y_test} = {force}(1-e^{{-{t_test}/\tau}})$$",
        rf"**4. Calculo tau real:** $$\tau \approx {tau_actual:.2f} \text{{ s}}$$",
        rf"**Respuesta:** El sistema tiene un retardo ($\tau={tau_actual:.2f} \text{{s}}$) frente al nominal ({tau_ideal}s)."
    ]

    t_vals = np.linspace(0, max(t_test * 2, tau_actual * 4), 200)
    y_actual = force * (1 - np.exp(-t_vals / tau_actual))
    y_ideal = force * (1 - np.exp(-t_vals / tau_ideal))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=y_actual, mode='lines', name=f'Real (tau={tau_actual:.1f}s)', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=t_vals, y=y_ideal, mode='lines', name=f'Ideal (tau={tau_ideal}s)', line=dict(color='green', width=2, dash='dash')))
    fig.update_layout(title="Respuesta del Cilindro", xaxis_title="Tiempo (s)", yaxis_title="Posicion (cm)", template="plotly_white")
    
    interpretation = "Interpretacion: La constante real determina la inercia del sistema. Un retraso excesivo sugiere problemas graves de mantenimiento como friccion excesiva, aceite degradado o fugas internas en el cilindro."
    return steps, fig, interpretation


def solve_case_5(H, R_top, h0, a=0.005, C_factor=0.6, g=9.8):
    """Torricelli - Tanque Conico"""
    H = max(H, 1e-5)
    R_top = max(R_top, 1e-5)
    h0 = max(h0, 0.0)
    
    K_val = (C_factor * a * np.sqrt(2 * g)) / (np.pi * (R_top/H)**2)
    t_end = (2/5) * (h0**(5/2)) / max(K_val, 1e-8)
    
    steps = [
        rf"**1. Semejanza de triangulos:** $$\frac{{r}}{{h}}=\frac{{{R_top}}}{{{H}}} \implies r={R_top/H:.2f}h$$",
        rf"**2. Area transversal:** $$A(h)=\pi({R_top/H:.2f}h)^2={np.pi*(R_top/H)**2:.4f}h^2$$",
        rf"**3. EDO Torricelli:** $${np.pi*(R_top/H)**2:.4f}h^2\frac{{dh}}{{dt}}=-Ca\sqrt{{2gh}}$$",
        r"**4. Separacion de variables:** $$h^{3/2}dh=-K dt$$",
        r"**5. Integral:** $$\frac{2}{5}h^{5/2}=-Kt+C_1$$"
    ]

    t_vals = np.linspace(0, t_end, 200)
    # np.maximum es critico aqui para evitar raices fraccionarias de numeros negativos microscopicos
    base_vals = np.maximum(0, h0**(5/2) - (5/2) * K_val * t_vals)
    h_vals = base_vals**(2/5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', name='Nivel Cono', line=dict(color='purple', width=3)))
    fig.update_layout(title="Vaciado Tanque Conico", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)", template="plotly_white")
    
    interpretation = "Interpretacion: El vaciado se acelera de manera critica hacia el final debido a la reduccion cuadratica del area transversal en la parte inferior del cono."
    return steps, fig, interpretation
