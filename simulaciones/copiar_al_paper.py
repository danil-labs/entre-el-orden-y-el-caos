"""Copia una figura de figuras/ a paper/figuras/ y anota de qué script sale.

    python simulaciones/copiar_al_paper.py logistica_bifurcacion.png

Las figuras de figuras/ no se versionan; las de paper/figuras/ sí, junto con su procedencia en
paper/figuras/PROCEDENCIA.md. Así quien revise el paper sabe con qué script regenerar cada figura.
"""
import re
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if len(sys.argv) != 2:
    sys.exit(__doc__)
nombre = sys.argv[1]
origen = RAIZ / "figuras" / nombre
if not origen.exists():
    sys.exit(f"No existe figuras/{nombre}. Corre primero el script que la genera.")

# ¿Qué script la genera? Buscamos el nombre del archivo en simulaciones/*.py y notebooks/*.ipynb.
fuentes = [p.relative_to(RAIZ).as_posix()
           for p in sorted((RAIZ / "simulaciones").glob("*.py")) + sorted((RAIZ / "notebooks").glob("*.ipynb"))
           if p.name != "copiar_al_paper.py" and nombre in p.read_text(encoding="utf-8")]
destino = RAIZ / "paper" / "figuras" / nombre
destino.parent.mkdir(exist_ok=True)
shutil.copy2(origen, destino)

registro = RAIZ / "paper" / "figuras" / "PROCEDENCIA.md"
texto = registro.read_text(encoding="utf-8") if registro.exists() else (
    "# Procedencia de las figuras del paper\n\n"
    "Cada figura de esta carpeta se regenera con el script indicado y se copia aquí con\n"
    "`python simulaciones/copiar_al_paper.py <figura>`. No edites estas figuras a mano.\n\n"
    "| Figura | Se genera con |\n|---|---|\n")
fila = f"| `{nombre}` | {', '.join(f'`{f}`' for f in fuentes) or 'NO ENCONTRADO: anótalo a mano'} |"
texto = re.sub(rf"^\| `{re.escape(nombre)}` \|.*$\n?", "", texto, flags=re.M)
registro.write_text(texto.rstrip("\n") + "\n" + fila + "\n", encoding="utf-8")
print(f"figuras/{nombre} -> paper/figuras/{nombre} (procedencia: {', '.join(fuentes) or '?'})")
