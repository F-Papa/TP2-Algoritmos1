from PIL import Image
from PIL import ImageOps

def verificador(ruta):
    try:
        im = Image.open(ruta)
        im.close()
    except:
        print("No ha sido posible cargar la imagen, de nombre: "+ruta)
        ruta = input("nom")
        verificador(ruta)
        
    return ruta


def contador_pixel(pixeles_totales,rojo,magenta,ruta):
    im = Image.open(ruta)
    borde = (0,20,57,60)
    im = ImageOps.crop(im, borde )#recorto la imagen
    #el getdata me da una tupla rgb por cada pixel
    for pixel in im.getdata():
        if pixel == (238, 17, 52) or  pixel == (205, 0, 17) or pixel == (171, 0, 18) or pixel == (154, 0, 0):
            rojo += 1
        if pixel == (187, 1, 102) or  pixel == (221, 1, 153) or pixel == (238, 0, 238) or pixel == (203, 0, 204) or pixel == (170, 0, 187) or pixel == (153, 0, 153):
            magenta += 1
        pixeles_totales +=  1
    im.close()
    pixeles = [magenta,rojo,pixeles_totales]
    
    return pixeles
        
def main ():
    opcion = 0
    while opcion != "2":
        print("1- Analisis de imagenees")
        print("2- Salir")
        opcion = input("Opcion: ")
        rojo = 0
        magenta = 0
        pixeles_totales = 0
        lista = []
        if opcion == "1":           
            ruta = ""
            ruta = input("Nombre imagen: ")
            ruta = verificador(ruta)
            print(contador_pixel(pixeles_totales,rojo,magenta,ruta))
            
    
main()
