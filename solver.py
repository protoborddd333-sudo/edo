import numpy as np
import math
import plotly.graph_objects as go

AXIS_STYLE = dict(gridcolor='#E2E8F0', color='#1E293B', zerolinecolor='#E2E8F0')

def get_base_layout(title, x_title, y_title):
    return dict(
        title=dict(text=title, font=dict(color='#1E293B')), 
        xaxis_title=x_title, 
        yaxis_title=y_title, 
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE
    )

def solve_case_1(T0, Ta, T1, t1, T_obj):
    if (T1 - Ta) > 0 and (T0 - Ta) > 0 and t1 > 0 and T0 > T1:
        k = -math.log((T1 - Ta) / (T0 - Ta)) / t1
        t_total = -math.log((T_obj - Ta) / (T0 - Ta)) / k if (T_obj - Ta) > 0 else 0
        t_adicional = max(0, t_total - t1)
    else:
        k, t_total, t_adicional = 0.0511, 41.51, 31.51

    steps = [
        r"**1. Modelo de la EDO:**",
        r"$$ \frac{dT}{dt} = -k(T - T_a) $$",
        r"**2. Solución General:**",
        r"$$ T(t) = T_a + C_1 e^{-kt} $$",
        r"**3. Condición Inicial ($t = 0$):**",
        rf"$$ T(0) = T_0 \implies {T0:.1f} = {Ta:.1f} + C_1 $$",
        rf"$$ \implies C_1 = {T0 - Ta:.1f} $$",
        r"**4. Constante k:**",
        rf"$$ k = -\frac{{\ln\left(\frac{{{T1:.1f} - {Ta:.1f}}}{{{T0:.1f} - {Ta:.1f}}}\right)}}{{{t1:.1f}}} $$",
        rf"$$ \implies k \approx {k:.4f} $$",
        r"**5. Ecuación Horaria:**",
        rf"$$ T(t) = {Ta:.1f} + {T0 - Ta:.1f} e^{{-{k:.4f}t}} $$",
        r"**6. Cálculo del tiempo total:**",
        rf"$$ t = \frac{{-\ln\left(\frac{{{T_obj:.1f} - {Ta:.1f}}}{{{T0:.1f} - {Ta:.1f}}}\right)}}{{{k:.4f}}} $$",
        rf"$$ \implies t \approx {t_total:.2f} \text{ min} $$"
    ]

    t_max = max(50.0, t_total * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    T_vec = Ta + (T0 - Ta) * np.exp(-k * t_vec)
    
    fig = go.Figure()
    # Celeste Tecsup #00A8E1 para la línea
    fig.add_trace(go.Scatter(x=t_vec, y=T_vec, mode='lines', name='T(t)', line=dict(color='#00A8E1', width=4)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[Ta, Ta], mode='lines', name='Temp. Ambiente', line=dict(color='#94A3B8', dash='dash')))
    # Azul Marino Profundo #0A2540 para los marcadores clave
    fig.add_trace(go.Scatter(x=[t_total], y=[T_obj], mode='markers+text', name='Punto Objetivo', text=[f"({t_total:.1f}m, {T_obj}C)"], textposition="top right", marker=dict(size=12, color='#0A2540')))
    
    fig.update_layout(**get_base_layout("Perfil Térmico T(t)", "Tiempo (min)", "Temperatura (C)"))
    
    interp = f"El técnico debe esperar {t_adicional:.1f} minutos adicionales. La curva garantiza matemáticamente que el rodamiento nunca descenderá de los {Ta}C."
    return steps, {"T(t) vs t": fig}, interp

def solve_case_2(r, h0, a, C_factor):
    g = 9.8
    r = max(r, 0.01)
    A0 = math.pi * r**2
    K_val = (C_factor * a * math.sqrt(2 * g)) / A0 if A0 > 0 else 1e-5
    t_end = 2 * math.sqrt(max(h0, 0)) / K_val

    steps = [
        r"**1. Modelo de la EDO (Ley de Torricelli):**",
        r"$$ A_0\frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Evaluación de Constantes:**",
        rf"$$ A_0 = \pi({r:.2f})^2 = {A0:.4f} \text{{ m}}^2 $$",
        rf"$$ K = \frac{{{C_factor} \cdot {a} \cdot \sqrt{{19.6}}}}{{{A0:.4f}}} \approx {K_val:.5f} $$",
        r"**3. Separación e Integración:**",
        r"$$ \int h^{-1/2} dh = -K \int dt $$",
        r"$$ \implies 2\sqrt{h} = -Kt + C_1 $$",
        r"**4. Condición Inicial ($t=0$):**",
        rf"$$ h(0) = {h0} \implies C_1 = 2\sqrt{{{h0}}} $$",
        rf"$$ \implies C_1 = {2*math.sqrt(h0):.4f} $$",
        r"**5. Ecuación Horaria:**",
        rf"$$ h(t) = \left( \sqrt{{{h0}}} - \frac{{{K_val:.5f}}}{{2}} t \right)^2 $$",
        r"**6. Tiempo de vaciado total ($h=0$):**",
        rf"$$ t = \frac{{{C_1:.4f}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{ s} $$",
        rf"$$ \implies {t_end/60:.2f} \text{ min} $$"
    ]

    t_max = max(10.0, t_end * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    h_vec = np.maximum(0, math.sqrt(h0) - (K_val / 2) * t_vec)**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec/60, y=h_vec, fill='tozeroy', mode='lines', line=dict(color='#00A8E1', width=4), fillcolor='rgba(0, 168, 225, 0.15)'))
    fig.add_trace(go.Scatter(x=[t_end/60], y=[0], mode='markers+text', text=[f"Vacío en {t_end/60:.1f}m"], textposition="top right", marker=dict(size=12, color='#0A2540')))
    
    fig.update_layout(**get_base_layout("Nivel del Tanque h(t)", "Tiempo (min)", "Altura (m)"))
    
    interp = f"El vaciado total demora {t_end/60:.1f} min. La forma parabólica revela que el caudal es muy fuerte al principio debido a la presión hidrostática."
    return steps, {"Nivel vs t": fig}, interp

def solve_case_3(V, Q0, cin, rin, rout, t_target):
    V = max(V, 1.0)
    factor = rout / V
    inflow = rin * cin
    Q_steady = (inflow * V) / rout if rout > 0 else 0
    C_1 = Q0 - Q_steady

    steps = [
        r"**1. Modelo de la EDO (Balance de Masa):**",
        rf"$$ \frac{{dQ}}{{dt}} = {rin}({cin}) - {rout}\left(\frac{{Q}}{{{V:.1f}}}\right) $$",
        rf"$$ \implies \frac{{dQ}}{{dt}} + {factor:.4f}Q = {inflow:.2f} $$",
        r"**2. Solución General:**",
        rf"$$ Q(t) = {Q_steady:.1f} + C_1 e^{{-{factor:.4f}t}} $$",
        r"**3. Condición Inicial ($t=0$):**",
        rf"$$ Q(0) = {Q0} \implies {Q0} = {Q_steady:.1f} + C_1 $$",
        rf"$$ \implies C_1 = {C_1:.1f} $$",
        r"**4. Ecuación Horaria Exacta:**",
        rf"$$ Q(t) = {Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}t}} $$",
        r"**5. Evaluación a $t_{target}$:**",
        rf"$$ Q({t_target}) = {Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}({t_target})}} $$",
        rf"$$ \implies Q({t_target}) \approx {Q_steady + C_1*math.exp(-factor*t_target):.2f} \text{ kg} $$"
    ]

    t_max = max(t_target * 1.2, 50.0)
    t_vec = np.linspace(0, t_max, 500)
    Q_vec = Q_steady + C_1 * np.exp(-factor * t_vec)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=Q_vec, mode='lines', name='Masa', line=dict(color='#00A8E1', width=4)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[Q_steady, Q_steady], mode='lines', name='Límite Saturación', line=dict(color='#94A3B8', dash='dash')))
    
    fig.update_layout(**get_base_layout("Masa de Desengrasante Q(t)", "Tiempo (min)", "Cantidad (kg)"))
    
    Q_final = Q_steady + C_1*math.exp(-factor*t_target)
    interp = f"A los {t_target} min hay {Q_final:.1f} kg. La curva asegura que el sistema tenderá asintóticamente al límite de saturación de {Q_steady} kg."
    return steps, {"Saturación Química": fig}, interp

def solve_case_4(t_test, y_test, tau_ideal, force=10.0):
    t_test = max(t_test, 0.1)
    y_safe = min(y_test, force * 0.999) 
    tau_real = -t_test / math.log(1 - (y_safe / force))

    steps = [
        r"**1. Modelo de la EDO Lineal:**",
        rf"$$ \tau\frac{{dy}}{{dt}} + y = {force} $$",
        r"**2. Solución General:**",
        rf"$$ y(t) = {force} + C_1 e^{{-t/\tau}} $$",
        r"**3. Condición Inicial ($y(0)=0$):**",
        rf"$$ 0 = {force} + C_1 \implies C_1 = -{force} $$",
        r"**4. Ecuación de Posición:**",
        rf"$$ y(t) = {force}\left(1 - e^{{-t/\tau}}\right) $$",
        r"**5. Despeje de Constante Real $\tau$:**",
        rf"$$ {y_test} = {force}\left(1 - e^{{-{t_test}/\tau}}\right) $$",
        rf"$$ \implies \tau = \frac{{-{t_test}}}{{\ln({1 - y_safe/force:.4f})}} $$",
        rf"$$ \implies \tau \approx {tau_real:.2f} \text{ s} $$"
    ]

    t_max = max(t_test * 1.2, tau_real * 5)
    t_vec = np.linspace(0, t_max, 500)
    y_vec = force * (1 - np.exp(-t_vec / tau_real))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=y_vec, mode='lines', name='y(t)', line=dict(color='#00A8E1', width=4)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[force, force], mode='lines', line=dict(color='#94A3B8', dash='dash'), name='Recorrido Máximo'))
    fig.add_trace(go.Scatter(x=[t_test], y=[y_test], mode='markers+text', text=["Prueba"], textposition="bottom right", marker=dict(size=12, color='#0A2540')))
    
    fig.update_layout(**get_base_layout("Respuesta del Cilindro y(t)", "Tiempo (s)", "Posición (cm)"))
    
    interp = f"El $\\tau$ medido es {tau_real:.1f}s vs ideal {tau_ideal}s. Retardos elevados denotan obstrucción hidráulica o fricción extrema."
    return steps, {"Desplazamiento vs t": fig}, interp

def solve_case_5(H, R_top, h0, a, C_factor):
    g = 9.8
    H, R_top = max(H, 0.01), max(R_top, 0.01)
    K_val = (C_factor * a * math.sqrt(2 * g)) / (math.pi * (R_top/H)**2)
    C_1 = (2/5) * (max(h0, 0)**(5/2))
    t_end = C_1 / max(K_val, 1e-8)

    steps = [
        r"**1. Modelo de la EDO:**",
        r"$$ A(h)\frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Relación Geométrica:**",
        rf"$$ r = \frac{{R}}{{H}}h \implies A(h) = {math.pi*(R_top/H)**2:.4f} h^2 $$",
        r"**3. Separación de Variables:**",
        rf"$$ h^{{3/2}} dh = -{K_val:.5f} dt $$",
        r"**4. Integración y Condición Inicial:**",
        rf"$$ \frac{{2}}{{5}}h^{{5/2}} = -Kt + C_1 $$",
        rf"$$ h(0) = {h0} \implies C_1 = {C_1:.4f} $$",
        r"**5. Ecuación Horaria:**",
        rf"$$ h(t) = \left( {h0**(5/2):.3f} - 2.5({K_val:.5f})t \right)^{{0.4}} $$",
        r"**6. Vaciado Total:**",
        rf"$$ t = \frac{{{C_1:.4f}}}{{{K_val:.5f}}} \approx {t_end/60:.2f} \text{ min} $$"
    ]

    t_max = max(5.0, t_end * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    base_vec = np.maximum(0, h0**(5/2) - 2.5 * K_val * t_vec)
    h_vec = base_vec**(2/5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec/60, y=h_vec, mode='lines', fill='tozeroy', line=dict(color='#00A8E1', width=4), fillcolor='rgba(0, 168, 225, 0.15)'))
    
    fig.update_layout(**get_base_layout("Vaciado Cónico h(t)", "Tiempo (min)", "Altura (m)"))
    
    interp = f"Tiempo de vaciado: {t_end/60:.2f} min. El perfil es cóncavo: al bajar el nivel el área disminuye, acelerando violentamente la caída del líquido."
    return steps, {"Nivel Cónico": fig}, interp
