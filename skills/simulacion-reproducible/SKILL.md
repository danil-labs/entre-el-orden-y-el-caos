---
name: simulacion-reproducible
description: Cómo escribir, ejecutar y entregar una simulación o un notebook que cualquiera puede volver a correr y obtener las mismas figuras y los mismos números. Úsala al crear o modificar un script de simulaciones/ o un notebook de notebooks/, cuando alguien pida «corre la simulación», «genera la figura de…», «haz un barrido de…», o antes de entregar un resultado que va a citarse en el paper.
---

# simulacion-reproducible

Un resultado es **reproducible** cuando otra persona, con el repositorio y `requirements.txt`,
corre un comando y obtiene la misma figura y el mismo número. Si para obtenerlo hizo falta un paso
a mano, una celda corrida en otro orden o una semilla que nadie anotó, no es reproducible.

## Reglas

1. **Un script por resultado, en `simulaciones/`.** Cada script dice en su docstring cómo se corre,
   qué figuras genera, qué archivo de números escribe y cuánto tarda.
2. **Rutas relativas a la raíz del repositorio**, nunca absolutas ni dependientes de la carpeta
   desde donde se corre. Usa `RAIZ`, `FIG` y `RES` de `simulaciones/comun.py`.
3. **Semillas fijas y declaradas.** Todo azar pasa por una semilla escrita como constante al
   principio del script (`SEMILLA = 2026`) y se anota en el JSON de resultados. Con numba, la
   semilla se pasa como argumento a la función compilada (`np.random.seed` dentro de ella).
4. **Figuras a `figuras/`, números a `resultados/`.** Con `guardar_figura` y `guardar_resultados`
   de `simulaciones/comun.py`: el JSON guarda también parámetros, semillas y versiones.
   Ningún número del paper se copia de la consola: sale de un `resultados/*.json`.
5. **Un control de corrección por modelo.** Antes de medir algo nuevo, comprueba que el código
   reproduce algo conocido: la Regla 90 da el triángulo de Pascal mod 2; el primer valor
   superestable de la logística es 1 + √5; λ(r = 4) = ln 2. Si el control falla, no hay resultado.
6. **Transitorio descartado y declarado.** Los sistemas que llegan a un estado estacionario (pila
   de arena, incendio, atractor de la logística) descartan el principio, y el script dice cuánto.
7. **Prueba de sensibilidad.** Cambia un parámetro que *no debería* importar (el ancho de 256 a
   257, la semilla, la longitud del transitorio). Si el resultado cambia, eso es un hallazgo y se
   reporta, no se esconde.
8. **Modo rápido.** Si el script tarda más de un minuto, ofrece `--rapido` con tamaños pequeños
   para comprobar que todo corre; los números del paper salen del modo normal.

## Notebooks

- Deben correr **de principio a fin** con «Reiniciar y ejecutar todo», sin celdas que dependan de
  haber corrido otra antes a mano.
- La primera celda de código detecta si está en Google Colab, monta Drive y define la carpeta de
  salida; fuera de Colab usa la raíz del repositorio.
- Sin dependencias raras: numpy, matplotlib, scipy y, si hacen falta, numba y powerlaw (con
  instalación dentro del notebook si faltan). Si usan GPU (CuPy), con respaldo a NumPy.
- Se versionan **sin salidas** (las figuras se regeneran); limpia las salidas antes de entregar.

## Entrega

Al terminar, devuelve:

```
Script:      simulaciones/<script>.py  (comando exacto; tiempo que tardó)
Figuras:     figuras/<a>.png, figuras/<b>.png
Números:     resultados/<nombre>.json → claves que importan y su valor
Control:     <qué se comprobó y si pasó>
Sensibilidad:<qué se cambió y qué pasó>
No funcionó: <lo que se intentó y falló, con el porqué si se sabe>
```

«No funcionó» nunca se omite: si todo funcionó, dilo.

## Ejemplo

```
Script:      python simulaciones/automatas_elementales.py  (~1 min)
Figuras:     figuras/ac_reglas.png, figuras/ac_barrido.png
Números:     resultados/automatas_elementales.json → reglas_con_compresion_menor_0_1 = 134
Control:     pascal_mod2_verificado = true
Sensibilidad:ancho 257 en lugar de 256 → la compresión de la Regla 90 pasa de 0.14 a 1.00 (sensibilidad_ancho_257)
No funcionó: la compresión no ordena las clases: la Regla 90 (clase III) comprime más que la 110 (clase IV)
```
