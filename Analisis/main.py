from tkinter.filedialog import askopenfile

from scipy.spatial import distance as dist
import imutils
from imutils import contours
from imutils import perspective
import numpy as np
import argparse
import imutils
import cv2
from tkinter import *

from PIL import ImageTk, Image as IMG

import os



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
def capturarImagen():
     video=cv2.VideoCapture(1)

     aux,captura=video.read()

     if aux==True:

         cv2.imwrite("Foto.jpg",captura)
         print("Ok ")

     cv2.imshow("foto", captura)
     video.release()

def abrirArchivo():
    global imagen
    imagen=filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccione la imagen",
                                           filetypes=(("Archivos jpg", "*.jpg"), ("Todos los archivos", "*.*")))
    img=Toplevel(root)
    img.title(imagen)
    img.geometry(Vhija)
    miImagen = cv2.imread(imagen)
    miImagen=cv2.cvtColor(miImagen,cv2.COLOR_BGR2RGB)
    miImagen=IMG.fromarray(miImagen)
    miImagen=ImageTk.PhotoImage(miImagen)
    pic=Label(img,image=miImagen)
    pic.image=miImagen
    pic.pack(side="left")

def procesarImagen():
    miImagen = cv2.imread(imagen)
    # cv2.imshow("Imagen",miImagen)
    # Se convierte en  gris la imagen y se desenfoca
    imGris = cv2.cvtColor(miImagen, cv2.COLOR_BGR2GRAY)
    imGris = cv2.GaussianBlur(imGris, (7, 7), 0)
    # cv2.imshow("Imagen Gris",imGris)
    imBorde = cv2.Canny(imGris, 50, 100)
    # cv2.imshow("Imagen Canny",imBorde)

    imBorde = cv2.dilate(imBorde, None, iterations=1)
    cv2.imshow("Imagen dilate", imBorde)
    imBorde = cv2.erode(imBorde, None, iterations=1)
    cv2.imshow("Imagen erode", imBorde)
    cnts = cv2.findContours(imBorde.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("Imagen contorno1", cnts)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("Imagen contorno fino", cnts)
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    orig = image.copy()
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
            continue
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        #cv2.imwrite('./Results/ref2.jpg', cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2))
        cv2.imshow("puntos de imagen", box)

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

    helpmenu = Menu(menu)
    menu.add_cascade(label='Ayuda', menu=helpmenu)
    helpmenu.add_command(label='Acerca de ..')


    menu.mainloop()


construirEntorno()

