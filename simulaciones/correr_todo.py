"""Corre todas las simulaciones del kit, una tras otra, y avisa si alguna falla.

    python simulaciones/correr_todo.py            # tamaños normales (~3 min con numba)
    python simulaciones/correr_todo.py --rapido   # tamaños pequeños, para probar que todo funciona;
                                                  # sus salidas llevan el sufijo _rapido
"""
import subprocess
import sys
import time
from pathlib import Path

for _flujo in (sys.stdout, sys.stderr):      # la consola de Windows no siempre usa UTF-8
    if hasattr(_flujo, "reconfigure"):
        _flujo.reconfigure(encoding="utf-8", errors="replace")

AQUI = Path(__file__).resolve().parent
SCRIPTS = ["logistica.py", "automatas_elementales.py", "pila_de_arena.py", "incendio_forestal.py"]
extra = ["--rapido"] if "--rapido" in sys.argv else []

fallos = []
for s in SCRIPTS:
    t0 = time.time()
    r = subprocess.run([sys.executable, str(AQUI / s), *extra])
    print(f"--- {s}: {'bien' if r.returncode == 0 else 'FALLÓ'} ({time.time() - t0:.0f} s)\n", flush=True)
    if r.returncode != 0:
        fallos.append(s)
if fallos:
    sys.exit(f"Fallaron: {', '.join(fallos)}")
print("Todas las simulaciones terminaron. Figuras en figuras/, números en resultados/.")
