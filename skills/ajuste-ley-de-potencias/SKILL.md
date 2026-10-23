---
name: ajuste-ley-de-potencias
description: Método para decidir si unos datos siguen una ley de potencias, con máxima verosimilitud y pruebas de razón de verosimilitud (Clauset, Shalizi y Newman 2009), comparando contra una ley de potencias con corte y variando el tamaño del sistema para no confundir un efecto de tamaño finito con la ausencia de criticalidad. Úsala cuando alguien pida «ajusta una ley de potencias», «¿es una ley de potencias?», «saca el exponente», al analizar avalanchas, incendios, frecuencias o cualquier distribución de cola pesada, y al revisar una afirmación de ley de potencias en el paper.
---

# ajuste-ley-de-potencias

Una recta en papel log-log **no es evidencia** de una ley de potencias. Datos log-normales dan una
cola casi recta (R² ≈ 0.99) y ajustar por mínimos cuadrados sobre un histograma da exponentes
sesgados. El método de Clauset, Shalizi y Newman (2009, *SIAM Review* 51:661–703,
doi 10.1137/070710111) sustituye la recta por tres preguntas: ¿desde dónde vale la cola (x_min)?,
¿qué exponente tiene (máxima verosimilitud)? y ¿la ley de potencias explica la cola mejor que las
alternativas (razón de verosimilitud)?

En un sistema **finito** hay una cuarta pregunta, y sin ella el método da la respuesta equivocada:
¿el corte de la distribución se mueve al crecer el tamaño del sistema?

La implementación está en `simulaciones/leyes_potencia.py` (paquete `powerlaw`). Los ejemplos
completos, en `simulaciones/pila_de_arena.py` e `simulaciones/incendio_forestal.py`.

## Entradas

- Los datos crudos (tamaños de avalancha, de incendio, frecuencias…), uno por evento. Nunca un
  histograma ya agregado.
- Si son discretos (enteros) o continuos.
- Si vienen de un modelo: el parámetro que limita el tamaño (L, θ…) y la posibilidad de correr
  varios valores.

## Pasos

1. **Dibuja la CCDF** P(X ≥ x) en log-log, no el histograma con bins lineales. Solo para mirar.
2. **Ajuste automático** (`ajuste_automatico`): x_min elegido minimizando la distancia de
   Kolmogorov-Smirnov, α por máxima verosimilitud con su error, y comparación contra log-normal y
   exponencial. Anota x_min y cuántos datos quedan en la cola (`n_cola`): con menos de ~100 en la
   cola, ninguna conclusión es firme.
3. **Lee las comparaciones con su p.** En `distribution_compare(a, b)`, R > 0 favorece a `a`, y
   el signo solo cuenta si p < 0.05. Con p ≥ 0.05 los datos **no distinguen** las dos
   distribuciones: no digas que gana la ley de potencias.
4. **Ajuste con corte** (`ajuste_con_corte`), con x_min fijo y bajo, dentro del rango de escala
   (en los ejemplos, x_min = 10): ley pura contra ley con corte exponencial
   p(x) ∝ x^(−α) e^(−λx) y contra log-normal. Si gana la de corte, anota 1/λ, la escala del corte.
5. **Varía el tamaño del sistema.** Corre al menos tres valores del parámetro que limita el
   tamaño (L = 32, 64, 128 en la pila de arena; θ = 100, 300, 1000 en el incendio) y dibuja las
   distribuciones juntas. Si el sistema es crítico, la parte recta se alarga y el corte (el máximo,
   el percentil 99.9, 1/λ) se mueve a la derecha. Ese desplazamiento es la evidencia; un solo
   tamaño no la da.
6. **Decide qué afirmar** con la tabla de abajo, y escribe también lo que no se puede afirmar.

| Lo que salió | Qué se puede escribir |
|---|---|
| Gana la de corte (p < 0.05) contra pura y log-normal, **y** el corte crece con el tamaño | «ley de potencias con corte de tamaño finito, exponente α ≈ …», con la figura de tamaño finito |
| Gana la de corte, pero no se varió el tamaño | «compatible con una ley de potencias con corte»; falta la prueba de tamaño finito |
| Log-normal y ley de potencias indistinguibles (p ≥ 0.05) | «cola pesada; los datos no distinguen ley de potencias de log-normal» |
| Gana la log-normal (R < 0, p < 0.05) | no hay ley de potencias; describe la distribución que sí ajusta |

## La advertencia de tamaño finito (lo que pasa con los modelos de este kit)

Con `python simulaciones/pila_de_arena.py` (ver `resultados/pila_de_arena.json`), el ajuste
automático en L = 128 elige x_min = 16 352, justo donde el sistema finito se corta, deja 839 datos
en la cola y **rechaza** la ley de potencias (pierde contra la log-normal, R = −5.8). Con x_min = 10,
la ley con corte gana contra la pura (R = 68.7) y contra la log-normal (R = 28.6), ambas con
p < 10⁻⁴, y al variar L el corte se mueve: la avalancha máxima pasa de 2 871 (L = 32) a 19 153
(L = 64) y 140 030 (L = 128). El incendio forestal repite el patrón con θ. La prueba «rigurosa»
aplicada a ciegas da la respuesta equivocada; hace falta entender el sistema.

Una señal más: en los dos modelos el ajuste automático da α = 3.000 exacto. Un exponente redondo e
idéntico en dos sistemas distintos sugiere que el optimizador topó con el borde de su rango de
parámetros; no lo reportes como medición.

Por tiempo, `simulaciones/leyes_potencia.py` prueba hasta 60 candidatos de x_min en escala logarítmica
(no todos los valores, como el método original) y los scripts ajustan una submuestra de hasta
50 000 eventos con semilla fija. Las dos cosas quedan anotadas en el JSON de resultados.

## Errores frecuentes

- Ajustar una recta a un histograma log-log y llamar α a su pendiente.
- Reportar α sin x_min, sin error y sin cuántos datos hay en la cola.
- Reportar R sin p, o tratar R > 0 con p = 0.4 como victoria.
- Presentar el exponente como definitivo. Los exponentes de la pila de arena y del incendio
  tienen correcciones conocidas en la literatura; sin compararlos con ella, son estimaciones.
- Variar el parámetro equivocado: en el incendio el corte lo fija θ mientras L sea grande;
  variar L con θ fijo no mueve el corte.

## Salida

```
Datos:            <qué son>, n = …, discretos/continuos
Automático:       x_min = …, n_cola = …, α = … ± …; vs log-normal R = …, p = …; vs exponencial R = …, p = …
Con corte:        x_min = …, α = …, 1/λ = …; corte vs pura R = …, p = …; corte vs log-normal R = …, p = …
Tamaño finito:    <parámetro> = …, …, … → máximo …, …, …; ¿se mueve el corte? sí/no
Se puede afirmar: …
No se puede:      …
Figuras/números:  figuras/…, resultados/…json
```
