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

def check_tamaño(imagen,ANCHO = 812 ,ALTO = 627):   
    if imagen.size == (ANCHO, ALTO):
        return True     
    else:
        return False
    
def png_jpg(nombre,imagen):   #Ahora el nombre es el mismo y solo cambia la extension
    imagen = imagen.convert('RGB')
    tokens = nombre.split(".png")
    imagen.save(tokens[0]+".jpg")
    return imagen    


def lat_long(coordenadas,ANCHO = 812,ALTO = 627):
    
    LONGITUD = 73.69945905 # longitud de referencia
    LATITUD = 27.301116798 # latitud de referencia 
    PIXEL_DISTANCIA = 0.0272000045 # relacion entre diferencia de latitudes/longitudes y pixeles
    RADIO = 30  # cuadrado de 20x20 con centro en la cordenada ingresada
    
    diferencia_longitud = LONGITUD - coordenadas[1]
    corte_izquierdo = (diferencia_longitud /PIXEL_DISTANCIA) - RADIO
    corte_izquierdo = int(corte_izquierdo)
    corte_derecho = ANCHO - ((corte_izquierdo) + 2 * RADIO)
    
    diferencia_latitud = coordenadas[0] - LATITUD
    corte_superior = (diferencia_latitud / PIXEL_DISTANCIA) - RADIO
    corte_superior = int(corte_superior)
    corte_inferior = ALTO - ((corte_superior) + 2 * RADIO)
    
    corte = (corte_izquierdo,corte_superior,corte_derecho,corte_inferior) # left, up, right, bottom

    return corte


def recorte(provincia,recortes_provincias):
    for clave in recortes_provincias :
        if clave == provincia:
            recorte_prov = recortes_provincias[clave]
            return recorte_prov

def zonas_provincias(recorte_prov,ALTO,ANCHO,corte_radio):
    alto_provincia = ALTO - (recorte_prov[1] + recorte_prov[3])
    alto_provincia  = int(alto_provincia /3)
    ancho_provincia = ANCHO - (recorte_prov[0] + recorte_prov[2])
    ancho_provincia  = int(ancho_provincia /3)
    
    sur = (recorte_prov[0] + ancho_provincia ,recorte_prov[1] + (2 * alto_provincia ), recorte_prov[2] + ancho_provincia,recorte_prov[3])# left, up, right, bottom
    centro = (recorte_prov[0] + ancho_provincia, recorte_prov[1] + alto_provincia , recorte_prov[2] + ancho_provincia , recorte_prov[3] + alto_provincia)
    norte = (recorte_prov[0] + ancho_provincia,recorte_prov[1],recorte_prov[2]+ ancho_provincia,recorte_prov[3] + (2 * alto_provincia))
    oeste = (recorte_prov[0], recorte_prov[1] + alto_provincia , recorte_prov[2] + (2*ancho_provincia) ,recorte_prov[3] + alto_provincia)
    este = (recorte_prov[0] + (2*ancho_provincia), recorte_prov[1] + alto_provincia , recorte_prov[2] , recorte_prov[3] + alto_provincia)
    noreste = (recorte_prov[0] + (2*ancho_provincia),recorte_prov[1],recorte_prov[2],recorte_prov[3] +(2 * alto_provincia))
    noroeste = (recorte_prov[0] ,recorte_prov[1],recorte_prov[2] + (2*ancho_provincia),recorte_prov[3] +(2 * alto_provincia))
    sureste = (recorte_prov[0] + (2*ancho_provincia),recorte_prov[1] + (2 * alto_provincia),recorte_prov[2],recorte_prov[3])
    suroeste = (recorte_prov[0],recorte_prov[1] + (2 * alto_provincia),recorte_prov[2] + (2*ancho_provincia),recorte_prov[3])
    zonas = {"norte":norte,"oeste":oeste,"este":este,"centro":centro,"noreste":noreste,"noroeste":noroeste,"sureste":sureste,"suroeste":suroeste,"sur":sur,"100km a la redonda":corte_radio}
    return zonas



def contador_pixel(imagen,zonas):
    pixeles = []
    pixeles_zonas = []
    for zona in zonas.items():
        im = ImageOps.crop(imagen, zona[1])
        rojo = 0
        magenta = 0
        pixeles_totales = 0
        for pixel in im.getdata():
            if pixel[0]>200 and pixel[1] < 70 and pixel[2]<100 or pixel[0]>120 and pixel[2]<30 :
                rojo += 1
            if pixel[0]>200 and pixel[1]<10 and pixel[2]>100:
                magenta += 1
            pixeles_totales +=  1
        pixeles = [magenta,rojo,pixeles_totales]
        pixeles_zonas.append([zona[0],pixeles])
    print(pixeles_zonas)
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
   
