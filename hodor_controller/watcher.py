
import argparse
import csv
import json
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

try:
    import serial
except ImportError:
    print("Error importing serial module - serial functions disabled")



class HodorWatcher:

    def __init__(self,rootdir=None,test_mode=False):
        self._gpio_setup()
        # setup serial port
        self._serial_enabled = False
        self._port = None
        self._event_seqnum = 0
        self._cycles = 0
        self._strobe_seconds = 3
        self._dots = False
        self._rootdir = None
        self._acl_path = None
        self._event_q_dir = None
        self._logdir = None
        self._log_path = None
        self._logger = None
        self._devicename = None
        if rootdir is not None:
            self._setrootdir(rootdir)

    def _setrootdir(self,the_root):
        if the_root is not None and os.path.exists(the_root):
            self._rootdir = the_root
        if not os.path.exists(self._rootdir):
            raise Exception('no root dir')
        # access list
        self._acl_path = os.path.join(self._rootdir,'bw_cardkey.csv')
        # event message dir
        self._event_q_dir = os.path.join(self._rootdir,'events')
        if not os.path.exists(self._event_q_dir):
            os.makedirs(self._event_q_dir)
        # setup logging
        FORMAT='%(asctime)-15s %(message)s'
        # logging.basicConfig(FORMAT)
        self._logdir = os.path.join(self._rootdir,'log')
        if not os.path.exists(self._logdir):
            os.makedirs(self._logdir)
        self._log_path = os.path.join(self._logdir,'hodor_watcher.log')
        self._logger = None
        logging.basicConfig(
            filename=self._log_path,
            level=logging.INFO,
            format=FORMAT
        )
        self._logger = logging.getLogger('hodor_watcher')

    def _gpio_setup(self):
        # setup GPIO
        if GPIO_ENABLED:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(16,GPIO.OUT)

    def _serial_setup(self):
        if self._devicename is not None:
            self._port = serial.Serial(
                self._devicename,
                baudrate=9600,
                timeout=1.0
            )
            if self._port is not None:
                self._serial_enabled = True

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
        if self._serial_enabled:
            rcv = self._port.readline(100)
        return rcv

    def process_arguments(self,arglist):
        prsr = argparse.ArgumentParser()
        prsr.add_argument('--root',required=True)
        prsr.add_argument('--dots',action='store_true')
        prsr.add_argument('--dev',help='serial device name/path')
        args = prsr.parse_args(arglist)
        if args.root is not None:
            self._setrootdir(args.root)
        if args.dots:
            self._dots = True
        if args.dev:
            self._devicename = args.dev

    def scan_for_key(self,received):
        """Cleans up incoming data ('received')

        Returns cleaned data or None if nothing left to return"""
        checkit = None
        try:
            checkit = received.decode('utf-8')
        except (AttributeError,UnicodeDecodeError):
            checkit = received
        if len(checkit) == 0 or checkit == '\x03':
            return None
        clean_checkit = re.sub(r'[\002\003]','',checkit.strip().upper())
        return clean_checkit

    def find_user(self,user_database,the_key):
        """Finds user given key

        Returns None if key not recognized, or a dict with user info"""
        the_user = None
        match_key = self.scan_for_key(the_key)
        if match_key in user_database:
            the_user = user_database[match_key]
        return the_user

    def eval_access(self,user_database,presented_key):
        """Checks presented_key against user_database for access grant.

        Returns two arguments: grant_info and user_info.  The grant_info
        value is a boolean value which is true if the user is allowed to
        enter.  The user_info value is a structure with user name and
        key information.
        """
        user_info = self.find_user(user_database,presented_key)
        grant_info = False
        if user_info is not None and user_info['ALLOW'].lower() == 'y':
            grant_info = True
        return grant_info, user_info

    def console_write(self,msg):
        sys.stdout.write(msg)

    def console(self,msg):
        print(msg)

    def log(self,msg,*args,**kwargs):
        if self._logger is not None:
            self._logger.info(msg,*args,**kwargs)

    def event_fname(self,set_tstamp=None):
        tstamp = time.strftime('%Y-%m-%d_%H%M%S')
        if set_tstamp is not None:
            tstamp = set_tstamp
        pidstamp = '{0:06d}'.format(os.getpid())
        enumstamp = '{0:06d}'.format(self._event_seqnum)
        self._event_seqnum += 1
        out = '{0}_{1}_{2}.event'.format(tstamp,pidstamp,enumstamp)
        return out

    def write_event(self,msg):
        base_fname = self.event_fname()
        ev_path = os.path.join(self._event_q_dir,base_fname)
        ev_obj = {
            'message': msg,
            'localtime': time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'utctime': time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())
        }
        fh = open(ev_path,'w')
        fh.write(json.dumps(ev_obj))
        fh.close()
        return ev_path

    def run_main(self,arglist=None):
        self.process_arguments(arglist)
        self._serial_setup()
        while True:
            if self._dots:
                self.console_write('.')
                self._cycles += 1
                if self._cycles % 60 == 0:
                    self._cycles = 0
                    print('')
            rcv = self.serial_readport(100)
            clean_rcv = self.scan_for_key(rcv)
            if clean_rcv is not None:
                self.console_write("\nreceived : {0}\n".format(repr(rcv)))
                # read the ACL database and try to match the key
                keydb_fh = open(self._acl_path)
                everyone = self.readdb(keydb_fh)
                keydb_fh.close()
                access_ok, dude = self.eval_access(everyone,clean_rcv)
                if dude is None:
                    unrec_msg = "Unrecognized key {0}".format(clean_rcv)
                    self.console(unrec_msg)
                    self.log(unrec_msg)
                    self.write_event(unrec_msg)
                else:
                    recognize_msg = "Recognized {0} ({1})".format(
                        dude['NAME'],
                        dude['KEY']
                    )
                    self.console(recognize_msg)
                    self.log(recognize_msg)
                    self.write_event(recognize_msg)
                    if access_ok:
                        grant_msg = "ACCESS GRANTED TO: {0} ({1})".format(
                            dude['NAME'],
                            dude['KEY']
                        )
                        self.console(grant_msg)
                        self.log(grant_msg)
                        self.write_event(grant_msg)
                        self.strobe_access()
                    else:
                        deny_msg = "DENYING {0} ({1})".format(
                            dude['NAME'],
                            dude['KEY']
                        )
                        self.console(deny_msg)
                        self.log(deny_msg)
                        self.write_event(deny_msg)
            sys.stdout.flush()

def main():
    ap = HodorWatcher()
    ap.run_main()

if __name__ == '__main__':
    main()
