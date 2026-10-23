"""Aplicación logística x_{n+1} = r x_n (1 - x_n): orden, duplicación de periodo y caos.

    python simulaciones/logistica.py

Figuras (en figuras/):
  logistica_bifurcacion.png   diagrama de bifurcación, r de 2.5 a 4
  logistica_sensibilidad.png  dos trayectorias que empiezan a 1e-10 de distancia
  logistica_lyapunov.png      exponente de Lyapunov contra r (λ > 0: caos)
  logistica_feigenbaum.png    convergencia de δ_n en dos mapas distintos (universalidad)
Números: resultados/logistica.json

Es determinista: no hay azar, la condición inicial es fija (X0).
Tarda ~1 minuto con numba.
"""
import numpy as np
import matplotlib.pyplot as plt
from comun import njit, guardar_figura, guardar_resultados, TINTA, TINTA2, AZUL, NARANJA, AQUA

X0 = 0.4                     # condición inicial de todas las trayectorias
DELTA = 4.669201609102990    # constante de Feigenbaum (valor de referencia)
PARAM = {"x0": X0, "bifurcacion": {"r": [2.5, 4.0, 4000], "transitorio": 2000, "muestras": 400},
         "lyapunov": {"r": [2.5, 4.0, 6000], "transitorio": 2000, "iteraciones": 20000},
         "sensibilidad": {"r": 3.9, "epsilon": 1e-10, "umbral": 0.1},
         "feigenbaum": {"niveles": 11}}


# ---------- 1. Diagrama de bifurcación ----------
@njit(cache=True)
def atractor(rs, x0, transitorio, muestras):
    out = np.empty((rs.size, muestras))
    for i in range(rs.size):
        r = rs[i]
        x = x0
        for _ in range(transitorio):
            x = r * x * (1 - x)
        for j in range(muestras):
            x = r * x * (1 - x)
            out[i, j] = x
    return out


def figura_bifurcacion():
    p = PARAM["bifurcacion"]
    rs = np.linspace(*p["r"][:2], p["r"][2])
    pts = atractor(rs, X0, p["transitorio"], p["muestras"])
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.scatter(np.repeat(rs, pts.shape[1]), pts.ravel(), s=0.02, c=TINTA, alpha=0.3,
               linewidths=0, rasterized=True)
    for r, t in [(3.0, "periodo 2"), (3.449, "periodo 4"), (3.5699, "caos"), (3.8284, "ventana de periodo 3")]:
        ax.axvline(r, color=NARANJA, lw=0.7, alpha=0.7)
        ax.text(r + 0.006, 0.03, t, color=TINTA2, fontsize=7, rotation=90, va="bottom")
    ax.set(xlabel="tasa de crecimiento r", ylabel="población a largo plazo x", xlim=(2.5, 4.0), ylim=(0, 1))
    ax.grid(False)
    guardar_figura(fig, "logistica_bifurcacion.png")


# ---------- 2. Sensibilidad a condiciones iniciales ----------
def serie(r, x0, n):
    out = np.empty(n)
    x = x0
    for i in range(n):
        out[i] = x
        x = r * x * (1 - x)
    return out


def figura_sensibilidad():
    p = PARAM["sensibilidad"]
    a, b = serie(p["r"], X0, 60), serie(p["r"], X0 + p["epsilon"], 60)
    paso = int(np.argmax(np.abs(a - b) > p["umbral"]))
    fig, ax = plt.subplots(figsize=(7, 2.6))
    ax.plot(a, color=AZUL, label="x₀ = 0.4")
    ax.plot(b, color=NARANJA, ls="--", label="x₀ = 0.4 + 10⁻¹⁰")
    ax.axvline(paso, color=TINTA2, lw=0.8)
    ax.text(paso + 0.6, 0.97, f"se separan en el paso {paso}", color=TINTA2, fontsize=7, va="top")
    ax.set(xlabel="paso n", ylabel="x", title=f"r = {p['r']}")
    ax.legend(loc="lower left", ncols=2)
    guardar_figura(fig, "logistica_sensibilidad.png")
    return paso


# ---------- 3. Exponente de Lyapunov ----------
@njit(cache=True)
def lyapunov(rs, x0, transitorio, n):
    out = np.empty(rs.size)
    for i in range(rs.size):
        r = rs[i]
        x = x0
        for _ in range(transitorio):
            x = r * x * (1 - x)
        s = 0.0
        for _ in range(n):
            x = r * x * (1 - x)
            s += np.log(abs(r * (1 - 2 * x)) + 1e-300)
        out[i] = s / n
    return out


def figura_lyapunov():
    p = PARAM["lyapunov"]
    rs = np.linspace(*p["r"][:2], p["r"][2])
    lam = lyapunov(rs, X0, p["transitorio"], p["iteraciones"])
    fig, ax = plt.subplots(figsize=(7, 2.6))
    ax.plot(rs, lam, color=TINTA, lw=0.6)
    ax.axhline(0, color=TINTA2, lw=0.8)
    ax.fill_between(rs, 0, lam, where=lam > 0, color=NARANJA, alpha=0.35, label="λ > 0: caos")
    ax.set(xlabel="r", ylabel="exponente de Lyapunov λ", ylim=(-2, 1), xlim=(2.5, 4))
    ax.legend(loc="lower left")
    guardar_figura(fig, "logistica_lyapunov.png")
    inicio = float(rs[np.argmax(lam > 1e-3)])
    return {"inicio_caos_r": round(inicio, 4), "lyapunov_en_r4": round(float(lam[-1]), 4),
            "referencia_r4_ln2": round(float(np.log(2)), 4)}


# ---------- 4. Constante de Feigenbaum en dos mapas ----------
def superestables(f, R0, rango_R1, niveles):
    """R_n: valores de r donde x = 0.5 (el máximo del mapa) está en una órbita de periodo 2^n."""
    def g(r, n):
        x = 0.5
        for _ in range(2 ** n):
            x = f(r, x)
        return x - 0.5

    def secante(n, a, b):
        fa, fb = g(a, n), g(b, n)
        for _ in range(200):
            if fb == fa:
                break
            c = b - fb * (b - a) / (fb - fa)
            a, fa, b, fb = b, fb, c, g(c, n)
            if abs(b - a) < 1e-15:
                break
        return b

    malla = np.linspace(*rango_R1, 20001)
    vals = [g(r, 1) for r in malla]
    k = next(i for i in range(1, len(malla)) if np.sign(vals[i]) != np.sign(vals[i - 1]))
    R = [R0, secante(1, malla[k - 1], malla[k])]
    for n in range(2, niveles):
        guia = R[-1] + (R[-1] - R[-2]) / DELTA
        R.append(secante(n, guia - 1e-6 * (R[-1] - R[-2]), guia))
    R = np.array(R)
    return R, (R[1:-1] - R[:-2]) / (R[2:] - R[1:-1])


def figura_feigenbaum():
    niv = PARAM["feigenbaum"]["niveles"]
    R_log, d_log = superestables(lambda r, x: r * x * (1 - x), 2.0, (3.0, 3.4), niv)
    R_sen, d_sen = superestables(lambda r, x: r * np.sin(np.pi * x), 0.5, (0.65, 0.85), niv)
    n = np.arange(2, 2 + d_log.size)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(n, d_log, "o-", ms=4, color=AZUL, label="logística: r·x·(1−x)")
    ax.plot(n, d_sen, "s--", ms=4, color=AQUA, label="seno: r·sin(πx)")
    ax.axhline(DELTA, color=NARANJA, lw=1, label=f"δ = {DELTA:.9f}…")
    ax.set(xlabel="nivel de duplicación n", ylabel="δₙ", ylim=(3.9, 5.0))
    ax.legend()
    guardar_figura(fig, "logistica_feigenbaum.png")
    return {"R_superestables_logistica": [round(float(x), 10) for x in R_log],
            "R1_exacto_1_mas_raiz5": round(1 + 5 ** 0.5, 10),
            "delta_logistica": [round(float(x), 6) for x in d_log],
            "delta_seno": [round(float(x), 6) for x in d_sen],
            "delta_referencia": DELTA}


if __name__ == "__main__":
    print("Aplicación logística")
    figura_bifurcacion()
    datos = {"sensibilidad_paso_de_separacion": figura_sensibilidad()}
    datos["lyapunov"] = figura_lyapunov()
    datos["feigenbaum"] = figura_feigenbaum()
    guardar_resultados("logistica", datos, "simulaciones/logistica.py", semillas=None, parametros=PARAM)
    print(f"  δ (logística, último nivel) = {datos['feigenbaum']['delta_logistica'][-1]}; "
          f"inicio del caos r ≈ {datos['lyapunov']['inicio_caos_r']}")
