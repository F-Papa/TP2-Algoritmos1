import requests
import json
from geopy.distance import geodesic

def smn_request(diccionario):
    """Extrae la información de SMN y, si no existe, genera un archivo para cada uno de los servicios para almacenar 
    la información.
    Precondición: diccionario con los links a cada uno de los servicios del SMN"""
    errores = []

    for key, item in diccionario.items():
        exito = False

        nombre = key+'.txt'

        try:
            resp = requests.get(item, allow_redirects = True)
            exito = True
        
        except:
            print(f"Error descargando {key} desde {item}")

        if exito:
            with open("temp//"+nombre, 'wb') as archivo:
                    archivo.write(resp.content)
        
        """except:
            print(f"Error abriendo archivo: {nombre}")"""            

def alertas(nombre_archivo):
    """Generá una lista con los datos necesarios de cada una de las aertas incluidas en archivo de alertas. 
    Precondición: El nombre del archivo que se desea procesar"""
    
    info = []
    with open("temp//"+nombre_archivo+".txt", "r", encoding="utf-8") as archivo:
        data = archivo.readlines()
        for elemento in data:
            elemento_json = json.loads(elemento)
            for i in range(len(elemento_json)):
                info.append({"Descripcion_Corta": elemento_json[i]["title"],
                                "Fecha": elemento_json[i]["date"],
                                "Descripción": elemento_json[i]["description"],
                                "Severidad": elemento_json[i]["severity"],})
                for j in range(len(elemento_json[i]["zones"])):
                    info[i]["Zona " + str(j+1)] = elemento_json[i]["zones"][str(j)]
    return info
            
def extendido(nombre_archivo):
    """Generá una lista con los datos necesarios de cada una de las ciudades incluidas en los archivos relacionados con el
    pronóstico extendido. 
    Precondición: El nombre del archivo que se desea procesar"""
    
    info = []
    with open("temp//"+ nombre_archivo + ".txt","r", encoding="utf-8") as archivo:
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

def aproximar(lat, lon, nombre_archivo):
    ubicacion_usuario = (lat,lon)
    primera_iteracion = True
    distancia_minima = 0
    elemento_a_devovler = ""

    with open("temp//" + nombre_archivo +".txt", "r", encoding="utf-8") as archivo:
        data = archivo.readlines()
        for elemento in data:
            elemento_json = json.loads(elemento)
            
            for i in range(len(elemento_json)):
                ubicacion_linea = (float(elemento_json[i]["lat"]), float(elemento_json[i]["lon"]))
                distancia_linea = abs(geodesic(ubicacion_usuario, ubicacion_linea).miles)
                
                if primera_iteracion or distancia_linea < distancia_minima:
                    distancia_minima = distancia_linea
                    elemento_a_devolver = elemento_json[i]["name"]
                    primera_iteracion = False

    return elemento_a_devolver               

def actual(nombre_archivo):
    """Generá una lista con los datos necesarios de cada una de las ciudades incluidas en los archivo actual. 
    Precondición: El nombre del archivo que se desea procesar"""
    
    info = []
    with open("temp//" + nombre_archivo +".txt", "r", encoding="utf-8") as archivo:
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

def buscar_por_ubicacion(lista, ciudad):
    """"En base a la información de latitud y longitud o ciudad, busca en una lista si se encuentra el elemento determinado.
    Precondición: 1. Lista con el prónostico extendido
                  2. Latitud del lugar de interés (opcional)
                  3. Longitud del lugar de interés (opcional)
                  4. En caso de no conocer la latidud y la logitud, es necesaria la ciudad.
    Postcondición: Un diccionario con la información brindada."""
    
    for elemento in lista:
        if elemento["Ciudad"].upper() == ciudad.upper():
            return elemento
