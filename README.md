# Resolver el problema del Steiner Tree con Simulated annealing
**Proyecto final Simulación Estocástica MA4402**

**Felipe Urrutia Vargas - Camilo Carvajal Reyes**

### Abstract
El problema del Steiner Tree consiste encontrar un árbol de peso mínimo que contiene un subconjunto de vértices de interés. Este problema es NP-completo y es resuelto con algoritmos deterministas a través de programación lineal mixta. Sin embargo, hay aproximaciones que utilizan algoritmos estocásticos como  Simulated annealing. El objetivo de este trabajo es implementar y mejorar un algoritmo de este tipo y evaluar su desempeño sobre un conjunto de grafos test. 

## Proyecto
### Introducción

**Definición (Steiner Tree)**

Para un grafo $G = (V, E)$, vértices terminales $S \subset V$ y pesos $w: E \rightarrow \mathbb{R}_+$, se desea encontrar un árbol $T$ de peso mínimo que contenga a lo menos los vértices en $S$, donde el peso del árbol $T$ es la suma de los pesos de cada una de sus aristas.

![](figura_steiner_tree.png?raw=true)

### Propuesta
Este método, que mejora la implementación desarrollada en  [1], define $\Lambda$ como el conjunto de los arboles sobre $G$ que contienen a los vértices terminales $S$. Luego, para un $x \in \Lambda$, la idea es construir un estado al azar $y$ a partir de $x$ tal que $y \in \Lambda$. Para lograrlo, se realizan las siguientes etapas:

- $y$ es una copia de $x$
-  Se elige al azar una arista $\hat{u}=ae \in E[y]$, como muestra el ejemplo de figura \ref{fig3}.
-  Se elige al azar un nodo no terminal $v$ de grado 2 (si es que hay)
-  La artista $\hat{u}$ se remueve de $y$. Esto provoca que el arbol $y$ sea un bosque con dos arboles $(y_a, y_e)$ y vertices $a, e$ en un arbol distinto, respectivamente
-  Se remueven de $y$ las aristas $u_1=\omega_1v,u_2=v\omega_2$ incidentes a aquel nodo. Esto provoca que el árbol $y$ sea un bosque con dos arboles $(y_1, y_2)$ y vértices $\omega_1, \omega_2$ en un árbol distinto, respectivamente.
-  Se elige al azar un camino $p$ de largo minimo sobre $G - \hat{u}$, que parte en $e$ y termina en algun vertice de $y_a$
- Se elige al azar un camino $p$ de largo mínimo sobre $G -\{u_1,u_2\}$, que parte en $\omega_1$ y termina en algún vértice de $y_2$
-  Añadir cada arista del camino $p$ al bosque $y$
\end{enumerate}

## Evaluación
Para evaluar la técnica propuesta, se considera el data-test en \cite{DataTest} que posee un conjunto de grafos de prueba junto al valor óptimo del Steiner Tree. Los grafos considerados contienen $80$ vértices, pero varían en su densidad y cantidad de nodos terminales.
%Densidades-tamaños-cantidad terminales.

### GridSearch
Se toma una sucesión $\beta_n$ de la forma

$$ \beta_n = a n^b, \quad \text{parámetros $a>0$ y $b\geq 0$} $$

y se evalúan sobre una grilla de valores para $a$ y $b$.

## Presentación
La presentación consistirá en:

Introducir el problema. Explicar la implementación. Proponer método de evaluación. Resultados del gridsearch. Comparar resultados obtenidos con algoritmo de PLM.

**Referencias**

Duin, C. Testset i080. 1993. URL http://steinlib.zib.de/showset.php?I080.

Schiemangk, C.  Design, analysis and implementation ofthermodynamically motivated simulation for optimiza-tion of subgraphs.  pp. 851–820, 1986.  URL https://doi.org/10.1007/BFb0043908.