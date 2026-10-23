"""Herramientas de ajuste de leyes de potencias (Clauset, Shalizi y Newman 2009) con el paquete `powerlaw`.

No es un script: lo importan pila_de_arena.py e incendio_forestal.py. El método completo, con sus
advertencias, está en skills/ajuste-ley-de-potencias/SKILL.md.

Convención de signos: en distribution_compare(a, b), R > 0 favorece a `a`; p < 0.05 indica que el
signo de R es significativo. Con p ≥ 0.05 los datos NO distinguen entre las dos.
"""
import warnings

import numpy as np
import powerlaw

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="Fitted parameters are very close to the edge")
warnings.filterwarnings("ignore", message="Initial guess is not within the specified bounds")


def pdf_log(x, nbins=40):
    """Densidad en bins logarítmicos (para dibujar; nunca para ajustar)."""
    x = np.asarray(x, float)
    bordes = np.logspace(0, np.log10(x.max()) + 0.01, nbins)
    h, _ = np.histogram(x, bordes)
    centro = np.sqrt(bordes[1:] * bordes[:-1])
    dens = h / (np.diff(bordes) * x.size)
    m = h > 0
    return centro[m], dens[m]


def _comparar(f, a, b):
    R, p = f.distribution_compare(a, b, normalized_ratio=True)
    # p con tres cifras significativas: 1e-30 no debe aparecer como 0.0
    return {"R": round(float(R), 2), "p": float(f"{float(p):.3g}")}


def submuestra(datos, n_max, semilla):
    """Hasta n_max eventos elegidos al azar con semilla fija. Los ajustes discretos con corte tardan
    minutos con cientos de miles de eventos; con 50 000 las pruebas siguen siendo concluyentes.
    Se declara en resultados: quien lea el número debe saber sobre cuántos datos se calculó."""
    datos = np.asarray(datos)
    if datos.size <= n_max:
        return datos
    return np.random.default_rng(semilla).choice(datos, n_max, replace=False)


def ajuste_automatico(datos, discreto=True, n_candidatos=60):
    """Paso 1 del método: x_min que minimiza la distancia de Kolmogorov-Smirnov, α por máxima
    verosimilitud y comparación contra log-normal y exponencial.

    Clauset et al. prueban como x_min cada valor distinto de los datos; con miles de valores eso tarda
    minutos. Aquí se prueban `n_candidatos` valores repartidos en escala logarítmica (se declara en el
    resultado). Para la búsqueda exhaustiva: powerlaw.Fit(datos, discrete=True)."""
    datos = np.asarray(datos)
    valores = np.unique(datos)[:-10]          # los 10 mayores no dejan cola suficiente
    if valores.size > n_candidatos:
        objetivo = np.logspace(np.log10(valores[0]), np.log10(valores[-1]), n_candidatos)
        valores = np.unique(valores[np.clip(np.searchsorted(valores, objetivo), 0, valores.size - 1)])
    mejor = None
    for x in valores:
        f = powerlaw.Fit(datos, discrete=discreto, xmin=float(x), verbose=False)
        if mejor is None or f.power_law.D < mejor.power_law.D:
            mejor = f
    f = mejor
    return {"busqueda_xmin": f"{valores.size} candidatos en escala logarítmica, distancia KS",
            "xmin": float(f.xmin), "n_cola": int(np.sum(datos >= f.xmin)), "ks_D": round(float(f.power_law.D), 4),
            "alfa": round(float(f.power_law.alpha), 3), "alfa_error": round(float(f.power_law.sigma), 3),
            "ley_vs_lognormal": _comparar(f, "power_law", "lognormal"),
            "ley_vs_exponencial": _comparar(f, "power_law", "exponential")}


def ajuste_con_corte(datos, xmin, discreto=True):
    """Paso 2: con xmin fijo y bajo (en el rango de escala), ley pura vs. con corte exponencial vs. log-normal."""
    f = powerlaw.Fit(datos, discrete=discreto, xmin=xmin, verbose=False)
    lam = float(f.truncated_power_law.parameter2)
    return {"xmin": xmin, "n_cola": int(np.sum(np.asarray(datos) >= xmin)),
            "alfa_pura": round(float(f.power_law.alpha), 3),
            "alfa_con_corte": round(float(f.truncated_power_law.alpha), 3),
            "escala_de_corte_1_sobre_lambda": round(1 / lam, 1) if lam > 0 else None,
            "corte_vs_pura": _comparar(f, "truncated_power_law", "power_law"),
            "corte_vs_lognormal": _comparar(f, "truncated_power_law", "lognormal"),
            "pura_vs_lognormal": _comparar(f, "power_law", "lognormal")}


def veredicto(c):
    """Lectura en palabras de ajuste_con_corte. Es una ayuda; quien escribe decide qué afirma."""
    a, b = c["corte_vs_pura"], c["corte_vs_lognormal"]
    if a["R"] > 0 and a["p"] < 0.05 and b["R"] > 0 and b["p"] < 0.05:
        return "ley de potencias con corte: mejor que la pura y que la log-normal"
    if b["p"] >= 0.05:
        return "indistinguible de una log-normal: no afirmar ley de potencias"
    return "no hay evidencia clara a favor de la ley de potencias con corte"
