---
name: paper-typst
description: Cómo escribir y compilar el paper corto del laboratorio en Typst (paper/main.typ), con cada afirmación atada a una figura, un número de resultados/ o una referencia verificada de paper/referencias.bib. Úsala al redactar o editar cualquier sección del paper, al compilarlo, al corregir errores de compilación de Typst, y cuando alguien pida «escribe la introducción», «redacta los resultados», «compila el paper» o «¿por qué no compila?».
---

# paper-typst

El paper vive en `paper/`: `main.typ` (el texto), `referencias.bib` (las referencias, verificadas)
y `figuras/` (copias versionadas de las figuras, con su procedencia). Cada frase que afirma algo
sobre el mundo o sobre nuestros resultados tiene detrás **una** de tres cosas: una figura de
`paper/figuras/`, un número de `resultados/*.json` o una clave de `paper/referencias.bib`.

## Compilar

Desde la raíz del repositorio:

```sh
typst compile --root paper paper/main.typ paper/main.pdf
typst watch   --root paper paper/main.typ paper/main.pdf   # recompila al guardar
```

En Terminus, Typst ya viene instalado. Si `typst` no está en el PATH, usa el ejecutable de
Terminus o instálalo desde https://typst.app (también se puede subir la carpeta `paper/` a la
web de Typst y compilar ahí). `--root paper` hace que las rutas de imágenes y del `.bib` sean
relativas a `paper/`. El PDF no se versiona.

## Estructura

La plantilla trae, en este orden: título y autores, **Resumen**, **Introducción**, **Métodos**,
**Resultados**, **Discusión** (con «Lo que no funcionó») y **Referencias**. Los marcadores
`#pendiente[...]` señalan lo que falta y salen en el PDF resaltados: un paper terminado no tiene
ninguno (búscalos con `grep -n "pendiente\[" paper/main.typ`).

## Pasos para escribir una sección

1. **Haz el inventario** de lo que hay: figuras en `paper/figuras/` (y su procedencia en
   `paper/figuras/PROCEDENCIA.md`), números en `resultados/`, claves en `paper/referencias.bib`.
   Lo que no está ahí no existe para el paper.
2. **Escribe cada afirmación con su respaldo al lado.**
   - Número: cópialo del JSON con el redondeo que permite su precisión, y di de qué archivo sale
     en un comentario: `// resultados/logistica.json → feigenbaum.delta_logistica[-1]`.
   - Figura: `@fig-etiqueta` en el texto, y la figura incluida con `#figure(...) <fig-etiqueta>`.
   - Referencia: `@clave` (por ejemplo `@may1976`). La clave debe existir en el `.bib`.
3. **Si falta el respaldo, no escribas la afirmación**: deja `#pendiente[falta: …]` y pídelo a quien
   lo produce (la figura o el número a quien simula, la referencia a quien la verifica).
4. **Resultados describe, Discusión interpreta.** En Resultados, qué se midió y qué salió. En
   Discusión, qué significa, qué no se puede afirmar y qué no funcionó.
5. **Compila** y corrige hasta que no haya errores ni advertencias.

## Typst en una página

```typst
= Sección                      // == subsección
*negrita*, _cursiva_, `código`
$x_(n+1) = r x_n (1 - x_n)$    // ecuación en línea
$ delta = lim_(n -> oo) (R_(n-1) - R_(n-2)) / (R_n - R_(n-1)) $ <ec-delta>   // en bloque, con etiqueta
Según @may1976, …              // cita
como muestra @fig-bifurcacion  // referencia a figura
#figure(image("figuras/x.png", width: 80%), caption: [Pie.]) <fig-x>
#figure(table(columns: 3, [a], [b], [c]), caption: [Tabla.]) <tab-x>
#bibliography("referencias.bib", title: "Referencias", style: "apa")
```

## Errores de compilación frecuentes

| Mensaje | Causa y arreglo |
|---|---|
| `file not found` en una imagen | La ruta es relativa a `paper/`: `figuras/x.png`, no `../figuras/x.png`. Copia la figura con `simulaciones/copiar_al_paper.py` |
| `label <x> does not exist in the document` | Citas `@x` y no hay figura con `<x>` ni clave `x` en el `.bib` |
| `failed to parse BibTeX` | Una llave sin cerrar o una coma que falta en `referencias.bib` |
| `unexpected …` dentro de `$…$` | En matemáticas los subíndices con más de un carácter van entre paréntesis: `x_(n+1)` |
| Un `#` o `@` literal sale raro | Escríbelo con barra: `\#`, `\@` |
