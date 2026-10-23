"""Incendio forestal de Drossel-Schwabl: incendios de todos los tamaños y su corte.

    python simulaciones/incendio_forestal.py            # L = 256, θ = 100, 300, 1000 (<1 min)
    python simulaciones/incendio_forestal.py --rapido   # θ = 100, 300, para probar

Figuras (en figuras/):
  bosque_estado.png            el bosque tras la simulación de θ más grande
  bosque_corte_theta.png       P(s) para cada θ: el corte crece con θ (árboles plantados por rayo)
Números: resultados/incendio_forestal.json

En este modelo el corte lo fija θ, no L, mientras L sea suficientemente grande para que el incendio
más grande quepa. Si al subir θ el corte deja de moverse, el que manda ya es L: súbelo.
"""
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
from comun import guardar_figura, guardar_resultados, SECUENCIAL
from modelos_soc import incendio
from leyes_potencia import pdf_log, submuestra, ajuste_automatico, ajuste_con_corte, veredicto

SEMILLA = 5
L = 256
XMIN_FIJO = 10
MAX_EVENTOS_AJUSTE = 50_000   # submuestra con semilla fija para que los ajustes tarden segundos
THETAS = [100, 300] if "--rapido" in sys.argv else [100, 300, 1000]
THETA_AJUSTE = THETAS[-1]


def plantados_para(theta):
    """~30 000 rayos por simulación más un transitorio fijo."""
    return 30 * theta * 1000 + 2_000_000


if __name__ == "__main__":
    print(f"Incendio forestal, L = {L}, θ = {THETAS}")
    datos = {"L": L, "por_theta": {}}
    fig, ax = plt.subplots(figsize=(6, 4))
    for theta, color in zip(THETAS, SECUENCIAL[-len(THETAS):]):
        t0 = time.time()
        fuegos, bosque = incendio(L, plantados_para(theta), theta, SEMILLA)
        fuegos = fuegos[len(fuegos) // 5:]          # descartamos el primer 20 %: transitorio
        x, y = pdf_log(fuegos)
        ax.loglog(x, y, "o-", ms=3, lw=1, color=color, label=f"θ = {theta}")
        datos["por_theta"][f"theta{theta}"] = {"incendios": int(fuegos.size), "maximo": int(fuegos.max()),
                                               "percentil_99_9": float(np.percentile(fuegos, 99.9)),
                                               "densidad_final_de_arboles": round(float(bosque.mean()), 4)}
        print(f"  θ = {theta}: {fuegos.size} incendios, máximo {fuegos.max()} ({time.time() - t0:.1f} s)")
        if theta == THETA_AJUSTE:
            t0 = time.time()
            muestra = submuestra(fuegos, MAX_EVENTOS_AJUSTE, SEMILLA)
            datos[f"ajuste_automatico_theta{theta}"] = ajuste_automatico(muestra)
            datos[f"ajuste_con_corte_theta{theta}"] = c = ajuste_con_corte(muestra, XMIN_FIJO)
            c["eventos_ajustados"] = int(muestra.size)
            c["veredicto"] = veredicto(c)
            print(f"  ajustes en θ = {theta} ({time.time() - t0:.1f} s): {c['veredicto']}")
            bosque_final = bosque
    ax.set(xlabel="árboles quemados s", ylabel="P(s)", title=f"Incendio forestal (L = {L}): el corte crece con θ")
    ax.legend()
    guardar_figura(fig, "bosque_corte_theta.png")

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(bosque_final, cmap="Greens", interpolation="nearest", vmin=0, vmax=1.3)
    ax.set_title(f"Bosque {L}×{L}, θ = {THETA_AJUSTE}: islas de todos los tamaños")
    ax.axis("off")
    guardar_figura(fig, "bosque_estado.png")

    maximos = [datos["por_theta"][f"theta{t}"]["percentil_99_9"] for t in THETAS]
    datos["el_percentil_99_9_crece_con_theta"] = bool(all(b > a for a, b in zip(maximos, maximos[1:])))
    guardar_resultados("incendio_forestal", datos, "simulaciones/incendio_forestal.py",
                       semillas={"incendio": SEMILLA},
                       parametros={"L": L, "thetas": THETAS, "plantados": "30000·θ + 2000000",
                                   "transitorio": "primer 20 %", "xmin_fijo": XMIN_FIJO,
                                   "max_eventos_ajuste": MAX_EVENTOS_AJUSTE})
