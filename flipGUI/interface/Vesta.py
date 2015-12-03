"""This module runs Vesta interface"""

import subprocess
import os
import sys
import threading

class Vesta(object):
    def __init__(self):
        self._path_vesta = None
        self._process = None
        self._vesta_file = None
        self._density_fpath = None
        self._peaks_fpath = None

    def terminate(self):
        """Terminating Vesta"""
        try:
            self._process.terminate()
        except:
            pass
        self._process = None

    def _start(self, caller, native_exists = True):
        """Starting Vesta as a subprocess"""
        if not native_exists:
            self._process = subprocess.Popen(
                                [#self._path_vesta,
                                    "open", self._density_fpath],
                                shell = False)                                     
        else:
            self._process = subprocess.Popen(
                                [#self._path_vesta,
                                    "open", self._vesta_file],
                                shell = False,
                                #stdin = subprocess.PIPE,
                                #stdout = subrocess.PIPE,
                                #stderr = subrpocess.PIPE
                                    close_fds = True
                                        )



    def update(self, caller, job = 'dF'):
        self._path_vesta = caller.visual_fpath

        #attempt to open native .vesta file(if it is in a refinement dir)
        try:
            self._vesta_file = os.path.join(caller.home_dir,
                                filter(lambda fname:\
                                        fname.endswith("_{}.vesta".format(job)),
                                os.listdir(caller.home_dir)).pop())
            
            self._start(caller)
        except:
            self._density_fpath = os.path.join(caller.home_dir, caller.tag +\
                                                "_{}.xplor".format(job))
            self._peaks_fpath = os.path.join(caller.home_dir, "peaks_dF.cif")

            self._start(caller, native_exists = False)
            

#class VestaProc(threading.Thread):
#    def __init__(self, fpath_vesta):
#        super(VestaProc, self).__init__()
#        self._fpath_vesta = fpath_vesta
#        self._stop = threading.Event()
#
#    def run(self):
#        self._process = subprocess.Popen(
#                                [self._path_vesta, self._density_fpath],
#                                shell = False) 
#
#    def stop(self):
#        self._stop.set()



            
    




        
