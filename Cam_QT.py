import os
import time
from time import sleep
import numpy as np

from PyQt5 import QtWidgets, QtGui, QtCore, uic
import matplotlib
#from matplotlib import pyplot as plt
#import RPi.GPIO as gpio
#import cv2
       
def mkdir():
    directory = ["Imagen" , "Video"]
    # Parent Directory path
    for i in directory:
        print(i)
        parent_dir = "/home/grupo2/Documentos"
        path = os.path.join(parent_dir, i)
        os.mkdir(path)
        print("Directory '% s' created" % directory)
    
        
def take_foto():
    c = time.strftime("%d-%m-%y") 
    f = time.strftime("%H-%M-%S")
    aux_foto=0
    cam = cv2.VideoCapture(0)
    while True:
        ret, image = cam.read()
        cv2.imshow('Fotoka',image)
        if cv2.waitKey(1) & 0xFF & gpio.input(8) == gpio.HIGH:
        #if k != -1:
            break
    cv2.imwrite('/home/grupo2/Documentos/Imagen/Img_' + str(aux_foto) + str(c) +"_"+ str(f)+'.jpg', image)
    cam.release()
    cv2.destroyAllWindows()
    aux_foto= aux_foto+1

def take_video():
    c = time.strftime("%d-%m-%y") 
    f = time.strftime("%H-%M-%S")
    cam = cv2.VideoCapture(0)
    salida = cv2.VideoWriter('/home/grupo2/Documentos/Video/Video_' + str(aux_video) + str(c) +"_"+ str(f)+'.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
    while (cam.isOpened()):
        ret, imagen = cam.read()
        if ret == True:
            cv2.imshow('video',imagen)
            salida.write(imagen)
            if cv2.waitKey(1) & 0xFF & gpio.input(10) == gpio.HIGH:
                sleep(5)
            #if k != -1:
                break
        else: break
    #cv2.imwrite('/home/grupo2/Documentos/Video/test.avi', imagen)
    cam.release()
    salida.release()
    cv2.destroyAllWindows()

################################## ADD QT
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as nvt
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes_1 = self.fig.add_subplot(211)
        self.axes_2 = self.fig.add_subplot(212)
        self.fig.tight_layout(pad=5)
        super(MplCanvas, self).__init__(self.fig)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.window = uic.loadUi("interfazCam.ui", self)

        self.plot = MplCanvas(self,width=10, height=6)
        self.window.graph.addWidget(nvt(self.plot, self))
        self.window.graph.addWidget(self.plot)
        self.window.img_cont.setPixmap(QtGui.QPixmap("NAME_FORT"))
        print("Bienvenido!")
        self.window.take_picture.clicked.connect(self.take_picture)
        self.window.fotor.clicked.connect(self.fotor)
        self.flag_conectar = 0
        self.window.tabWidget.setCurrentIndex(0)

        self.index = 0
    def fotor():
        self.r = 1
    def take_picture(self):
        self.r = 0
        take_foto(r)
        try:
            if not self.flag_conectar:
                self.serialPort.setPort(str(self.window.puertos.currentText()))
                self.serialPort.open()
                self.window.ConnectArduino.setText("Disconnect")
                print("Puerto serial activado")
                self.flag_conectar = 1
                self.setTimer()
                
            else:
                self.serialPort.close()
                self.window.ConnectArduino.setText("Connect")
                print("Puerto serial desactivado")
                self.flag_conectar = 0
                self.timer_1.stop()  
                self.timer_2.stop()
                self.timer_3.stop()
        except Exception as e:
            print("error en la funcion conectar")
            print(e)
 
##################################
mkdir()
while(1):

##################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



# TAREA 2
#- La interfaz al iniciar deberá solicitar un usuario y contraseña, estos deberán estar contenidos 
#  en una tabla de una base de datos MySQL llamada usuarios Al ingresar un usuario y 
#  contraseña invalida deberá entregar un mensaje de error. 

#- La interfaz deberá tener 2 contenedores, el primero llamado Adquisición de fotos y la 
#  segundo Adquisición de video.

#- La pestaña de Adquisición de fotos deberá solicitar una cabecera de nombre para las fotos. 
#  Al apretar el boto de la interfaz el sistema deberá tomar una foto, guardar con el nombre 
#  de la cabecera y un contador. Además, se deberá agregar en una tabla de la BD llamada 
#  Log_Camara el usuario que tomo la foto, la cantidad de fotos que se llevan tomadas, el 
#  y el timestamp. Además, la interfaz deberá mostrar la cantidad de fotos 
#  totales tomadas y las de la sesión. Cuando se aprete el botón de la toma de foto la interfaz 
#  deberá encender un “Led digital”.

#- La pestaña de Adquisición de video deberá solicitar una cabecera de nombre para los videos. 
#  Al apretar el boto de la interfaz el sistema deberá tomar empezar a adquirir video, guardar 
#  con el nombre de la cabecera y un contador. Además, se deberá agregar en una tabla de la 
#  BD llamada Log_video el usuario que tomo el video, la cantidad de videos adquiridos, el 
#  nombre del video, la duración del video y el timestamp. Además, la interfaz deberá mostrar 
#  la cantidad de videos totales y las de la sesión. Cuando se aprete el botón de la adquirir 
#  video la interfaz deberá encender un “Led digital” que deberá hacer un blink mientras se 
#  adquiera el video, esta adquisición deberá ser interrumpida con un botón de stop.

#- Todos los códigos asociados deberán estar ingresados a un Github Publico






# TAREA 1
# Diseñar un sistema de captura de imagenes y video con las siguientes caracteristicas:
    # (i) El sistema debe contar con 2 botones, el primero debe ser capaz de que el sistema tome una foto a traves de una 
    # webcam conectada a 
    # las raspberry. El segundo boton debe dar inicio y fin a la toma de video 
    # (ii) Al arrancar el codigo el sistema debe prender el led, luego mientras el sistema este tomando la foto y 
    # el video el led debe estar ralizando un blink, al terminar el proceso el led se debe mantener endencido
    # (iii) Las imagenes y videos se deben guardar en carpetas diferentes, creadas por el mismo codigo, el nombre de estas 
    # carpeta es "Imagenes y  "Videos"
    # cada imagen y video debe ser guardado con el nombre img_n_d, siendo n la canditada de fotos guardas en la carpeta y d la 
    # fecha en la cual se tomo
    # analogamente los videos seran guardados como video_n_d
    #