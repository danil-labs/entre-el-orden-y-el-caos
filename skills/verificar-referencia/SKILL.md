---
name: verificar-referencia
description: Verifica que una referencia bibliográfica existe y dice lo que se le atribuye, contra el DOI y la página del editor, y la deja como entrada BibTeX correcta. Úsala antes de añadir cualquier cita a paper/referencias.bib, al revisar una cita del paper, cuando alguien pida «busca referencias sobre…», «¿esta cita es real?», «comprueba el DOI», o cuando una referencia venga de la memoria de un modelo, de otro paper o de una lista sin DOI.
---

# verificar-referencia

Una referencia está **verificada** cuando tres cosas coinciden en una fuente primaria (el DOI
resuelto o la página del editor): que existe, que sus metadatos son los que escribimos, y que
contiene lo que el paper le atribuye. Si falta cualquiera de las tres, no está verificada y no
entra en `paper/referencias.bib`.

Los modelos de lenguaje inventan referencias plausibles: autores reales, revista real, título
verosímil, DOI que no resuelve o que lleva a otro artículo. Por eso ninguna referencia se da por
buena porque «suena bien» o porque la recuerda un agente.

## Entradas

- Lo que se quiere citar: una afirmación concreta («la pila de arena muestra criticalidad
  autoorganizada») o una referencia candidata (autores, año, título, revista, DOI si lo hay).
- Si es una búsqueda: el tema y cuántas referencias se necesitan.

## Pasos

1. **Consigue el DOI.** Si la candidata no lo trae, búscalo por título en Crossref
   (`https://api.crossref.org/works?query.bibliographic=<título+autor>&rows=5`) o en la página de
   la revista. Sin DOI ni URL estable del editor, la referencia queda como *no verificada*.
2. **Resuelve el DOI.** Abre `https://doi.org/<doi>` y los metadatos en
   `https://api.crossref.org/works/<doi>`. Compara uno por uno: autores (orden y ortografía),
   año, título exacto, revista, volumen, páginas o número de artículo. Una sola discrepancia es
   un hallazgo: corrige con lo que dice el editor, nunca con lo que decía la candidata.
3. **Comprueba lo que se le atribuye.** Lee al menos el resumen (y, si es posible, la sección
   pertinente). La referencia debe sostener la afirmación concreta del paper, no solo el tema.
   Si solo se pudo leer el resumen, dilo en el campo `note` de la entrada.
4. **Escribe la entrada BibTeX** con la clave `apellidoAño` en minúsculas (`may1976`,
   `wolfram1983`; si se repite, `wolfram1983a`). Incluye siempre `doi`. No inventes campos que
   no viste: si no hay número, no pongas `number`.
5. **Anota la verificación** en la propia entrada, en un comentario justo encima:
   `% verificada: <fecha AAAA-MM-DD>, DOI resuelto, metadatos de Crossref; atribución: <qué sostiene>`.

## Salida

Para cada referencia, una línea de estado y, si pasó, la entrada:

```
[verificada]     may1976 — May (1976) Nature 261:459–467 — sostiene: duplicación de periodo y caos en la logística
[corregida]      bak1987 — el año decía 1988; el editor dice 1987
[no verificada]  <candidata> — el DOI resuelve a otro artículo / no existe / no se pudo leer
```

Las *no verificadas* no se escriben en el `.bib`: se devuelven a quien las pidió con el motivo.

## Ejemplo de entrada correcta

```bibtex
% verificada: 2026-10-22, DOI resuelto, metadatos de Crossref; atribución: modelo de la pila de arena
@article{bak1987,
  author  = {Bak, Per and Tang, Chao and Wiesenfeld, Kurt},
  title   = {Self-organized criticality: An explanation of the 1/f noise},
  journal = {Physical Review Letters},
  volume  = {59},
  number  = {4},
  pages   = {381--384},
  year    = {1987},
  doi     = {10.1103/PhysRevLett.59.381},
}
```

## Errores frecuentes

- Un DOI que resuelve, pero a otro artículo del mismo autor. Compara siempre el título.
- Preprint contra versión publicada: cita la publicada si existe, y comprueba que el resultado
  citado sigue en ella.
- Atribuir a una referencia lo que dice otra que la cita. Si la afirmación viene de una reseña,
  cita la reseña o lee la original.
- Sin acceso a la red no se puede verificar: la referencia queda *no verificada*, no «probablemente
  correcta».
