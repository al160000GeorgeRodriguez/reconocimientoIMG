from tkinter.filedialog import askopenfile
from reportlab.pdfgen import canvas
from tkinter import Canvas
import webbrowser
from reportlab.lib.pagesizes import letter
from scipy.spatial import distance as dist
import imutils
from imutils import contours
from imutils import perspective
import numpy as np
import argparse 
import imutils
from time import time
import cv2
from tkinter import *
from datetime import datetime
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from PIL import ImageTk, Image as IMG

import os

global lblImagen
#Convierte el formato de video opencv al entorno TK
def convertirTk(miImagen):
    laImagen = cv2.cvtColor(miImagen, cv2.COLOR_BGR2RGB)
    laImagen = IMG.fromarray(laImagen)
    return ImageTk.PhotoImage(image=laImagen)

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
tiempoCaptura=0.0
tiempoProcesamiento = 0.0
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
# medidas de la pantalla
global alto
alto = 1024
global ancho
ancho=800
global calibracion2mmP1
global calibracion2mmP2
global longitud
longitud = 310

calibracion2mmP1 = int(ancho / 1.2)
calibracion2mmP2 = int(ancho / 3.3)



def capturarImagen():
    global camara, alto, ancho, tiempoCaptura
    tiempoCaptura=time()
    def back():
        video = cv2.VideoCapture(1)
    video=cv2.VideoCapture(1)

    ubicacionX = int( alto / 6)
    ubicacionY = int(ancho / 10)
    diferencia = int(ancho / 10 - ancho / 11)
    # (int(alto / 3) + int(alto / 2)+ int(alto / 4)
    puntoUno = (calibracion2mmP1 - longitud - 250, ubicacionY - diferencia)
    puntoDos = (calibracion2mmP2 + longitud - 250, ubicacionY)
    colorRectangulo = (0, 0, 0)
    #longitud de la líneas del objetivo



   # imgx = Toplevel(root)
    #btnCapturar = Button(imgx, text="Capturar", width=10)
    #btnCapturar.grid(column=0, row=0, padx=3, pady=5)
    #imgx.title("Captura...")
    #imgx.geometry(Vhija)
    #lblIma = Label(imgx)
    global imagen
    while(True):
        aux,captura=video.read()
       # if aux==True:
        #
         #   print("Ok ")
        if cv2.waitKey(1) & 0xFF == ord('x'):
            nombrearch = fd.asksaveasfilename(initialdir="./Prueba/", title="Guardar como",filetypes=(("Archivos *.jpg", "*.jpg"), ("todos los archivos", "*.*")))
            if nombrearch != '':
                lblImagen =nombrearch+".jpg"
                cv2.imwrite(lblImagen, captura)
                imagen=lblImagen
                mb.showinfo("Información", "¡La imagen se guardó correctamente!")
                pImagenTK(lblImagen)
                break

        #height,ancho=cv2.getWindowImageRect(captura)

        resolucion=convertirTk(captura)
        alto=resolucion.height()*2.75
        ancho=resolucion.width()*1.5
        # Línea horizontal
        cv2.line(captura,(int(alto/2)-longitud,int(ancho/2)),(int(alto/2)+longitud,int(ancho/2)),(0,0,255),1,1,1)
        # Línea vertical
        cv2.line(captura,(int(alto/2),int(ancho/2)-longitud),(int(alto/2),int(ancho/2)+longitud),(0,0,255),1,1,1)

        cv2.rectangle(captura, puntoUno, puntoDos, colorRectangulo, 2, 1, 1)

        # Línea de referencia
       # cv2.line(captura, (int(alto / 3)+int(alto / 2), int(ancho / 1.3) - longitud), (int(alto / 3)+int(alto / 2), int(ancho / 3.2) + longitud),
        #         (255,0 , 0), 1, 1, 1)
        #cv2.line(captura, (int(alto / 3) + int(alto / 2), calibracion2mmP1 - longitud),
        #         (int(alto / 3) + int(alto / 2), calibracion2mmP2 + longitud),
        #         (128, 0, 0), 1, 1, 1)
                #cv2.circle(captura,(300,240),100,(127,127,127),8)
        #cImagenTK(captura)

        cv2.imshow("Presione x para capturar", captura)
       # btnAbrir = Button(img, text="Abrir", width=10, command=abrirArchivo)
        #btnAbrir.grid(column=0, row=0, padx=3, pady=5)
        #lblIma.configure(image=resolucion)

        #lblIma.image = resolucion
        #lblIma.grid(column=0, row=1)
        #btnCapturar = Button(img, text="Procesar", width=10, command=procesarImagen)
        #btnCapturar.grid(column=2, row=0, padx=3, pady=5)
        #cv2.createButton("Back",back,None,cv2.QT_PUSH_BUTTON,0)

    video.release()
    cv2.destroyWindow("Presione x para capturar")
    tiempoCaptura=time()-tiempoCaptura


#Convierte el formato opencv a TK por medio de un path
def pImagenTK(uImg):
    miImagen = cv2.imread(uImg)
    img=Toplevel(root)
    img.title(uImg)
    img.geometry(Vhija)
    tImagen=convertirTk(miImagen)
    lblImagen = Label(img)
    lblImagen.configure(image=tImagen)
    lblImagen.image=tImagen
    lblImagen.pack(side="left")
        #lblImagen.grid(column=0, row=1)

    #pic=Label(img)
    #pic.image=tImagen
    #pic.pack(side="left")

def abrirArchivo():
    global imagen
    imagen=filedialog.askopenfilename(initialdir=os.getcwd()+"/Prueba", title="Seleccione la imagen", filetypes=(("Archivos jpg", "*.jpg"), ("Todos los archivos", "*.*")))
    if imagen != '':
        pImagenTK(imagen)
    else:
        mb.showinfo("Información", "¡No ha seleccionado archivo!")


def obtenerNArchivo():
    ref = os.path.split(imagen)
    return ref[1]

def truncate(num,n):
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            try:
                return float(temp[:x+n+1])
            except:
                return float(temp)
    return float(temp)


def dibujarLineas(tltrX, tltrY,blbrX, blbrY,tlblX, tlblY, trbrX, trbrY, unaImagen):
    tamCirc=3
    # Dibuja los puntos medios entre los rectangulos
    cv2.circle(unaImagen, (int(tltrX), int(tltrY)), tamCirc, (255, 0, 0), -1)
    cv2.circle(unaImagen, (int(blbrX), int(blbrY)), tamCirc, (255, 0, 0), -1)
    cv2.circle(unaImagen, (int(tlblX), int(tlblY)), tamCirc, (255, 0, 0), -1)
    cv2.circle(unaImagen, (int(trbrX), int(trbrY)), tamCirc, (255, 0, 0), -1)
    # Dibuja las lineas entre los puntos medios

    cv2.line(unaImagen, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
             (255, 0, 255), 2)
    cv2.line(unaImagen, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
             (255, 0, 255), 2)
    return unaImagen
def sel():
   selection = "You selected the option " + str(var.get())
   labx.config(text = selection)
def opciones():
    op=Toplevel(root)
    op.title("Tipo de cable")
    op.geometry("240x320")
    var = IntVar()
    
    R1 = Radiobutton(op, text="TW", variable=var, value=1, command=sel)
    R1.pack(side="left")
    R2 = Radiobutton(op, text="THW", variable=var, value=2, command=sel)
    R2.pack(side="left")
    R3 = Radiobutton(op, text="Option 3", variable=var, value=3, command=sel)
    R3.pack(side="left")
    labx = Label(op)
    root.update()

def procesarImagen():
    global tiempoProcesamiento
    opciones()
    tiempoProcesamiento=time()
    miImagen = cv2.imread(imagen)
    ubicacionX=int(alto / 6)
    ubicacionY=int(ancho/10)
    diferencia=int(ancho/10-ancho/11)
    #(int(alto / 3) + int(alto / 2)+ int(alto / 4)
    puntoUno=(calibracion2mmP1 - longitud-250 , ubicacionY-diferencia)
    puntoDos=(calibracion2mmP2 + longitud-250, ubicacionY)
    #puntoUno=(ubicacionX ,calibracion2mmP1 - longitud )
    #puntoDos=(ubicacionX, calibracion2mmP2 + longitud)
    colorRectangulo=(0,0,0)
    cv2.rectangle(miImagen,puntoUno,puntoDos,colorRectangulo, 2, 1, 1)
    #cv2.line(miImagen,puntoUno,puntoDos,colorRectangulo, 2, 1, 1)
    # Se convierte en  gris la imagen y se desenfoca
    imGris = cv2.cvtColor(miImagen, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Imagen en gris",imGris)
    imGris = cv2.GaussianBlur(imGris, (7, 7), 0)
    #El desenfoque elimina el ruido proveniente de la camara y requisito previo para Canny
    #   cv2.imshow("Imagen Gris",imGris)

    imBorde = cv2.Canny(imGris, 50, 100)

    #cv2.imshow("Imagen Canny",imBorde)

    imBorde = cv2.dilate(imBorde, None, iterations=1)
    #cv2.imshow("Imagen dilate", imBorde)
    imBorde = cv2.erode(imBorde, None, iterations=1)
    #cv2.imshow("Imagen erode", imBorde)

    cnts = cv2.findContours(imBorde.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    #cv2.imshow("Imagen contorno1", cnts)
    cnts = imutils.grab_contours(cnts)
    #laImagen=cv2.drawContours(miImagen,cnts,-1,(0,255,0),2)
    #cv2.imshow("contorno",laImagen)


    #cv2.imshow("Imagen contorno fino", cnts)
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    orig = miImagen.copy()
    orig2= miImagen.copy()
    colLong1=(0, 50, 0)
    colText1=(125,250,250)
    iteraciones=0
    iteraciones2=0
    ultimodimA=0
    ultimodimB=0
    LMuestra=1.1
    listaDeResultados=[0]*50
    for c in cnts:
        iteraciones=iteraciones+1
        #Si el area es pequeña no se considera
        #print("Contorno: ",cv2.contourArea(c))
        if cv2.contourArea(c) < 100:
            continue
        #se obtiene el área
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)

        box = np.array(box, dtype="int")

        box = perspective.order_points(box)
        #Se dibujan rectangulos alrededor de las imagenes de interes
        cv2.drawContours(orig, [box.astype("int")], -1, colLong1, 2)
        #Se guarda la imagen
        #cv2.imshow("imagen artificial", orig)
        ref2 = './Resultados/ref2'+obtenerNArchivo()
        cv2.imwrite(ref2,orig)
        #cv2.imwrite(ref2, cv2.drawContours(orig, [box.astype("int")], -1, (0, 128, 255), 2))
        #for (x, y) in box:
            #cv2.circle(orig, (int(x), int(y)), 2, (0, 0, 255), -1)

        # se desempacan los puntos de la caja
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = puntoMedio(tl, tr)
        (blbrX, blbrY) = puntoMedio(bl, br)
        #Se calculan los puntos medio de arriba a abajo y de arriba a derecha

        (tlblX, tlblY) = puntoMedio(tl, bl)
        (trbrX, trbrY) = puntoMedio(tr, br)

        orig=dibujarLineas(tltrX, tltrY,blbrX, blbrY,tlblX, tlblY, trbrX, trbrY, orig)

        ref3='./Resultados/ref3'+obtenerNArchivo()
        cv2.imwrite(ref3, orig)
        #cv2.imshow("puntos de imagen 2", orig)
        # Se muestra la distancia euclidiana
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # Se le asigna la muestra
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / LMuestra

        # compute the size of the object
        dimA =truncate(dA / pixelsPerMetric,1)
        dimB = truncate(dB / pixelsPerMetric,1)

        # Se dibujan las medidas y las lineas correspondientes
        if (iteraciones>1) and (dimA != dimB) and (ultimodimA != dimA) and (ultimodimA != dimB):
            orig2 = dibujarLineas(tltrX, tltrY, blbrX, blbrY, tlblX, tlblY, trbrX, trbrY, orig2)
            cv2.putText(orig2,"{:.1f}mm".format(dimA),
                    (int(tltrX) , int(tltrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, colText1, 1)
            listaDeResultados[iteraciones2]=dimA
            iteraciones2 = iteraciones2 + 1
        #str(iteraciones) + " " +
        if (ultimodimB != dimB) and (ultimodimB != dimA):
            orig2 = dibujarLineas(tltrX, tltrY, blbrX, blbrY, tlblX, tlblY, trbrX, trbrY, orig2)
            cv2.putText(orig2,"{:.1f}mm".format(dimB),
                    (int(trbrX), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, colText1, 1)
            listaDeResultados[iteraciones2]=dimB
            iteraciones2 = iteraciones2 + 1
        #str(iteraciones) + " " +
        #print(iteraciones," dimA == dimB ",dimA,dimA == dimB,dimB)
        #print(iteraciones," ultimodimB == dimB",ultimodimB,ultimodimB == dimB,dimB)
        #print(iteraciones," ultimodimA == dimA",ultimodimA,ultimodimA == dimA,dimA)

        #cv2.putText(orig,str(iteraciones)+"  "+"{:.1f}mm".format(dimB/2),(int(tltrX) , int(tltrY)+30), cv2.FONT_HERSHEY_SIMPLEX,0.5, colText1, 2)
        ultimodimA=dimA
        ultimodimB=dimB


        # show the output image
        # cv2.imshow("Image", orig)
        refinal='./Resultados/Final' + obtenerNArchivo()
        cv2.imwrite(refinal, orig2)
        #cv2.imshow("puntos de imagen Final "+str(iteraciones), orig)
        #cv2.waitKey(0)
        #construirCanva()
    #cv2.imshow("puntos de imagen Final", orig)
    cv2.imshow("Puntos de imagen final ",orig2)
    listaDeRes=sorted(listaDeResultados,reverse= True)
    print(listaDeRes)
    tiempoProcesamiento = time() - tiempoProcesamiento
    print(tiempoProcesamiento)
    construirPDF(listaDeRes)


def retirarExtension(archivoI):
    arc = archivoI.split(sep=".", maxsplit=2)
    return arc[0]

#Tamaño carta
global anchoCarta,altoCarta,Titulo, Mreal,Mcalculado,HMinima,HMaxima,DMinima,DMaximo,wImagen,hImagen,x0,x1,x3,y1, TxtSeparacion
anchoCarta,altoCarta=letter
Titulo="Reporte"
Mreal="Medida real"
Mcalculado="Medida cálculado "
HMinima=   "Grosor mínimo:   "
HMaxima =  "Grosor máximo:   "
DMinima =  "Diámetro mínimo: "
DMaximo =  "Diámetro máximo: "
wImagen=440
hImagen=320
x0=50
x1=(anchoCarta-len(Titulo))/2
x3=300
y1=50
TxtSeparacion=30
def construirCanva():
    imgy=Toplevel(root)
    imgy.title("Resultado")
    #imgy.geometry(Vhija)
    res = Label(imgy)
    Midocumento = Canvas(res, width=640,height=480)
    Midocumento.create_text(x1, altoCarta-y1,font=("Purisa",12), text=Titulo)
    Midocumento.pack()


def construirPDF(Mimg):
    #Tamaño carta
    anchoCarta,altoCarta=letter
    Titulo="Reporte"
    Mreal="Medida real"
    Mcalculado="Medida cálculado "
    HMinima=   "Grosor mínimo:   "
    HMaxima =  "Grosor máximo:   "
    DMinima =  "Diámetro mínimo: "
    DMaximo =  "Diámetro máximo: "
    tCaptura="Tiempo de captura: "
    tProcesamiento="Tiempo de procesamiento: "
    wImagen=440
    hImagen=320
    x0=50
    x1=(anchoCarta-len(Titulo))/2
    x3=300
    y1=50
    y2=250
    TxtSeparacion=30
    dk=0
    nimagen =retirarExtension(obtenerNArchivo())
    if (nimagen[0]!="#"):
        HMi=0.0
        HMa=0.0
        DMi=0.0
        DMa=0.0
    else:
        print(nimagen[7:10])
        HMi=float(nimagen[7:10])/100

        HMa=float(nimagen[3:6])/100
        DMi=float(nimagen[15:18])/100
        DMa=float(nimagen[11:14])/100

    HMiX=(Mimg[0]-Mimg[1])/2
    HMaX=(Mimg[0]-Mimg[2])/2
    DMiX=Mimg[0]
    DMaX=Mimg[0]

    doc='./Resultados/Documento'+datetime.today().strftime('%y%m%d%H%M')+'.pdf'


    #lblImagen.pack(side="left")
    #res.grid(column=0, row=1)
    documento=canvas.Canvas(doc, pagesize=letter)

    documento.drawString(x1, altoCarta-y1, Titulo)

    documento.drawImage(os.getcwd()+"/Resultados/Final"+ obtenerNArchivo(),(anchoCarta-wImagen)/2,altoCarta-wImagen,width=wImagen,height=hImagen)
    #print(Mimg)

    # Reporte de la parte calculada
    documento.drawString(x0, altoCarta - y1 - wImagen - TxtSeparacion, Mcalculado)
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*2, HMinima+"{:.1f} mm".format(HMiX))
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*3, HMaxima+"{:.1f} mm".format(HMaX))
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*4, DMinima+str(DMiX)+" mm")
    documento.drawString(x0, altoCarta-y1-wImagen-TxtSeparacion*5, DMaximo+str(DMaX)+" mm")

    #Reporte de la medida de comparación

    documento.drawString(x3, altoCarta - y1 - wImagen - TxtSeparacion, Mreal)
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*2, HMinima+str(HMi)+" mm")
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*3, HMaxima+str(HMa)+" mm")
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*4, DMinima+str(DMi)+" mm")
    documento.drawString(x3, altoCarta-y1-wImagen-TxtSeparacion*5, DMaximo+str(DMa)+" mm")

    # Tiempo de procesamiento y captura

    documento.drawString(x0, altoCarta-y2-wImagen-TxtSeparacion*1, tCaptura+"{:.2f} segundos".format(tiempoCaptura))
    documento.drawString(x0, altoCarta-y2-wImagen-TxtSeparacion*2, tProcesamiento+"{:.2f} segundos".format(tiempoProcesamiento))

    #Salva el documento
    documento.showPage()
    documento.save()

    #abrir el navegador
   # webbrowser.open_new(doc)
def cerrarTodo():
    cv2.destroyAllWindows()


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
    amenu.add_command(label='Cerrar todo', command=cerrarTodo)
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

