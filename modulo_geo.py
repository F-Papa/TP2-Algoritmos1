from geopy.geocoders import Nominatim
from urllib.request import urlopen
#import json

def get_provincia(latitud, longitud):
    """ Pre-Condición: Recibe latitud y longitud como float o como string
        Post-Condición: Devuelve una tupla con el nombre de la ciudad y de la provincia al que corresponden estas coordenadas (ciudad, provincia)"""

    provincias =    ["Buenos Aires", "Catamarca", "Chaco", "Chubut", "Córdoba", "Corrientes", "Entre Ríos", "Formosa", "Jujuy",
                    "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro", "Salta", "San Juan", "San Luis",
                    "Santa Cruz", "Santa Fe", "Santiago del Estero", "Tierra del Fuego", "Tucumán"]

    geolocator = Nominatim(user_agent="App Tormenta")
    ubicacion = geolocator.reverse(f"{latitud},{longitud}")
    tokens_ubicacion = ubicacion.address.split(',')
    print(tokens_ubicacion)
    for item in tokens_ubicacion:
        item = item.lstrip()

        if item in provincias:
            return item