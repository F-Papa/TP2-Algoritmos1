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

def tamaño_correcto(imagen,tamaño,ancho,alto):
    if imagen.size == (ancho,alto):
        tamaño = 1
    return tamaño

def png_jpg(imagen):
    imagen = imagen.convert('RGB')
    nombre = "imagen.jpg"
    imagen.save(nombre)
    return imagen

def lat_long(coordenadas,ancho,alto):
    
    longitud = 73.70045905 # longitud de referencia
    latitud = 27.601116798 # latitud de referencia 
    pixel_distancia = 0.0268380045 # relacion entre diferencia de latitudes/longitudes y pixeles
    radio = 25  # cuadrado de 25x25 con centro en la cordenada ingresada
    
    diferencia_longitud = longitud - coordenadas[1]
    corte_izquierdo = (diferencia_longitud /pixel_distancia) - radio
    corte_izquierdo = int(corte_izquierdo)
    corte_derecho = ancho - ((corte_izquierdo) + 2 * radio)
    
    diferencia_latitud = coordenadas[0] - latitud
    corte_superior = (diferencia_latitud / pixel_distancia) - radio
    corte_superior = int(corte_superior)
    corte_inferior = alto - ((corte_superior) + 2 * radio)
    
    corte = (corte_izquierdo,corte_superior,corte_derecho,corte_inferior) # left, up, right, bottom

    return corte


def recorte(provincia,recortes_provincias):
    for clave in recortes_provincias :
        if clave == provincia:
            recorte_prov= recortes_provincias[clave]
    return recorte_prov

def zonas_provincias(provincia,alto,corte_radio):
    altura_provincia = alto - (provincia[1] + provincia[3])
    altura_provincia  = int(altura_provincia /3)
    sur = (provincia[0] ,provincia[1] + (2 * altura_provincia ), provincia[2] ,provincia[3])# left, up, right, bottom
    centro = (provincia[0] , provincia[1] + altura_provincia , provincia[2] , provincia[3] + altura_provincia)
    norte = (provincia[0] ,provincia[1],provincia[2] ,provincia[3] + (2 * altura_provincia))
    zonas = {"norte":norte,"centro":centro,"sur":sur,"100km":corte_radio}
    return zonas


def contador_pixel(imagen,zonas):
    pixeles = []
    pixeles_zonas = []
    for zona in zonas.items():
        im = ImageOps.crop(imagen, zona[1])
        im.show()
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



    
   
