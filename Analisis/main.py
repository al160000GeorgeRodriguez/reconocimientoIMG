from tkinter.filedialog import askopenfile
from reportlab.pdfgen import canvas
import webbrowser
from reportlab.lib.pagesizes import letter
from scipy.spatial import distance as dist
import imutils
from imutils import contours
from imutils import perspective
import numpy as np
import argparse 
import imutils
import cv2
from tkinter import *
from datetime import datetime

from PIL import ImageTk, Image as IMG

import os
#Convierte el formato de video opencv al entorno TK
def convertirTk(miImagen):
    laImagen = cv2.cvtColor(miImagen, cv2.COLOR_BGR2RGB)
    laImagen = IMG.fromarray(laImagen)
    return ImageTk.PhotoImage(laImagen)

# Función para calcular el punto medio de dos coordenadas
def puntoMedio(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# La función permite interactuar con un cuadro de dialogo para abrir una imagen
archivoImagen: any
#Abre un archivo con extención jpg
Vmadre="1024x800"
Vhija="600x480"
root = Tk()
imagen=""
camara=0

def cambioDeCamara():
    global camara
    camara=not(camara)

def cImagenTK(uImg):
    miImagen = uImg
    img=Toplevel(root)
    img.title("Captura")
    img.geometry(Vhija)
    tImagen=convertirTk(miImagen)
    pic=Label(img,image=tImagen)
    pic.image=tImagen
    pic.pack(side="left")

def sImagenTK(miImagen):

    img=Toplevel(root)
    img.title("Captura")
    img.geometry(Vhija)
    tImagen=convertirTk(miImagen)
    pic=Label(img,image=tImagen)
    pic.image=tImagen
    pic.pack(side="left")



def capturarImagen():
    global camara
    def back():
        video = cv2.VideoCapture(1)
    video=cv2.VideoCapture(1)
    #medidas de la pantalla
    alto=1024
    ancho=800
    #longitud de la líneas del objetivo
    longitud=400
    calibracion2mmP1=int(ancho / 1.2)
    calibracion2mmP2=int(ancho / 3.3)

    while(True):
        aux,captura=video.read()
       # if aux==True:
        #
         #   print("Ok ")
        if cv2.waitKey(1) & 0xFF == ord('x'):
            cv2.line(captura, (int(alto / 3) + int(alto / 2), calibracion2mmP1 - longitud),
                     (int(alto / 3) + int(alto / 2), calibracion2mmP2 + longitud),
                     (128, 0, 0), 1, 1, 1)
            cv2.imwrite("Foto10.jpg", captura)
            break

        #height,ancho=cv2.getWindowImageRect(captura)

        resolucion=convertirTk(captura)
        alto=resolucion.height()*2.75
        ancho=resolucion.width()*1.5
        # Línea horizontal
        cv2.line(captura,(int(alto/2)-longitud,int(ancho/2)),(int(alto/2)+longitud,int(ancho/2)),(0,0,255),1,1,1)
        # Línea vertical
        cv2.line(captura,(int(alto/2),int(ancho/2)-longitud),(int(alto/2),int(ancho/2)+longitud),(0,0,255),1,1,1)
        # Línea de referencia
        cv2.line(captura, (int(alto / 3)+int(alto / 2), int(ancho / 1.3) - longitud), (int(alto / 3)+int(alto / 2), int(ancho / 3.2) + longitud),
                 (255,0 , 0), 1, 1, 1)

                #cv2.circle(captura,(300,240),100,(127,127,127),8)
        #cImagenTK(captura)

        cv2.imshow("foto", captura)

        #cv2.createButton("Back",back,None,cv2.QT_PUSH_BUTTON,0)

    video.release()

#Convierte el formato opencv a TK por medio de un path
def pImagenTK(uImg):
    miImagen = cv2.imread(uImg)
    img=Toplevel(root)
    img.title(uImg)
    img.geometry(Vhija)
    tImagen=convertirTk(miImagen)
    pic=Label(img,image=tImagen)
    pic.image=tImagen
    pic.pack(side="left")

def abrirArchivo():
    global imagen
    imagen=filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccione la imagen",
                                           filetypes=(("Archivos jpg", "*.jpg"), ("Todos los archivos", "*.*")))
    pImagenTK(imagen)

def obtenerNArchivo():
    ref = os.path.split(imagen)
    return ref[1]
def procesarImagen():
    miImagen = cv2.imread(imagen)

    # Se convierte en  gris la imagen y se desenfoca
    imGris = cv2.cvtColor(miImagen, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Imagen en gris",imGris)
    imGris = cv2.GaussianBlur(imGris, (7, 7), 0)
    #El desenfoque elimina el ruido proveniente de la camara y requisito previo para Canny
    #   cv2.imshow("Imagen Gris",imGris)
    imBorde = cv2.Canny(imGris, 50, 100)
    # cv2.imshow("Imagen Canny",imBorde)

    imBorde = cv2.dilate(imBorde, None, iterations=1)
    #cv2.imshow("Imagen dilate", imBorde)
    imBorde = cv2.erode(imBorde, None, iterations=1)
    cv2.imshow("Imagen erode", imBorde)

    cnts = cv2.findContours(imBorde.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    #cv2.imshow("Imagen contorno1", cnts)
    cnts = imutils.grab_contours(cnts)
    #laImagen=cv2.drawContours(miImagen,cnts,-1,(0,255,0),5)
    #cv2.imshow("contorno",laImagen)


    #cv2.imshow("Imagen contorno fino", cnts)
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    orig = miImagen.copy()
    for c in cnts:
        #Si el area es pequeña no se considera if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
            continue
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        #Se guarda la imagen

        ref2 = './Resultados/ref2'+obtenerNArchivo()
        cv2.imwrite(ref2, cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2))
        #cv2.imshow("puntos de imagen", box)
        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = puntoMedio(tl, tr)
        (blbrX, blbrY) = puntoMedio(bl, br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = puntoMedio(tl, bl)
        (trbrX, trbrY) = puntoMedio(tr, br)

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                 (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                 (255, 0, 255), 2)

        ref3='./Resultados/ref3'+obtenerNArchivo()
        cv2.imwrite(ref3, orig)
        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # (in this case, inches)
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / 0.89

        # compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}in".format(dimA),
                    (int(tltrX), int(tltrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 139), 2)
        cv2.putText(orig, "{:.1f}in".format(dimB),
                    (int(trbrX - 50), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 139), 2)

        # show the output image
        # cv2.imshow("Image", orig)
        refinal='./Resultados/Final' + obtenerNArchivo()
        cv2.imwrite(refinal, orig)
        construirPDF(refinal)
        cv2.waitKey(0)
def construirPDF(img):
    #Tamaño carta
    anchoCarta,altoCarta=letter
    Titulo="Reporte"
    Mreal="Medida real"
    Mcalculado="Medida cálculado"
    HMinima="Grosor mínimo: "
    HMaxima = "Grosor máximo: "
    DMinima = "Diámetro mínimo: "
    DMaximo = "Diámetro máximo: "
    wImagen=440
    hImagen=320
    x0=50
    x1=(anchoCarta-len(Titulo))/2
    x3=300
    y1=50
    TxtSeparacion=30
    doc='./Resultados/Documento'+datetime.today().strftime('%y%m%d%H%M')+'.pdf'
    documento=canvas.Canvas(doc, pagesize=letter)
    documento.drawString(x1, altoCarta-y1, Titulo)

    documento.drawImage(img,(anchoCarta-wImagen)/2,altoCarta-wImagen,width=wImagen,height=hImagen)

    # Reporte de la parte calculada
    documento.drawString(x0, altoCarta - y1 - wImagen - TxtSeparacion, Mcalculado)
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*2, HMinima)
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*3, HMaxima)
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*4, DMinima)
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*5, DMaximo)

    #Reporte de la medida de comparación
    documento.drawString(x3, altoCarta - y1 - wImagen - TxtSeparacion, Mreal)
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*2, HMinima)
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*3, HMaxima)
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*4, DMinima)
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*5, DMaximo)
#Salva el documento
    documento.save()
    #abrir el navegador
   # webbrowser.open_new(doc)

def construirEntorno():
    menu = Menu(root)
    root.config(menu=menu)
    root.geometry(Vmadre)
    root.title("Análisis de imagenes")
    #Genera los menus de la aplicación
    amenu = Menu(menu)
    menu.add_cascade(label='Archivo', menu=amenu)
    amenu.add_command(label='Capturar...',command=capturarImagen)
    amenu.add_command(label='Abrir...', command=abrirArchivo)
    amenu.add_separator()
    amenu.add_command(label='Salir', command=root.quit)
    procesarmenu = Menu(menu)
    menu.add_cascade(label='Procesar', menu=procesarmenu)
    procesarmenu.add_command(label='Medir',command=procesarImagen)
    procesarmenu.add_command(label='Cambiar de cámara',command=cambioDeCamara)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Ayuda', menu=helpmenu)
    helpmenu.add_command(label='Acerca de ..')


    menu.mainloop()


construirEntorno()

