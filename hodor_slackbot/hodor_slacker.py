
import argparse
import json
import logging
import os
import sys

class HodorSlacker:

    def __init__(self,setroot=None):
        self._rootdir = '.'
        self._evdir = None
        self._statepath = None
        self._statefile = '.hodor_lastslack'
        self._log_path = None
        self._logbasename ='hodor_slacklog.txt'
        self._logger = None
        self._countmax = None
        if setroot is not None and os.path.exists(setroot):
            self._configure(setroot)


    def _configure(self,rootdir):
        self._rootdir = rootdir
        if not os.path.exists(self._rootdir):
            raise Exception('working directory not found')
        self._evdir = os.path.join(rootdir,'events')
        if not os.path.exists(self._evdir):
            raise Exception('event dir not found')
        self._statepath = os.path.join(self._rootdir,self._statefile)
        if not os.path.exists(self._statepath):
            fh = open(self._statepath,'w')
            fh.close()
        # setup logging
        FORMAT='%(asctime)-15s %(message)s'
        self._log_path = os.path.join(self._rootdir,self._logbasename)
        self._logger = None
        logging.basicConfig(
            filename=self._log_path,
            level=logging.INFO,
            format=FORMAT
        )
        self._logger = logging.getLogger('hodor_watcher')

    def process_arguments(self,arglist=None):
        prsr = argparse.ArgumentParser()
        prsr.add_argument('--root',required=True)
        opts = prsr.parse_args(arglist)
        if opts.root is not None and os.path.exists(opts.root):
            self._configure(opts.root)

    def console(self,msg):
        print(msg)

    def log(self,msg,*args,**kwargs):
        if self._logger is not None:
            self._logger.info(msg,*args,**kwargs)

    def record_lastseen(self,setpath):
        if not os.path.exists(setpath):
            raise ValueError('path {0} not found'.format(setpath))
        fh = open(self._statepath,'w')
        fh.write(setpath)
        fh.close()
        return True

    def get_lastseen(self):
        out = None
        try:
            if os.path.exists(self._statepath):
                lastpath = file(self._statepath).read()
                if os.path.exists(lastpath):
                    out = lastpath
        except TypeError:
            pass
        return out

    def find_new_events(self):
        lastseen = self.get_lastseen()
        lastfname = None
        if lastseen is not None:
            lastfname = os.path.basename(lastseen)
        seenfiles = []
        if self._evdir is not None:
            seenfiles = os.listdir(self._evdir)
        else:
            raise Exception('event directory not found')
        outfiles = None
        if lastseen is not None:
            outfiles = [p for p in seenfiles if p > lastfname]
        else:
            outfiles = seenfiles
        outpaths = [os.path.join(self._evdir,f) for f in outfiles]
        returnpaths = sorted(outpaths)
        return returnpaths

    def run_main(self,arglist=None):
        self.process_arguments(arglist)
        message_count = 0
        while True:
            if self._countmax is not None and message_count >= self._countmax:
                break
            recent = self.find_new_events()
            for ev_path in recent:
                ev_obj = None
                ev_obj = json.loads(file(ev_path).read(1024))
                msg = 'slacker caught: {0}'.format(ev_obj['message'])
                self.console(msg)
                self.log(msg)
                self.record_lastseen(ev_path)
                message_count += 1
                if self._countmax is not None:
                    if message_count >= self._countmax:
                        break
        return 0

def main():
    ap = HodorSlacker()
    sys.exit(ap.run_main())

if __name__ == '__main__':
    main()