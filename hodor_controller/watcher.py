
import csv
import logging
import RPi.GPIO as GPIO
import serial
import string
import sys
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing GPIO module")







class HodorWatcher:

    def __init__(self):
        # setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(16,GPIO.OUT)
        # setup serial port
        self._port = serial.Serial("/dev/serial0",baudrate=115200,timeout=1.0)
        self._cycles = 0
        self._strobe_seconds = 10
        # setup logging
        FORMAT='%(asctime)-15s %(message)s'
        # logging.basicConfig(FORMAT)
        logging.basicConfig(filename='/home/pi/log/hodor_watcher.log',level=logging.INFO,format=FORMAT)
        self._logger = logging.getLogger('hodor_watcher')


    def strobe_access(self):
        GPIO.output(16,GPIO.HIGH)
        time.sleep(self._strobe_seconds)
        GPIO.output(16,GPIO.LOW)

    def readdb(self):
        fh = open('/home/pi/bw_cardkey.csv')
        rdr = csv.DictReader(fh)
        user_array = []
        for ro in rdr:
            user_array.append(ro)
        users = {}
        for u in user_array:
            users[u['KEY']] = u
        fh.close()
        return users


    def run_main(self):
        everyone = self.readdb()
        print(repr(everyone))
        while True:
            sys.stdout.write('.')
            self._cycles += 1
            if self._cycles % 60 == 0:
                self._cycles = 0
                print('')
            rcv = self._port.readline(100)
	    if len(rcv) > 0:
                sys.stdout.write("\nreceived : {0}\n".format(repr(rcv)))
                clean_rcv = rcv.strip().upper()
                if clean_rcv in everyone:
                    dude = everyone[clean_rcv]
                    print("Recognized {0} ({1})".format(dude['NAME'],dude['KEY']))
                    self._logger.info("Recognized {0} ({1})".format(dude['NAME'],dude['KEY']))
                    if dude['ALLOW'] == 'y':
                        print("ACCESS GRANTED TO: {0} ({1})".format(dude['NAME'],dude['KEY']))
                        self._logger.info("ACCESS GRANTED TO: {0} ({1})".format(dude['NAME'],dude['KEY']))
                        self.strobe_access()
                    else:
                        print("DENYING {0} ({1})".format(dude['NAME'],dude['KEY']))
                        self._logger.info("DENYING {0} ({1})".format(dude['NAME'],dude['KEY']))
                else:
                    print("Unrecognized key {0}".format(clean_rcv))
                    self._logger.info("Unrecognized key {0}".format(clean_rcv))
            sys.stdout.flush()

def main():
    ap = HodorWatcher()
    ap.run_main()

if __name__ == '__main__':
    main()

