* UNIFORMS (pickle) con uniformes
* params (json) con parametros
* gridsearch (json) con rango de hyperparametros


Cada carpeta i080-id tiene pares de archivos de la forma

* {path_approach}_{remove_approach}_ixa={i}_ixb={j}_CM.pickle
* {path_approach}_{remove_approach}_ixa={i}_ixb={j}_times.pickle 

donde path_approach = BFS, remove_approach = Node, i denota que a=i-esimo valor del rango para a y j denota que b=j-esimo valor del rango para b; terminar con _CM denota que el archivo en la Cadena de Markov con los estados y _times los tiempos.
