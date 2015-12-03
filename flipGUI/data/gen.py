import os
import re

out = open('groupsHM.py','w')
out.write("table = dict(\n")
pat = re.compile(r"(?P<nr>\d+)\s+(?P<HM>'.*')")

with open('groupsHM.txt','r') as f:
    for line in f:
        mob = re.search(pat, line)
        out.write("{}:{},\n".format(mob.group('nr'), mob.group('HM')))
out.write(")\n")
out.close()
