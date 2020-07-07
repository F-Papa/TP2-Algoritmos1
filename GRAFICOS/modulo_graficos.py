ROJO   = "\033[1;31m"  
AZUL  = "\033[1;34m"
CYAN  = "\033[1;36m"
VERDE = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
ARCOIRIS = "ARCOIRIS"

colores = [ROJO, AZUL, CYAN, VERDE, RESET]

def get_max_min(valores):
    """ Pre-Condicion: Recibe una iterable con elementos numericos
        Post-Condicion: Devuelve una tupla del modo (valor_maximo, valor_minimo)"""

    max, min = float(0), float(0)
    contador = 0
    
    for item in valores:
    
        if contador == 0:
            max, min = item, item

        if item>max:
            max = item
        elif item<min:
            min = item

        contador+=1
    
    return (max, min)

def grafico_barras(eje_vertical, eje_horizontal, unidad_medicion = "", flag_color = RESET):
    """Pre-Condicion: Recibe a las listas eje_vertical (cualquier tipo) y eje_horizontal (numerico). El usuario tiene la opcion
    de ingresar un sufijo/unidad (unidad_medicion) y una bandera de color (ROJO, AZUL, CYAN, VERDE, ARCOIRIS, RESET).
    Post-Condicion: Imprime un grafico de barras con los datos ingresados en el color deseado. Si se ingreso una unidad de medicion, esta aparece despues de cada valor.
    Si los valores ingresados son compatibles entre si devuelve 1, en caso contrario devuelve 0"""    

    if len(eje_horizontal) != len(eje_vertical):    #No se puede graficar pues el eje vertical y el eje x no tienen la misma cantidad de elementos
        return 0
    
    max_min = get_max_min(eje_horizontal)
    rango = max_min[0] - max_min[1]
    escala = (rango)/100
    i = 0

    for j in range(len(eje_horizontal)):

        #Interpretacion flag color
        if flag_color == ARCOIRIS:
            if i<3:
                i+=1
            else:
                i=0     
        else:
            i = colores.index(flag_color)  

        #Activa el color        
        print(colores[i], end= "") 

        #Imprime el grafico
        if eje_horizontal[j] == 0:
           print(eje_vertical[j], " ", eje_horizontal[j], unidad_medicion)
           
        else:
            unidades = round((eje_horizontal[j]-max_min[1])/escala)
            print(eje_vertical[j], " ", "█"*(unidades+3), eje_horizontal[j],unidad_medicion)

    #Resetea el color a blanco   
    print (RESET)   
    return 1


""" Para probar:

lista1 = [2010, 2011, 2012, 2013, 2014]
lista2 = [123, 201, 0, 11, 54]
grafico_barras(lista1, lista2, "Kg", RESET)

"""