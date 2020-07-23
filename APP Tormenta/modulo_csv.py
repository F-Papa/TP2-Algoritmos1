import csv
import datetime

def get_max(archivo, posicion_valor, años_a_retroceder = 0):
    """ Pre-Condicion Recibe los valores de un archivo csv (cadena), la posicion del
        valor cuyo maximo se desea averiguar (int), y la cantidad de años que se desea tener cuenta (int, 0 por defecto). Si años_a_retroceder es igual a 0, solo se
        tendran en cuenta los datos del año actual.
        Post-Condicion: Devuelve el maximo de esos valores"""

    año_actual = get_año_actual()
    valores = csv.reader(archivo)
    next(valores)
    max = float(0)

    for linea in valores:
        año_linea = extraer_año(linea)

        if años_a_retroceder > (año_actual - año_linea):
            if max < float(linea[posicion_valor]):
                max = float(linea[posicion_valor])
    
    return max

def lista_a_int(lista):
    """ Pre-Condicion: Recibe un numero como lista de digitos
        Post-Condicion: Devuelve ese numero como un int"""
    
    num_a_devolver = 0
    for i in range(len(lista)):
        num_a_devolver += int(lista[-1-i])*(10**i)
    return num_a_devolver

def extraer_año(linea):
    """ Pre-Condicion: Recibe una lista en la que el primer item es un año (cadena)
        Post-Condicion: Devuelve el año de esa entrada (int)"""

    buffer=[]
    for i in range(4):
        buffer.append(linea[0][-4+i])
    return lista_a_int(buffer)

def get_año_actual():
    """Post-Condicion: devuelve el año actual (int)"""

    fecha_actual = datetime.datetime.now()
    return fecha_actual.year

def promediar(lista_1, lista_2):
    """ Pre-Condicion: Recibe 2 listas con valores numericos    
        Post-Condicion: Devuelve otra lista con los promedios de los valores de la otra lista, esta es una lista vacia si lista_1 y lista_2 no tienen
        igual cantidad de elementos"""

    lista_a_devolver = []

    if len(lista_1) == len(lista_2):

        for i in range(len(lista_1)):
            
            lista_a_devolver.append(int(int(lista_1[i]) + int(lista_2[i]))/2)

    return lista_a_devolver


def get_promedio(archivo, posicion_valor, años_a_retroceder=0):
    """ Pre-Condicion: Recibe una lista de lineas en formato CSV (archivo), la posicion en la lista del valor que se desea promediar (posicion_valor, int )
        y la cantidad de años que se desean revisar (años_a_retroceder, int, 0 por defecto). Si años_a_retroceder es igual a 0, solo se promediaran los datos del año actual.
        Post-Condicion: devuelve una lista con los promedios del valor ubicado en la posicion pedida para cada año y una lista con los años evaluados."""

    valores = csv.reader(archivo)
    next(valores)
    lineas = [linea for linea in valores]
    
    sumatoria = float(0)
    contador_items = float(0)
    lista_a_devolver = []
    lista_años = []
    
    año_actual = get_año_actual()
    contador_años = 0
    i = len(lineas)-1

    while i>=0 and contador_años < años_a_retroceder:
        
        año_linea = extraer_año(lineas[i])
        año_linea_sig = extraer_año(lineas[i-1])

        if (año_actual - año_linea) < años_a_retroceder:
            
            sumatoria += float(lineas[i][posicion_valor])

            contador_items += 1

            if año_linea not in lista_años:
                lista_años.append(año_linea)

            if i == 0 or año_linea_sig != año_linea:
                lista_a_devolver.append(sumatoria/contador_items)
                contador_años +=1
                contador_items, sumatoria = 0, 0
            
        i -=1

    return lista_a_devolver, lista_años

def cargar_archivo(directorio):
    """ Pre-Condicion: Recibe el directorio de un archivo csv como cadena.
        Pos-Condicion: Devuelve una lista en la que cada linea (separada por endline) es una item"""
    
    lista_a_devolver = []

    try: 
        with open(directorio, newline='\n') as archivo:
            lista_a_devolver = [linea for linea in archivo]
    except:
        print("Error abriendo el archivo:", directorio)

    return lista_a_devolver    
