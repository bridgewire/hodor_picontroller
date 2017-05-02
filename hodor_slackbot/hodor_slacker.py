
import os

class HodorSlacker:

    def __init__(self,setroot=None):
        self._rootdir = None
        self._evdir = None
        self._statepath = None
        if setroot is not None and os.path.exists(setroot):
            self._configure(setroot)


    def _configure(self,rootdir):
        self._rootdir = rootdir
        if not os.path.exists(self._rootdir):
            raise Exception('working directory not found')
        self._evdir = os.path.join(rootdir,'events')
        if not os.path.exists(self._evdir):
            raise Exception('event dir not found')
        self._statepath = os.path.join(self._rootdir,'.hodor_lastslack')
        if not os.path.exists(self._statepath):
            fh = open(self._statepath,'w')
            fh.close()

    def record_lastseen(self,setpath):
        if not os.path.exists(setpath):
            raise ValueError('path {0} not found'.format(setpath))
        fh = open(self._statepath,'w')
        fh.write(setpath)
        fh.close()
        return True

    def get_lastseen(self):
        out = None
        if os.path.exists(self._statepath):
            lastpath = file(self._statepath).read()
            if os.path.exists(lastpath):
                out = lastpath
        return out

    def find_new_events(self):
        lastseen = os.path.basename(self.get_lastseen())
        seenfiles = os.listdir(self._evdir)
        outfiles = None
        if lastseen is not None:
            outfiles = [p for p in seenfiles if p > lastseen]
        else:
            outfiles = seenfiles
        return outfiles

    def run_main():
        pass

def main():
    ap = HodorSlacker()
    ap.run_main()

if __name__ == '__main__':
    main()
