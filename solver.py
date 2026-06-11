import numpy as np
import plotly.graph_objects as go

def solve_case_1(T0, Ta, T1, t1, T_target):
    """Ley de Enfriamiento de Newton"""
    # Calculo analitico
    k = -np.log((T1 - Ta) / (T0 - Ta)) / t1
    t_target = -np.log((T_target - Ta) / (T0 - Ta)) / k
    t_adicional = t_target - t1
    
    steps = [
        r"**1. Modelo:** $$\frac{dT}{dt}=-k(T-T_a)$$",
        r"**2. Solucion general:** $$T(t)=T_a+(T_0-T_a)e^{-kt}$$",
        rf"**3. Calculo de k:** $$k=-\frac{{\ln(75/125)}}{{10}} \approx {k:.4f}$$",
        rf"**4. Calculo del tiempo final:** $$t=\frac{{-\ln(15/125)}}{{{k:.4f}}} \approx {t_target:.2f} \text{{ min}}$$",
        rf"**Respuesta:** El tecnico debe esperar **{t_adicional:.2f} min** extra."
    ]

    t_vals = np.linspace(0, t_target + 10, 200)
    T_vals = Ta + (T0 - Ta) * np.exp(-k * t_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=T_vals, mode='lines', name='Enfriamiento'))
    fig.add_trace(go.Scatter(x=[0, t1, t_target], y=[T0, T1, T_target], mode='markers+text', 
                             text=['Inicio', 'Medicion 1', 'Punto Seguro'], textposition="top right"))
    fig.add_hline(y=Ta, line_dash="dash", line_color="blue", annotation_text="Temp. Ambiente")
    fig.update_layout(title="Perfil Termico", xaxis_title="Tiempo (min)", yaxis_title="Temperatura (C)")
    
    interpretation = "Interpretacion: Decaimiento exponencial. El enfriamiento inicial es rapido pero se ralentiza al acercarse a la temperatura ambiente."
    return steps, fig, interpretation


def solve_case_2(r, h0, a, C_factor, g=9.8):
    """Ley de Torricelli - Tanque Cilindrico"""
    A = np.pi * r**2
    K_val = (C_factor * a * np.sqrt(2 * g)) / A
    t_end = 2 * np.sqrt(h0) / K_val
    
    steps = [
        r"**1. Modelo:** $$A\frac{dh}{dt}=-Ca\sqrt{2gh}$$",
        r"**2. Variables separables:** $$\int h^{-1/2} dh = \int -K dt$$",
        rf"**3. Constante K:** $$K=\frac{{{C_factor} \times {a} \times \sqrt{{19.6}}}}{{\pi}} \approx {K_val:.5f}$$",
        rf"**4. Tiempo vaciado total:** $$t=\frac{{2\sqrt{{{h0}}}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{{ s}}$$",
        rf"**Respuesta:** El tanque tardara **{t_end/60:.2f} minutos** en vaciarse."
    ]

    t_vals = np.linspace(0, t_end, 200)
    h_vals = (np.sqrt(h0) - (K_val / 2) * t_vals)**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', name='Nivel'))
    fig.update_layout(title="Vaciado Hidrodinamico", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)")
    
    interpretation = "Interpretacion: El descenso no es lineal, forma una curva parabolica. Mayor presion hidrostatica inicial genera un drenaje mas veloz al comienzo."
    return steps, fig, interpretation


def solve_case_3(V, Q0, cin, rin, rout, t_target):
    """Mezclas - Volumen Constante"""
    factor = rout / V
    inflow = rin * cin
    Q_steady = (inflow * V) / rout
    Q_final = Q_steady + (Q0 - Q_steady) * np.exp(-factor * t_target)
    
    steps = [
        r"**1. Modelo:** $$\frac{dQ}{dt}=r_{in}c_{in} - r_{out}\frac{Q}{V}$$",
        rf"**2. Sustitucion:** $$\frac{dQ}{dt}=({rin})({cin}) - ({rout})\frac{Q}{{{V}}}$$",
        r"**3. EDO Lineal:** $$\frac{dQ}{dt} + 0.01Q = 1$$",
        rf"**4. Solucion general:** $$Q(t)={Q_steady:.1f}(1 - e^{{-0.01t}})$$",
        rf"**Respuesta:** A los {t_target} min, habra **{Q_final:.2f} kg** de desengrasante."
    ]

    t_vals = np.linspace(0, t_target + 30, 200)
    Q_vals = Q_steady + (Q0 - Q_steady) * np.exp(-factor * t_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=Q_vals, mode='lines', name='Desengrasante (kg)'))
    fig.add_hline(y=Q_steady, line_dash="dash", line_color="blue", annotation_text="Saturacion")
    fig.update_layout(title="Cinetica de Mezcla", xaxis_title="Tiempo (min)", yaxis_title="Cantidad (kg)")
    
    interpretation = "Interpretacion: Saturacion asintotica. Util para asegurar que el proceso de lavado comience cuando la mezcla alcance la concentracion homogenea esperada."
    return steps, fig, interpretation


def solve_case_4(t_test, y_test, tau_ideal, force=10):
    """Actuador Hidraulico"""
    tau_actual = -t_test / np.log(1 - (y_test / force))
    
    steps = [
        r"**1. Modelo Lineal:** $$\tau\frac{dy}{dt}+y=10$$",
        r"**2. Solucion:** $$y(t)=10(1-e^{-t/\tau})$$",
        rf"**3. Despeje de tau:** $$6.32 = 10(1-e^{{-{t_test}/\tau}})$$",
        rf"**4. Calculo tau real:** $$\tau \approx {tau_actual:.2f} \text{{ s}}$$",
        rf"**Respuesta:** El sistema tiene un retardo ($\tau={tau_actual:.2f} \text{{s}}$) que duplica el nominal ({tau_ideal}s)."
    ]

    t_vals = np.linspace(0, t_test * 2, 200)
    y_actual = force * (1 - np.exp(-t_vals / tau_actual))
    y_ideal = force * (1 - np.exp(-t_vals / tau_ideal))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=y_actual, mode='lines', name=f'Real (tau={tau_actual:.1f}s)'))
    fig.add_trace(go.Scatter(x=t_vals, y=y_ideal, mode='lines', name=f'Ideal (tau={tau_ideal}s)', line=dict(dash='dash')))
    fig.update_layout(title="Respuesta del Cilindro", xaxis_title="Tiempo (s)", yaxis_title="Posicion (cm)")
    
    interpretation = "Interpretacion: La constante real duplica a la ideal. El retraso extremo sugiere problemas como friccion excesiva, aceite degradado o fugas internas."
    return steps, fig, interpretation


def solve_case_5(H, R_top, h0, a=0.005, C_factor=0.6, g=9.8):
    """Torricelli - Tanque Conico"""
    # Relacion de semejanza: r/h = R/H => r = (R/H)*h
    K_val = (C_factor * a * np.sqrt(2 * g)) / (np.pi * (R_top/H)**2)
    t_end = (2/5) * (h0**(5/2)) / K_val
    
    steps = [
        r"**1. Semejanza de triangulos:** $$\frac{r}{h}=\frac{R}{H} \implies r=0.25h$$",
        r"**2. Area transversal:** $$A(h)=\pi(0.25h)^2=\frac{\pi}{16}h^2$$",
        r"**3. EDO Torricelli:** $$\frac{\pi}{16}h^2\frac{dh}{dt}=-Ca\sqrt{2gh}$$",
        r"**4. Separacion de variables:** $$h^{3/2}dh=-\frac{16Ca\sqrt{2g}}{\pi}dt$$",
        r"**5. Integral:** $$\frac{2}{5}h^{5/2}=-Kt+C_1$$"
    ]

    t_vals = np.linspace(0, t_end, 200)
    h_vals = (h0**(5/2) - (5/2) * K_val * t_vals)**(2/5)
    h_vals = np.nan_to_num(h_vals, nan=0.0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals/60, y=h_vals, mode='lines', fill='tozeroy', name='Nivel Cono'))
    fig.update_layout(title="Vaciado Tanque Conico", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)")
    
    interpretation = "Interpretacion: El vaciado se acelera de manera critica hacia el final debido a la reduccion cuadratica del area transversal."
    return steps, fig, interpretation
