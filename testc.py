# -*- coding: utf-8 -*-
import random
from itertools import count
from tkinter import Y, ttk
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter import messagebox
import os
import threading

import pandas as pd
from tkinter.constants import CENTER, INSERT, LEFT
import matplotlib.pyplot as plt
from matplotlib import style 
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from measureProcessPath import *

import numpy as np
# import scipy as sc




HEIGHT=650
WIDTH=700
STRINGDIMENSION = str(WIDTH) + "x" + str(HEIGHT)

def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

Font_tuple_title = ("Courier", 20, "bold")
Font_tuple_sublabel = ("Courier", 10)
Font_tuple_botton = ("Courier", 9)


style.use('ggplot')
fig = Figure(figsize=(12,5), dpi=60)
ax = fig.add_subplot(111)
# self.globalpath = ""


class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("PW1710 medition")
        main_window.geometry(STRINGDIMENSION)

        self.nb = ttk.Notebook(main_window)

        self.meditionTab = ttk.Frame(self.nb)
        self.graphicsTab = ttk.Frame(self.nb)

        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=Font_tuple_sublabel, padding=[5, 5], background="white")

        self.nb.add(self.meditionTab, text=' Carga de Datos ')
        self.nb.add(self.graphicsTab, text='     Gráfico     ')
        self.nb.place( x=0, y=0, width=WIDTH, height=HEIGHT)

        self.title = tk.Label(self.meditionTab, text="PW1710 RX", font = Font_tuple_title, bg="yellow")
        self.title.place(x=34, y=29, width=700-34*2, height=29)

# Build the possibility of select numbers of different medition

        self.meditionNdeInter = tk.Label(self.meditionTab, text="N de intervalos", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.meditionNdeInter.place(x=34, y=87, width=150, height=29)
        
        self.comboExample = ttk.Combobox(self.meditionTab, 
                            values=[ "1", "2", "3", "4", "5"], justify="center")
        self.comboExample.place(x=200, y=87, width=185, height=29)
        
        self.loadData = tk.Button(self.meditionTab, text="Carga datos", font=Font_tuple_botton, borderwidth="5", command=self.appearloadmedition)
        self.loadData.place(x=350+34+15, y=87, width=150, height=29)


# Build the possibility of select a directory to save the file

        self.scrollbar = tk.Scrollbar(self.meditionTab)
        self.scrollbar.place(x=34, y=87+15+29, width=350, height=29)

        self.textBar = tk.Text(self.meditionTab, yscrollcommand=self.scrollbar.set)
        self.textBar.place(x=34, y=87+15+29, width=350, height=29)

        self.scrollbar.config(command=self.textBar.yview)


        self.loadData = tk.Button(self.meditionTab, text="Selecionar carpeta", font=Font_tuple_botton, borderwidth="5", command=self.folderBrowse)
        self.loadData.place(x=350+34+15, y=87+15+29, width=150, height=29)

# Build the possibility of put the name of the file
        self.signnameOfFile = tk.Label(self.meditionTab, text="Nombre de Archivo", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.signnameOfFile.place(x=34, y=131+15+29, width=150, height=29)

        valueDefault = StringVar(self.meditionTab, value = "archivoPrueba.txt")
        self.nameOfFile = tk.Entry(self.meditionTab,font=Font_tuple_sublabel, fg=from_rgb((0,10,20)), bg="white", textvariable=valueDefault, justify="center" )
        self.nameOfFile.place(x=34+150+15, y=131+15+29, width=185, height=29)


# Build the first column of a medition table
        self.c1_initialangle = tk.Label(self.meditionTab, text="° incial", wraplength=100, font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.c1_initialangle.place(x=200, y=175+15+29, width=95, height=39)

        self.c2_finalangle = tk.Label(self.meditionTab, text="° final", wraplength=100, font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.c2_finalangle.place(x=324, y=175+15+29, width=95, height=39)

        self.c3_finalangle = tk.Label(self.meditionTab, text="paso - min 0.001", wraplength=100,font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.c3_finalangle.place(x=448, y=175+15+29, width=95, height=39)

        self.c4_finalangle = tk.Label(self.meditionTab, text="tiempo por paso", wraplength=100, font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.c4_finalangle.place(x=572, y=175+15+29, width=95, height=39)

        self.stringPath = r""
        self.place(width=WIDTH, height=HEIGHT)

        Fig = Figure(figsize=(12,5), dpi=60)
        FigSubPlot = Fig.add_subplot(111)
        self.x = []
        self.y = []
        self.count = 0
        self.line1, = FigSubPlot.plot(self.x,self.y,"r-")
        self.canvas = FigureCanvasTkAgg(Fig, master = self.graphicsTab)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        self.update()

    def refreshFigure(self,x,y):
        self.line1.set_data(x,y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())
        self.canvas.draw()


    def folderBrowse(self):
        self.folder_path = StringVar()
        self.filename = filedialog.askdirectory()
        self.folder_path.set(self.filename)
        self.stringPath = self.stringPath + self.filename
        # Change label contents
        self.textBar.insert(tk.INSERT,self.filename)
        # print(self.textBar.get("1.0", 'end-1c'), self.nameOfFile.get())

    def appearloadmedition(self):
        
        self.destroyLabels()

        if(self.comboExample.get() == ""):
            messagebox.showinfo('Message', "Elegir una opción válida")
        else:
            self.amountOfMedition = int(self.comboExample.get())
            if(self.amountOfMedition == 1):
                self.firstmedition()
                self.heightCanceledButton = 273+(15+29)*2
                self.meditionButton = tk.Button(self.meditionTab, text="Empezar medición", font=Font_tuple_botton, borderwidth="5", command=self.saveValues)
                # self.meditionButton.place(x= (WIDTH-130)/2,y=273+15+29, width=130, height=29)
                self.meditionButton.place(x= (WIDTH-130)/2,y=273+15+29, width=130, height=29)
            elif (self.amountOfMedition == 2):
                self.heightCanceledButton = 273+(15+29)*3
                self.firstmedition()
                self.secondmedition()
                self.meditionButton = tk.Button(self.meditionTab, text="Empezar medición", font=Font_tuple_botton, borderwidth="5", command=self.saveValues)
                self.meditionButton.place(x= (WIDTH-130)/2,y=273+(15+29)*2, width=130, height=29)
            elif (self.amountOfMedition == 3):
                self.heightCanceledButton = 273+(15+29)*4
                self.firstmedition()
                self.secondmedition()
                self.thirdmedition()
                self.meditionButton = tk.Button(self.meditionTab, text="Empezar medición", font=Font_tuple_botton, borderwidth="5", command=self.saveValues)
                self.meditionButton.place(x= (WIDTH-130)/2,y=273+(15+29)*3, width=130, height=29)
            elif (self.amountOfMedition == 4 ):
                self.heightCanceledButton = 273+(15+29)*5
                self.firstmedition()
                self.secondmedition()
                self.thirdmedition()
                self.fourthmedition()
                self.meditionButton = tk.Button(self.meditionTab, text="Empezar medición", font=Font_tuple_botton, borderwidth="5", command=self.saveValues)
                self.meditionButton.place(x= (WIDTH-130)/2,y=273+(15+29)*4, width=130, height=29)
            elif (self.amountOfMedition == 5 ):
                self.heightCanceledButton = 273+(15+29)*6
                self.firstmedition()
                self.secondmedition()
                self.thirdmedition()
                self.fourthmedition()
                self.fifthmedition()
                self.meditionButton = tk.Button(self.meditionTab, text="Empezar medición", font=Font_tuple_botton, borderwidth="5", command=self.saveValues)
                self.meditionButton.place(x= (WIDTH-130)/2,y=273+(15+29)*5, width=130, height=29)
    
    def destroyLabels(self):
        try:
            self.meditionButton.destroy()
        except:
            print("No pudimos destruir el boton")
        try:
            self.destroyfistmedition()
        except:
            print("No pudimos destruir la primera medición")
        try:
            self.destroysecondmedition()
        except:
            print("No pudimos destruir la segunda medición")
        try:
            self.destroythirdmedition()
        except:
            print("No pudimos destruir la tercera medición")
        try:
            self.destroyfourthmedition()
        except:
            print("No pudimos destruir la tercera medición")
        try:
            self.destroyfifthmedition()
        except:
            print("No pudimos destruir la tercera medición")

    plt.style.use('fivethirtyeight')

    def destroyfistmedition(self):
        self.labelfirstmedition.destroy()
        self.initanglefirstmedition.destroy()
        self.finalanglefirstmedition.destroy()
        self.timefirstmedition.destroy()
        self.stepsfirstmedition.destroy()

    def destroysecondmedition(self):
        self.labelsecondmedition.destroy()
        self.initanglesecondmedition.destroy()
        self.finalanglesecondmedition.destroy()
        self.timesecondmedition.destroy()
        self.stepssecondmedition.destroy()

    def destroythirdmedition(self):
        self.labelthirdmedition.destroy()
        self.initanglethirdmedition.destroy()
        self.finalanglethirdmedition.destroy()
        self.timethirdmedition.destroy()
        self.stepsthirdmedition.destroy()

    def destroyfourthmedition(self):
        self.labelfourthmedition.destroy()
        self.initanglefourthmedition.destroy()
        self.finalanglefourthmedition.destroy()
        self.timefourthmedition.destroy()
        self.stepsfourthmedition.destroy()
    
    def destroyfifthmedition(self):
        self.labelfifthmedition.destroy()
        self.initanglefifthmedition.destroy()
        self.finalanglefifthmedition.destroy()
        self.timefifthmedition.destroy()
        self.stepsfifthmedition.destroy()

    def firstmedition(self):
        self.labelfirstmedition = tk.Label(self.meditionTab, text="Primera medicion", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.labelfirstmedition.place(x=34, y=219+15+39, width=150, height=29)

        self.initanglefirstmedition = tk.Entry(self.meditionTab)
        self.initanglefirstmedition.place(x=200, y=219+15+39, width=95, height=29)
        
        self.finalanglefirstmedition = tk.Entry(self.meditionTab)
        self.finalanglefirstmedition.place(x=324, y=219+15+39, width=95, height=29)

        self.stepsfirstmedition = tk.Entry(self.meditionTab)
        self.stepsfirstmedition.place(x=448, y=219+15+39, width=95, height=29)        

        self.timefirstmedition = tk.Entry(self.meditionTab)
        self.timefirstmedition.place(x=572, y=219+15+39, width=95, height=29)

    def secondmedition(self):
        self.labelsecondmedition = tk.Label(self.meditionTab, text="Segunda medicion", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.labelsecondmedition.place(x=34, y=273+15+29, width=150, height=29)

        self.initanglesecondmedition = tk.Entry(self.meditionTab)
        self.initanglesecondmedition.place(x=200, y=273+15+29, width=95, height=29)
        
        self.finalanglesecondmedition = tk.Entry(self.meditionTab)
        self.finalanglesecondmedition.place(x=324, y=273+15+29, width=95, height=29)

        self.stepssecondmedition = tk.Entry(self.meditionTab)
        self.stepssecondmedition.place(x=448, y=273+15+29, width=95, height=29)        

        self.timesecondmedition = tk.Entry(self.meditionTab)
        self.timesecondmedition.place(x=572, y=273+15+29, width=95, height=29)

    def thirdmedition(self):
        self.labelthirdmedition = tk.Label(self.meditionTab, text="Tercera medicion", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.labelthirdmedition.place(x=34, y=317+15+29, width=150, height=29)

        self.initanglethirdmedition = tk.Entry(self.meditionTab)
        self.initanglethirdmedition.place(x=200, y=317+15+29, width=95, height=29)
        
        self.finalanglethirdmedition = tk.Entry(self.meditionTab)
        self.finalanglethirdmedition.place(x=324, y=317+15+29, width=95, height=29)

        self.stepsthirdmedition = tk.Entry(self.meditionTab)
        self.stepsthirdmedition.place(x=448, y=317+15+29, width=95, height=29)        

        self.timethirdmedition = tk.Entry(self.meditionTab)
        self.timethirdmedition.place(x=572, y=317+15+29, width=95, height=29)


    def fourthmedition(self):
        self.labelfourthmedition = tk.Label(self.meditionTab, text="Cuarta medicion", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.labelfourthmedition.place(x=34, y=361+15+29, width=150, height=29)

        self.initanglefourthmedition = tk.Entry(self.meditionTab)
        self.initanglefourthmedition.place(x=200, y=361+15+29, width=95, height=29)
        
        self.finalanglefourthmedition = tk.Entry(self.meditionTab)
        self.finalanglefourthmedition.place(x=324, y=361+15+29, width=95, height=29)

        self.stepsfourthmedition = tk.Entry(self.meditionTab)
        self.stepsfourthmedition.place(x=448, y=361+15+29, width=95, height=29)        

        self.timefourthmedition = tk.Entry(self.meditionTab)
        self.timefourthmedition.place(x=572, y=361+15+29, width=95, height=29)

    def fifthmedition(self):
        self.labelfifthmedition = tk.Label(self.meditionTab, text="Quinta medicion", font = Font_tuple_sublabel, bg=from_rgb((0,10,20)), fg="white")
        self.labelfifthmedition.place(x=34, y=405+15+29, width=150, height=29)

        self.initanglefifthmedition = tk.Entry(self.meditionTab)
        self.initanglefifthmedition.place(x=200, y=405+15+29, width=95, height=29)
        
        self.finalanglefifthmedition = tk.Entry(self.meditionTab)
        self.finalanglefifthmedition.place(x=324, y=405+15+29, width=95, height=29)

        self.stepsfifthmedition = tk.Entry(self.meditionTab)
        self.stepsfifthmedition.place(x=448, y=405+15+29, width=95, height=29)        

        self.timefifthmedition = tk.Entry(self.meditionTab)
        self.timefifthmedition.place(x=572, y=405+15+29, width=95, height=29)


    def verificationValues(self, dictMedition, loadNumber):
        for key, value in dictMedition.items():
            if(value == ""):
                messagebox.showinfo('Message', "Faltan datos en la medición N: "+ str(loadNumber))
                return None

        if (float(dictMedition["initAngle"]) > float(dictMedition["finalAngle"])):
            messagebox.showinfo('Message', "El angulo inicial es mayor al angulo final en la medición N: "+ str(loadNumber))
        if(float(dictMedition["sizeOfsteps"]) < 0.001):
            messagebox.showinfo('Message', "Paso de ángulo más chico del permitido en la medición N: "+ str(loadNumber))

    def timePerStepsFunction(self, step):
        # This polynomial of degrees two was made by taking times from the measuring machine
        return 0.323 * step * step - 0.9166 * step + 1.53

    def calculatedTime(self, dict):
        totalTime = 0
        fA = float(dict["finalAngle"])
        iA = float(dict["initAngle"])
        sA = float(dict["sizeOfsteps"])
        tm = float(dict["time"])
        numberOfIntervals =  (fA - iA) / sA
        print(numberOfIntervals, self.timePerStepsFunction(sA), tm + 0.3)
        totalTime = numberOfIntervals * (self.timePerStepsFunction(sA) + ( tm +0.3))
        return totalTime/3600

    def measurementProcess(self):
        amountOfStep = math.floor((self.finalA-self.initA)/self.incrementAngle)
        print("La cantidad de pasos a realizar son: {}".format(amountOfStep))

        #CONNECTION WITH GONIOMETRO
        #serialInstance(baudrate, port, bytesize, parity, stopbits)
        timeout = self.timeStep + SECURITYTIME
        GONIOMETRO = se.Serial()
        GONIOMETRO = parametersSerial( GONIOMETRO, 9600, 'COM6', 8, 'N', 1, timeout)
        #CONNECTION WITH MEASURINGMACHINE
        MEASURINGMACHINE = se.Serial()
        MEASURINGMACHINE = parametersSerial( MEASURINGMACHINE, 4800, 'COM7', 8, 'N', 1, timeout)

        try:
            GONIOMETRO.open()
            MEASURINGMACHINE.open()
        except se.serialutil.SerialException:
            GONIOMETRO.open()
            MEASURINGMACHINE.open()
            print("\nNo se pudo realizar la conexion, fijese si son correctos los parametros de coneccion")
            checkConnection(GONIOMETRO, MEASURINGMACHINE)
            exit()

        checkConnection(GONIOMETRO, MEASURINGMACHINE)
        
        setAngle = self.initA


        nameArchiveBis = self.globalpath
        print("El ARCHIVE QUE NO ANDA ES ESTE ", self.globalpath)
        instanceTxt = open(nameArchiveBis, 'a')
        instanceTxt.close()

        # Set the angle in the Initial angle
        setTheAngleInGoniometro = 'SAN '+ str(setAngle) + '\r'
        # Waiting the goniometer to reach the angle
        angleReached(GONIOMETRO, setTheAngleInGoniometro)

        setGoniometerMod = 'MOD 3\r'
        angleReached(GONIOMETRO, setGoniometerMod)

        self.startMedition()

        while(setAngle <= self.finalA):

            if(self.stateMedition == 0):
                initialCondition(GONIOMETRO)
                destroy(GONIOMETRO, MEASURINGMACHINE)
                messagebox.showinfo('Message', "La medición se cancelo exitosamente")
                break

            # Build a command
            command = "MCR " + str(self.timeStep) + '\r'
            # Send a command to medition machine

            medition = meditionReached(MEASURINGMACHINE, command)
            acumMed = transformString(medition,1)
            
            print("{:.3f} {}".format(setAngle, medition))
            print("El valor obtenido es:", acumMed)

            setAngle = setAngle + self.incrementAngle

            instanceTxt = open(nameArchiveBis, 'a')
            stringSetAngle = "{:.3f}".format(setAngle)
            stringWrite = "{} {}".format(stringSetAngle, acumMed).strip("\n")
            stringWrite = stringWrite + "\r"

            self.x.append(round(setAngle,3))
            self.y.append(round(acumMed,1))
            
            instanceTxt.write(stringWrite)
            instanceTxt.close

            setTheAngleInGoniometro = 'STM {:.3f} 0\r'.format(self.incrementAngle)
            angleReached(GONIOMETRO, setTheAngleInGoniometro)

            # Waiting the goniometer to reach the angle

        #Destoy classes. Serials and xlswriter
        initialCondition(GONIOMETRO)
        destroy(GONIOMETRO, MEASURINGMACHINE)

    def canceledMedition(self):
        self.stateMedition = 0
        self.x = []
        self.y = []

    def startMedition(self):
        if(self.stateMedition == 1 and self.x != [] and self.y != []):
                X = np.array(self.x)
                Y = np.array(self.y)
                print(X)
                print(Y)
                self.refreshFigure(X,Y)
                app.after(2000,self.startMedition)


    def saveValues(self):

        self.canceledButton = tk.Button(self.meditionTab, text="Cancelar medición", font=Font_tuple_botton, borderwidth="5", command=self.canceledMedition)
        self.canceledButton.place(x= (WIDTH-130)/2,y=self.heightCanceledButton, width=130, height=29)

        self.stateMedition = 1

        # self.startMedition()


        while(not os.path.exists(self.stringPath)):
            messagebox.showinfo('Message', "el directorio ingresado no es válido ")
            return None
        
        self.stringPathFile = r""
        self.stringPathFile = self.stringPathFile + self.stringPath + "/" + self.nameOfFile.get()
        print(self.stringPathFile)
        self.globalpath  = self.stringPathFile

        self.listOfTuple = []
        if (self.amountOfMedition >= 1):
            self.firstTuple =   {   "initAngle" : self.initanglefirstmedition.get(), 
                                    "finalAngle" : self.finalanglefirstmedition.get(),
                                    "time": self.timefirstmedition.get(),
                                    "sizeOfsteps": self.stepsfirstmedition.get()
                                }
            
            self.listOfTuple.append(self.firstTuple)
            self.verificationValues(self.firstTuple, 1)
        if (self.amountOfMedition >= 2):
            self.secondTuple =   {   "initAngle" : self.initanglesecondmedition.get(), 
                                    "finalAngle" : self.finalanglesecondmedition.get(),
                                    "time": self.timesecondmedition.get(),
                                    "sizeOfsteps": self.stepssecondmedition.get()
                                }
            self.listOfTuple.append(self.secondTuple)
            self.verificationValues(self.secondTuple, 2)
        if (self.amountOfMedition >= 3):
            self.thirdTuple =   {   "initAngle" : self.initanglethirdmedition.get(), 
                                    "finalAngle" : self.finalanglethirdmedition.get(),
                                    "time": self.timethirdmedition.get(),
                                    "sizeOfsteps": self.stepsthirdmedition.get()
                                }
            self.listOfTuple.append(self.thirdTuple)
            self.verificationValues(self.thirdTuple, 3)
        if (self.amountOfMedition >= 4):
            self.fourthTuple =   {   "initAngle" : self.initanglefourthmedition.get(), 
                                    "finalAngle" : self.finalanglefourthmedition.get(),
                                    "time": self.timefourthmedition.get(),
                                    "sizeOfsteps": self.stepsfourthmedition.get()
                                }
            self.listOfTuple.append(self.fourthTuple)
            self.verificationValues(self.fourthTuple, 4)
        if (self.amountOfMedition >= 5):
            self.fifthTuple =   {   "initAngle" : self.initanglefifthmedition.get(), 
                                    "finalAngle" : self.finalanglefifthmedition.get(),
                                    "time": self.timefifthmedition.get(),
                                    "sizeOfsteps": self.stepsfifthmedition.get()
                                }
            self.listOfTuple.append(self.fifthTuple)
            self.verificationValues(self.fifthTuple, 5)
        self.placeAndNameOfFile =  self.textBar.get("1.0", 'end-1c') + "/" +self.nameOfFile.get()
        # print(self.listOfTuple, "\n", self.placeAndNameOfFile)

        self.timeAcumulated = 0
        for self.items in self.listOfTuple:
            self.timeAcumulated = self.timeAcumulated + self.calculatedTime(self.items)

        self.parte_decimal, self.parte_entera = math.modf(self.timeAcumulated)

        self.mssg = "El tiempo estimado es de {} hs {} min ".format(int(self.parte_entera), round(60*self.parte_decimal))
        messagebox.showinfo('Message', self.mssg)


        for self.items in self.listOfTuple:
            self.initA = float(self.items["initAngle"])
            self.finalA = float(self.items["finalAngle"])
            self.incrementAngle = float(self.items["sizeOfsteps"])
            self.timeStep = float(self.items["time"])
            
            processThread = threading.Thread(target=self.measurementProcess)
            processThread.daemon = True
            processThread.start()

def graphicInterfecace():
    main_window = tk.Tk()
    app = Application(main_window)
    # ani = FuncAnimation(fig, animate, interval=1000)
    app.mainloop()