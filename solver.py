# solver.py
# Compatible con Python 3.12, Streamlit Cloud, NumPy y Plotly

import math
import numpy as np
import plotly.graph_objects as go


def base_layout(title, x_title, y_title):
    return dict(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
    )


def safe_positive(value, default):
    try:
        value = float(value)
        if value > 0:
            return value
        return default
    except Exception:
        return default


# ==========================================================
# CASO 1: ENFRIAMIENTO DE NEWTON
# ==========================================================

def solve_case_1(T0=150, Ta=25, T1=100, t1=10, T_obj=40):
    T0 = safe_positive(T0, 150)
    Ta = float(Ta)
    T1 = float(T1)
    t1 = safe_positive(t1, 10)
    T_obj = float(T_obj)

    if T0 <= Ta:
        T0 = 150
    if T1 <= Ta or T1 >= T0:
        T1 = 100
    if T_obj <= Ta or T_obj >= T0:
        T_obj = 40

    k = -math.log((T1 - Ta) / (T0 - Ta)) / t1
    t_total = -math.log((T_obj - Ta) / (T0 - Ta)) / k
    t_extra = max(0, t_total - t1)

    steps = [
        "### 1. Modelo de la EDO",
        r"$$\frac{dT}{dt}=-k(T-T_a)$$",
        "### 2. Solución general",
        r"$$T(t)=T_a+(T_0-T_a)e^{-kt}$$",
        "### 3. Cálculo de la constante k",
        rf"$$k=-\frac{{\ln\left(\frac{{{T1:.2f}-{Ta:.2f}}}{{{T0:.2f}-{Ta:.2f}}}\right)}}{{{t1:.2f}}}={k:.5f}$$",
        "### 4. Ecuación de temperatura",
        rf"$$T(t)={Ta:.2f}+{T0-Ta:.2f}e^{{-{k:.5f}t}}$$",
        "### 5. Tiempo para alcanzar la temperatura segura",
        rf"$$t={t_total:.2f}\ \text{{min}}$$",
        rf"$$t_{{adicional}}={t_extra:.2f}\ \text{{min}}$$",
    ]

    t_max = max(t_total * 1.25, 50)
    t = np.linspace(0, t_max, 400)
    T = Ta + (T0 - Ta) * np.exp(-k * t)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=T, mode="lines", name="Temperatura T(t)"))
    fig.add_trace(go.Scatter(x=[t1], y=[T1], mode="markers+text", text=["Medición"], textposition="top right", name="Medición"))
    fig.add_trace(go.Scatter(x=[t_total], y=[T_obj], mode="markers+text", text=["Punto seguro"], textposition="top right", name="Temperatura segura"))
    fig.add_hline(y=Ta, line_dash="dash", annotation_text="Temperatura ambiente")
    fig.update_layout(**base_layout("Caso 1: Enfriamiento de Newton", "Tiempo (min)", "Temperatura (°C)"))

    interpretation = (
        f"El rodamiento llega a {T_obj:.2f} °C a los {t_total:.2f} minutos. "
        f"Como ya pasaron {t1:.2f} minutos, el técnico debe esperar {t_extra:.2f} minutos adicionales. "
        "La curva baja rápido al inicio y luego se vuelve más lenta porque se aproxima a la temperatura ambiente."
    )

    return steps, {"Curva de enfriamiento": fig}, interpretation


# ==========================================================
# CASO 2: TORRICELLI TANQUE CILÍNDRICO
# ==========================================================

def solve_case_2(r=1, h0=4, a=0.005, C_factor=0.6, g=9.8):
    r = safe_positive(r, 1)
    h0 = safe_positive(h0, 4)
    a = safe_positive(a, 0.005)
    C_factor = safe_positive(C_factor, 0.6)
    g = safe_positive(g, 9.8)

    A = math.pi * r**2
    K = (C_factor * a * math.sqrt(2 * g)) / A
    C1 = 2 * math.sqrt(h0)
    t_end = C1 / K

    steps = [
        "### 1. Modelo de Torricelli",
        r"$$A\frac{dh}{dt}=-Ca\sqrt{2gh}$$",
        "### 2. Área del tanque",
        rf"$$A=\pi r^2=\pi({r:.2f})^2={A:.4f}\ m^2$$",
        "### 3. Separación de variables",
        r"$$\frac{dh}{\sqrt{h}}=-Kdt$$",
        rf"$$K=\frac{{Ca\sqrt{{2g}}}}{{A}}={K:.6f}$$",
        "### 4. Integración",
        r"$$2\sqrt{h}=-Kt+C_1$$",
        rf"$$C_1=2\sqrt{{{h0:.2f}}}={C1:.4f}$$",
        "### 5. Tiempo de vaciado",
        rf"$$t=\frac{{C_1}}{{K}}=\frac{{{C1:.4f}}}{{{K:.6f}}}={t_end:.2f}\ s$$",
        rf"$$t={t_end/60:.2f}\ min$$",
    ]

    t = np.linspace(0, t_end, 400)
    h = np.maximum(0, np.sqrt(h0) - (K / 2) * t) ** 2

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t / 60, y=h, mode="lines", fill="tozeroy", name="Altura h(t)"))
    fig.add_trace(go.Scatter(x=[t_end / 60], y=[0], mode="markers+text", text=["Vacío"], textposition="top right", name="Vaciado total"))
    fig.update_layout(**base_layout("Caso 2: Vaciado de tanque cilíndrico", "Tiempo (min)", "Altura (m)"))

    interpretation = (
        f"El tanque se vacía en {t_end/60:.2f} minutos. "
        "La altura no disminuye de forma lineal: al inicio baja más rápido por la mayor presión hidrostática."
    )

    return steps, {"Vaciado cilíndrico": fig}, interpretation


# ==========================================================
# CASO 3: MEZCLAS
# ==========================================================

def solve_case_3(V=500, Q0=0, cin=0.2, rin=5, rout=5, t_target=60):
    V = safe_positive(V, 500)
    Q0 = float(Q0)
    cin = safe_positive(cin, 0.2)
    rin = safe_positive(rin, 5)
    rout = safe_positive(rout, 5)
    t_target = safe_positive(t_target, 60)

    factor = rout / V
    entrada = rin * cin
    Q_estable = (entrada * V) / rout
    C1 = Q0 - Q_estable
    Q_final = Q_estable + C1 * math.exp(-factor * t_target)

    steps = [
        "### 1. Balance de masa",
        r"$$\frac{dQ}{dt}=r_{in}c_{in}-r_{out}\frac{Q}{V}$$",
        "### 2. Sustitución de datos",
        rf"$$\frac{{dQ}}{{dt}}={rin:.2f}({cin:.2f})-{rout:.2f}\frac{{Q}}{{{V:.2f}}}$$",
        rf"$$\frac{{dQ}}{{dt}}+{factor:.5f}Q={entrada:.5f}$$",
        "### 3. Solución general",
        rf"$$Q(t)={Q_estable:.4f}+C_1e^{{-{factor:.5f}t}}$$",
        "### 4. Condición inicial",
        rf"$$Q(0)={Q0:.2f}\Rightarrow C_1={C1:.4f}$$",
        "### 5. Evaluación",
        rf"$$Q({t_target:.2f})={Q_final:.4f}\ kg$$",
    ]

    t_max = max(t_target * 1.4, 120)
    t = np.linspace(0, t_max, 400)
    Q = Q_estable + C1 * np.exp(-factor * t)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=Q, mode="lines", name="Cantidad Q(t)"))
    fig.add_trace(go.Scatter(x=[t_target], y=[Q_final], mode="markers+text", text=[f"{Q_final:.2f} kg"], textposition="top right", name="Resultado"))
    fig.add_hline(y=Q_estable, line_dash="dash", annotation_text="Estado estacionario")
    fig.update_layout(**base_layout("Caso 3: Mezcla de desengrasante", "Tiempo (min)", "Cantidad de desengrasante (kg)"))

    interpretation = (
        f"Después de {t_target:.2f} minutos hay {Q_final:.2f} kg de desengrasante. "
        f"La curva se aproxima al estado estacionario de {Q_estable:.2f} kg."
    )

    return steps, {"Mezcla": fig}, interpretation


# ==========================================================
# CASO 4: ACTUADOR HIDRÁULICO
# ==========================================================

def solve_case_4(t_test=8, y_test=6.32, tau_ideal=4, recorrido=10):
    t_test = safe_positive(t_test, 8)
    recorrido = safe_positive(recorrido, 10)
    tau_ideal = safe_positive(tau_ideal, 4)
    y_test = float(y_test)

    if y_test <= 0 or y_test >= recorrido:
        y_test = 6.32

    tau_real = -t_test / math.log(1 - y_test / recorrido)

    steps = [
        "### 1. Modelo del actuador",
        rf"$$\tau\frac{{dy}}{{dt}}+y={recorrido:.2f}$$",
        "### 2. Solución general",
        rf"$$y(t)={recorrido:.2f}(1-e^{{-t/\tau}})$$",
        "### 3. Cálculo de tau real",
        rf"$$ {y_test:.2f}={recorrido:.2f}(1-e^{{-{t_test:.2f}/\tau}})$$",
        rf"$$\tau={tau_real:.4f}\ s$$",
        "### 4. Función de posición",
        rf"$$y(t)={recorrido:.2f}(1-e^{{-t/{tau_real:.4f}}})$$",
    ]

    t_max = max(t_test * 2, tau_real * 5)
    t = np.linspace(0, t_max, 400)
    y_real = recorrido * (1 - np.exp(-t / tau_real))
    y_ideal = recorrido * (1 - np.exp(-t / tau_ideal))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y_real, mode="lines", name=f"Real tau={tau_real:.2f}s"))
    fig.add_trace(go.Scatter(x=t, y=y_ideal, mode="lines", name=f"Ideal tau={tau_ideal:.2f}s"))
    fig.add_trace(go.Scatter(x=[t_test], y=[y_test], mode="markers+text", text=["Prueba"], textposition="bottom right", name="Dato medido"))
    fig.update_layout(**base_layout("Caso 4: Respuesta de actuador hidráulico", "Tiempo (s)", "Posición (cm)"))

    interpretation = (
        f"La constante de tiempo real es {tau_real:.2f} s. "
        f"Comparada con la ideal de {tau_ideal:.2f} s, permite evaluar si el actuador responde lento. "
        "Un valor mayor puede indicar fricción, fuga interna, obstrucción o aumento de viscosidad del fluido."
    )

    return steps, {"Actuador hidráulico": fig}, interpretation


# ==========================================================
# CASO 5: TANQUE CÓNICO
# ==========================================================

def solve_case_5(H=2, R_top=0.5, h0=2, a=0.005, C_factor=0.6, g=9.8):
    H = safe_positive(H, 2)
    R_top = safe_positive(R_top, 0.5)
    h0 = safe_positive(h0, H)
    a = safe_positive(a, 0.005)
    C_factor = safe_positive(C_factor, 0.6)
    g = safe_positive(g, 9.8)

    if h0 > H:
        h0 = H

    ratio = R_top / H
    area_coef = math.pi * ratio**2
    K = (C_factor * a * math.sqrt(2 * g)) / area_coef
    t_end = ((2 / 5) * h0**(5 / 2)) / K

    steps = [
        "### 1. Relación geométrica del cono",
        r"$$\frac{r}{h}=\frac{R}{H}$$",
        rf"$$r={ratio:.4f}h$$",
        "### 2. Área variable",
        rf"$$A(h)=\pi({ratio:.4f}h)^2={area_coef:.5f}h^2$$",
        "### 3. Ley de Torricelli",
        r"$$A(h)\frac{dh}{dt}=-Ca\sqrt{2gh}$$",
        "### 4. EDO separable",
        rf"$$h^{{3/2}}dh=-{K:.6f}dt$$",
        "### 5. Integración",
        r"$$\frac{2}{5}h^{5/2}=-Kt+C_1$$",
        rf"$$h(t)=\left({h0**(5/2):.4f}-2.5({K:.6f})t\right)^{{2/5}}$$",
        "### 6. Tiempo total de vaciado",
        rf"$$t={t_end:.2f}\ s={t_end/60:.2f}\ min$$",
    ]

    t = np.linspace(0, t_end, 400)
    base = np.maximum(0, h0**(5 / 2) - 2.5 * K * t)
    h = base ** (2 / 5)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t / 60, y=h, mode="lines", fill="tozeroy", name="Altura h(t)"))
    fig.add_trace(go.Scatter(x=[t_end / 60], y=[0], mode="markers+text", text=["Vacío"], textposition="top right", name="Vaciado"))
    fig.update_layout(**base_layout("Caso 5: Vaciado de tanque cónico", "Tiempo (min)", "Altura (m)"))

    interpretation = (
        f"El modelo indica un tiempo aproximado de vaciado de {t_end/60:.2f} minutos. "
        "A diferencia del tanque cilíndrico, el área transversal cambia con la altura, por eso el comportamiento de la curva es no lineal."
    )

    return steps, {"Vaciado cónico": fig}, interpretation
