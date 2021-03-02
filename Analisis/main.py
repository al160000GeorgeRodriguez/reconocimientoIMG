from tkinter.filedialog import askopenfile

from scipy.spatial import distance as dist
import imutils
from imutils import contours
from imutils import perspective
import numpy as np
import argparse
import imutils
import cv2
from tkinter import filedialog

from tkinter import *
import os
# Función para calcular el punto medio de dos coordenadas
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
# La función permite interactuar con un cuadro de dialogo para abrir una imagen
def abrirArchivo():
    archivoImagen=filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccione la imagen",filetypes=(("Archivos jpg","*.jpg"),("Todos los archivos","*.*")))
    miImagen=cv2.imread(archivoImagen)
    #cv2.imshow("Imagen",miImagen)
    # Se convierte en  gris la imagen y se desenfoca
    imGris=cv2.cvtColor(miImagen,cv2.COLOR_BGR2GRAY)
    imGris=cv2.GaussianBlur(imGris,(7,7),0)
   # cv2.imshow("Imagen Gris",imGris)
    #
    imBorde=cv2.Canny(imGris,50,100)
   # cv2.imshow("Imagen Canny",imBorde)


    imBorde = cv2.dilate(imBorde, None, iterations=2)
    cv2.imshow("Imagen dilate", imBorde)
    imBorde = cv2.erode(imBorde, None, iterations=2)
    cv2.imshow("Imagen erode",imBorde)
    cnts = cv2.findContours(imBorde.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("Imagen contono1", cnts)
    cnts = imutils.grab_contours(cnts)
    cv2.imshow("Imagen contorno fino",cnts)
def construirEntorno():
    root = Tk()
    menu = Menu(root)
    root.config(menu=menu)
    root.geometry("800x600")
    root.title("Análisis de imagenes")
    amenu = Menu(menu)
    menu.add_cascade(label='Archivo', menu=amenu)
    amenu.add_command(label='Nuevo')
    amenu.add_command(label='Abrir...',command=abrirArchivo)
    amenu.add_separator()
    amenu.add_command(label='Salir', command=root.quit)
    helpmenu = Menu(menu)
    menu.add_cascade(label='Ayuda', menu=helpmenu)
    helpmenu.add_command(label='Acerca de ..')
    menu.mainloop()
construirEntorno()







