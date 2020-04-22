
import argparse
import json
import logging
import os
import re
import subprocess
import sys
import yaml


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
        self._slack_ep_url = None

    def _configure(self,rootdir):
        self._rootdir = rootdir
        if not os.path.exists(self._rootdir):
            raise Exception('working directory not found')
        self._evdir = os.path.join(self._rootdir,'events')
        if not os.path.exists(self._evdir):
            raise OSError('event dir {0} not there'.format(self._evdir))
        self._statepath = os.path.join(self._rootdir,self._statefile)
        if not os.path.exists(self._statepath):
            fh = open(self._statepath,'w')
            fh.close()
        self._configpath = os.path.join(
            self._rootdir,
            '.hodor_slacker_config.yml'
        )
        if os.path.exists(self._configpath):
            cfg_obj = yaml.load(open(self._configpath).read(2048))
            self._slack_ep_url = cfg_obj['slack_endpoint']
        # setup logging
        FORMAT='%(asctime)-15s %(message)s'
        logdir = os.path.join(self._rootdir,'log')
        self._log_path = os.path.join(logdir,self._logbasename)
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

    def clean_msg_for_slack(self,msg):
        safe_msg = re.sub(r'[^ A-Za-z0-9-_().]','',msg)
        return safe_msg

    def slackit(self,msg):
        safe_msg = self.clean_msg_for_slack(msg)
        json_payload = json.dumps({'text':safe_msg})
        cmdlist = [
            'curl',
            '-X',
            'POST',
            '-H',
            'Content-type: application/json',
            '--data',
            "{0}".format(json_payload),
            self._slack_ep_url
        ]
        print(repr(cmdlist))
        retval = subprocess.call(cmdlist)
        return retval

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
                with open(self._statepath,'r') as fh:
                    lastpath = fh.read()
                    if os.path.exists(lastpath):
                        out = lastpath
        except TypeError:
            pass
        return out

    def find_new_event_names(self):
        lastseen = self.get_lastseen()
        lastfname = None
        if lastseen is not None:
            lastfname = os.path.basename(lastseen)
        seenfiles = []
        if self._evdir is not None:
            seenfiles = os.listdir(self._evdir)
        else:
            raise OSError('event dir {0} not found'.format(self._evdir))
        outfiles = None
        if lastseen is not None:
            outfiles = [p for p in seenfiles if p > lastfname]
        else:
            outfiles = seenfiles
        outpaths = [f for f in outfiles]
        returnpaths = sorted(outpaths)
        return returnpaths

    def find_new_events(self):
        names = self.find_new_event_names()
        paths = [os.path.join(self._evdir,n) for n in names]
        return paths

    def run_main(self,arglist=None):
        self.process_arguments(arglist)
        message_count = 0
        while True:
            if self._countmax is not None and message_count >= self._countmax:
                break
            recent = self.find_new_events()
            for ev_path in recent:
                ev_text = None
                ev_obj = None
                msg = None
                try:
                    ev_fh = open(ev_path,'r')
                    ev_text = ev_fh.read(1024)
                    ev_fh.close()
                    ev_obj = json.loads(ev_text)
                    msg = '{0}'.format(ev_obj['message'])
                except:
                    err_tpl = \
                        'READ ERROR ev_path: {0} text "{1}" obj {2!r} msg {3}'
                    err_msg = err_tpl.format(
                        ev_path,
                        ev_text,
                        ev_obj,
                        msg
                    )
                    self.console(err_msg)
                    self.log(err_msg)
                if msg is None:
                    self.record_lastseen(ev_path)
                    continue
                self.console(msg)
                self.log(msg)
                rc = self.slackit(msg)
                slackresultmsg = 'slack curl returned {0}'.format(rc)
                self.console(slackresultmsg)
                self.log(slackresultmsg)
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
