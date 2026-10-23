---
name: figura-para-paper
description: Cómo hacer y llevar al paper una figura que se lee impresa, dice una sola cosa y se regenera con un script del repositorio. Úsala al crear o retocar una figura destinada a paper/, cuando alguien pida «haz la figura de…», «pon la figura en el paper», «mejora esta gráfica», y al revisar si una figura del paper sostiene lo que dice su pie.
---

# figura-para-paper

Una figura del paper **dice una sola cosa**, que su pie enuncia, y se **regenera** con un comando.
Si no puedes escribir en una frase qué debe ver el lector, la figura todavía no existe.

## Pasos

1. **Escribe primero el pie.** Una frase con la afirmación («El corte de la distribución de
   avalanchas crece con el tamaño del sistema») y después qué se grafica, con unidades y
   parámetros (L, semilla, número de eventos). El pie no promete nada que la figura no muestre.
2. **Elige la forma por el trabajo del dato.**
   - Distribución de cola pesada: CCDF o densidad en bins logarítmicos, ejes log-log.
   - Evolución con un parámetro (bifurcación, Lyapunov): parámetro en el eje x.
   - Varias series de un parámetro ordenado (L = 32, 64, 128): un solo tono de claro a oscuro
     (`SECUENCIAL` en `simulaciones/comun.py`), no colores arbitrarios.
   - Categorías sin orden: los colores categóricos en orden fijo (`AZUL`, `NARANJA`, `AQUA`).
   - Nunca dos ejes y distintos en la misma gráfica: dos paneles.
3. **Genérala con un script**, usando el estilo de `simulaciones/comun.py` (fondo blanco, marcas
   finas, rejilla tenue) y `guardar_figura`. Nada de retoques a mano en un editor de imágenes.
4. **Legibilidad impresa.** Texto ≥ 7 pt al tamaño final; ancho de columna ≈ 8 cm, página
   completa ≈ 17 cm. Ejes con nombre y unidades, leyenda si hay dos o más series, y la identidad
   de cada serie nunca solo por color (marcador o línea distintos, o etiqueta directa).
5. **Cópiala al paper** con `python simulaciones/copiar_al_paper.py <figura>.png`. Eso la pone en
   `paper/figuras/` y anota de qué script sale en `paper/figuras/PROCEDENCIA.md`. Las figuras de
   `figuras/` no se versionan; las de `paper/figuras/` sí.
6. **Inclúyela en Typst** con una etiqueta y refiérela desde el texto:

   ```typst
   #figure(
     image("figuras/logistica_bifurcacion.png", width: 100%),
     caption: [La población a largo plazo pasa de un punto fijo a ciclos de periodo 2, 4, … y al caos. $x_0 = 0.4$, 400 puntos por valor de $r$ tras 2000 pasos de transitorio.],
   ) <fig-bifurcacion>
   ```

## Comprobación antes de entregar

- [ ] El pie enuncia una afirmación y la figura la muestra sin necesidad del texto.
- [ ] Hay un script que la regenera y está anotado en `paper/figuras/PROCEDENCIA.md`.
- [ ] Los números del pie (parámetros, n) coinciden con el JSON de `resultados/`.
- [ ] Se lee impresa en blanco y negro.
