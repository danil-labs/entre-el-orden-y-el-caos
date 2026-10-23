"""Autómatas celulares elementales (las 256 reglas de Wolfram): Reglas 30, 90 y 110 y barrido completo.

    python simulaciones/automatas_elementales.py

Figuras (en figuras/):
  ac_reglas.png    Reglas 30, 90 y 110 desde una sola celda encendida
  ac_barrido.png   las 256 reglas en el plano compresión–entropía, con reglas de referencia marcadas
Números:
  resultados/automatas_elementales.json   resumen, verificación y sensibilidad al ancho
  resultados/automatas_256_reglas.csv     una fila por regla: compresión, entropía, densidad

Dos medidas de «complejidad aparente» de cada diagrama espacio-tiempo:
  - razón de compresión zlib (bytes comprimidos / bytes crudos): ~0 = muy regular, ~1 = incompresible;
  - entropía de Shannon de bloques de K celdas, normalizada a [0, 1].
Ninguna de las dos ordena por sí sola las clases de Wolfram (con ancho 256, la Regla 90, de clase III,
comprime más que la 110, de clase IV): es parte de lo que hay que discutir.
Tarda ~1 minuto.
"""
import math
import zlib

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from comun import RES, RAPIDO, guardar_figura, guardar_resultados, TINTA, TINTA2, AZUL, NARANJA, AQUA, TENUE

SEMILLA = 2026
ANCHO, PASOS, TRANSITORIO, K = 256, 256, 64, 6
# Reglas de referencia y su clase de Wolfram (1984) más citada. Son ejemplos, no una clasificación nuestra.
REFERENCIA = {0: "I", 255: "I", 4: "II", 108: "II", 30: "III", 90: "III", 110: "IV"}


def paso(estado, regla):
    """Un paso de la regla `regla` (0–255) con frontera periódica."""
    vecindad = (np.roll(estado, 1) << 2) | (estado << 1) | np.roll(estado, -1)
    return (regla >> vecindad) & 1


def simular(regla, ancho, pasos, inicio, rng=None, posicion=None):
    """Diagrama espacio-tiempo (pasos × ancho). inicio = 'centro' (una celda encendida, en el centro
    o en `posicion`) o 'azar'."""
    if inicio == "centro":
        e = np.zeros(ancho, dtype=np.int64)
        e[ancho // 2 if posicion is None else posicion] = 1
    else:
        e = rng.integers(0, 2, ancho).astype(np.int64)
    d = np.empty((pasos, ancho), dtype=np.int64)
    for t in range(pasos):
        d[t] = e
        e = paso(e, regla)
    return d


def compresion(d):
    crudo = np.packbits(d.astype(np.uint8)).tobytes()
    return len(zlib.compress(crudo, 9)) / len(crudo)


def entropia_bloques(d, k=K):
    ventanas = sum(np.roll(d, -i, axis=1) << (k - 1 - i) for i in range(k)).ravel()
    p = np.bincount(ventanas, minlength=2 ** k) / ventanas.size
    p = p[p > 0]
    return max(0.0, float(-(p * np.log2(p)).sum() / k))


def verifica_pascal(n=64):
    """Control de corrección: la Regla 90 desde una celda reproduce el triángulo de Pascal módulo 2."""
    d = simular(90, 2 * n + 1, n, "centro")
    return all(d[t, n - t + 2 * j] == math.comb(t, j) % 2 for t in range(n) for j in range(t + 1))


def barrido(ancho, rng):
    filas = []
    for r in range(256):
        d = simular(r, ancho, PASOS, "azar", rng)[TRANSITORIO:]
        filas.append({"regla": r, "compresion": compresion(d), "entropia": entropia_bloques(d),
                      "densidad": float(d.mean())})
    return filas


def figura_reglas():
    cmap = ListedColormap(["white", TINTA])
    fig, ejes = plt.subplots(1, 3, figsize=(8, 2.2))
    # La Regla 110 solo crece hacia la izquierda: la celda inicial va cerca del borde derecho.
    for ax, r, c, pos in zip(ejes, [30, 90, 110], ["clase III", "clase III (Pascal mod 2)", "clase IV"], [None, None, 158]):
        ax.imshow(simular(r, 161, 80, "centro", posicion=pos), cmap=cmap, interpolation="nearest")
        ax.set_title(f"Regla {r} · {c}", fontsize=9)
        ax.axis("off")
    guardar_figura(fig, "ac_reglas.png")


def figura_barrido(filas):
    comp = np.array([f["compresion"] for f in filas])
    ent = np.array([f["entropia"] for f in filas])
    colores = {"I": TENUE, "II": AQUA, "III": NARANJA, "IV": AZUL}
    fig, ax = plt.subplots(figsize=(5.6, 4))
    ax.scatter(comp, ent, s=14, c=TINTA2, alpha=0.35, edgecolor="none", label="256 reglas")
    for r, c in REFERENCIA.items():
        ax.scatter(comp[r], ent[r], s=60, c=colores[c], edgecolor="white", linewidth=1.5, zorder=3)
        if r == 255:
            continue                       # cae encima de la Regla 0
        ax.annotate("0 y 255" if r == 0 else str(r), (comp[r], ent[r]), xytext=(5, 4), textcoords="offset points", fontsize=7, color=TINTA)
    for c, col in colores.items():
        ax.scatter([], [], c=col, s=40, edgecolor="white", label=f"clase {c} (referencia)")
    ax.set(xlabel="razón de compresión (zlib)", ylabel=f"entropía de bloques (k = {K}), normalizada")
    ax.legend(fontsize=7, loc="lower right")
    guardar_figura(fig, "ac_barrido.png")


if __name__ == "__main__":
    print("Autómatas celulares elementales")
    rng = np.random.default_rng(SEMILLA)
    figura_reglas()
    filas = barrido(ANCHO, rng)
    figura_barrido(filas)

    lineas = ["regla,compresion,entropia,densidad"] + [
        f"{f['regla']},{f['compresion']:.5f},{f['entropia']:.5f},{f['densidad']:.5f}" for f in filas]
    (RES / ("automatas_256_reglas_rapido.csv" if RAPIDO else "automatas_256_reglas.csv")).write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("  números  -> resultados/automatas_256_reglas.csv")

    # ¿Cambia algo si el ancho no es potencia de 2? (misma semilla, ancho 257)
    filas257 = barrido(ANCHO + 1, np.random.default_rng(SEMILLA))
    comp = np.array([f["compresion"] for f in filas])
    ent = np.array([f["entropia"] for f in filas])
    orden = np.argsort(comp)
    datos = {
        "pascal_mod2_verificado": verifica_pascal(),
        "compresion_media": round(float(comp.mean()), 4),
        "entropia_media": round(float(ent.mean()), 4),
        "correlacion_compresion_entropia": round(float(np.corrcoef(comp, ent)[0, 1]), 4),
        "reglas_con_compresion_menor_0_1": int((comp < 0.1).sum()),
        "reglas_con_compresion_mayor_0_9": int((comp > 0.9).sum()),
        "menos_comprimibles": [int(i) for i in orden[-8:][::-1]],
        "referencia": {str(r): {"clase": c, "compresion": round(comp[r], 3), "entropia": round(ent[r], 3)}
                       for r, c in REFERENCIA.items()},
        "sensibilidad_ancho_257": {str(r): {"compresion": round(filas257[r]["compresion"], 3),
                                            "entropia": round(filas257[r]["entropia"], 3)} for r in REFERENCIA},
    }
    guardar_resultados("automatas_elementales", datos, "simulaciones/automatas_elementales.py",
                       semillas={"condicion_inicial_azar": SEMILLA},
                       parametros={"ancho": ANCHO, "pasos": PASOS, "transitorio": TRANSITORIO, "k_bloques": K})
    r90, r90b = datos["referencia"]["90"], datos["sensibilidad_ancho_257"]["90"]
    print(f"  Pascal mod 2: {datos['pascal_mod2_verificado']}; Regla 90 compresión ancho 256 = "
          f"{r90['compresion']} vs ancho 257 = {r90b['compresion']}")
