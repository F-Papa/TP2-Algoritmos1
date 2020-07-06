import requests
import numpy as np

def smn_request(diccionario):
    for key, item in diccionario.items():
        response = requests.get(item)
        np.savetxt(fname = key+'.txt', X = response)

def main():
    urls_smn = {'actual':'https://ws.smn.gob.ar/map_items/weather',
                'especiales': 'https://ws.smn.gob.ar/alerts/type/IE',
                'corto_plazo': 'https://ws.smn.gob.ar/alerts/type/AC',
                'alertas': 'https://ws.smn.gob.ar/alerts/type/AL',
                'pronostico_1dia': 'https://ws.smn.gob.ar/map_items/forecast/1',
                'pronostico_2dia': 'https://ws.smn.gob.ar/map_items/forecast/2',
                'pronostico_3dia': 'https://ws.smn.gob.ar/map_items/forecast/3',
                'otros_pronosticos': 'https://ws.smn.gob.ar/forecast/'}
    
    smn_request(urls_smn)

main()