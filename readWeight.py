import serial, time

s=serial.Serial("/dev/ttyACM0",9600)		#change the serial port to the one being used example "/dev/ttyUSB" or "/dev/serial0" or "/dev/ttyACM0" etc
											#can check if data is present on the port by using this command "minicom -D </dev/<port used ex: /dev/ttyUSB0 > -b <baud ex : 9600>"
while(True):
	data = s.readline().decode()
	with open("weightBuffer.txt","w") as file:
		file.write(data)
		file.close()
	time.sleep(0.5)				#sleep for half second
