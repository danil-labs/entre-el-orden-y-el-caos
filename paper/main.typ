// =====================================================================================
// Plantilla de paper corto del laboratorio · Taller «Entre el orden y el caos»
//
// Compilar desde la raíz del repositorio:
//   typst compile --root paper paper/main.typ paper/main.pdf
//
// Reglas (ver AGENTS.md y skills/paper-typst/SKILL.md):
//   - cada afirmación lleva al lado su respaldo: una figura de figuras/ (en esta carpeta),
//     un número de resultados/ (con un comentario que diga archivo y clave) o una cita @clave;
//   - lo que falta se marca con #pendiente[...]; un paper terminado no tiene ninguno.
//
// El texto que hay es un EJEMPLO con la aplicación logística, para que veas cómo se respalda
// cada frase. Reemplázalo por tu pregunta, tus figuras y tus números.
// =====================================================================================

// ---------- Datos del paper: cámbialos ----------
#let titulo = [Del orden al caos en la aplicación logística: \ una reproducción de la constante de Feigenbaum]
#let autores = ("Nombre Apellido", "Nombre Apellido")          // ← tus nombres
#let afiliacion = [Institución · Taller «Entre el orden y el caos»]
#let correo = "correo@ejemplo.org"
#let fecha = datetime.today().display("[day]/[month]/[year]")

// ---------- Marcador de lo que falta (sale resaltado en el PDF) ----------
#let pendiente(cuerpo) = box(
  fill: rgb("#fff4d6"), stroke: 0.6pt + rgb("#e0a800"), inset: (x: 4pt, y: 2pt), radius: 2pt,
  text(fill: rgb("#7a5800"), size: 0.9em)[*Tu turno:* #cuerpo],
)

// ---------- Diseño ----------
#set document(title: "Paper del laboratorio", author: autores)
#set page(paper: "a4", margin: (x: 2.2cm, y: 2.4cm), numbering: "1")
#set text(lang: "es", size: 10.5pt)
#set par(justify: true, leading: 0.62em, spacing: 1em)
#set heading(numbering: "1.")
#show heading.where(level: 1): set block(above: 1.4em, below: 0.7em)
#set math.equation(numbering: "(1)")
#show figure.caption: set text(size: 9pt)
#show link: set text(fill: rgb("#2a78d6"))

// ---------- Título ----------
#align(center)[
  #text(size: 16pt, weight: "bold")[#titulo]
  #v(0.4em)
  #autores.join(", ") \
  #text(size: 9pt)[#afiliacion · #link("mailto:" + correo)[#correo] · #fecha]
]
#v(0.8em)

// ---------- Resumen ----------
#block(inset: (x: 1.2cm))[
  #set par(justify: true)
  #text(weight: "bold")[Resumen.]
  // Cuatro frases: la pregunta, el método, el resultado principal con su número, y qué significa.
  Estudiamos cómo la aplicación logística $x_(n+1) = r x_n (1 - x_n)$ pasa del orden al caos al
  aumentar la tasa de crecimiento $r$. Con simulaciones deterministas calculamos el diagrama de
  bifurcación, el exponente de Lyapunov y los valores superestables de la cascada de duplicación
  de periodo. El cociente entre intervalos sucesivos converge a
  $delta_10 = 4.669201$, // resultados/logistica.json → resultados.feigenbaum.delta_logistica[-1]
  la constante de Feigenbaum hasta la sexta cifra, y el caos empieza en
  $r approx 3.570$. // resultados/logistica.json → resultados.lyapunov.inicio_caos_r
  #pendiente[reescribe el resumen con tu pregunta y tu resultado principal, con su número.]
]

= Introducción
// Qué se pregunta, por qué importa y qué se sabía. Cada antecedente con su cita verificada.

Una ecuación determinista de una sola variable puede producir un comportamiento que parece
aleatorio. May mostró que la aplicación logística, un modelo mínimo de población, recorre al
variar $r$ una sucesión de duplicaciones de periodo que desemboca en el caos @may1976. Los
autómatas celulares son otro ejemplo de reglas locales simples con comportamiento complejo
@wolfram1983, y la pila de arena muestra cómo un sistema puede organizarse solo hacia un estado
crítico @bak1987.

#pendiente[escribe tu pregunta de investigación en una frase, y qué se sabía antes (con referencias que haya verificado \@bibliotecario).]

= Métodos
// Lo necesario para que otra persona reproduzca todo: modelo, parámetros, semillas, comando.

Iteramos la aplicación logística
$ x_(n+1) = r x_n (1 - x_n) $ <ec-logistica>
desde $x_0 = 0.4$ para 4000 valores de $r$ entre 2.5 y 4, descartando 2000 pasos de transitorio y
graficando los 400 siguientes. El exponente de Lyapunov se estima como el promedio de
$ln|r(1 - 2x_n)|$ a lo largo de 20 000 iteraciones. Los valores superestables $R_n$ (aquellos en
que $x = 1\/2$ pertenece a una órbita de periodo $2^n$) se obtienen por el método de la secante, y
$ delta_n = (R_(n-1) - R_(n-2)) / (R_n - R_(n-1)). $ <ec-delta>
Todo el cálculo es determinista y se regenera con `python simulaciones/logistica.py`.

#pendiente[describe tu modelo o tus datos, los parámetros, las semillas y el comando que regenera cada figura.]

= Resultados
// Qué se midió y qué salió. Sin interpretar todavía. Cada número con su comentario de origen.

La @fig-bifurcacion muestra la cascada: un punto fijo hasta $r = 3$, ciclos de periodo 2, 4, 8…
y, a partir de $r approx 3.570$, el caos, interrumpido por ventanas periódicas como la de periodo 3.
// resultados/logistica.json → resultados.lyapunov.inicio_caos_r = 3.5702
Como control, el primer valor superestable de periodo 2 coincide con el exacto,
$R_1 = 1 + sqrt(5) = 3.2360679775$, // resultados/logistica.json → resultados.feigenbaum.R_superestables_logistica[1]
y el exponente de Lyapunov en $r = 4$ vale 0.6932, frente a $ln 2 = 0.6931$.
// resultados/logistica.json → resultados.lyapunov.lyapunov_en_r4
Con @ec-delta, $delta_n$ converge a 4.669201 en el décimo nivel. // resultados/logistica.json → resultados.feigenbaum.delta_logistica

#figure(
  image("figuras/logistica_bifurcacion.png", width: 100%),
  caption: [Diagrama de bifurcación de la aplicación logística: la población a largo plazo pasa de
    un punto fijo a ciclos de periodo 2, 4, … y al caos. $x_0 = 0.4$; 400 puntos por cada uno de
    los 4000 valores de $r$, tras 2000 pasos de transitorio. Se regenera con
    `simulaciones/logistica.py`.],
) <fig-bifurcacion>

#pendiente[tus resultados: una figura por afirmación (pídela a \@simulador) y cada número con su comentario de origen.]

= Discusión
// Qué significa, qué NO se puede afirmar y qué no funcionó.

El valor de $delta$ no depende de los detalles de la ecuación: el mismo cálculo con el mapa
$r sin(pi x)$ converge a la misma constante (4.669199 en el décimo nivel), lo que ilustra la
universalidad de la cascada. // resultados/logistica.json → resultados.feigenbaum.delta_seno[-1]
Esto no demuestra la universalidad: solo la comprueba en dos mapas con un máximo cuadrático.

== Lo que no funcionó
// Obligatorio. Lo que se intentó y falló, o los límites del método. Si todo funcionó, dilo.
La convergencia de $delta_n$ no es monótona: $delta_4 = 4.66296$ queda por debajo de la
constante, antes de acercarse a ella. // resultados/logistica.json → resultados.feigenbaum.delta_logistica[2]
Nos detuvimos en $n = 10$ porque el costo crece como $2^n$; no comprobamos a partir de qué nivel
domina el error de redondeo, así que no afirmamos más cifras que las seis que coinciden.

#pendiente[qué significa tu resultado, qué no puedes afirmar y qué no funcionó.]

// ---------- Referencias ----------
// Solo claves de referencias.bib, que mantiene el bibliotecario. Typst muestra solo las citadas.
#bibliography("referencias.bib", title: "Referencias", style: "apa")
