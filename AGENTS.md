# Laboratorio de investigación con agentes · reglas

Este repositorio es un laboratorio pequeño: simulaciones, notebooks y un paper corto en Typst. Las
reglas de abajo valen para todos, personas y agentes. Cuando una regla y una petición chocan, gana la
regla y se le avisa a la persona.

## Comandos

Desde la raíz del repositorio (Python 3.10 o posterior):

```sh
python -m pip install -r requirements.txt          # una vez
python simulaciones/correr_todo.py --rapido        # comprobar que todo corre (~3 min)
python simulaciones/correr_todo.py                 # resultados para el paper (~3 min)
python simulaciones/logistica.py                   # o un script suelto
python simulaciones/copiar_al_paper.py logistica_bifurcacion.png
typst compile --root paper paper/main.typ paper/main.pdf
```

Los notebooks de `notebooks/` corren de principio a fin en Google Colab o en local
(«Ejecutar todo»). Los agentes se validan con el validador de agent-creator:
`python <agent-creator>/scripts/validate_agent.py --root . --strict`.

## Reglas

1. **Reproducibilidad.** Toda figura y todo número sale de un script de `simulaciones/` o de un
   notebook de `notebooks/` que lo regenera con un comando. Todo azar tiene semilla fija, escrita
   como constante y guardada en el JSON de resultados. Rutas relativas a la raíz, nunca absolutas.
   Método: `skills/simulacion-reproducible/SKILL.md`.
2. **Ninguna referencia sin verificar.** Una cita entra en `paper/referencias.bib` solo si su DOI
   resuelve, sus metadatos coinciden con los del editor y sostiene la frase donde se cita. Nadie
   cita de memoria, ni personas ni agentes. Método: `skills/verificar-referencia/SKILL.md`.
3. **Cada afirmación del paper tiene respaldo en el repositorio**: una figura de `paper/figuras/`,
   un número de `resultados/` (con un comentario que dice archivo y clave) o una cita verificada.
   Sin respaldo, la afirmación no se escribe: se deja un `#pendiente[...]`.
   Método: `skills/paper-typst/SKILL.md`.
4. **Se reporta también lo que no funcionó.** Todo informe de simulación tiene «No funcionó» y
   todo paper tiene «Lo que no funcionó» en la Discusión. Una prueba de sensibilidad que «estorba»
   se reporta, no se esconde.
5. **Una ley de potencias se afirma solo con el método completo**: máxima verosimilitud,
   comparación contra ley con corte y log-normal, y variación del tamaño del sistema.
   Método: `skills/ajuste-ley-de-potencias/SKILL.md`.
6. **No se publican datos privados.** Nada de datos personales, de pacientes, de terceros sin
   permiso, credenciales ni archivos con licencia que no permita redistribuirlos. Los datos
   privados se quedan fuera del repositorio (la carpeta `datos-privados/` está ignorada por git) y
   en Colab se leen desde tu Drive, no se copian aquí.
7. **Un dueño por carpeta.** Cada agente escribe solo en lo suyo (tabla de abajo); para cambiar lo
   de otro, se le pide a su dueño.

## Dónde va cada cosa

| Carpeta o archivo | Qué contiene | Dueño | ¿Se versiona? |
|---|---|---|---|
| `simulaciones/` | Scripts reproducibles; `comun.py` con rutas y estilo | @simulador | sí |
| `notebooks/` | Notebooks para Colab, sin salidas | @simulador | sí |
| `figuras/` | Figuras generadas por los scripts | @simulador | no (se regeneran) |
| `resultados/` | Números en JSON/CSV, con semillas y parámetros | @simulador | sí |
| `paper/main.typ` | El paper | @redactor | sí |
| `paper/figuras/` | Copias de las figuras que usa el paper y su `PROCEDENCIA.md` | @simulador | sí |
| `paper/referencias.bib` | Referencias verificadas | @bibliotecario | sí |
| `skills/` | Los métodos que comparten los agentes | la persona | sí |
| `.agents/agents/` | Los agentes | la persona | sí |
| PDF del paper, entornos, cachés | Se regeneran | — | no |

## Agentes

| Agente | Qué hace | Techo | Skills |
|---|---|---|---|
| `bibliotecario` | Busca, verifica y mantiene `paper/referencias.bib` | edita y usa la web | `verificar-referencia` |
| `simulador` | Escribe y corre simulaciones y notebooks; entrega figuras y números | edita y ejecuta | `simulacion-reproducible`, `ajuste-ley-de-potencias`, `figura-para-paper` |
| `redactor` | Escribe y compila el paper con lo que hay en el repositorio | edita y ejecuta | `paper-typst`, `figura-para-paper` |
| `revisor` | Contrasta cada afirmación del paper con su respaldo y dictamina | solo lectura (y web, para resolver DOI) | `paper-typst`, `ajuste-ley-de-potencias`, `figura-para-paper`, `verificar-referencia`, como criterio de revisión |

Los agentes siguen la especificación v1 de agent-creator
(https://github.com/danil-labs/agent-creator). Sus flujos y relevos están en cada
`.agents/agents/<nombre>/agent.md`; el flujo habitual es
simulador y bibliotecario → redactor → revisor → de vuelta al dueño de cada observación.
El paper lo da por terminado la persona, no un agente.
