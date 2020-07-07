import csv
import datetime
import modulo_graficos as graf

path_archivo = 'C:\\Users\\franc\\source\\repos\\SMN TP\\weatherdata--389-603.csv'   #Aca va el directorio del archivo

def lista_a_int(lista):
    """Pre-Condicion: Recibe un numero como lista de digitos
    Post-Condicion: Devuelve ese numero como un int"""
    
    num_a_devolver = 0
    for i in range(len(lista)):
        num_a_devolver += int(lista[-1-i])*(10**i)
    return num_a_devolver

def extraer_año(linea):
    """Pre-Condicion: Recibe una lista en la que el primer item es un año (cadena)
    Post-Condicion: Devuelve el año de esa entrada (int)"""

    buffer=[]
    for i in range(4):
        buffer.append(linea[0][-4+i])
    return lista_a_int(buffer)

def get_max(archivo, posicion_valor, numero_años = 1):
    """Pre-Condicion Recibe los valores de un archivo csv (cadena), la posicion del
    valor cuyo maximo se desea averiguar (int), y la cantidad de años que se desea tener cuenta (int, 1 por defecto)
        Post-Condicion: Devuelve el maximo de esos valores"""

    año_actual = get_año_actual()
    valores = csv.reader(archivo)
    next(valores)
    max = float(0)

    for linea in valores:
        año_linea = extraer_año(linea)

        if numero_años > (año_actual - año_linea):
            if max < float(linea[posicion_valor]):
                max = float(linea[posicion_valor])
    
    return max

def get_año_actual():
    """Post-Condicion: devuelve el año actual (int)"""

    fecha_actual = datetime.datetime.now()
    return fecha_actual.year

def promedio_reciente(archivo, posicion_valor, numero_años = 1):
    """Pre-Condicion Recibe los valores de un archivo csv (cedena), la posicion del
    valor que se desea promediar (int), y la cantidad de años que se desea tener cuenta (int, 1 por defecto)
        Post-Condicion: Devuelve un promedio de todos esos valores"""
    
    valores = csv.reader(archivo)
    next(valores)
    año_actual = get_año_actual()
    sumatoria = float(0)
    contador = 0

    for linea in valores:
        año_linea = extraer_año(linea)

        if numero_años > (año_actual - año_linea):
            sumatoria += float(linea[posicion_valor])
            contador += 1

    if contador != 0:
        return sumatoria/contador

    else: 
        return 0

def cargar_archivo(directorio):
    """ Pre-Condicion: Recibe el directorio de un archivo csv como cadena.
        Pos-Condicion: Devuelve una lista en la que cada linea (separada por endline) es una item"""

    with open(directorio, newline='\n') as archivo:
        lista_a_devolver = [linea for linea in archivo]

    return lista_a_devolver    

def main():
    """Procedimiento para probar el correcto funcionamiento de las otras funciones"""

    lineas_archivo = cargar_archivo(path_archivo)

    n_años = 8

    promedio_temp_max = promedio_reciente(lineas_archivo, 4, n_años)
    promedio_temp_min = promedio_reciente(lineas_archivo, 5, n_años)
    promedio_temp_total = (promedio_temp_max + promedio_temp_min)/2
    
    print("Temperatura promedio de los ultimos {} años: {}.".format(n_años, promedio_temp_total))
    
    promedio_humedad = promedio_reciente(lineas_archivo, 8, n_años)
    print("Humedad promedio de los ultimos {} años: {}.".format(n_años, promedio_humedad))

    print(get_max(lineas_archivo, 4, n_años))
    print(get_max(lineas_archivo, 8, n_años))
    
main()


