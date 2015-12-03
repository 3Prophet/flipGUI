import shutil
import tempfile
import os
import Tkinter
import ttk
import threading

from flipGUI.interface import FlipGUI

def pytest_funcarg__empty_dir(request):
    """Creating temporary empty directory to run the test"""
    def setup():

        current = os.path.dirname(os.path.realpath(__file__))
        return tempfile.mkdtemp(dir = current)
    
    def cleanup(tdir):
        shutil.rmtree(tdir)

    return request.cached_setup(
                                setup = setup,
                                teardown = cleanup,
                                scope = "session"
                                )

def pytest_funcarg__flipgui(request):
    """Creating flipGUI.interface.FlipGUI.FlipGUI instance
    for running tests"""

    def setup():
        root = Tkinter.Tk()
        gui = FlipGUI.FlipGUI(root)

        #running root.mainloop() in a separate thread
        t_main = threading.Thread(
                target = root.mainloop,
                args = ()
                )
        t_main.start()

        return gui 

    def cleanup(gui):
        gui.b_exit.invoke() 

    return request.cached_setup(
                                setup = setup,
                                teardown = cleanup,
                                scope = "session"
                                )
        
def pytest_funcarg__button_editing(request):
    return ("Open .ins", "Open .res", "Open .lst")

def pytest_funcarg__button_refinement(request):
    return ("Refine", ".res -> .ins", "duplicate .ins", "plot Fo/Fc" )

def pytest_funcarg__button_maps(request):
    return ('Fobs', 'Fcalc', 'diffF')
