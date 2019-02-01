import serial
import time

s=serial.Serial("/dev/ttyACM0",9600)

while(True):
    data_recv=s.readline().decode()
    with open("weightBuffer.txt","r") as file:
        data = file.read()
        if(data_recv != data):
            with open("weightBuffer.txt","w") as fileW:
                fileW.write(str(data_recv))
                fileW.close()
        file.close()
