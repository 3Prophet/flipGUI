"""Tests functionality of funcitons from flipGUI.routines.symbolic.parser
module"""

from flipGUI.routines.symbolic import parser

def test_Parser(symops, parseresult):
    """Tests correctness of  Parser class action upon symop"""
    for nr, symop in enumerate(symops):
        assert parser.Parser(symop) == parseresult[nr]

def test_Parser_cap(symops_cap, parseresult):
    """Tests correctness of Parser class action upon capitalized symops"""
    for nr, symop in enumerate(symops_cap):
        assert parser.Parser(symop) == parseresult[nr]

def test_Parser_spaced(symops_spaced, symops):
    """Tests correctness of Parser class action upon spaced symops"""
    for nr, symop in enumerate(symops):
        assert parser.Parser(symop) == parser.Parser(symops_spaced[nr])

def test_assemble(symops, symops_sec):
    """Test, which checks correctness of function parser.assemble, 
    which reverses what parser.Parser does"""
    for nr, symop in enumerate(symops):
        #reverting parsing result
        back = parser.assemble(parser.Parser(symop))
        assert any([ back == symops[nr], back == symops_sec[nr]])


