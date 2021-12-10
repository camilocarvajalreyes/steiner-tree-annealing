### Archivo preparacion.jl
### Version 2020, curso MA4702.
### Universidad de Chile.


#Funciones auxiliares

function(leearchivo(nombre_archivo))
## Recibe un archivo con las coordenadas de N ciudades, devolviendo N, las coordenadas x, las coordenadas y.
    archivo = open(nombre_archivo)
    Lineas = readlines(archivo)
    n = length(Lineas)
        coordx = []
        coordy = []
        distance = []
    for i in 1:n
        x,y,d=split(Lineas[i])
        push!(coordx,parse(Float64,x))
        push!(coordy,parse(Float64,y))
        push!(distance,parse(Float64,d))
    end
    return n,coordx,coordy, distance
end;

function encuentracomponente(N, v, F)
    componente = Int[]
    lista = [v]

    # hacemos DFS, hasta que la lista esté vacía
    while !isempty(lista)
        # primer elemento de la cola
        actual = popfirst!(lista);
        if !(actual in componente) 
            push!(componente, actual);
        end
        # buscar vecinos
        for vecino in 1:N
            if (([actual,vecino] in F || [vecino,actual] in F) && !(vecino in componente))
               pushfirst!(lista, vecino);
            end
        end
    end
    return componente
end


function encuentracomponentedirigida(N, v, F)
    componente = Int[]
    lista = [v]

    # hacemos DFS, hasta que la lista esté vacía
    while !isempty(lista)
        # primer elemento de la cola
        actual = popfirst!(lista);
        if !(actual in componente) 
            push!(componente, actual);
        end
        # buscar vecinos
        for vecino in 1:N
            if ([actual,vecino] in F && !(vecino in componente))
               pushfirst!(lista, vecino);
            end
        end
    end
    return componente
end


function dibujapesos(coordx,coordy,pesos)
## Recibe dos arreglos de N valores donde (coordx[i],coordy[i]) son las coordenadas de la ciudad i
## Recibe además una matriz arcos de N x N, donde arcos[i,j] es el peso del arco [i,j]
## Dibuja los N puntos en el plano y dibuja los arcos con ancho de linea proporcional al peso.
    N=length(coordx)
    scatter(coordx,coordy,txt=text.(1:N,10,:bottom))
    for k in findall(!iszero, pesos)
        plot!([coordx[k[1]],coordx[k[2]]],[coordy[k[1]],coordy[k[2]]],arrow = false,lc=:blue, linewidth = 2*pesos[k[1],k[2]])
    end
    display(plot!(leg=false))
end

function dibujaaristas(coordx,coordy,aristas)
## Recibe dos arreglos de N valores donde (coordx[i],coordy[i]) son las coordenadas de la ciudad i
## Recibe además una lista de aristas "aristas"
## Dibuja los N puntos en el plano y dibuja las aristas con ancho de linea proporcional al peso.
    N=length(coordx)
    scatter(coordx,coordy,txt=text.(1:N,10,:bottom))
    for k in 1:length(aristas)
        plot!([coordx[aristas[k][1]],coordx[aristas[k][2]]],[coordy[aristas[k][1]],coordy[aristas[k][2]]],arrow = false,lc=:blue, linewidth = 2)
    end
    display(plot!(leg=false))
end

