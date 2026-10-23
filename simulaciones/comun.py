"""Piezas comunes de las simulaciones del kit: rutas, estilo de figura y guardado.

Todas las rutas son relativas a la raíz del repositorio, así que los scripts se
pueden correr desde cualquier carpeta:

    python simulaciones/logistica.py

Cada script escribe sus figuras en `figuras/` y sus números en `resultados/`.
"""
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sin ventana: funciona igual en una terminal, en un servidor o en Colab
import matplotlib.pyplot as plt
import numpy as np

# En Windows la consola suele usar cp1252 y no sabe escribir «δ» o «λ»: forzamos UTF-8.
for _flujo in (sys.stdout, sys.stderr):
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

try:  # numba compila los bucles; sin numba el código es el mismo, solo más lento
    from numba import njit
    HAY_NUMBA = True
except ImportError:  # pragma: no cover
    HAY_NUMBA = False

    def njit(*args, **kwargs):
        if args and callable(args[0]):
            return args[0]
        return lambda f: f

# Con --rapido los scripts usan tamaños pequeños; sus salidas llevan el sufijo «_rapido» para que
# nunca sustituyan a las del modo normal, que son las que se citan en el paper.
RAPIDO = "--rapido" in sys.argv
_SUFIJO = "_rapido" if RAPIDO else ""

RAIZ = Path(__file__).resolve().parent.parent
FIG = RAIZ / "figuras"
RES = RAIZ / "resultados"
FIG.mkdir(exist_ok=True)
RES.mkdir(exist_ok=True)

# ---- estilo: fondo claro, marcas finas, rejilla tenue (pensado para imprimirse en un paper) ----
TINTA, TINTA2, TENUE, REJILLA = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"     # colores categóricos, en este orden
# Rampa secuencial (un solo tono, de claro a oscuro) para series ordenadas, como tamaños L.
SECUENCIAL = ["#9cc3ee", "#5f9de4", "#2a78d6", "#1b4f8f"]

plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "text.color": TINTA, "axes.labelcolor": TINTA, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.edgecolor": TENUE, "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "legend.frameon": False, "lines.linewidth": 1.4,
})


def guardar_figura(fig, nombre):
    """Guarda `figuras/<nombre>` en PNG (200 ppp) y devuelve la ruta relativa al repo.
    En modo --rapido, `figuras/<nombre>_rapido.png`."""
    fig.tight_layout()
    nombre = nombre.replace(".png", f"{_SUFIJO}.png")
    ruta = FIG / nombre
    fig.savefig(ruta, dpi=200)
    plt.close(fig)
    print(f"  figura   -> {ruta.relative_to(RAIZ).as_posix()}")
    return ruta.relative_to(RAIZ).as_posix()


def _a_json(x):
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    raise TypeError(f"no sé convertir {type(x)} a JSON")


def guardar_resultados(nombre, datos, script, semillas, parametros):
    """Escribe `resultados/<nombre>.json` con los números y con lo necesario para reproducirlos."""
    contenido = {
        "script": script,
        "semillas": semillas,
        "parametros": parametros,
        "entorno": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "plataforma": platform.platform(),
            "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "resultados": datos,
    }
    ruta = RES / f"{nombre}{_SUFIJO}.json"
    ruta.write_text(json.dumps(contenido, indent=2, ensure_ascii=False, default=_a_json), encoding="utf-8")
    print(f"  números  -> {ruta.relative_to(RAIZ).as_posix()}")
    return ruta
