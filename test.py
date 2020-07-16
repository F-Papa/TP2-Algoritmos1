from PIL import Image
from PIL import ImageOps

def verificador(ruta):
    try:
        im = Image.open(ruta)
    except:
        print("No ha sido posible cargar la imagen, de nombre: "+ruta)
        ruta = input("Nombre de la imagen:")
        verificador(ruta)
        
    return im

def png_jpg(ruta):
    im = Image.open(ruta)
    im.mode
    im = im.convert('RGB')
    ruta = "imagen.jpg"
    im.save(ruta)
    print(im)
    return im

def buscar_provincia(recorte_provincias,provincia):
    for i in recorte_provincias:
        if i == provincia:
            provincia1  = recorte_provincias[i]
    return provincia1


    


def contador_pixel(pixeles_totales,rojo,magenta,im,provincia1):
    
    im = ImageOps.crop(im, provincia1 )
    for pixel in im.getdata():
        if pixel[0]>200 and pixel[2]<100 or pixel[0]>120 and pixel[2]<30 :
            rojo += 1
        if pixel[0]>200 and pixel[1]<10 and pixel[2]>100:
            magenta += 1
        pixeles_totales +=  1
    im.show()
    im.close()
    pixeles = [magenta,rojo,pixeles_totales]
    print(pixeles)
    
        
    return pixeles
    


    
def alertas(pixeles):
    if pixeles[0] > 5:
        print("Alerta de granizo")
    if pixeles[1]>5:
        print("Alerta de tormenta")
    if pixeles[1]>5 and pixeles[0]>5:
        print("Alerta de tormenta y granizo")
    if pixeles[1]<5 and pixeles[0]<5:
        print("No hay tormentas")

    
   
def analisis_foto():
    rojo = 0
    magenta = 0
    pixeles_totales = 0
    recorte_provincias = {"Buenos Aires":(385,210,200,100),"La Pampa":(220,270,420,170),"Rio Negro":(120,405,400,65),"Neuquen":(120,330,570,90),"Mendoza":(145,160,525,240),"San Luis":(245,145,475,305),"Cordoba":(300,50,370,345),"Santa Fe":(400,20,270,370),"Entre Rios":(475,80,230,380),"San Juan":(145,20,540,440)}
    pixeles_provincias = []
    pixeles=[]
    im = 0
    provincia1 = ()
    prov = input("Ingrese una provincia:")
    provincia1 = buscar_provincia(recorte_provincias,prov)
    ruta = input("Nombre del archivo: ")
    im = verificador(ruta)
    print(im)
    if ruta.find("png") != -1:
        im = png_jpg(ruta)
    alertas(contador_pixel(pixeles_totales,rojo,magenta,im,provincia1))
            


def main ():
    opcion = 0
    while opcion != "2":
        print("1- Analisis de imagenees")
        print("2- Salir")
        opcion = input("Opcion: ")
        if opcion == "1":
            analisis_foto()
main()
