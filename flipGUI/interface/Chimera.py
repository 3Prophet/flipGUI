"""This module runs Chimera interface"""

import requests
import subprocess
import os


class Chimera(object):
    def __init__(self):
        self._path_chimera = None
        self._port_nr = None
        self._url = None
        self._process = None

    def terminate(self):
        """Terminating Chimera"""
        if self._process:
            requests.post(self._url, params = { 'command': ['stop']})
            self._process.terminate()
            self._process = None

    def _start(self):
        """Starting Chimera server as a subprocess and retrieving its url"""
        self._process = subprocess.Popen(
                                [self._path_chimera, "--start", "RESTServer"],
                                 stdout = subprocess.PIPE,
                                 close_fds = True
                                        )
        #reading port nr on localhost
        self._port_nr = self._process.stdout.readline().strip().split()[-1]
        #creating url to communicate with chimera
        self._url = \
            "http://localhost:{port_number}/run".format(
                                            **{"port_number": self._port_nr})
    #def save_session(self, caller):
    #    if not self._process:
    #        pass
    #    else:
    #        requests.post(
    #            self._url,
    #            params = {'command': ['session {} save'.format(
    #                    os.path.join(caller.home_dir, caller.tag + ".py"))]}
    #            )
                        

    def update(self, caller, job = 'dF'):
        if not self._process:
            self._path_chimera = caller.visual_fpath
            self._start()
        requests.post(self._url, 
                params = {
                    'command': ['close #0;' +
                                'open {}_{}.xplor'.format(
                        os.path.join(caller.home_dir, caller.tag), job) ]})


        #requests.post(self._url, 
        #        params = {
        #            'command': ['close session;'+'open '+ \
        #        os.path.join(caller.home_dir, caller.tag+"_"+job+".xplor")]})

            
    




        
