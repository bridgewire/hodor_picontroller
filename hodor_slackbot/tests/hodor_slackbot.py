
import datetime
from ..hodor_slacker import HodorSlacker
import json
import os
import tempfile
import time
import unittest

class TestHodorSlackbot(unittest.TestCase):

    def setUp(self):
        self._workdir = tempfile.mkdtemp()
        self._evdir = os.path.join(self._workdir,'events')
        os.makedirs(self._evdir)
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
        evtext = file(evpath).read()
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

    def test_find_new_events(self):
        eventnames = ['fne{0}.ev'.format(x) for x in range(1,5)]
        eventpaths = [
            self.write_test_event(base,base) for base in eventnames
        ]
        self._ap.record_lastseen(eventpaths[1])
        gotpaths = self._ap.find_new_events()
        self.assertEqual(gotpaths,['fne3.ev', 'fne4.ev'])
