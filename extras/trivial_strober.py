
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
GPIO.output(16,GPIO.LOW)

# setup serial port

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
	if (cycles % 2)==1:
		print("STROBE DOOR")
		strobe_access()
		time.sleep(1)
	sys.stdout.flush()




