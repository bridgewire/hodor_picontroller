
import csv
import logging
import os
import re
import string
import sys
import time

GPIO_ENABLED = True

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Error importing GPIO module - GPIO functions disabled")
    GPIO_ENABLED = False

SERIAL_ENABLED = True

try:
    import serial
except ImportError:
    print("Error importing serial module - serial functions disabled")
    SERIAL_ENABLED = False



class HodorWatcher:

    def __init__(self,rootdir,test_mode=False):
        self._gpio_setup()
        # setup serial port
        self._port = None
        self._serial_setup()
        self._cycles = 0
        self._strobe_seconds = 5
        self._rootdir = os.environ['HOME']
        if rootdir is not None and os.path.exists(rootdir):
            self._rootdir = rootdir
        if not os.path.exists(self._rootdir):
            raise Exception('no root dir')
        # access list
        self._acl_path = os.path.join(self._rootdir,'bw_cardkey.csv')
        # event message dir
        self._event_q_dir = os.path.join(self._rootdir,'events')
        os.makedirs(self._event_q_dir)
        # setup logging
        FORMAT='%(asctime)-15s %(message)s'
        # logging.basicConfig(FORMAT)
        self._logdir = os.path.join(self._rootdir,'log')
        os.makedirs(self._logdir)
        self._log_path = os.path.join(self._logdir,'hodor_watcher.log')
        self._logger = None
        logging.basicConfig(
            filename=self._log_path,
            level=logging.INFO,
            format=FORMAT
        )
        self._logger = logging.getLogger('hodor_watcher')
        self._dots = False

    def _gpio_setup(self):
        # setup GPIO
        if GPIO_ENABLED:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(16,GPIO.OUT)

    def _serial_setup(self):
        if SERIAL_ENABLED:
            self._port = serial.Serial("/dev/serial0",baudrate=9600,timeout=1.0)

    def strobe_access(self):
        if GPIO_ENABLED:
            GPIO.output(16,GPIO.HIGH)
        time.sleep(self._strobe_seconds)
        if GPIO_ENABLED:
            GPIO.output(16,GPIO.LOW)

    def readdb(self,fh):
        rdr = csv.DictReader(fh)
        user_array = []
        for ro in rdr:
            user_array.append(ro)
        users = {}
        for u in user_array:
            matchkey = re.sub(r'-','',u['KEY'])
            users[matchkey] = u
        return users

    def serial_readport(self,bytes):
        rcv = ''
        if SERIAL_ENABLED:
            rcv = self._port.readline(100)
        return rcv

    def process_arguments(self,arglist):
        prsr = argparse.ArgumentParser()
        prsr.add_argument('--dots',action='store_true')
        args = prsr.parse_args(arglist)
        if args.dots:
            self._dots = True

    def scan_for_key(self,received):
        """Cleans up incoming data ('received')

        Returns cleaned data or None if nothing left to return"""
        if len(received) == 0 or received == '\x03':
            return None
        clean_received = re.sub(r'[\002\003]','',received.strip().upper())
        return clean_received

    def find_user(self,user_database,the_key):
        """Finds user given key

        Returns None if key not recognized, or a dict with user info"""
        the_user = None
        match_key = self.scan_for_key(the_key)
        if match_key in user_database:
            the_user = user_database[match_key]
        return the_user

    def console_write(msg):
        sys.stdout.write(msg)

    def console(msg):
        print(msg)

    def log(msg,*args,**kwargs):
        if self._logger is not None:
            self._logger.info(msg,*args,**kwargs)

    def run_main(self,arglist=None):
        self.process_arguments(arglist)
        keydb_fh = open(self._acl_path)
        everyone = self.readdb(keydb_fh)
        keydb_fh.close()
        print(repr(everyone))
        while True:
            self.console_write('.')
            self._cycles += 1
            if self._cycles % 60 == 0:
                self._cycles = 0
                print('')
            rcv = self.serial_readport(100)
            clean_rcv = self.scan_for_key(100)
            if clean_rcv is not None:
                self.console_write("\nreceived : {0}\n".format(repr(rcv)))
                # to clean out whitespace, XON/XOFF flow control chars
                dude = self.find_user(everyone,clean_rcv)
                if dude is None:
                    self.console("Unrecognized key {0}".format(clean_rcv))
                    self.log("Unrecognized key {0}".format(clean_rcv))
                else:
                    self.console("Recognized {0} ({1})".format(dude['NAME'],dude['KEY']))
                    self.log("Recognized {0} ({1})".format(dude['NAME'],dude['KEY']))
                    if dude['ALLOW'] == 'y':
                        self.console("ACCESS GRANTED TO: {0} ({1})".format(dude['NAME'],dude['KEY']))
                        self.log("ACCESS GRANTED TO: {0} ({1})".format(dude['NAME'],dude['KEY']))
                        self.strobe_access()
                    else:
                        self.console("DENYING {0} ({1})".format(dude['NAME'],dude['KEY']))
                        self.log("DENYING {0} ({1})".format(dude['NAME'],dude['KEY']))
            sys.stdout.flush()

def main():
    ap = HodorWatcher()
    ap.run_main()

if __name__ == '__main__':
    main()
