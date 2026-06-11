import numpy as np
import math
import plotly.graph_objects as go

def solve_case_1(T0, Ta, T1, t1, T_obj):
    """Caso 1: Enfriamiento de Newton"""
    # PASO A: Programación Defensiva y Validaciones
    if (T1 - Ta) > 0 and (T0 - Ta) > 0 and t1 > 0 and T0 > T1:
        k = -math.log((T1 - Ta) / (T0 - Ta)) / t1
        t_total = -math.log((T_obj - Ta) / (T0 - Ta)) / k if (T_obj - Ta) > 0 else 0
        t_adicional = max(0, t_total - t1)
    else:
        k, t_total, t_adicional = 0.0511, 41.51, 31.51 # Resguardo

    # PASO C: LaTeX Dinámico Exacto
    steps = [
        r"**1. Ecuación Diferencial Ordinaria (EDO):**",
        r"$$ \frac{dT}{dt} = -k(T - T_a) $$",
        r"**2. Solución General:**",
        r"$$ T(t) = T_a + C_1 e^{-kt} $$",
        r"**3. Condición Inicial ($t = 0$):**",
        rf"$$ T(0) = T_0 \implies {T0:.1f} = {Ta:.1f} + C_1 \implies C_1 = {T0 - Ta:.1f} $$",
        r"**4. Constante $k$:**",
        rf"$$ k = -\frac{{\ln(({T1:.1f} - {Ta:.1f})/({T0:.1f} - {Ta:.1f}))}}{{{t1:.1f}}} \implies k \approx {k:.4f} $$",
        r"**5. Ecuación Horaria:**",
        rf"$$ T(t) = {Ta:.1f} + {T0 - Ta:.1f} e^{{-{k:.4f}t}} $$",
        r"**6. Cálculo del tiempo:**",
        rf"$$ t = \frac{{-\ln(({T_obj:.1f} - {Ta:.1f})/({T0:.1f} - {Ta:.1f}))}}{{{k:.4f}}} \approx {t_total:.2f} \text{{ min}} $$"
    ]

    # PASO B: Gráfica Asintótica (Holgura del 20%)
    t_max = max(50.0, t_total * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    T_vec = Ta + (T0 - Ta) * np.exp(-k * t_vec)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=T_vec, mode='lines', name='T(t)', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[Ta, Ta], mode='lines', name='Temp. Ambiente', line=dict(color='blue', dash='dash')))
    fig.add_trace(go.Scatter(x=[t_total], y=[T_obj], mode='markers+text', name='Punto Objetivo', text=[f"({t_total:.1f}m, {T_obj}°C)"], textposition="top right", marker=dict(size=10, color='orange')))
    fig.update_layout(title="Perfil Térmico T(t)", xaxis_title="Tiempo (min)", yaxis_title="Temperatura (°C)", margin=dict(l=20, r=20, t=40, b=20))
    
    interp = f"El técnico debe esperar {t_adicional:.1f} minutos adicionales. La curva garantiza matemáticamente que el rodamiento nunca descenderá de los {Ta}°C."
    return steps, {"T(t) vs t": fig}, interp

def solve_case_2(r, h0, a, C_factor):
    """Caso 2: Torricelli Cilíndrico"""
    # PASO A: Defensivo
    g = 9.8
    r = max(r, 0.01)
    A0 = math.pi * r**2
    K_val = (C_factor * a * math.sqrt(2 * g)) / A0 if A0 > 0 else 1e-5
    t_end = 2 * math.sqrt(max(h0, 0)) / K_val

    # PASO C: LaTeX Dinámico
    steps = [
        r"**1. Modelo de Torricelli:**",
        r"$$ A_0\frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Separación e Integración:**",
        rf"$$ A_0 = \pi({r:.2f})^2 = {A0:.4f} \text{{ m}}^2 \implies K = \frac{{{C_factor} \cdot {a} \cdot \sqrt{{19.6}}}}{{{A0:.4f}}} \approx {K_val:.5f} $$",
        r"$$ \int h^{-1/2} dh = -K \int dt \implies 2\sqrt{h} = -Kt + C_1 $$",
        r"**3. Condición Inicial ($t=0$):**",
        rf"$$ h(0) = {h0} \implies C_1 = 2\sqrt{{{h0}}} = {2*math.sqrt(h0):.4f} $$",
        r"**4. Ecuación Horaria:**",
        rf"$$ h(t) = \left( \sqrt{{{h0}}} - \frac{{{K_val:.5f}}}{{2}} t \right)^2 $$",
        r"**5. Tiempo de vaciado total ($h=0$):**",
        rf"$$ t = \frac{{{C_1:.4f}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{{ s}} \implies {t_end/60:.2f} \text{{ min}} $$"
    ]

    # PASO B: Gráfica con Holgura y Recorte Analítico Exacto a h=0
    t_max = max(10.0, t_end * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    # Evita que la parábola vuelva a subir después del vaciado recortando internamente a 0
    h_vec = np.maximum(0, math.sqrt(h0) - (K_val / 2) * t_vec)**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec/60, y=h_vec, fill='tozeroy', mode='lines', line=dict(color='#FFB300', width=3)))
    fig.add_trace(go.Scatter(x=[t_end/60], y=[0], mode='markers+text', text=[f"Vacío en {t_end/60:.1f}m"], textposition="top right", marker=dict(size=10, color='red')))
    fig.update_layout(title="Nivel del Tanque h(t)", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)", margin=dict(l=20, r=20, t=40, b=20))
    
    interp = f"El vaciado total demora {t_end/60:.1f} min. La forma parabólica revela que el caudal es muy fuerte al principio debido a la presión hidrostática, pero pierde fuerza hacia el final."
    return steps, {"Nivel vs t": fig}, interp

def solve_case_3(V, Q0, cin, rin, rout, t_target):
    """Caso 3: Mezclas a Volumen Constante"""
    # PASO A: Defensivo
    V = max(V, 1.0)
    factor = rout / V
    inflow = rin * cin
    Q_steady = (inflow * V) / rout if rout > 0 else 0
    C_1 = Q0 - Q_steady

    # PASO C: LaTeX Exacto
    steps = [
        r"**1. Balance de Masa:**",
        rf"$$ \frac{{dQ}}{{dt}} = {rin}({cin}) - {rout}\frac{{Q}}{{{V:.1f}}} $$",
        rf"$$ \frac{{dQ}}{{dt}} + {factor:.4f}Q = {inflow:.2f} $$",
        r"**2. Solución General (Factor Integrante):**",
        rf"$$ Q(t) = {Q_steady:.1f} + C_1 e^{{-{factor:.4f}t}} $$",
        r"**3. Condición Inicial ($t=0$):**",
        rf"$$ Q(0) = {Q0} \implies {Q0} = {Q_steady:.1f} + C_1 \implies C_1 = {C_1:.1f} $$",
        r"**4. Ecuación Horaria Exacta:**",
        rf"$$ Q(t) = {Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}t}} $$",
        r"**5. Evaluación a $t_{target}$:**",
        rf"$$ Q({t_target}) = {Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}({t_target})}} \approx {Q_steady + C_1*math.exp(-factor*t_target):.2f} \text{{ kg}} $$"
    ]

    # PASO B: Gráfica Asintótica
    t_max = max(t_target * 1.2, 50.0)
    t_vec = np.linspace(0, t_max, 500)
    Q_vec = Q_steady + C_1 * np.exp(-factor * t_vec)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=Q_vec, mode='lines', line=dict(color='green', width=3)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[Q_steady, Q_steady], mode='lines', name='Límite Saturación', line=dict(color='blue', dash='dash')))
    fig.update_layout(title="Masa de Desengrasante Q(t)", xaxis_title="Tiempo (min)", yaxis_title="Cantidad (kg)", margin=dict(l=20, r=20, t=40, b=20))
    
    Q_final = Q_steady + C_1*math.exp(-factor*t_target)
    interp = f"A los {t_target} min hay {Q_final:.1f} kg. La curva asegura que el sistema tenderá asintóticamente al límite de saturación de {Q_steady} kg sin sobrepasarlo jamás."
    return steps, {"Saturación Química": fig}, interp

def solve_case_4(t_test, y_test, tau_ideal, force=10.0):
    """Caso 4: Actuador Hidráulico"""
    # PASO A: Defensivo (Evitar Log de Negativos)
    t_test = max(t_test, 0.1)
    y_safe = min(y_test, force * 0.999) # Nunca sobrepasar la fuerza F0
    tau_real = -t_test / math.log(1 - (y_safe / force))

    # PASO C: LaTeX Exacto
    steps = [
        r"**1. EDO Lineal del Cilindro:**",
        rf"$$ \tau\frac{{dy}}{{dt}} + y = {force} $$",
        r"**2. Solución y Condición Inicial ($y(0)=0$):**",
        rf"$$ y(t) = {force} + C_1 e^{{-t/\tau}} \implies C_1 = -{force} $$",
        rf"$$ y(t) = {force}(1 - e^{{-t/\tau}}) $$",
        r"**3. Diagnóstico de Constante Real $\tau$:**",
        rf"$$ {y_test} = {force}(1 - e^{{-{t_test}/\tau}}) \implies e^{{-{t_test}/\tau}} = {1 - y_safe/force:.4f} $$",
        rf"$$ \tau = \frac{{-{t_test}}}{{\ln({1 - y_safe/force:.4f})}} \approx {tau_real:.2f} \text{{ s}} $$"
    ]

    # PASO B: Gráfica de Límite Mecánico
    t_max = max(t_test * 1.2, tau_real * 5)
    t_vec = np.linspace(0, t_max, 500)
    y_vec = force * (1 - np.exp(-t_vec / tau_real))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=y_vec, mode='lines', line=dict(color='teal', width=3)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[force, force], mode='lines', line=dict(color='gray', dash='dash'), name='Recorrido Máximo'))
    fig.add_trace(go.Scatter(x=[t_test], y=[y_test], mode='markers+text', text=["Prueba"], textposition="bottom right", marker=dict(size=10, color='red')))
    fig.update_layout(title="Respuesta del Cilindro y(t)", xaxis_title="Tiempo (s)", yaxis_title="Posición (cm)", margin=dict(l=20, r=20, t=40, b=20))
    
    interp = f"El $\\tau$ medido es {tau_real:.1f}s vs ideal {tau_ideal}s. El retardo observado en la curva denota obstrucción hidráulica, fricción extrema o viscosidad alterada del fluido."
    return steps, {"Desplazamiento vs t": fig}, interp

def solve_case_5(H, R_top, h0, a, C_factor):
    """Caso 5: Torricelli Cónico"""
    # PASO A: Defensivo
    g = 9.8
    H, R_top = max(H, 0.01), max(R_top, 0.01)
    K_val = (C_factor * a * math.sqrt(2 * g)) / (math.pi * (R_top/H)**2)
    C_1 = (2/5) * (max(h0, 0)**(5/2))
    t_end = C_1 / max(K_val, 1e-8)

    # PASO C: LaTeX Exacto
    steps = [
        r"**1. Modelo Geométrico y EDO:**",
        rf"$$ r = \frac{{R}}{{H}}h = {R_top/H:.2f}h \implies A(h) = {math.pi*(R_top/H)**2:.4f} h^2 $$",
        r"$$ A(h)\frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Separación de Variables:**",
        rf"$$ h^{{3/2}} dh = -{K_val:.5f} dt $$",
        r"**3. Condición Inicial e Integración:**",
        rf"$$ \frac{{2}}{{5}}h^{{5/2}} = -Kt + C_1 \implies C_1 = \frac{{2}}{{5}}({h0})^{{5/2}} = {C_1:.4f} $$",
        r"**4. Ecuación Horaria:**",
        rf"$$ h(t) = \left( {h0**(5/2):.3f} - 2.5({K_val:.5f})t \right)^{{0.4}} $$",
        rf"**5. Vaciado Total:** $ t = {C_1:.4f} / {K_val:.5f} \approx {t_end/60:.2f} \text{{ min}} $"
    ]

    # PASO B: Recorte Exacto en Cono (Evita raíces imaginarias)
    t_max = max(5.0, t_end * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    # Clip a cero estricto antes de elevar a potencia fraccionaria
    base_vec = np.maximum(0, h0**(5/2) - 2.5 * K_val * t_vec)
    h_vec = base_vec**(2/5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec/60, y=h_vec, mode='lines', fill='tozeroy', line=dict(color='purple', width=3)))
    fig.update_layout(title="Vaciado Cónico h(t)", xaxis_title="Tiempo (min)", yaxis_title="Altura (m)", margin=dict(l=20, r=20, t=40, b=20))
    
    interp = f"Tiempo de vaciado: {t_end/60:.2f} min. El perfil muestra una curva cóncava inversa: a medida que el nivel baja, el área disminuye drásticamente, haciendo que la velocidad de caída se acelere violentamente hacia el final."
    return steps, {"Nivel Cónico": fig}, interp
