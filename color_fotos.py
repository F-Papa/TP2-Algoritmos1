from PIL import Image
from PIL import ImageOps

def verificador(nombre):
    try:
        imagen = Image.open(nombre)
    except:
        print("No ha sido posible cargar la imagen, de nombre: " + nombre)
        nombre =  input("Ingrese un nombre nuevamente:")
        imagen,nombre = verificador(nombre)      
    return imagen,nombre

def check_tamaño(imagen):    #Ex TamañoF

    if imagen.size == (812, 627):
        return True
        
    else:
        return False

def png_jpg(ruta,imagen):   #Ahora el nombre es el mismo y solo cambia la extension
    imagen = imagen.convert('RGB')
    tokens = ruta.split(".png")
    imagen.save(tokens[0]+".jpg")
    return imagen

def lat_long(coordenadas):
    
    LONGITUD = 73.70045905 # longitud de referencia
    LATITUD = 27.601116798 # latitud de referencia 
    PIXEL_DISTANCIA = 0.0268380045 # relacion entre diferencia de latitudes/longitudes y pixeles
    RADIO = 20  # cuadrado de 20x20 con centro en la cordenada ingresada
    ANCHO_IMAGEN = 812
    ALTO_IMAGEN = 627
    
    diferencia_longitud = LONGITUD - coordenadas[1]
    corte_izquierdo = (diferencia_longitud /PIXEL_DISTANCIA) - RADIO
    corte_izquierdo = int(corte_izquierdo)
    corte_derecho = ANCHO_IMAGEN - ((corte_izquierdo) + 2 * RADIO)
    
    diferencia_latitud = coordenadas[0] - LATITUD
    corte_superior = (diferencia_latitud / PIXEL_DISTANCIA) - RADIO
    corte_superior = int(corte_superior)
    corte_inferior = ALTO_IMAGEN - ((corte_superior) + 2 * RADIO)
    
    corte = (corte_izquierdo,corte_superior,corte_derecho,corte_inferior) # left, up, right, bottom
    punto = (corte_izquierdo + (RADIO - 1) ,corte_superior + (RADIO-1),corte_derecho + (RADIO-1),corte_inferior + (RADIO-1)) #sumo el RADIO para que solo me quede el punto y poder identificar la provincia
    # el -1 viene a que al pasar los cortes a numeros enteros existe un error de 1pixel y ese punto no existe

    return corte, punto

def buscar_provincia(recorte_provincias,corte_punto):
    provincia = ()
    for recorte in recorte_provincias.items():
        if recorte[1][0] < corte_punto[1][0] and  recorte[1][1] < corte_punto[1][1] and  recorte[1][2] < corte_punto[1][2] and  recorte[1][3] < corte_punto[1][3]:
            return recorte #Simplifico esto para que termine una vez que la encuntra

def zonas_provincias(provincia,corte_punto):
    altura_provincia = provincia[1][1] - provincia[1][3]
    if altura_provincia  < 0:
        altura_provincia  = altura_provincia  * (-1)
    altura_provincia  = int(altura_provincia /3)
    sur = (provincia[1][0] ,provincia[1][1] + (2 * altura_provincia ), provincia[1][2] ,provincia[1][3])
    centro = (provincia[1][0] , provincia[1][1] + altura_provincia , provincia[1][2] , provincia[1][3] + altura_provincia)
    norte = (provincia[1][0] ,provincia[1][1],provincia[1][2] ,provincia[1][3] + (2 * altura_provincia))
    zonas = {"norte":norte,"centro":norte,"sur":norte,"100km":corte_punto[0]}
    return zonas


def contador_pixel(pixeles_totales,rojo,magenta,imagen,zonas):
    pixeles = []
    pixeles_zonas = []
    for zona in zonas.items():
        im = ImageOps.crop(imagen, zona[1])
        for pixel in im.getdata():
            if pixel[0]>200 and pixel[2]<100 or pixel[0]>120 and pixel[2]<30 :
                rojo += 1
            if pixel[0]>200 and pixel[1]<10 and pixel[2]>100:
                magenta += 1
            pixeles_totales +=  1

        pixeles = [magenta,rojo,pixeles_totales]
        pixeles_zonas.append([zona[0],pixeles])
    imagen.close()
    return pixeles_zonas


def alertas(pixeles_zonas,provincia):
    print(provincia[0],":")
    for zona in pixeles_zonas:
        porcentaje = int((zona[1][2] * 1.5)/100)
        print(zona[0],":")
        if zona[1][0] > 5:
            print("Alerta de granizo")
        if zona[1][1] > porcentaje:
            print("Alerta de tormenta")
        if zona[1][1] > 5 and  zona[1][1] < porcentaje:
            print("Alerta de lluvia")
        if zona[1][1] > 5 and zona[1][0]>5:
            print("Alerta de tormenta y granizo")
        if zona[1][1] < 5 and zona[1][0]<5:
            print("No hay tormentas")

    
   
