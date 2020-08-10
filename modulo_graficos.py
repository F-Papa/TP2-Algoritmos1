class Color:                     #Se crea una clase para poder acceder a sus miembros desde afuera del modulo en caso de ser necesario.
    ROJO   = "\033[1;31m"  
    AZUL  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    VERDE = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"
    ARCOIRIS = "ARCOIRIS"

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


def grafico_barras(eje_vertical, eje_horizontal, unidad_medicion = "", color = Color.RESET):
    """Pre-Condicion: Recibe a las listas eje_vertical (cualquier tipo) y eje_horizontal (numerico). El usuario tiene la opcion
    de agregar un sufijo/unidad (unidad_medicion) y un color (Color.ROJO, Color.AZUL, Color.CYAN, Color.VERDE, Color.ARCOIRIS, Color.RESET).
    Post-Condicion: Imprime un grafico de barras con los datos ingresados en el color deseado. Si se ingreso una unidad de medicion, esta aparece despues de cada valor.
    Si los valores ingresados son compatibles entre si devuelve 1, en caso contrario devuelve 0 y no se imprime ningun gráfico"""    
    
    colores = [Color.ROJO, Color.AZUL, Color.CYAN, Color.VERDE, Color.RESET]  #Se elije usar una lista para poder recorrerla con un indice, cosa que el diccionario no permite.

    if len(eje_horizontal) != len(eje_vertical):    #No se puede graficar pues el eje vertical y el eje x no tienen la misma cantidad de elementos
        print("error")
        return 0
    
    max_min = get_max_min(eje_horizontal)
    rango = max_min[0] - max_min[1]
    escala = (rango)/100
    i = 0

    for j in range(len(eje_horizontal)):

        #Interpretacion color
        if color == Color.ARCOIRIS:
            if i < len(colores)-1:
                i+=1
            else:
                i=0     
        else:
            i = colores.index(color)  

        #Activa el color        
        print(colores[i], end= "") 

        #Imprime el grafico
        if eje_horizontal[j] == 0:
           print(eje_vertical[j], " ", eje_horizontal[j], unidad_medicion)
           
        else:   
            unidades = round((eje_horizontal[j]-max_min[1])/escala)
            print(eje_vertical[j], " ", "█"*(unidades+3), eje_horizontal[j],unidad_medicion)

    #Resetea el color a blanco   
    print (Color.RESET)   
    return 1



