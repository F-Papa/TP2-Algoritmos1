#import requests
import json

def solicitar_usuario():
    """Le solicita al usuario los datos de úbicación"""
    
    respuesta = input("¿Conocés la latitud y la logitud de la ciudad que querés ver el clima? S/N ").upper()
    if respuesta == "S":
        lat = input("Por favor, ingresa la latitud en el formato 'dd.ddd'. Se aceptan números negativos.\n Si no estás seguro y querés salir, presiona 1. ")
        lon = input("Por favor, ingresa la longitud en el formato 'dd.ddd'. Se aceptan números negativos.\n Si no estás seguro y querés salir, presiona 1. ")
        ciudad = ""
        while (len(lat) < 6 or len(lon) < 6) and lat != "0" and lon != "0":
            if len(lat) < 6 and lat != "1":
                lat = input("La latitud ingresada es invalida. Recorda que el formato es 'dd.ddd'. Se aceptan números negativos.\n Si no estás seguro y querés salir, presiona 1. ")
            elif len(lon) < 6 and lon !="1":   
                lon = input("La longitud ingresada es invalida. Recorda que el formato es 'dd.ddd'. Se aceptan números negativos.\n Si no estás seguro y querés salir, presiona 1. ")
            else:
                lat="0"
                lon="0"
                ciudad = input("En ese caso, ¿podrías indicarnos de qué ciudad te gustaría conocer el estado actual? ").title()
    else:
        lat="0"
        lon="0"
        ciudad = input("En ese caso, ¿podrías indicarnos de qué ciudad te gustaría conocer el estado actual? ").title()
    return [lat,lon,ciudad]

def smn_request(diccionario):
    '''Extrae la información de SMN y, si no existe, genera un archivo para cada uno de los servicios para almacenar 
    la información.
    Precondición: diccionario con los links a cada uno de los servicios del SMN'''
    
    for key, item in diccionario.items():
        resp = requests.get(item, allow_redirects = True)
        nombre = key+'.txt'
        with open(nombre, 'wb') as archivo:
            archivo.write(resp.content)

def extendido(nombre_archivo):
    """Generá una lista con los datos necesarios de cada una de las ciudades incluidas en los archivos relacionados con el
    pronóstico extendido. 
    Precondición: El nombre del archivo que se desea procesar"""
    
    info = []
    with open(nombre_archivo + ".txt","r", encoding="utf-8") as archivo:
        data = archivo.readlines()
        for elemento in data:
            elemento_json = json.loads(elemento)
            for i in range(len(elemento_json)):
                info.append({"Ciudad": elemento_json[i]["name"],
                             "Provincia": elemento_json[i]["province"],
                             "Latitud": elemento_json[i]["lat"],
                             "Longitud": elemento_json[i]["lon"],
                             "Temperatura_mañana": elemento_json[i]["weather"]["morning_temp"],
                             "Descripción_mañana": elemento_json[i]["weather"]["morning_desc"],
                             "Temperatura_tarde": elemento_json[i]["weather"]["afternoon_temp"],
                             "Descripción_tarde": elemento_json[i]["weather"]["afternoon_desc"]})
    return info

def actual(nombre_archivo):
    info = []
    with open(nombre_archivo +".txt", "r", encoding="utf-8") as archivo:
        data = archivo.readlines()
        for elemento in data:
            elemento_json = json.loads(elemento)
            for i in range(len(elemento_json)):
                info.append({ "Ciudad": elemento_json[i]["name"],
                              "Provincia":elemento_json[i]["province"],
                              "Latitud": elemento_json[i]["lat"],
                              "Longitud": elemento_json[i]["lon"],
                              "Humedad": elemento_json[i]["weather"]["humidity"],
                              "Presión": elemento_json[i]["weather"]["pressure"],
                              "Temperatura": elemento_json[i]["weather"]["temp"],
                              "Sensasión_Térmica": elemento_json[i]["weather"]["st"],
                              "Visibilidad": elemento_json[i]["weather"]["visibility"],
                              "Velocidad_del_viento": elemento_json[i]["weather"]["wind_speed"]})
    return info

def buscar_ubicacion(lista, latitud, longitud, ciudad):
    """En base a la información de latitud y longitud o ciudad, busca en una lista si se encuentra el elemento determinado.
       Precondición: 1. Lista con el prónostico extendido
                     2. Latitud del lugar de interés (opcional)
                     3. Longitud del lugar de interés (opcional)
                     4. En caso de no conocer la latidud y la logitud, es necesaria la ciudad."""
    for elemento in lista:
        if latitud == "0":
            if elemento["Ciudad"] == ciudad:
                return elemento
        elif latitud in elemento["Latitud"] and longitud in elemento["Longitud"]:
            return elemento

def calcular_distancia(lat1,long1,lat2,long2):
    """ Pre-Condición: Recibe dos coordenadas (float, dd.ddd)
        Post-Condición: Devuelve la distancia entre los 2 puntos dados (float)"""

    return ( (lat2-lat1)**2 + (long2-long1)**2 )**(1/2)

def get_provincia_mas_cercana(latitud, longitud):
    """ Pre-Condición: Recibe latitud y longitud como parametros (float, dd.ddd)
        Post-Condición: Devuelve el nombre de la Provincia cuya capital está más cerca de las coordenadas introducidas (string)"""

    coord_ciudades =    {'Buenos Aires':        [-34.613, -58.377],
                        'Córdoba':              [-31.414, -64.181],
                        'Mendoza':              [-32.891, -68.827],
                        'Tucumán':              [-28.824, -65.223],
                        'Salta':                [-24.786, -65.412],
                        'Santa Fe':             [-31.649, -60.709],
                        'San Juan':             [-31.538, -68.536],
                        'Chaco':                [-27.461, -58.984],
                        'Santiago del Estero':  [-27.795, -64.261],
                        'Misiones':             [-27.367, -55.896],
                        'Jujuy':                [-24.195, -65.297],
                        'Entre Ríos':           [-31.733, -60.529],
                        'La Rioja':             [-34.729, -58.264],
                        'Chubut':               [-43.300, -65.102],
                        'Tierra del Fuego':     [-54.811, -68.316],
                        'La Pampa':             [-36.617, -64.283],
                        'Santa Cruz':           [-51.633, -69.233],
                        'Corrientes':           [-27.468, -58.834],
                        'Río Negro':            [-43.300, -65.102],
                        'Neuquén':              [-38.952, -68.059],
                        'San Luis':             [-33.295, -66.336],
                        'Catamarca':            [-28.470, -65.785],
                        'Formosa':              [-26.185, -58.173]}
    menor_dist = -1
    nombre_menor_dist = ''
    
    
    for key, value in coord_ciudades.items():
        dist_item_actual = calcular_distancia(latitud, longitud, value[0], value[1])
        
        if menor_dist == -1 or menor_dist > dist_item_actual:

            menor_dist = dist_item_actual
            nombre_menor_dist = key 
    
    return nombre_menor_dist

def get_alertas_cercanas(lista_alertas, provincia_mas_cercana):
    """ Pre-Condición: Recibe una lista de alertas 
        Post-Condición: Devuelve una lista con los ID de aquellas alertas que contienen a 'provincia_mas_cercana' en su descripción."""
    lista_a_devolver = []

    with open(nombre_archivo +".txt", "r", encoding="utf-8") as archivo:
        data = archivo.readlines()
       
        for elemento in data:
            elemento_json = json.loads(elemento)
            
            for i in range(len(elemento_json)):
                if provincia_mas_cercana in elemento_json[i]["description"]:
                    lista_a_devolver.append(elemento_json[i]["_id"])
    
    return lista_a_devolver

def main():
    urls_smn= {'actual':            'https://ws.smn.gob.ar/map_items/weather',
              'especiales':         'https://ws.smn.gob.ar/alerts/type/IE',
              'corto_plazo':        'https://ws.smn.gob.ar/alerts/type/AC',
              'alertas':            'https://ws.smn.gob.ar/alerts/type/AL',
              'pronostico_1dia':    'https://ws.smn.gob.ar/map_items/forecast/1',
              'pronostico_2dia':    'https://ws.smn.gob.ar/map_items/forecast/2',
              'pronostico_3dia':    'https://ws.smn.gob.ar/map_items/forecast/3',
              'otros_pronosticos':  'https://ws.smn.gob.ar/forecast/'}
    
    #Solicitud del ingreso de datos al usuario

    """ingreso = solicitar_usuario()
    lat = ingreso[0]
    lon = ingreso[1]
    ciudad = ingreso[2]
    
    #Crea los archivos .txt que de los cuales se extraerá la información necesaria
    smn_request(urls_smn)"""
main()