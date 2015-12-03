import tempfile
import shutil
import os

def pytest_funcarg__adapter(request):
    #class Adapter(object):
    #    """Adapter object to emulate any class where attributes have set and
    #    get method"""
    #    class JavaLike(object):
    #        """Class which instances have set() and get() """
    #        def __init__(self, value)
    #            self.attr = value
    #        def get(self):
    #            return self.attr

    #        def set(self, value)
    #            self.attr = value
    #    def __init__(self, 
def in_path(self, program = None):
    """Returns true if the program is in the search PATH"""
            
    path = os.environ['PATH']
    
        assert program != None
        
        for item in path.split(":"):
            if os.path.exists(os.path.join(item,program)) and\
            not os.path.isdir(os.path.join(item,program)):
                return True
        return False

def pytest_funcarg__tempdir(request):
    """Creating temporary directory for testing"""
    tdir = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(tdir)

    request.addfinalizer(cleanup)
    return tdir




