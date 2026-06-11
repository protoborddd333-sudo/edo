import numpy as np
import math
import plotly.graph_objects as go

AXIS_STYLE = dict(gridcolor='#E2E8F0', color='#1E293B', zerolinecolor='#E2E8F0')

def get_base_layout(title, x_title, y_title):
    return dict(
        title=dict(text=title, font=dict(color='#00A8E1')), 
        xaxis_title=x_title, 
        yaxis_title=y_title, 
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE
    )

def solve_case_1(T0, Ta, T1, t1, T_obj):
    if (T1 - Ta) > 0 and (T0 - Ta) > 0 and t1 > 0 and T0 != T1:
        k = -math.log((T1 - Ta) / (T0 - Ta)) / t1
        t_total = -math.log((T_obj - Ta) / (T0 - Ta)) / k if (T_obj - Ta) > 0 else 0
        t_adicional = max(0, t_total - t1)
    else:
        k, t_total, t_adicional = 0.0001, 0.0, 0.0

    steps = [
        r"**1. Modelo Matematico (Ley de Newton):**",
        r"$$ \frac{dT}{dt} = -k(T - T_a) $$",
        r"**2. Solucion Analitica General:**",
        r"$$ T(t) = T_a + C_1 e^{-kt} $$",
        r"**3. Evaluacion de Condicion Inicial (t = 0):**",
        rf"$$ T(0) = T_0 \implies {T0:.1f} = {Ta:.1f} + C_1 $$",
        rf"$$ \implies C_1 = {T0 - Ta:.1f} $$",
        r"**4. Calculo de Constante de Decaimiento Termico (k):**",
        rf"$$ k = -\frac{{\ln\left(\frac{{{T1:.1f} - {Ta:.1f}}}{{{T0:.1f} - {Ta:.1f}}}\right)}}{{{t1:.1f}}} $$",
        rf"$$ \implies k \approx {k:.4f} $$",
        r"**5. Ecuacion Horaria del Perfil Termico:**",
        rf"$$ T(t) = {Ta:.1f} + {T0 - Ta:.1f} e^{{-{k:.4f}t}} $$",
        r"**6. Tiempo proyectado para alcanzar la Temperatura Objetivo:**",
        rf"$$ t = \frac{{-\ln\left(\frac{{{T_obj:.1f} - {Ta:.1f}}}{{{T0:.1f} - {Ta:.1f}}}\right)}}{{{k:.4f}}} $$",
        rf"$$ \implies t \approx {t_total:.2f} \text{ unidades de tiempo} $$"
    ]

    t_max = max(10.0, t_total * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    T_vec = Ta + (T0 - Ta) * np.exp(-k * t_vec)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=T_vec, mode='lines', name='Temperatura', line=dict(color='#00A8E1', width=4)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[Ta, Ta], mode='lines', name='Asíntota (Medio)', line=dict(color='#94A3B8', dash='dash')))
    fig.add_trace(go.Scatter(x=[t_total], y=[T_obj], mode='markers+text', name='Objetivo', text=[f"({t_total:.1f}, {T_obj})"], textposition="top right", marker=dict(size=12, color='#0A2540')))
    fig.update_layout(**get_base_layout("Curva de Transferencia de Calor", "Tiempo", "Temperatura"))
    
    interp = f"Analisis: El objeto tomara un tiempo total de {t_total:.2f} para alcanzar los {T_obj} grados. Considerando que ya han transcurrido {t1} unidades de tiempo, se requiere un tiempo de espera adicional de {t_adicional:.2f}. La curva tiende asintoticamente al valor del medio ({Ta})."
    return steps, {"Curva Termica": fig}, interp

def solve_case_2(r, h0, a, C_factor):
    g = 9.8
    r = max(r, 0.001)
    A0 = math.pi * r**2
    K_val = (C_factor * a * math.sqrt(2 * g)) / A0 if A0 > 0 else 1e-5
    t_end = 2 * math.sqrt(max(h0, 0)) / K_val

    steps = [
        r"**1. Modelo Matematico (Ley de Torricelli):**",
        r"$$ A_0\frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Parametrizacion del Area Transversal:**",
        rf"$$ A_0 = \pi({r:.2f})^2 = {A0:.4f} \text{ m}^2 $$",
        rf"$$ K = \frac{{{C_factor} \cdot {a} \cdot \sqrt{{2 \cdot 9.8}}}}{{{A0:.4f}}} \approx {K_val:.5f} $$",
        r"**3. Integracion Diferencial:**",
        r"$$ \int h^{-1/2} dh = -K \int dt $$",
        r"$$ \implies 2\sqrt{h} = -Kt + C_1 $$",
        r"**4. Evaluacion de Condicion Inicial (t=0):**",
        rf"$$ h(0) = {h0} \implies C_1 = 2\sqrt{{{h0}}} $$",
        rf"$$ \implies C_1 = {2*math.sqrt(h0):.4f} $$",
        r"**5. Ecuacion Horaria del Nivel de Fluido:**",
        rf"$$ h(t) = \left( \sqrt{{{h0}}} - \frac{{{K_val:.5f}}}{{2}} t \right)^2 $$",
        r"**6. Computo de Tiempo de Vaciado (h=0):**",
        rf"$$ t = \frac{{{C_1:.4f}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{ segundos} $$"
    ]

    t_max = max(10.0, t_end * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    h_vec = np.maximum(0, math.sqrt(h0) - (K_val / 2) * t_vec)**2
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=h_vec, fill='tozeroy', mode='lines', line=dict(color='#00A8E1', width=4), fillcolor='rgba(0, 168, 225, 0.15)'))
    fig.add_trace(go.Scatter(x=[t_end], y=[0], mode='markers+text', text=[f"Vaciado: {t_end:.1f}s"], textposition="top right", marker=dict(size=12, color='#0A2540')))
    fig.update_layout(**get_base_layout("Descenso Hidrodinamico", "Tiempo (segundos)", "Altura (m)"))
    
    interp = f"Analisis: La evacuacion completa del fluido requiere {t_end:.2f} segundos (aprox {t_end/60:.2f} minutos). El grafico parabolico demuestra que la tasa de variacion (caudal de salida) es no lineal, siendo mayor al inicio debido a la presion de la columna de {h0} metros."
    return steps, {"Nivel de Fluido": fig}, interp

def solve_case_3(V, Q0, cin, rin, rout, t_target):
    V = max(V, 0.001)
    factor = rout / V
    inflow = rin * cin
    Q_steady = (inflow * V) / rout if rout > 0 else 0
    C_1 = Q0 - Q_steady

    steps = [
        r"**1. Modelo Diferencial (Balance de Masa):**",
        rf"$$ \frac{{dQ}}{{dt}} = (\text{Tasa Entrada}) - (\text{Tasa Salida}) $$",
        rf"$$ \implies \frac{{dQ}}{{dt}} + {factor:.4f}Q = {inflow:.2f} $$",
        r"**2. Solucion Analitica (Factor Integrante):**",
        rf"$$ Q(t) = {Q_steady:.1f} + C_1 e^{{-{factor:.4f}t}} $$",
        r"**3. Evaluacion de Condicion Inicial (t=0):**",
        rf"$$ Q(0) = {Q0} \implies {Q0} = {Q_steady:.1f} + C_1 $$",
        rf"$$ \implies C_1 = {C_1:.1f} $$",
        r"**4. Ecuacion Horaria Exacta:**",
        rf"$$ Q(t) = {Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}t}} $$",
        r"**5. Proyeccion para el instante de evaluacion:**",
        rf"$$ Q({t_target}) = {Q_steady:.1f} {C_1:+.1f} e^{{-{factor:.4f}({t_target})}} $$",
        rf"$$ \implies Q({t_target}) \approx {Q_steady + C_1*math.exp(-factor*t_target):.2f} \text{ masa} $$"
    ]

    t_max = max(t_target * 1.2, 50.0)
    t_vec = np.linspace(0, t_max, 500)
    Q_vec = Q_steady + C_1 * np.exp(-factor * t_vec)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=Q_vec, mode='lines', name='Sustancia', line=dict(color='#00A8E1', width=4)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[Q_steady, Q_steady], mode='lines', name='Limite Teórico', line=dict(color='#94A3B8', dash='dash')))
    fig.update_layout(**get_base_layout("Cinetica de Mezcla Homogenea", "Tiempo", "Masa disuelta"))
    
    Q_final = Q_steady + C_1*math.exp(-factor*t_target)
    interp = f"Analisis: Evaluando el sistema a los {t_target} de tiempo, la cantidad contenida es de {Q_final:.2f}. El diseño del proceso asegura que, eventualmente, el estado estacionario alcanzara de forma natural un limite absoluto de {Q_steady:.2f}."
    return steps, {"Cinética de Masa": fig}, interp

def solve_case_4(t_test, y_test, tau_ideal, force):
    t_test = max(t_test, 0.001)
    y_safe = min(y_test, force * 0.999) 
    tau_real = -t_test / math.log(1 - (y_safe / force)) if force > 0 else 0.001

    steps = [
        r"**1. Modelo Lineal de Primer Orden:**",
        rf"$$ \tau\frac{{dy}}{{dt}} + y = {force} $$",
        r"**2. Solucion General:**",
        rf"$$ y(t) = {force} + C_1 e^{{-t/\tau}} $$",
        r"**3. Evaluacion de Sistema en Reposo (y(0)=0):**",
        rf"$$ 0 = {force} + C_1 \implies C_1 = -{force} $$",
        r"**4. Funcional de Posicion Transitoria:**",
        rf"$$ y(t) = {force}\left(1 - e^{{-t/\tau}}\right) $$",
        r"**5. Diagnostico del Parametro Tau:**",
        rf"$$ {y_test} = {force}\left(1 - e^{{-{t_test}/\tau}}\right) $$",
        rf"$$ \implies \tau = \frac{{-{t_test}}}{{\ln({1 - y_safe/force:.4f})}} $$",
        rf"$$ \implies \tau \approx {tau_real:.2f} \text{ s} $$"
    ]

    t_max = max(t_test * 1.2, tau_real * 5)
    t_vec = np.linspace(0, t_max, 500)
    y_vec = force * (1 - np.exp(-t_vec / tau_real))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=y_vec, mode='lines', name='y(t)', line=dict(color='#00A8E1', width=4)))
    fig.add_trace(go.Scatter(x=[0, t_max], y=[force, force], mode='lines', line=dict(color='#94A3B8', dash='dash'), name='Limite Asintotico'))
    fig.add_trace(go.Scatter(x=[t_test], y=[y_test], mode='markers+text', text=["Punto Test"], textposition="bottom right", marker=dict(size=12, color='#0A2540')))
    fig.update_layout(**get_base_layout("Respuesta Dinamica de Planta", "Tiempo (s)", "Magnitud"))
    
    desviacion = abs(tau_real - tau_ideal) / tau_ideal * 100 if tau_ideal > 0 else 0
    interp = f"Analisis: La constante de tiempo computada es {tau_real:.2f}s, en contraste con el valor nominal de {tau_ideal}s. Esto representa una desviacion metrica del {desviacion:.1f}%. Cambios significativos en este valor son indicadores directos de alteraciones fisicas en la planta (ej. aumento de inercia o perdidas de presion)."
    return steps, {"Respuesta Temporal": fig}, interp

def solve_case_5(H, R_top, h0, a, C_factor):
    g = 9.8
    H, R_top = max(H, 0.001), max(R_top, 0.001)
    K_val = (C_factor * a * math.sqrt(2 * g)) / (math.pi * (R_top/H)**2)
    C_1 = (2/5) * (max(h0, 0)**(5/2))
    t_end = C_1 / max(K_val, 1e-8)

    steps = [
        r"**1. Modelo de Fluido No Lineal:**",
        r"$$ A(h)\frac{dh}{dt} = -C a \sqrt{2gh} $$",
        r"**2. Sustitucion por Geometria Conica:**",
        rf"$$ r = \frac{{R}}{{H}}h \implies A(h) = {math.pi*(R_top/H)**2:.4f} h^2 $$",
        r"**3. Separacion en Ecuacion Diferencial:**",
        rf"$$ h^{{3/2}} dh = -{K_val:.5f} dt $$",
        r"**4. Integracion Indefinida y C_1:**",
        rf"$$ \frac{{2}}{{5}}h^{{5/2}} = -Kt + C_1 $$",
        rf"$$ h(0) = {h0} \implies C_1 = {C_1:.4f} $$",
        r"**5. Ecuacion Horaria Despejada:**",
        rf"$$ h(t) = \left( {h0**(5/2):.3f} - 2.5({K_val:.5f})t \right)^{{0.4}} $$",
        r"**6. Tiempo Limite Operativo:**",
        rf"$$ t = \frac{{{C_1:.4f}}}{{{K_val:.5f}}} \approx {t_end:.2f} \text{ segundos} $$"
    ]

    t_max = max(5.0, t_end * 1.2)
    t_vec = np.linspace(0, t_max, 500)
    base_vec = np.maximum(0, h0**(5/2) - 2.5 * K_val * t_vec)
    h_vec = base_vec**(2/5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vec, y=h_vec, mode='lines', fill='tozeroy', line=dict(color='#00A8E1', width=4), fillcolor='rgba(0, 168, 225, 0.15)'))
    fig.add_trace(go.Scatter(x=[t_end], y=[0], mode='markers+text', text=[f"Vaciado en {t_end:.1f}s"], textposition="top right", marker=dict(size=12, color='#0A2540')))
    fig.update_layout(**get_base_layout("Perfil de Altura No Lineal", "Tiempo (segundos)", "Altura (m)"))
    
    interp = f"Analisis: La ecuacion diferencial arroja un vaciado critico a los {t_end:.2f} segundos. Debido a la reduccion cuadratica del area transversal en geometrias conicas, la aceleracion del vaciado es extrema en las etapas finales del proceso, requiriendo consideraciones especiales en el control industrial."
    return steps, {"Altura Conica": fig}, interp
