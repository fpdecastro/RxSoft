#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      paqui
#
# Created:     31/05/2021
# Copyright:   (c) paqui 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from datetime import date
import math
import serial as se
import xlsxwriter as xl
import math
import time
import datetime as dt

# Wait time tolerance
SECURITYTIME = 5

GREETINGS = '''

BIENVENIDO A PW3710 DIFRACTOMETER CONTROL UNIT
LA COMUNICACI?N SE ESTABLECE VIA RS232 POR PUERTO SERIAL

            '''

def parametersSerial( serialObject, db, port, bytesize, parity, stopbits, timeOut):
    serialObject.baudrate = db
    serialObject.port = port
    serialObject.bytesize = bytesize
    serialObject.parity = parity
    serialObject.stopbits = stopbits
    serialObject.timeout = timeOut
    return serialObject

def checkConnection(firstSerial, secondSerial):
    if(not firstSerial.isOpen() and not secondSerial.isOpen()):
        print("Fallo de conexion de ambas puertos")
    elif (not firstSerial.isOpen() and secondSerial.isOpen()):
        print("Se puso establecer la conexion PWP 1606 pero fallo la conexion con PWP3710")
    elif (firstSerial.isOpen() and not secondSerial.isOpen()):
        print("Se puso establecer la conexion PWP 1606 pero fallo la conexion con PWP3710")
    elif( firstSerial.isOpen() and secondSerial.isOpen()):
        print("Conexion exitosa de ambas puertos")


def transformString( medition, direction):
    stringNumber = ""
    #Start from behind (1)
    if direction == 1:
        for i in range(len(medition)):
            char = medition[-1:]
            if char != " ":
                stringNumber = char + stringNumber
                medition = medition[:len(medition)-1]
            else:
                break
        stringNumber = stringNumber.strip("\n")
        stringNumber = stringNumber.strip("\r")
    #Start from the front (0)
    elif direction == 0:
        for char in range(medition):
            if char == " ":
                medition = medition[1:]
            else:
                break
        for charBis in range(medition):
            if charBis != " ":
                stringNumber = stringNumber + charBis
                medition = medition[1:]
            else:
                break
    else:
        exit()
    return float(stringNumber)*1000

    
def meditionReached(serialObject, command):
    serialObject.write(command.encode())
    # Wait middle second to read the buffer
    time.sleep(0.5)
    # Clean the buffer
    serialObject.flushOutput()
    serialObject.flushInput()
    while True:
        answer = serialObject.readline()
        if answer == "\n".encode():
            answer = serialObject.readline().decode()
            break
    return answer

def initialCondition(serialObject):
    setTheInitialAngle = 'SAN 0\r'
    angleReached(serialObject, setTheInitialAngle)


def destroy(firstSerial, secondSerial):
    firstSerial.close()
    secondSerial.close()

def greaterThanOrEqual(alfa, beta):
    return beta - alfa <= 0

def stdinFromKeyboard(nameVariable, units):
    while True:
        instruction = "Ingrese el "+ nameVariable + ' ('+ units + '): '
        try:
            inputValue = float(input(instruction))
            break
        except ValueError:
            print("El valor ingresado no es un numero valido")
    return inputValue

def angleReachedbis(serialObject, command):
    serialObject.write(command.encode())
    # Give time serial port time to recover
    serialObject.flush()
    time.sleep(0.5)
    # Clean the buffer
    #serialObject.flushInput()
    while True:
       answer = serialObject.readline().decode()
       print(answer)
       if answer == "C=":
           print("El ángulo se alcanzo exitosamente", command)
           break

def angleReached(serialObject, command):
    initialTime = dt.datetime.now()
    serialObject.write(command.encode())
    serialObject.flush()
    time.sleep(0.5)
    # We're expecting some response!

    if(command[0:3].lower() == "stm"):
        ans = serialObject.readline()
        if(ans == "\n".encode() or ans == "C=\n".encode()):
            ans = serialObject.readline()
            print("Angulo actual",ans.decode())
    else:
        while True:
            ans = serialObject.readline()
            if(ans == "\n".encode() or ans == "C=\n".encode()):
                print("Se alcanzo el àngulo ", command)
                break

   #ans = serialObject.readline().decode()
    finalTime = dt.datetime.now()
    difTime = finalTime - initialTime
    print(difTime)

def stepHigherThanAcceptable(incrementAngle):
    return incrementAngle < 0.005

def main():
    print(GREETINGS)

    # Input measurement process variables
    initialAngle = stdinFromKeyboard("Angulo inicial", "G")
    finalAngle = stdinFromKeyboard("Angulo final", "G")
    incrementAngle = stdinFromKeyboard("Incremento de angulo", "G")
    timePerStep = stdinFromKeyboard("Tiempo por paso", "s")

    # Check initial and final angle
    while( greaterThanOrEqual(initialAngle, finalAngle)):
        print("\nIngrese un Angulo inicial menor y/o diferente al Angulo final")
        initialAngle = stdinFromKeyboard("Angulo inicial", "?")
        finalAngle = stdinFromKeyboard("Angulo final", "?")
        incrementAngle = stdinFromKeyboard("Incremento de angulo", "G")
        incrementAngle = stdinFromKeyboard("Tiempo por pasos", "s")

    # Check the increment
    while( stepHigherThanAcceptable(incrementAngle) ):
        print("\nIngrese paso de ángulo mayor")
        initialAngle = stdinFromKeyboard("Angulo inicial", "?")
        finalAngle = stdinFromKeyboard("Angulo final", "?")
        incrementAngle = stdinFromKeyboard("Incremento de angulo", "G")
        incrementAngle = stdinFromKeyboard("Tiempo por pasos", "s")

    #Start the measurement process
    # measurementProcess(initialAngle, finalAngle, incrementAngle, timePerStep)

# if __name__ == '__main__':
#     main()
