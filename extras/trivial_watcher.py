
import serial
import string
import sys
import time

# setup serial port
port = serial.Serial("/dev/tty.usbserial",baudrate=9600,timeout=1.0,bytesize=8,parity='N',stopbits=1,rtscts=False,xonxoff=False)

cycles = 0

while True:
	sys.stdout.write('.')
	cycles += 1
	if cycles % 60 == 0:
		cycles = 0
		print('')
	rcv = port.readline(100)
	if len(rcv) > 0:
		sys.stdout.write("\nreceived : {0}\n".format(repr(rcv)))
		clean_rcv = rcv.strip()
		if clean_rcv == '12':
			print("ACCESS GRANTED")
			strobe_access()
		else:
			print("Access denied")
	sys.stdout.flush()




