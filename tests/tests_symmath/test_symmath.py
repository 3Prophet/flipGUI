"""Tests functionality of funcitons from flipGUI.routines.symbolic.symmath
module"""

from flipGUI.routines.symbolic import symmath

def pytest_funcarg__symops_inv(request):
    """alternative representation of symops_inv list"""
    return ['-x,-y,-z', '-x,-z,-y','x,-y,-z', '2x,-y,-z', '-x,-y,z-1/2',
                           '-x,-y,2z-1/2', '-1/2x,-y,-z', '-y,-x,-1/2+z' ]

def pytest_funcarg__symops_inv_sec(request):
    """alternative representation of symops_inv list"""
    return ['-x,-y,-z', '-x,-z,-y','x,-y,-z', '2x,-y,-z', '-x,-y,-1/2+z',
                           '-x,-y,-1/2+2z', '-1/2x,-y,-z', '-y,-x,z-1/2' ]

def test_invert(symops, symops_inv, symops_inv_sec):
    """Tests symmath.invert_symop that iverts symbolic operation"""
    for nr, symop in enumerate(symops):
        inverted = symmath.invert_symop(symop)
        assert any([inverted == symops_inv[nr], 
                    inverted == symops_inv_sec[nr]])

def test_invert_twice(symops, symops_sec):
    """Confirms that double inversion does not change symbolic operation"""
    for nr, symop in enumerate(symops):
        double_inverted = symmath.invert_symop(
                                symmath.invert_symop(symop))
        assert any([double_inverted == symop,
                    double_inverted == symops_sec[nr]])



