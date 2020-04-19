
import datetime
from hodor_slackbot.hodor_slacker import HodorSlacker
import json
import os
import sys
import tempfile
import time
import unittest

class TestHodorSlacker(unittest.TestCase):

    def setUp(self):
        self._workdir = tempfile.mkdtemp()
        self._evdir = os.path.join(self._workdir,'events')
        os.mkdir(self._evdir)
        self._ap = HodorSlacker(self._workdir)

    def write_test_event(self,fname,msg):
        ev_obj = {
            'message': msg
        }
        ev_path = os.path.join(self._evdir,fname)
        ev_fh = open(ev_path,'w')
        ev_fh.write(json.dumps(ev_obj))
        ev_fh.close()
        return ev_path

    def test_record_lastseen(self):
        evpath = self.write_test_event('foo.ev','blah')
        got1 = self._ap.record_lastseen(evpath)
        self.assertEqual(got1,True)
        evtext = open(evpath).read()
        self.assertEqual(evtext,'{"message": "blah"}')
        badpath = evpath + 'nonsense'
        self.assertRaises(ValueError,self._ap.record_lastseen,badpath)

    def test_get_lastseen(self):
        got00 = self._ap.get_lastseen()
        self.assertEqual(got00,None)
        ev1path = self.write_test_event('f1.ev','blah')
        got01 = self._ap.get_lastseen()
        self.assertEqual(got01,None)
        self._ap.record_lastseen(ev1path)
        got1 = self._ap.get_lastseen()
        self.assertEqual(got1,ev1path)
        # explicitly handle case where statepath is undefined
        self._ap._statepath = None
        got2 = self._ap.get_lastseen()

    def test_find_new_event_names(self):
        self.assertEqual(self._ap._statefile,'.hodor_lastslack')
        gotpaths0 = self._ap.find_new_event_names()
        self.assertEqual(gotpaths0,[])
        eventnames = ['fne{0}.ev'.format(x) for x in range(1,5)]
        eventpaths = [
            self.write_test_event(base,base) for base in eventnames
        ]
        self._ap.record_lastseen(eventpaths[1])
        gotpaths1 = self._ap.find_new_event_names()
        self.assertEqual(gotpaths1,['fne3.ev', 'fne4.ev'])
        self._ap.record_lastseen(eventpaths[3])
        gotpaths2 = self._ap.find_new_event_names()
        self.assertEqual(gotpaths2,[])
        # explicitly handle case where self._evdir is undefined
        self._ap._evdir = None
        self.assertRaises(OSError,self._ap.find_new_event_names)

    def test_find_new_events(self):
        self.assertEqual(self._ap._statefile,'.hodor_lastslack')
        gotpaths0 = self._ap.find_new_events()
        self.assertEqual(gotpaths0,[])
        eventnames = ['fne{0}.ev'.format(x) for x in range(1,5)]
        eventpaths = [
            self.write_test_event(base,base) for base in eventnames
        ]
        self._ap.record_lastseen(eventpaths[1])
        gotfullpaths1 = self._ap.find_new_events()
        for p in gotfullpaths1:
            self.assertEqual(os.path.exists(p),True)
        gotnames1 = [os.path.basename(p) for p in gotfullpaths1]
        self.assertEqual(gotnames1,['fne3.ev', 'fne4.ev'])
        self._ap.record_lastseen(eventpaths[3])
        gotfullpaths2 = self._ap.find_new_events()
        self.assertEqual(gotfullpaths2,[])
        # explicitly handle case where self._evdir is undefined
        self._ap._evdir = None
        self.assertRaises(OSError,self._ap.find_new_events)
