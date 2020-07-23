def calcular_distancia(lat1,long1,lat2,long2):
    """ Pre-Condición: Recibe dos coordenadas (float, dd.ddd)
        Post-Condición: Devuelve la distancia entre los 2 puntos dados (float)"""

    return ( (lat2-lat1)**2 + (long2-long1)**2 )**(1/2)

def get_provincia_mas_cercana(latitud, longitud):
    """ Pre-Condición: Recibe latitud y longitud como parametros (float, dd.ddd)
        Post-Condición: Devuelve el nombre de la Provincia cuya capital está más cerca de las coordenadas introducidas (string)"""

    coord_provincias =   {'Buenos Aires':       [-34.613, -58.377],
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
    
    
    for key, value in coord_provincias.items():
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