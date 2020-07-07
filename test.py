import requests

def smn_request(diccionario):
    '''Extrae la información de SMN y, si no existe, genera un archivo para cada uno de los servicios para almacenar 
    la información.
    Precondición: diccionario con los links a cada uno de los servicios del SMN'''
    
    for key, item in diccionario.items():
        resp = requests.get(item, allow_redirects = True)
        nombre = key+'.txt'
        with open(nombre, 'wb') as archivo:
            archivo.write(resp.content)
        

def main():
    urls_smn= {'actual':'https://ws.smn.gob.ar/map_items/weather',
              'especiales':'https://ws.smn.gob.ar/alerts/type/IE',
              'corto_plazo':'https://ws.smn.gob.ar/alerts/type/AC',
              'alertas':'https://ws.smn.gob.ar/alerts/type/AL',
              'pronostico_1dia':'https://ws.smn.gob.ar/map_items/forecast/1',
              'pronostico_2dia':'https://ws.smn.gob.ar/map_items/forecast/2',
              'pronostico_3dia':'https://ws.smn.gob.ar/map_items/forecast/3',
              'otros_pronosticos':'https://ws.smn.gob.ar/forecast/'}
    
    smn_request(urls_smn)

main()