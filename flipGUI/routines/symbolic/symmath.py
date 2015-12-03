"""Symbolic operations"""

import re

from flipGUI.routines.symbolic import parser

def invert_symop(symb):
    """ 'x,y,z' --> '-x,-y,-z'"""
    issymbol = lambda s: re.compile(r"[A-Za-z]+").search(s)
    isnumber = lambda s: re.compile(r"[+-]?\d+[./]?(\d+)?").search(s)
    iszero = lambda s: re.compile(r"[+-]*0").search(s)

    minus = "-"
    plus = "+"
    parsed_list = parser.Parser(symb)
    def invert_symbol(symb):
        """x -> -x"""
        if iszero(symb):
            return "0"
        if issymbol(symb):
            return symb
        if isnumber(symb):
            if minus in symb:
                return symb[1:]
            if plus in symb:
                return "-{}".format(symb[1:])
            else:
                return "-{}".format(symb)

    def invert_line(line):
        return map(invert_symbol, line)

    
    return parser.assemble(map(invert_line, parser.Parser(symb)))

    
    

