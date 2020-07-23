import modulo_csv as CSV
import modulo_geo as GEO
import modulo_graficos as GRAF

def ListadoAlertas():
    a = 2

def menu():
    eleccion = "0"
    while eleccion not in "12345": 
        print_opciones()
        eleccion = input()
        print()
    
    return eleccion

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

def main():
    print_bienvenida()
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
            a = 1
            #...
        elif eleccion == "3":
            a = 1
            #...
        elif eleccion == "4":
            a = 1
            #...
        else:
            desea_salir = True
        
            
            
            
                
            
            
            
            
                

    



main()