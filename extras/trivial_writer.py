
import re
import serial
import string
import sys
import time

# setup serial port
port = serial.Serial("/dev/tty.usbserial",baudrate=9600,timeout=1,bytesize=8,parity='N',stopbits=1,xonxoff=False,rtscts=False)

t = 0

while True:
    print('console: {0}'.format(t))
    port.write('serialout: {0}'.format(t))
    t = t + 1
    time.sleep(1)

cycles = 0

watch_preclean = True

while True:
    if watch_preclean:
        sys.stdout.write('.')
    cycles += 1
    if cycles % 60 == 0:
        cycles = 0
        if watch_preclean:
            print('')
#    w = port.in_waiting
#    if w > 0:
    if True:
        w=0
        if watch_preclean:
            print('waiting bytes: {0}'.format(w))
        rcv = port.read(w)
        if len(rcv) > 0:
            if watch_preclean:
                sys.stdout.write("\nreceived : {0}\n".format(repr(rcv)))
            zclean_rcv = re.sub(r'\000','',rcv)
            if watch_preclean:
                sys.stdout.write("\nzerocleaned : {0} {1}\n".format(repr(zclean_rcv),len(zclean_rcv)))
            if len(zclean_rcv) > 0:
                clean_rcv = zclean_rcv.strip()
                sys.stdout.write("\nscanning : {0} {1}\n".format(repr(clean_rcv),len(clean_rcv)))

                if clean_rcv == '12':
                    print("ACCESS GRANTED")
                    strobe_access()
                else:
                    print("Access denied")
    sys.stdout.flush()

