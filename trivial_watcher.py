
import RPi.GPIO as GPIO
import serial
import string
import sys
import time

# setup GPIO
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing GPIO module")

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16,GPIO.OUT)

# setup serial port
port = serial.Serial("/dev/serial0",baudrate=115200,timeout=1.0)

cycles = 0

def strobe_access():
	GPIO.output(16,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(16,GPIO.LOW)

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




