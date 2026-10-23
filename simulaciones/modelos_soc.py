"""Dos autómatas celulares de criticalidad autoorganizada, compilados con numba.

- pila_de_arena: Bak, Tang y Wiesenfeld (1987). Cada grano cae en una celda al azar; una celda con
  4 o más granos se derrumba y reparte uno a cada vecina. En el borde la arena se cae.
  Devuelve el tamaño de cada avalancha (número de derrumbes) y el estado final.
- incendio: Drossel y Schwabl (1992). Se planta un árbol por paso; cada `theta` árboles cae un rayo en
  una celda al azar y, si hay árbol, se quema todo el bosque conectado a ella.
  Devuelve el tamaño de cada incendio (árboles quemados) y el bosque final.

Las semillas se pasan siempre como argumento: con la misma semilla, el mismo resultado.
"""
import numpy as np
from comun import njit


@njit(cache=True)
def pila_de_arena(L, granos, semilla):
    np.random.seed(semilla)
    z = np.zeros((L, L), np.int64)
    tam = np.zeros(granos, np.int64)
    pila = np.empty(L * L * 8, np.int64)
    for g in range(granos):
        i = np.random.randint(L)
        j = np.random.randint(L)
        z[i, j] += 1
        n = 0
        tope = 0
        if z[i, j] >= 4:
            pila[0] = i * L + j
            tope = 1
        while tope > 0:
            tope -= 1
            k = pila[tope]
            a = k // L
            b = k % L
            if z[a, b] < 4:
                continue
            z[a, b] -= 4
            n += 1
            if z[a, b] >= 4:
                pila[tope] = k
                tope += 1
            for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x = a + da
                y = b + db
                if 0 <= x < L and 0 <= y < L:
                    z[x, y] += 1
                    if z[x, y] == 4:
                        pila[tope] = x * L + y
                        tope += 1
        tam[g] = n
    return tam, z


@njit(cache=True)
def incendio(L, plantados, theta, semilla):
    np.random.seed(semilla)
    bosque = np.zeros(L * L, np.uint8)
    fuegos = np.empty(plantados // theta + 1, np.int64)
    nf = 0
    cola = np.empty(L * L, np.int64)
    for t in range(plantados):
        k = np.random.randint(L * L)
        bosque[k] = 1
        if (t + 1) % theta == 0:
            k = np.random.randint(L * L)
            if bosque[k] == 1:
                bosque[k] = 0
                cola[0] = k
                ini = 0
                fin = 1
                while ini < fin:
                    c = cola[ini]
                    ini += 1
                    a = c // L
                    b = c % L
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        x = a + da
                        y = b + db
                        if 0 <= x < L and 0 <= y < L and bosque[x * L + y] == 1:
                            bosque[x * L + y] = 0
                            cola[fin] = x * L + y
                            fin += 1
                fuegos[nf] = fin
                nf += 1
    return fuegos[:nf], bosque.reshape(L, L)
