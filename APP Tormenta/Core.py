import modulo_csv as CSV
import modulo_geo as GEO
import modulo_graficos as GRAF
import modulo_proceso_smn as smn
import color_fotos as analisis

def analisis_foto(coordenadas):
    nombre = ""
    tamaño = 0
    rojo = 0
    magenta = 0
    pixeles_totales = 0
    recorte_provincias = {"Buenos Aires":(385,210,200,100),"La Pampa":(220,270,420,170),"Rio Negro":(120,405,400,65),"Neuquen":(120,330,570,90),"Mendoza":(145,160,525,240),"San Luis":(245,145,475,305),"Cordoba":(300,50,370,345),"Santa Fe":(400,20,270,370),"Entre Rios":(475,80,230,380),"San Juan":(145,20,540,440)}
    corte_punto = analisis.lat_long(coordenadas)
    provincia = analisis.buscar_provincia(recorte_provincias,corte_punto)
    zonas = analisis.zonas_provincias(provincia,corte_punto)
    while tamaño == 0:
        nombre = input("Ingrese el nombre de la imagen: ")
        imagen,nombre = analisis.verificador(nombre)
        tamaño = analisis.tamañoF(imagen,tamaño)
        if tamaño == 0:
            print("El tamaño de la imagen no es el esperado (812x627)")       
    if nombre.find("png") != -1:
        imagen = analisis.png_jpg(nombre,imagen)
    pixeles_zonas = analisis.contador_pixel(pixeles_totales,rojo,magenta,imagen,zonas)
    analisis.alertas(pixeles_zonas,provincia)


def ListadoAlertas():
    a = 2

def menu():
    eleccion = "0"
    while eleccion not in "12345": 
        print_opciones()
        eleccion = input()
        print()
    
    return eleccion

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
                ciudad = input("En ese caso, ¿podrías indicarnos qué ciudad te gustaría conocer su estado actual?").title()
    else:
        lat="0"
        lon="0"
        ciudad = input("En ese caso, ¿podrías indicarnos qué ciudad te gustaría conocer su estado actual?").title()
    return [lat,lon,ciudad]

def print_separador(longitud = 20):
    print('-'*longitud)
    print()

def print_opciones():
    print("[1] Analizar un archivo CSV")
    print("[2] Alertas para unas coordenadas determinadas")
    print("[3] Pronostico extendido para una ciudad")
    print("[4] Analizar una imagen de radar")
    print("[5] Salir")

def print_bienvenida():
    print("Bienvenido a Tormenta")

def imprimir_extendido(lista, latitud, longitud, ciudad):
    """Imprime el pronóstico extendido de la ciudad seleccionada
       Precondición: Una lista que contenga el nombre de los archivos que contienen la información del pronóstico extendido;
                     Latitud y Longitud o Ciudad otorgados por el usuario."""
    
    dia_1 = smn.buscar_ubicacion(smn.extendido(lista[0]), latitud, longitud, ciudad)
    dia_2 = smn.buscar_ubicacion(smn.extendido(lista[1]), latitud, longitud, ciudad)
    dia_3 = smn.buscar_ubicacion(smn.extendido(lista[2]), latitud, longitud, ciudad)
    teperatura_1dia = str(dia_1["Temperatura_mañana"])+"°C/"+str(dia_1["Temperatura_tarde"])+"°C"
    teperatura_2dia = str(dia_2["Temperatura_mañana"])+"°C/"+str(dia_2["Temperatura_tarde"])+"°C"
    teperatura_3dia = str(dia_3["Temperatura_mañana"])+"°C/"+str(dia_3["Temperatura_tarde"])+"°C"

    print ("{:<10} \t {:<15} \t {:<15} \t {:<15}".format("Ciudad","1 día: Mañana/Tarde",
                                                         "2 días: Mañana/Tarde", "3 días: Mañana/Tarde"))
    print ("{:<10} \t {:<15} \t {:<15} \t {:<15}".format(dia_1["Ciudad"],teperatura_1dia, teperatura_2dia, teperatura_3dia))
    
        
def imprimir_actual(nombre_archivo, latitud,longitud,ciudad):
    """Imprime el pronóstico extendido de la ciudad seleccionada
       Precondición: nombre del archivo que contiene el clima actual;
                     Latitud y Longitud o Ciudad otorgados por el usuario."""
    
    clima_actual = smn.buscar_ubicacion(smn.actual(nombre_archivo), latitud, longitud, ciudad)
    recomendacion = ""
    if clima_actual["Temperatura"] < 10:
        recomendacion = "Hoy va a hacer frío. Recuerden, llevar abrigo."
    elif clima_actual["Temperatura"] < 15: 
        recomendacion = "Hoy va a hacer día fresco. No descuidarse."
    elif clima_actual["Temperatura"] < 20:
        recomendacion = "Hoy va a hacer día lindo para pasear. Disfruten el día."
    elif clima_actual["Temperatura"] < 30:
        recomendacion = "Hoy va a hacer día caluroso. Cuidense del sol."
    else:
        recomendacion = "Mucho cuidado con el calor personas mayores y niños. Tomen mucha agua para avitar golpes de calor."
    print("El teperatura actual en {} es: {}°C. La visibilidad es de {}km y la velovidad del viento es de {}km/m.\n{}".format(clima_actual["Ciudad"], 
                                                                                                                              clima_actual["Temperatura"], 
                                                                                                                              clima_actual["Visibilidad"], 
                                                                                                                              clima_actual["Velocidad_del_viento"],
                                                                                                                              recomendacion))
                 

def main():
    urls_smn= {'actual':'https://ws.smn.gob.ar/map_items/weather',
              'especiales':'https://ws.smn.gob.ar/alerts/type/IE',
              'corto_plazo':'https://ws.smn.gob.ar/alerts/type/AC',
              'alertas':'https://ws.smn.gob.ar/alerts/type/AL',
              'pronostico_1dia':'https://ws.smn.gob.ar/map_items/forecast/1',
              'pronostico_2dias':'https://ws.smn.gob.ar/map_items/forecast/2',
              'pronostico_3dias':'https://ws.smn.gob.ar/map_items/forecast/3',
              'otros_pronosticos':'https://ws.smn.gob.ar/forecast/'}
    
    smn.smn_request(urls_smn)    
    print_bienvenida()
    desea_salir = False
    #Solicitud de datos de latitud y longitud o ciudad al usuario
    ingreso = solicitar_usuario()
    lat = ingreso[0]
    lon = ingreso[1]
    ciudad = ingreso[2]
    #Imprimir pronóstico actual
    
    imprimir_actual("actual", lat, lon, ciudad)
    
    while not desea_salir:
        eleccion = menu()
        
        if eleccion == "1":
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
                
        elif eleccion == "2":
            a = 1
            #...
        elif eleccion == "3":
            #Imprimir pronóstico extendido
            a = 1
            archivos_extendido = ["pronostico_1dia", "pronostico_2dias", "pronostico_3dias"]
            imprimir_extendido(archivos_extendido, lat, lon, ciudad)
            
        elif eleccion == "4":
            coordenadas = ()
            lat_f = float(lat)
            lat_f = lat_f * -1
            long_f = float(long)
            long_f = long_f * -1
            coordenadas = (lat_f,long_f)
           
            a = 1
            analisis_foto(coordenadas)
        else:
            desea_salir = True
        
            
            
            
                
            
            
            
            
                

    



main()
