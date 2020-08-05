from geopy.geocoders import Nominatim
from urllib.request import urlopen
#import json

def get_ciudad_provincia(latitud, longitud):
    """ Pre-Condición: Recibe latitud y longitud como float o como string
        Post-Condición: Devuelve una tupla con el nombre de la ciudad y de la provincia al que corresponden estas coordenadas (ciudad, provincia)"""

    geolocator = Nominatim(user_agent="App Tormenta")
    ubicacion = geolocator.reverse(f"{latitud},{longitud}")
    tokens_ubicacion = ubicacion.address.split(',')
    return tokens_ubicacion[2].lstrip() , tokens_ubicacion[3].lstrip()


def filtrar_alertas_provincia(lista_alertas, provincia):
    """ Pre-Condición: Recibe una lista de alertas 
        Post-Condición: Devuelve una lista con aquellas alertas que contienen a 'provincia' en su descripción. (alertas relevantes)"""
   
    lista_a_devolver = []

    for item in alertas:
        if provincia in item["description"]:
            lista_a_devolver.append(item)
    
    return lista_a_devolver