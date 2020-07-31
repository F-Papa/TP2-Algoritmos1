import modulo_csv as CSV
#import modulo_geo as GEO
import modulo_graficos as GRAF
import modulo_proceso_smn as smn
import color_fotos as analisis

def analisis_foto(coordenadas):
    nombre = ""
    tamaño_es_correcto = False #Cambio a Bool y renombro la variable y la funcion para que sea mas legible
    rojo = 0
    magenta = 0
    pixeles_totales = 0
    recorte_provincias = {"Buenos Aires":(385,210,200,100),"La Pampa":(220,270,420,170),"Rio Negro":(120,405,400,65),"Neuquen":(120,330,570,90),"Mendoza":(145,160,525,240),"San Luis":(245,145,475,305),"Cordoba":(300,50,370,345),"Santa Fe":(400,20,270,370),"Entre Rios":(475,80,230,380),"San Juan":(145,20,540,440)}
    
    corte_punto = analisis.lat_long(coordenadas)
    provincia = analisis.buscar_provincia(recorte_provincias,corte_punto)
    zonas = analisis.zonas_provincias(provincia,corte_punto)

    while not tamaño_es_correcto:

        nombre = input("Ingrese el nombre de la imagen: ")
        imagen,nombre = analisis.verificador(nombre)

        tamaño_es_correcto = analisis.check_tamaño(imagen)

        if not tamaño_es_correcto:
            print("El tamaño de la imagen no es el esperado (812x627)") 

    if "png" in nombre: #Expresion simplificada

        imagen = analisis.png_jpg(nombre,imagen)

    pixeles_zonas = analisis.contador_pixel(pixeles_totales,rojo,magenta,imagen,zonas)
    
    print_separador()

    analisis.alertas(pixeles_zonas,provincia)


def ListadoAlertas():
    a = 2

def menu():
    eleccion = "0"
    while eleccion not in "123456": 
        print_opciones()
        eleccion = input()
        print()
    
    return eleccion

def solicitar_usuario():
    """Le solicita al usuario los datos de úbicación"""
    return input("¿Podrías indicarnos en qué ciudad te encuentras? -> ").title()
    
def print_separador(longitud = 20):
    print('-'*longitud)
    print()

def print_opciones():
    
    print("TORMENTA")
    print("--------")
    print("[1] Analizar un archivo CSV")
    print("[2] Alertas")
    print("[3] Pronostico extendido para una ciudad")
    print("[4] Analizar una imagen de radar")
    print("[5] Cambiar de ciudad")
    print("[6] Salir")

def print_bienvenida():
    print("Bienvenido a Tormenta")

def verif_coord(coord_str):
    negativo = True
    error = True
    coord = float(0)
    
    if coord_str == coord_str.lstrip('-'):
        negativo = False
        
    coord_str = coord_str.lstrip('-')
    
    if len(coord_str) == 6:
        error = False
        
        try:
            coord = float(coord_str)
            if negativo:
                coord = -coord
            
        except:
            error = True    
            
    if error:
        print("Formato incorrecto, recuerde que este es: (-)dd.ddd")
                
    return coord

def get_coord():
    print("Porfavor ingrese sus coordenadas")
    lat = float(0)
    lon = float(0)
    eleccion = ""
    
    while lat == 0 and eleccion != "*":
        eleccion = input("Latitud: ")
        lat = verif_coord(eleccion)
        
    while lon == 0 and eleccion != "*":
        eleccion = input("Longitud: ")
        lon = verif_coord(eleccion)
         
    return (lat, lon)

def imprimir_extendido(lista, ciudad):
    """Imprime el pronóstico extendido de la ciudad seleccionada
       Precondición: Una lista que contenga el nombre de los archivos que contienen la información del pronóstico extendido;
                     Latitud y Longitud o Ciudad otorgados por el usuario."""
    
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
        
def imprimir_actual(nombre_archivo,ciudad):
    """Imprime el pronóstico extendido de la ciudad seleccionada
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
        
        print("La temperatura actual en {} es: {}°C. La visibilidad es de {}km y la velocidad del viento es de {}km/m.\n{}\n\n".format(clima_actual["Ciudad"], 
                                                                                                                                      clima_actual["Temperatura"], 
                                                                                                                                      clima_actual["Visibilidad"], 
                                                                                                                                      clima_actual["Velocidad_del_viento"],
                                                                                                                                      recomendacion))
    else:
        print(f"No se encontraron datos del clima actual en {ciudad}\n")

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
    
    ciudad = solicitar_usuario() #Solicitud de datos de ciudad al usuario
    
    print_separador()
    
    imprimir_actual("actual", ciudad) #Imprimir pronóstico actual
    
    
    desea_salir = False
    
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
            eleccion = "0"
            
            while eleccion not in "123":
                print("[1] Alertas a nivel nacional")
                print("[2] Alertas cercanas a unas coordenadas")
                print("[3] Volver al menu")
                eleccion = input()
            
            if eleccion == "1":
                a = 1
            elif eleccion == "2":
                a = 1
            
            print_separador()
            
        elif eleccion == "3":
            #Imprimir pronóstico extendido
            archivos_extendido = ["pronostico_1dia", "pronostico_2dias", "pronostico_3dias"]
            imprimir_extendido(archivos_extendido, ciudad)
            
            print()
            
        elif eleccion == "4":
            #Procesamiento de imagen de radar.

            lat, lon = get_coord()
           #-34.593056, -58.445746     
            if lat != 0 and lon !=0:
                analisis_foto((-lat, -lon))
            
            print_separador()
            
        elif eleccion == "5":
            ciudad = solicitar_usuario()
            imprimir_actual("actual", ciudad)
            
        elif eleccion == "6":
            desea_salir = True
        
            
            

main()
