import modulo_csv as CSV
import modulo_geo as GEO
import modulo_graficos as GRAF
import modulo_proceso_smn as smn
import color_fotos as analisis

def analisis_foto(lat, lon):
    provincia = GEO.get_provincia(lat, lon)
    coordenadas = (-lat, -lon)
    nombre,entrada = "", ""
    tamaño_es_correcto = False #Cambio a Bool y renombro la variable y la funcion para que sea mas legible
    ANCHO = 812
    ALTO = 627
    recortes_provincias = {"Buenos Aires":(385,210,200,100),"La Pampa":(220,270,420,170),"Rio Negro":(120,405,400,65),"Neuquén":(120,330,570,90),"Mendoza":(145,160,525,240),"San Luis":(245,145,475,305),"Cordoba":(300,50,370,345),"Santa Fe":(405,20,275,375),"Entre Rios":(475,80,230,380),"San Juan":(145,20,540,440)}
    corte_radio = analisis.lat_long(coordenadas,ANCHO,ALTO)
    recorte_prov = analisis.recorte(provincia,recortes_provincias)
    zonas = analisis.zonas_provincias(recorte_prov,ALTO,ANCHO,corte_radio)
    
    while not tamaño_es_correcto and entrada != "*":
        nombre = input("Ingrese el nombre de la imagen: ")
        imagen,nombre = analisis.verificador(nombre)
        tamaño_es_correcto = analisis.check_tamaño(imagen,ANCHO,ALTO)
        if not tamaño_es_correcto:
            print("El tamaño de la imagen no es el esperado (812x627)") 
            entrada = input("Si desea salir ingrese *: ")

    if "png" in nombre: #Expresion simplificada
        imagen = analisis.png_jpg(nombre,imagen)

    pixeles_zonas = analisis.contador_pixel(imagen,zonas)
    print_separador()
    analisis.alertas(pixeles_zonas,provincia)

def menu(archivos_encontrados):
    """Verifica la entrada del usuario en el menu""" 
    eleccion = "0"
    while eleccion not in "123456": 
        print_opciones(archivos_encontrados)
        eleccion = input()
        print()
    
    return eleccion

def solicitar_usuario():
    """Post-Condicion: Le solicita al usuario los datos de úbicación"""
    return input("¿Podrías indicarnos en qué ciudad te encuentras? -> ").title()
    
def print_separador(longitud = 20):
    """Post-Condicion: Imprime una linea de guiones"""

    print('-'*longitud)
    print()

def print_opciones(archivos_encontrados):
    
    """Pre-Condicion: archivos_encontrados, true si el programa consiguio acceder a los datos del SMN, false de caso contrario
    Post-Condicion: Imprime las opciones del menu principal disponibles para el estado del programa"""
    
    print("TORMENTA")
    print("--------")
    
    if archivos_encontrados:
        print("[1] Analizar un archivo CSV")
        print("[2] Alertas")
        print("[3] Pronostico extendido para una ciudad")
        print("[4] Analizar una imagen de radar")
        print("[5] Cambiar de ciudad")

    else:
        print("[1] Analizar un archivo CSV")
        print("[2] NO DISPONIBLE")
        print("[3] NO DISPONIBLE")
        print("[4] Analizar una imagen de radar")
        print("[5] NO DISPONIBLE")
    
    print("[6] Salir")

def print_bienvenida():
    """Post-Condicion: Imprime en pantalla la bienvenida deseada"""
    print("\nBienvenido a Tormenta")

def verif_coord(coord_str):
    """ Pre-Condicion: Recibe una valor de latitud o longitud como string
        Post-Condicion: Devuelve el string convertido a float y un True si esta en formato (-)dd.ddd. En caso contrario devuelve 0 y False"""

    negativo = True
    coord = float(0)
    exito = False
    
    if coord_str == coord_str.lstrip('-'):
        negativo = False
        
    coord_str = coord_str.lstrip('-')
    
    if len(coord_str) == 6 and coord_str[2] == '.' and (coord_str.replace('.', '')).isnumeric():      
        
        coord = float(coord_str)
        if coord <= 90:
            if negativo:
                coord = -coord
            
            exito = True

        else:
            print("Las coordenadas solo pueden ir desde -90.000 hasta 90.000")
        
        
    
    elif coord_str != "*":
        print("Formato incorrecto, recuerde que este es: (-)dd.ddd")

    return coord, exito  

def get_coord():
    """Post-Condicion: Devuelve una tupla con 2 floats que pide al usuario (latitud, longitud)"""

    print("Porfavor ingrese sus coordenadas. Para volver ingrese *")
    lat = float(0)
    lon = float(0)
    eleccion = ""
    
    exito = False
    while not exito and eleccion != "*":
        eleccion = input("Latitud: ")
        lat, exito = verif_coord(eleccion)

    exito = False    
    while not exito and eleccion != "*":
        eleccion = input("Longitud: ")
        lon, exito = verif_coord(eleccion)
         
    return (lat, lon)

def imprimir_extendido(lista, ciudad):
    """Imprime el pronóstico extendido de la ciudad seleccionada
       Precondición: Una lista que contenga el nombre de los archivos que contienen la información del pronóstico extendido;
                     y una Ciudad otorgada por el usuario."""
                     
    
    dia_1 = smn.buscar_por_ubicacion(smn.extendido(lista[0]), ciudad)
    dia_2 = smn.buscar_por_ubicacion(smn.extendido(lista[1]), ciudad)
    dia_3 = smn.buscar_por_ubicacion(smn.extendido(lista[2]), ciudad)
    
    if dia_1:
        temperatura_1dia = str(dia_1["Temperatura_mañana"])+"°C/"+str(dia_1["Temperatura_tarde"])+"°C"
        temperatura_2dia = str(dia_2["Temperatura_mañana"])+"°C/"+str(dia_2["Temperatura_tarde"])+"°C"
        temperatura_3dia = str(dia_3["Temperatura_mañana"])+"°C/"+str(dia_3["Temperatura_tarde"])+"°C"

        print ("{:<10} \t {:<15} \t {:<15} \t {:<15}".format("Ciudad","1 día: Mañana/Tarde",
                                                             "2 días: Mañana/Tarde", "3 días: Mañana/Tarde"))
        print ("{:<10} \t {:<15} \t {:<15} \t {:<15}".format(dia_1["Ciudad"],temperatura_1dia, temperatura_2dia, temperatura_3dia))
    else:
        
        print(f"No se encontraron datos del clima extendido en {ciudad}\n")

def imprimir_alertas_nacionales(lista):
    "Imprime las alertas a nivel nacional obtenidad del Sistema Meteorológico Nacional"
    for i in range(len(lista)):
        zonas = ""
        for clave, elemento in lista[i].items():
            if "Zona" in clave:
                zonas += elemento+", "
        print("Alerta a nivel nacional nro.: {}.".format(i+1))
        print("Fecha: {}.".format(lista[i]["Fecha"]))
        print("Zonas afectadas: {}.".format(zonas[:-2]))
        print()
        print(lista[i]["Descripción"])
        print_separador()
    print()

def alertas_cercanas(lista, provincia):
    """Imprime las alertas emitidas para la pronvincia indicada por el usuario"""
    
    print(f"En {provincia.title()} hay las siguientes alertas:\n")
    contador_alertas = 0

    for i in range(len(lista)):
        for clave, elemento in lista[i].items():

            if clave == "Descripción" and provincia.upper() in elemento.upper():
                print(f"Alerta nro. {contador_alertas+1}: {elemento}\n")
                contador_alertas+=1
        
    
    if contador_alertas == 0:
        print("Ninguna\n")

def imprimir_actual(nombre_archivo,ciudad):
    """Imprime el pronóstico extendido de la ciudad seleccionada, devuelve 1 si fue exitoso o 0 si no se encontraron datos de la ciudad pedida
       Precondición: nombre del archivo que contiene el clima actual;
                     Latitud y Longitud o Ciudad otorgados por el usuario."""
    
    clima_actual = smn.buscar_por_ubicacion(smn.actual(nombre_archivo), ciudad)
    
    if clima_actual:
        if clima_actual["Temperatura"] < 10:
            recomendacion = "Hoy va a hacer frío. Recuerden llevar abrigo."
        elif clima_actual["Temperatura"] < 15: 
            recomendacion = "Hoy va a hacer día fresco. No descuidarse."
        elif clima_actual["Temperatura"] < 20:
            recomendacion = "Hoy va a hacer día lindo para pasear. Disfruten el día."
        elif clima_actual["Temperatura"] < 30:
            recomendacion = "Hoy va a hacer día caluroso. Cuidense del sol."
        else:
            recomendacion = "Mucho cuidado con el calor personas mayores y niños. Tomen mucha agua para evitar golpes de calor."
        
        print("La temperatura actual en {} ({}) es: {}°C. La visibilidad es de {}km y la velocidad del viento es de {}km/m.\n{}\n".format(clima_actual["Ciudad"],
                                                                                                                                      clima_actual["Provincia"], 
                                                                                                                                      clima_actual["Temperatura"], 
                                                                                                                                      clima_actual["Visibilidad"], 
                                                                                                                                      clima_actual["Velocidad_del_viento"],
                                                                                                                                      recomendacion))
        return 1
    
    else:
        print(f"No se encontraron datos del clima actual en {ciudad}\n")
        return 0

def imprimir_actual_aprox():
    lat, lon = get_coord()
    ciudad = smn.aproximar(lat,lon,"actual")
    print()
    imprimir_actual("actual", ciudad)  

    return ciudad

def main():
    #Punto de Entrada

    urls_smn= {'actual':'https://ws.smn.gob.ar/map_items/weather',
              'especiales':'https://ws.smn.gob.ar/alerts/type/IE',
              'corto_plazo':'https://ws.smn.gob.ar/alerts/type/AC',
              'alertas':'https://ws.smn.gob.ar/alerts/type/AL',
              'pronostico_1dia':'https://ws.smn.gob.ar/map_items/forecast/1',
              'pronostico_2dias':'https://ws.smn.gob.ar/map_items/forecast/2',
              'pronostico_3dias':'https://ws.smn.gob.ar/map_items/forecast/3',
              'otros_pronosticos':'https://ws.smn.gob.ar/forecast/'}
    
    print_bienvenida() 
    
    archivos_encontrados = True

    try:

        smn.smn_request(urls_smn)
        ciudad = solicitar_usuario()
    
        print_separador()
        
        if not imprimir_actual("actual", ciudad):
            imprimir_actual_aprox()  
    
    except:

        print("Error abriendo los datos de clima, algunas funciones no estarán disponibles")
        archivos_encontrados = False

      
    desea_salir = False
    
    while not desea_salir:
        eleccion = menu(archivos_encontrados)
        
        if eleccion == "1":
            #CSV

            dir = input("Ingrese el nombre/directorio del archivo CSV: ")
            lineas = CSV.cargar_archivo(dir)         
            
            if len(lineas) > 0:
                
                print_separador()

                promedio_temp_max, lista_años = CSV.get_promedio(lineas, 4, 4)
                promedio_temp_min, lista_años = CSV.get_promedio(lineas, 5, 4)

                promedio_temp = CSV.promediar(promedio_temp_max, promedio_temp_min)
                print("Promedio de Temperatura en últimos 5 años:")
                GRAF.grafico_barras(lista_años, promedio_temp, "°C", GRAF.Color.VERDE)

                promedio_humedad_relativa, lista_años = CSV.get_promedio(lineas, 8 , 4)
                print("Promedio de Humedad en últimos 5 años:")
                GRAF.grafico_barras(lista_años, promedio_humedad_relativa, "", GRAF.Color.CYAN)
                
                max_lluvia = CSV.get_max(lineas, 6, 4)
                print(GRAF.Color.AZUL+"Precipitaciones máx. de los últimos 5 años:", max_lluvia, "mm")
                
                max_temp = CSV.get_max(lineas, 4, 4)
                print(GRAF.Color.ROJO+"Temperatura máx. de los últimos 5 años:", max_temp, "°C")
                    
                print(GRAF.Color.RESET)
                print_separador()
                
        elif eleccion == "2" and archivos_encontrados:
            #Alertas

            eleccion = "0"
            while eleccion not in "123":
                print("[1] Alertas a nivel nacional")
                print("[2] Alertas por ubicación")
                print("[3] Volver al menu")
                eleccion = input()
            
            if eleccion == "1":
                #Alertas a nivel nacional

                alertas_nacional = smn.alertas("alertas")
                imprimir_alertas_nacionales(alertas_nacional)

            elif eleccion == "2":
                #Alertas cercanas a unas coordenadas

                eleccion = "0"
                while eleccion not in "123":
                    print("[1] Buscar por provincia")
                    print("[2] Buscar por coordenadas")
                    print("[3] Volver al menu")
                    eleccion = input()

                if eleccion != "3":

                    if eleccion == "1":
                        #Buscar por provincia

                        provincia = input("Nombre de la provincia: ").title()

                    elif eleccion == "2":
                        #Buscar por coordenadas

                        lat, lon = get_coord()                       

                        provincia = GEO.get_provincia(lat, lon)
                    
                    try:
                        alertas_provincial = smn.alertas("alertas")                   

                        alertas_cercanas(alertas_provincial, provincia)
                    
                    except:
                        print("\nError, intente nuevamente")
            
        elif eleccion == "3" and archivos_encontrados:
            #Imprimir pronóstico extendido

            archivos_extendido = ["pronostico_1dia", "pronostico_2dias", "pronostico_3dias"]
            imprimir_extendido(archivos_extendido, ciudad)
      
            print()
            
        elif eleccion == "4":
            #Procesamiento de imagen de radar.

            lat, lon = get_coord()
            
            try:
                analisis_foto(lat, lon)
            except:
                print("\nLas coordenadas introducidas no corresponden a la region del mapa")
            
            print_separador()
            
        elif eleccion == "5" and archivos_encontrados:
            #Cambiar de ciudad

            ciudad = solicitar_usuario()

            if not imprimir_actual("actual", ciudad):
                imprimir_actual_aprox()
                          
        elif eleccion == "6":
            desea_salir = True      
            
main()
