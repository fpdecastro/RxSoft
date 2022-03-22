import serial
import datetime as dt
import time

def parametersSerial( serialObject, db, port, bytesize, parity, stopbits):
    serialObject.baudrate = db
    serialObject.port = port
    serialObject.bytesize = bytesize
    serialObject.parity = parity
    serialObject.stopbits = stopbits
    return serialObject

def meditionReached(serialObject, command):
    serialObject.write(command.encode())
    # Wait middle second to read the buffer
    time.sleep(0.5)
    # Clean the buffer
    serialObject.flushOutput()
    serialObject.flushInput()
    print(command.encode())
    while True:
        answer = serialObject.readline()
        print(answer)
        if answer == "\n".encode():
            answer = serialObject.readline().decode()
            break
    return answer

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
            print(ans.decode())
            if(ans == "\n".encode() or ans == "C=\n".encode()):
                print("Se alcanzo el àngulo ", command)
                break

   #ans = serialObject.readline().decode()
    finalTime = dt.datetime.now()
    difTime = finalTime - initialTime
    print(difTime)

SELECTION = '''
Con quien quiere hablar?
[1] Goniometro
[2] Sensor 
'''      


if __name__ == "__main__":
    

    while True:
        print(SELECTION)
        option = int(input())

        if option == 1 or option == 2:
            if option == 1:
                goniometer = serial.Serial()
                goniometer.port = 'COM6'
                goniometer.baudrate = 9600
                goniometer.stopbits = 1
                goniometer.bytesize = 8
                goniometer.parity = 'N'
                goniometer.timeout = 10
                goniometer.open()
                print("connection succesfully")
                while True:        
                    command = input("Insert the command: ")
                    if(command == "exit"):
                        break
                    command = command + "\r"
                    angleReached(goniometer, command)

            else:

                sensormachine = serial.Serial()
                sensormachine.port = 'COM7'
                sensormachine.baudrate = 4800
                sensormachine.stopbits = 1
                sensormachine.bytesize = 8
                sensormachine.parity = 'N'
                sensormachine.timeout = 5
                sensormachine.open()

                while True:        
                    # ans = sensormachine.readline()
                    # print(ans)
                    command = input("Insert the command: ")
                    if(command == "exit"):
                        break
                    command = command + "\r"
                    medition = meditionReached(sensormachine, command)
                    print(medition)
