"""Pila de arena de Bak-Tang-Wiesenfeld: avalanchas, ley de potencias y tamaño finito.

    python simulaciones/pila_de_arena.py            # L = 32, 64, 128 (~2 min)
    python simulaciones/pila_de_arena.py --rapido   # L = 32, 64 (<1 min), para probar
    python simulaciones/pila_de_arena.py --completo # añade L = 256 (varios minutos)

Figuras (en figuras/):
  arena_estado.png          la pila en estado crítico (el L más grande)
  arena_tamano_finito.png   P(s) para cada L: el corte se mueve a la derecha al crecer L
Números: resultados/pila_de_arena.json

Qué hace, en orden (ver skills/ajuste-ley-de-potencias/SKILL.md):
  1. ajuste automático (xmin por KS) en L = 128;
  2. ajuste con xmin fijo y bajo: ley pura vs. con corte vs. log-normal;
  3. tamaño finito: ¿la avalancha máxima y el percentil 99.9 crecen con L?
"""
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
from comun import guardar_figura, guardar_resultados, SECUENCIAL
from modelos_soc import pila_de_arena
from leyes_potencia import pdf_log, submuestra, ajuste_automatico, ajuste_con_corte, veredicto

SEMILLA = 3
XMIN_FIJO = 10
MAX_EVENTOS_AJUSTE = 50_000   # submuestra con semilla fija para que los ajustes tarden segundos
L_AJUSTE = 128
if "--rapido" in sys.argv:
    TAMANOS = [32, 64]
    L_AJUSTE = 64
elif "--completo" in sys.argv:
    TAMANOS = [32, 64, 128, 256]
else:
    TAMANOS = [32, 64, 128]


def granos_para(L):
    """Suficientes granos para llegar al estado crítico y juntar estadística: crece como L²."""
    return int(60 * L * L) + 300_000


if __name__ == "__main__":
    print(f"Pila de arena, L = {TAMANOS}")
    datos = {"por_tamano": {}}
    fig, ax = plt.subplots(figsize=(6, 4))
    for L, color in zip(TAMANOS, SECUENCIAL[-len(TAMANOS):]):
        t0 = time.time()
        g = granos_para(L)
        tam, z = pila_de_arena(L, g, SEMILLA)
        aval = tam[g // 3:]              # descartamos el primer tercio: transitorio hasta el estado crítico
        aval = aval[aval > 0]
        x, y = pdf_log(aval)
        ax.loglog(x, y, "o-", ms=3, lw=1, color=color, label=f"L = {L}")
        datos["por_tamano"][f"L{L}"] = {"granos": g, "avalanchas": int(aval.size), "maxima": int(aval.max()),
                                        "percentil_99_9": float(np.percentile(aval, 99.9))}
        print(f"  L = {L}: {aval.size} avalanchas, máxima {aval.max()} ({time.time() - t0:.1f} s)")
        if L == L_AJUSTE:
            t0 = time.time()
            muestra = submuestra(aval, MAX_EVENTOS_AJUSTE, SEMILLA)
            datos[f"ajuste_automatico_L{L}"] = ajuste_automatico(muestra)
            datos[f"ajuste_con_corte_L{L}"] = c = ajuste_con_corte(muestra, XMIN_FIJO)
            c["eventos_ajustados"] = int(muestra.size)
            c["veredicto"] = veredicto(c)
            print(f"  ajustes en L = {L} ({time.time() - t0:.1f} s): {c['veredicto']}")
        estado_final = (L, z)
    ax.set(xlabel="tamaño de avalancha s", ylabel="P(s)", title="El corte crece con el tamaño del sistema")
    ax.legend()
    guardar_figura(fig, "arena_tamano_finito.png")

    L, z = estado_final
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(z, cmap="Blues", interpolation="nearest", vmin=-1, vmax=3)
    ax.set_title(f"Pila de arena {L}×{L} en estado crítico (granos por celda, 0–3)")
    ax.axis("off")
    guardar_figura(fig, "arena_estado.png")

    maximos = [datos["por_tamano"][f"L{L}"]["maxima"] for L in TAMANOS]
    datos["el_maximo_crece_con_L"] = bool(all(b > a for a, b in zip(maximos, maximos[1:])))
    guardar_resultados("pila_de_arena", datos, "simulaciones/pila_de_arena.py",
                       semillas={"pila_de_arena": SEMILLA},
                       parametros={"tamanos": TAMANOS, "granos": "60·L² + 300000", "transitorio": "primer tercio",
                                   "xmin_fijo": XMIN_FIJO, "L_ajuste": L_AJUSTE,
                                   "max_eventos_ajuste": MAX_EVENTOS_AJUSTE})
