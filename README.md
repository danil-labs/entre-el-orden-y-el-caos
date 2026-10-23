# Kit de laboratorio · Entre el orden y el caos

Kit del taller «Entre el orden y el caos: investigación con agentes de IA en Terminus». Con él montas
tu propio laboratorio de investigación con agentes y escribes un paper corto: tú pones la pregunta y
el criterio, los agentes buscan, programan, grafican y redactan el primer borrador, y otro agente
revisa que cada afirmación tenga respaldo.

Trae listo:

- **Cuatro agentes** que se reparten el trabajo sin pisarse: `bibliotecario`, `simulador`,
  `redactor` y `revisor` (en `.agents/agents/`).
- **Cinco skills** con los métodos que siguen: verificar una referencia, hacer una simulación
  reproducible, ajustar una ley de potencias, hacer una figura para el paper y escribir el paper en
  Typst (en `skills/`).
- **Simulaciones** de dos temas de ejemplo: la aplicación logística (bifurcación, caos, Lyapunov,
  constante de Feigenbaum) y los autómatas celulares (Reglas 30, 90 y 110, las 256 reglas, la pila
  de arena y el incendio forestal, con leyes de potencias).
- **Dos notebooks** para Google Colab.
- **Una plantilla de paper** en Typst que ya compila, con una figura de ejemplo y marcadores
  «Tu turno» donde va lo tuyo.

Las reglas del laboratorio están en [`AGENTS.md`](AGENTS.md). Léelas: los agentes las siguen y tú
también.

## Qué hay en cada carpeta

```
AGENTS.md              las reglas del laboratorio y quién es dueño de qué
.agents/agents/        los cuatro agentes (formato agent-creator v1)
skills/                los métodos que usan los agentes
simulaciones/          scripts reproducibles; cada uno escribe en figuras/ y resultados/
notebooks/             01_logistica_y_caos.ipynb y 02_automatas_celulares.ipynb (para Colab)
figuras/               figuras generadas (no se versionan: se regeneran)
resultados/            números en JSON y CSV, con semillas y parámetros
paper/                 main.typ, referencias.bib y figuras/ del paper
requirements.txt       dependencias de Python
```

## 1. Abrirlo en Terminus

1. Copia o clona la carpeta `kit-taller` en tu computadora. Si quieres guardar tu historial en
   GitHub, crea un repositorio vacío tuyo y súbela ahí; el kit no trae remoto.
2. Abre Terminus y añade la carpeta del kit a tu espacio de trabajo.
3. Crea una tarea sobre esa carpeta con el agente de IA que uses (Claude, Codex u otro). Terminus
   lee los agentes de `.agents/agents/` y las reglas de `AGENTS.md`.
4. Primera petición, para comprobar que todo está en su sitio:
   > Lee `AGENTS.md` y dime qué agentes hay, qué hace cada uno y qué comando regenera las figuras.

Para correr las simulaciones en tu computadora necesitas Python 3.10 o posterior:

```sh
python -m pip install -r requirements.txt
python simulaciones/correr_todo.py --rapido     # comprueba que todo corre (~3 min)
```

## 2. Trabajar con los agentes

Cada agente tiene un trabajo y una frontera. Para pedirle algo, nómbralo con `@`. Los agentes se
pasan el trabajo entre ellos con el mismo mecanismo, y cada relevo lleva qué se entrega, dónde está
y qué quedó abierto.

| Agente | Le pides | No hace |
|---|---|---|
| `@bibliotecario` | Buscar y verificar referencias; mantener `paper/referencias.bib` | Escribir el paper |
| `@simulador` | Correr y escribir simulaciones y notebooks; figuras y números | Escribir el paper o el `.bib` |
| `@redactor` | Escribir y compilar secciones del paper | Inventar números o citas |
| `@revisor` | Revisar el paper contra figuras, datos y referencias | Corregir nada: solo lee |

Ejemplos de peticiones:

- «@bibliotecario busca y verifica 5 referencias sobre criticalidad autoorganizada en la pila de
  arena, para sostener la primera frase de la introducción.»
- «@simulador corre la logística y genera la figura de bifurcación; llévala al paper.»
- «@simulador corre la pila de arena con L = 32, 64 y 128 y dime si se puede afirmar una ley de
  potencias.»
- «@simulador repite el barrido de las 256 reglas con ancho 257 y dime qué cambia.»
- «@redactor escribe la sección de resultados con la figura de tamaño finito y los números de
  `resultados/pila_de_arena.json`.»
- «@revisor revisa la sección de resultados.»

Un flujo completo de una hora, aproximadamente:

1. **Pregunta** (tú): escoge algo pequeño y verificable. Ideas: ¿cambia δ con otro mapa? ¿qué
   reglas elementales son sensibles al ancho? ¿el corte del incendio crece con θ?
2. **Referencias** (`@bibliotecario`) y **simulación** (`@simulador`), en paralelo.
3. **Redacción** (`@redactor`), solo con lo que quedó en el repositorio.
4. **Revisión** (`@revisor`) y correcciones de cada dueño, hasta que el dictamen sea «listo».
5. **Tu revisión**: abre las figuras, comprueba dos o tres números contra `resultados/`, abre los DOI.
   El agente escribe el borrador; el criterio es tuyo.

## 3. Compilar el paper

El paper está en `paper/main.typ`. Desde la raíz del kit:

```sh
typst compile --root paper paper/main.typ paper/main.pdf
```

Terminus trae Typst; si no lo tienes en la terminal, instálalo desde https://typst.app o sube la
carpeta `paper/` a la web de Typst y compila ahí. También puedes pedírselo a `@redactor`. Los
recuadros amarillos «Tu turno» marcan lo que falta: un paper terminado no tiene ninguno.

Para llevar una figura al paper:

```sh
python simulaciones/copiar_al_paper.py arena_tamano_finito.png
```

La copia queda en `paper/figuras/` y su script de origen, en `paper/figuras/PROCEDENCIA.md`.

## 4. Notebooks en Google Colab desde una carpeta de Drive

Los notebooks corren de principio a fin en Colab sin instalar nada a mano (instalan `powerlaw` si
falta; numpy, matplotlib, scipy y numba ya vienen en Colab).

1. Sube la carpeta `kit-taller` completa a **Mi unidad** de Google Drive (arrástrala a
   drive.google.com).
2. En Drive, entra a `kit-taller/notebooks/`, haz clic derecho en `01_logistica_y_caos.ipynb` →
   **Abrir con** → **Google Colaboratory**. (Si no aparece, en el mismo menú elige «Conectar más
   aplicaciones» y añade Colaboratory.)
3. **Entorno de ejecución → Ejecutar todo.** La primera celda pide permiso para montar tu Drive:
   acéptalo. Las figuras se guardan en `kit-taller/figuras/` y los números en
   `kit-taller/resultados/` de tu Drive.
4. Si pusiste la carpeta en otro lugar, cambia la ruta `RAIZ` en la primera celda de código.
5. Opcional: **Entorno de ejecución → Cambiar tipo de entorno → GPU**. El notebook 01 usa la GPU si
   hay CuPy y, si no, NumPy; el resultado es el mismo.

Para traer a tu computadora lo que hiciste en Colab, descarga las figuras o los JSON desde Drive a
las carpetas `figuras/` y `resultados/` del kit. Si cambiaste el código de un notebook, descarga el
`.ipynb` (Archivo → Descargar) y reemplaza el del kit. Tus datos privados se quedan en tu Drive: no
los copies al repositorio.

## 5. Validar los agentes

Si cambias un agente, valídalo con el validador de agent-creator:

```sh
git clone https://github.com/danil-labs/agent-creator
python agent-creator/scripts/validate_agent.py --root . --strict
```

## Referencias de los temas de ejemplo

Verificadas, en [`paper/referencias.bib`](paper/referencias.bib): May (1976) *Nature* 261:459, la
aplicación logística; Wolfram (1983) *Rev. Mod. Phys.* 55:601, los autómatas celulares; Bak, Tang y
Wiesenfeld (1987) *Phys. Rev. Lett.* 59:381, la pila de arena. El método de ajuste de leyes de
potencias es de Clauset, Shalizi y Newman (2009) *SIAM Review* 51:661; antes de citarlo en tu
paper, pídele a `@bibliotecario` que lo verifique.
