
from hodor_controller.watcher import HodorWatcher
import StringIO
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
        fh1 = StringIO.StringIO(dbtext1)
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
