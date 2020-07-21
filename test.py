import requests
import json

def solicitar_usuario():
    """Le solicita al usuario los datos de úbicación"""
    
    respuesta = input("¿Conoces la latitud y la logitud de la ciudad que querés ver el clima? S/N ").upper()
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
                ciudad = input("En ese caso, ¿podrías indicarnos qué ciudad te gustaría conocer su estado actual? ").title()
    else:
        lat="0"
        lon="0"
        ciudad = input("En ese caso, ¿podrías indicarnos qué ciudad te gustaría conocer su estado actual? ").title()
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

def alertas(nombre_archivo):
    """Generá una lista con los datos necesarios de cada una de las aertas incluidas en archivo de alertas. 
    Precondición: El nombre del archivo que se desea procesar"""
    
    info = []
    with open(nombre_archivo+".txt", "r", encoding="utf-8") as archivo:
        data = archivo.readlines()
        for elemento in data:
            elemento_json = json.loads(elemento)
            for i in range(len(elemento_json)):
                alertas.append({"Descripcion_Corta": elemento_json[i]["title"],
                                "Fecha": elemento_json[i]["date"],
                                "Descripción": elemento_json[i]["description"],
                                "Severidad": elemento_json[i]["severity"],})
                for j in range(len(elemento_json[i]["zones"])):
                    alertas[i]["Zona " + str(j+1)] = elemento_json[i]["zones"][str(j)]
    return info

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
    """Generá una lista con los datos necesarios de cada una de las ciudades incluidas en los archivo actual. 
    Precondición: El nombre del archivo que se desea procesar"""
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
        

def main():
    urls_smn= {'actual':'https://ws.smn.gob.ar/map_items/weather',
              'especiales':'https://ws.smn.gob.ar/alerts/type/IE',
              'corto_plazo':'https://ws.smn.gob.ar/alerts/type/AC',
              'alertas':'https://ws.smn.gob.ar/alerts/type/AL',
              'pronostico_1dia':'https://ws.smn.gob.ar/map_items/forecast/1',
              'pronostico_2dia':'https://ws.smn.gob.ar/map_items/forecast/2',
              'pronostico_3dia':'https://ws.smn.gob.ar/map_items/forecast/3',
              'otros_pronosticos':'https://ws.smn.gob.ar/forecast/'}
    
    #Solicitud del ingreso de datos al usuario
    ingreso = solicitar_usuario()
    lat = ingreso[0]
    lon = ingreso[1]
    ciudad = ingreso[2]
    
    #Crea los archivos .txt que de los cuales se extraerá la información necesaria
    smn_request(urls_smn)

main()