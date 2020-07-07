from PIL import Image

def ingreso_ruta(pixeles):
    while pixeles == []:
        ruta = input("Nombre de la imagen:")
        pixeles = contadorPixel(ruta,pixeles)


def contador_pixel(ruta,pixeles):

    try:
        im = Image.open(ruta)
        for pixel in im.getdata():
            if pixel == (255,0,0):
                rojo += 1
            elif pixel == (0,255,0):
                    verde += 1
            elif pixel ==(0,0,255):
                azul += 1
        pixeles = [rojo,verde,azul]
    
    except:
        print("No ha sido posible cargar la imagen, de nombre: "+ruta)
    
    return pixeles

def main():
    pixeles=[]
    ingreso_ruta(pixeles)
main()
