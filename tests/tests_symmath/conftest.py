def pytest_funcarg__symops(request):
    """some symmmetry operations in symbolic form"""
    return ['x,y,z', 'x,z,y','-x,y,z', '-2x,y,z', 'x,y,1/2-z',
                'x,y,1/2-2z', '1/2x,y,z', 'y,x,-z+1/2' ]

def pytest_funcarg__symops_sec(request):
    """alternative representation of symops list"""
    return ['x,y,z', 'x,z,y','-x,y,z', '-2x,y,z', 'x,y,-z+1/2',
                           'x,y,-2z+1/2', '1/2x,y,z', 'y,x,1/2-z' ]

def pytest_funcarg__symops_cap(request, symops):
    """capitalized symops"""
    return map(lambda symop: symop.capitalize(), symops)

def pytest_funcarg__symops_spaced(request):
    """symops with introduced spaces"""
    return ['x, y,  z', 'x,z ,y','- x,y, z', '-2x ,y ,z', 'x,y, 1/2 - z',
                'x ,y,1/2 -2z', '1/2x  ,y ,z', 'y, x, -z + 1/2' ]


def pytest_funcarg__parseresult(request):
    """This is how parser.Parser suppose to parser symops."""
    return [
        [['1', 'x', '0'], ['1', 'y', '0'], ['1', 'z', '0']],
        [['1', 'x', '0'], ['1', 'z', '0'], ['1', 'y', '0']],
        [['-1', 'x', '0'], ['1', 'y', '0'], ['1', 'z', '0']],
        [['-2', 'x', '0'], ['1', 'y', '0'], ['1', 'z', '0']],
        [['1', 'x', '0'], ['1', 'y', '0'], ['-1', 'z', '1/2']],
        [['1', 'x', '0'], ['1', 'y', '0'], ['-2', 'z', '1/2']],
        [['1/2', 'x', '0'], ['1', 'y', '0'], ['1', 'z', '0']],
        [['1', 'y', '0'], ['1', 'x', '0'], ['-1', 'z', '1/2']]
        ]


