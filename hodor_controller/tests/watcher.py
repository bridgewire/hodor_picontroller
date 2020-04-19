
from hodor_controller.watcher import HodorWatcher
import json
import os
try:
    from io import StringIO
except ImportError:
    # obsolete as of this writing, but still throw a sop to Python 2.7
    from StringIO import StringIO
import tempfile
import unittest

class TestHodorWatcher(unittest.TestCase):

    def setUp(self):
        self._workdir = tempfile.mkdtemp()
        self._ap = HodorWatcher(rootdir=self._workdir,test_mode=True)

    def test_scan_for_key(self):
        self.assertEqual(self._ap.scan_for_key(''),None)
        self.assertEqual(self._ap.scan_for_key('\x03'),None)
        self.assertEqual(self._ap.scan_for_key(' blah '),'BLAH')
        self.assertEqual(self._ap.scan_for_key('\x02blat \r\n'),'BLAT')

    def test_readdb(self):
        dbtext1 = """KEY,NAME,ALLOW
01-01,Alice Blogs,y
02-blah,Foo Bar,n
1-3,Whoever,
"""
        fh1 = StringIO(dbtext1)
        got_db1 = self._ap.readdb(fh1)
        expect_db1 = {
            '13': {'ALLOW': '', 'NAME': 'Whoever', 'KEY': '1-3'},
            '0101': {'ALLOW': 'y', 'NAME': 'Alice Blogs', 'KEY': '01-01'},
            '02blah': {'ALLOW': 'n', 'NAME': 'Foo Bar', 'KEY': '02-blah'}
        }
        self.assertEqual(got_db1,expect_db1)

    def test_find_user(self):
        testdb1 = {
            '13': {'ALLOW': '', 'NAME': 'Whoever', 'KEY': '1-3'},
            '0101': {'ALLOW': 'y', 'NAME': 'Alice Blogs', 'KEY': '01-01'},
            '02BLAH': {'ALLOW': 'n', 'NAME': 'Foo Bar', 'KEY': '02-blah'}
        }
        self.assertEqual(self._ap.find_user(testdb1,'not_in_db'),None)
        expect_user2 = testdb1['02BLAH']
        self.assertEqual(self._ap.find_user(testdb1,'02BLAH'),expect_user2)
        self.assertEqual(self._ap.find_user(testdb1,'02blah'),expect_user2)

    def test_event_fname(self):
        ref_tstamp = '2001-01-01_123456'
        fn1 = self._ap.event_fname(set_tstamp=ref_tstamp)
        fn2 = self._ap.event_fname(set_tstamp=ref_tstamp)
        expect_pid = '{0:06d}'.format(os.getpid())
        expect_fn1 = '{0}_{1}_000000.event'.format(ref_tstamp,expect_pid)
        expect_fn2 = '{0}_{1}_000001.event'.format(ref_tstamp,expect_pid)
        self.assertEqual(fn1,expect_fn1)
        self.assertEqual(fn2,expect_fn2)

    def test_write_event(self):
        ref_tstamp = '2001-01-01_123456'
        expect_pid = '{0:06d}'.format(os.getpid())
        got1 = self._ap.write_event('event1')
        got2 = self._ap.write_event('event2')
        self.assertEqual(os.path.exists(got1),True)
        fh1 = open(got1,'r')
        text1 = fh1.read()
        fh1.close()
        self.assertEqual(json.loads(text1)['message'],'event1')
        self.assertEqual(os.path.exists(got2),True)
        fh2 = open(got2,'r')
        text2 = fh2.read()
        fh2.close()
        self.assertEqual(json.loads(text2)['message'],'event2')

    def test_eval_access(self):
        testdb1 = {
            '13': {'ALLOW': '', 'NAME': 'Whoever', 'KEY': '1-3'},
            '0101': {'ALLOW': 'y', 'NAME': 'Alice Blogs', 'KEY': '01-01'},
            '02BLAH': {'ALLOW': 'n', 'NAME': 'Foo Bar', 'KEY': '02-blah'}
        }
        grant1, user1 = self._ap.eval_access(testdb1,'not_in_db')
        self.assertEqual(grant1,False)
        self.assertEqual(user1,None)
        grant2, user2 = self._ap.eval_access(testdb1,'02blah')
        self.assertEqual(grant2,False)
        self.assertEqual(user2,{
            'KEY': '02-blah',
            'NAME': 'Foo Bar',
            'ALLOW': 'n'
        })
        grant3, user3 = self._ap.eval_access(testdb1,'0101')
        self.assertEqual(grant3,True)
        self.assertEqual(user3,{
            'KEY': '01-01',
            'NAME': 'Alice Blogs',
            'ALLOW': 'y'
        })
