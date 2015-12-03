"""Parsing symbolic operations and reversing the result of parsing"""

import re

class Parser(list):
    """Example of what it does: '-x,2y,z+1/2'--->[['-1','x','0'],
                                                  ['2','y','0'],
                                                  ['1','z','1/2']]
    It returns list which entries contain results of parsing.
    """

    def __init__(self, symop):
        """Symop has to be of the form '-x,2y,z' """
        self._symop = symop.lower()
        self._parsed = self.__call__()
        super(Parser, self).__init__(self._parsed)
        
    def __call__(self):
        """Returns the final result upon the call"""
        tags = self._tags()
        rt_pairs_start = self._rt_pairs_start(tags)
        rt_mult_order = self._rt_mult_order(rt_pairs_start)
        return [item for item in rt_mult_order]

    def _tags(self):
        """  1-x,y+1,-z'--> ['1-x','y+1','-z']"""
        for item in self._symop.strip().split(','):
            yield item.strip()

    def _rt_pairs_start(self, tags):
        """ '-1/2x+1' --->['-1/2x','+1']
                 '-x' --->['-x']
                 etc...
        """
        for tag in tags:
            #removing white spaces: '- 1/2 x + 1' ---> '-1/2x+1'
            tag = "".join(tag.strip().split())
            #separating rotational from translational parts
            #rt_list_start = re.split(r'([+-]?(?:\d+)?/?(?:\d+)?[xyz])',
            #                            tag.strip())
            rt_list_start =\
                    re.split(r'([+-]?(?:\d*.\d+)?(?:\d+)?/?(?:\d+)?[xyz])', 
                                        tag.strip())
            cleaned = filter(lambda item: item != "", rt_list_start)
            yield cleaned

    def _rt_mult_order(self, rt_list_start):
        """ ['-1/2x','+1'] ---> ['-1/2','x','1'] 
                    ['-x'] ---> ['-1','x','0']
                                [multiplier, [xyz], translation]   
        """
        test_set = set('xyz')
        for alist in rt_list_start:
            rt_mult_order = [None, None, None] #[multiplier, [xyz], translation]
            for item in alist:
                if not test_set.isdisjoint(set(item)):  #if contains x,y or z 
                    patt = re.compile(r'(?P<sign>[+-]?)(?P<mult>[+-]?'\
                                      r'(?:\d+)?/?(?:\d+)?)(?P<let>[xyz])')
                    parsed = re.search(patt, item)
                    if parsed.group('mult') == '':
                        if parsed.group('sign') == '':
                            rt_mult_order[0] = '1'
                        else:
                            rt_mult_order[0] = parsed.group('sign')+'1'
                    else:
                        if parsed.group('sign') == '':
                            rt_mult_order[0] = parsed.group('mult')
                        else:
                            rt_mult_order[0] = parsed.group('sign')+\
                                            parsed.group('mult')
                    rt_mult_order[1] = parsed.group('let')
                else:                                   #if translation
                    rt_mult_order[2] = item
            if rt_mult_order[-1] == None:               #if no translation
                rt_mult_order[-1]  = '0'
            if "+" in rt_mult_order[-1]:
                rt_mult_order[-1] =\
                    re.search(re.compile(r"\+(.*)"), rt_mult_order[-1]).group(1)
            yield rt_mult_order

def assemble(parsed_list):
    """Reverses what Parser class does:"""

    iszero = lambda x: re.compile(r"[+-]*0").search(x)

    def rotate(line):
        if line[0] == "-1":
            return "-{}".format(line[1])
        elif line[0] == "1":
            return line[1]
        else:
            return "{}{}".format(line[0], line[1])

    def translate(line):
        if iszero(line[-1]):
            return ""
        else:
            return line[-1] 

    def assemble_line(rot, tr):
        """Assembles results of rotate and translate"""
        if tr == "": 
            return rot
        minus = "-"
        if  minus in tr and minus not in rot:
            return rot + tr
        if minus in rot and minus not in tr:
            return tr + rot
        else:
            return rot + tr

    def assemble_result(inp_list):
        return ",".join(
                    map(lambda line: assemble_line(rotate(line),
                                     translate(line)),
                                inp_list))

    return assemble_result(parsed_list)
    

   
if __name__ == "__main__":
    for symop in ['x, y,  z', 'x,z ,y','- x,y, z', '-2x ,y ,z', 'x,y, 1/2 - z',
            'x ,y,1/2 -2z', '1/2x  ,y ,z', 'y, x, -z + 1/2' ]:
        
        print symop, Parser(symop)
