"""Parsing .ins and .fcf files to produce input for superflip and various
plotting"""

import os
import sys
import re
import math
import numpy

from flipGUI.routines.symbolic import symmath
from flipGUI.routines import generators
from flipGUI.data import groupsHM

def gen_fcf_list5(fpath):
    """Parses lines of .fcf file generated with LIST 5 into dictionaries:
        {'h':int(value), 'k': int(value), 'l': int(value),
          'Fo': float(value), 'Fc': float(value), 'phase_deg': float(value)}"""
    maps_keys = ('h', 'k', 'l', 'Fo','Fc', 'phase_deg')
    maps_types =(int, int, int, float, float, float) 
    line_pattern =  re.compile(
                          r'\s*(-?\d+)\s+(-?\d+)\s+(-?\d+)'\
                          r'\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*'\
                          )
    
    for parsed_line_dict in generators.dicts_from_flines(fpath, line_pattern,
                                    maps_keys, maps_types):
        yield parsed_line_dict

def gen_fo4sflip(fpath):
    """A line of reflections input corresponding
    'dataformat amplitude phase' for Fo synthesis"""
    for reflection_dict in gen_fcf_list5(fpath):
        yield "{:4d}{:4d}{:4d}{:10.2f}{:10.5f}\n".format(
                                        reflection_dict['h'],
                                        reflection_dict['k'],
                                        reflection_dict['l'],
                                        reflection_dict['Fo'],
                                        reflection_dict['phase_deg'] / 360.0
                                        )

def gen_fc4sflip(fpath):
    """A line of reflections input corresponding
    'dataformat amplitude phase' for Fc synthesis"""
    for reflection_dict in gen_fcf_list5(fpath):
        yield "{:4d}{:4d}{:4d}{:10.2f}{:10.5f}\n".format(
                                        reflection_dict['h'],
                                        reflection_dict['k'],
                                        reflection_dict['l'],
                                        reflection_dict['Fc'],
                                        reflection_dict['phase_deg'] / 360.0
                                        )


def gen_df_4sflip(fpath):
    """A line of reflections input corresponding
    'dataformat amplitude phase' for difference fourier"""
    for reflection_dict in gen_fcf_list5(fpath):
        dF = reflection_dict['Fo'] - reflection_dict['Fc']
        if dF < 0.0:
            phase =  ((reflection_dict['phase_deg'] / 360.0) + 0.5) % 1
            dF_abs = abs(dF)
        else:
            phase = reflection_dict['phase_deg'] / 360.0
            dF_abs = dF
        yield "{:4d}{:4d}{:4d}{:10.2f}{:10.5f}\n".format(
                                        reflection_dict['h'],
                                        reflection_dict['k'],
                                        reflection_dict['l'],
                                        dF_abs,
                                        phase
                                        )

def gen_fo_fc_2plot(fpath):
    """A line of reflections to be plotted by matplotlib"""
    for reflection_dict in gen_fcf_list5(fpath):
        yield [reflection_dict['Fo'], reflection_dict['Fc']]

def max_hkl_fcf_list5(fpath):
    dict_seqs = gen_fcf_list5(fpath) 
    hkl_abs = (map(abs, [dict_seq['h'], dict_seq['k'], dict_seq['l']])\
                                    for dict_seq in dict_seqs)
    
    return dict(zip(('h','k', 'l'), map(max,zip(*list(hkl_abs)))))


def centering_vecs(nr):
    """Lattice type: 1=P, 2=I, 3=rhombohedral obverse on hexagonal axes,
    4=F, 5=A, 6=B, 7=C. N must be made negative if the structure is 
    non-centrosymmetric."""
    centering_dict = {
                        1: "0 0 0",
                        2: "0 0 0\n0.5 0.5 0.5",
                        3: "0 0 0\n2/3 1/3 1/3\n1/3 2/3 2/3",
                        4: "0 0 0\n0 0.5 0.5\n0.5 0.5 0\n0.5 0 0.5",
                        5: "0 0 0\n0 0.5 0.5",
                        6: "0 0 0\n0.5 0 0.5",
                        7: "0 0 0\n0.5 0.5 0"
    }
    if nr not in centering_dict.keys():
        raise IndexError("Wrong number in the LATT field of your .ins/.res file!")
    return centering_dict[nr]

def parse_ins(fpath_ins):
    """Parses .ins file and returns information relevant for creation
    of .inflip file"""

    def dispatcher(list_matched_objects):
        """fills parsing_dict with key-value pairs"""
        parsing_dict = dict()
        for line in list_matched_objects:
            match_obj = line.pop()
            if match_obj.group('tag') in parsing_dict:
                parsing_dict[match_obj.group('tag')] += \
                        "\n{}".format(match_obj.group('value'))
            else:
                parsing_dict[match_obj.group('tag')] = match_obj.group('value')
        return parsing_dict

    tags = ['CELL', 'SYMM', 'LATT', 'LIST']
    re_compile_objs = map(lambda tag: \
            re.compile("(?P<tag>{})\\s+(?P<value>\\S+.*)".format(tag)), tags)
    filenames = generators.gen_find(os.path.basename(fpath_ins),
                                    os.path.dirname(fpath_ins))
    fobjects = generators.gen_open(filenames)
    lines = generators.gen_cat(fobjects)
    list_matched_objects = generators.gen_grep(lines, re_compile_objs,
                                                yield_line = False)
    parsing_dict  = dispatcher(list_matched_objects)
    return parsing_dict




def gen_inflip_from_ins(fpath_ins, fpath_inflip, purpose, voxel = 'AUTO'):
    """generates .inflip file from .ins file"""
    def commands_inflip():
        inflip_inp = "{fname}\noutputfile {fname}_{job}.xplor\n"\
                     "outputformat xplor\nexpandedlog yes\n"\
                     "#coverage no\nperform fourier\ncell {cell}\n"\
                     "dimension 3\nrealdimension 3\nvoxel {voxel}\ncenters\n"\
                     "{centers}\nendcenters\nsymmetry\n{symmetry}\n"\
                     "endsymmetry\n#Keywords for charge flipping\n"\
                     "#delta AUTO\n#weakratio 0.000\n#Biso 0.000\n"\
                     "#polish yes 200\n#randomseed AUTO\n#derivesymmetry no\n"\
                     "#searchsymmetry average\n"\
                     "dataformat amplitude phase\n".format(**inflip_dict)
        for line in inflip_inp.split("\n"):
            yield line

    def reflections_inflip():
        yield "fbegin\n"
        for line in purposes[purpose](fpath_fcf):
            yield line
        yield "endf\n"
    
    def centers():
        return  centering_vecs(abs(eval(parsing_dict['LATT'])))

    def symmetry():
        """Generates centers and symmetry for inflip"""
        hasinversion = lambda parsing_dict: eval(parsing_dict['LATT']) > 0
        symmops = 'x,y,z\n' + parsing_dict["SYMM"]

        #this adds inverted symmetry operations in case LATT is less than 0        
        if hasinversion(parsing_dict):
            symmops += "\n{}".format(
                "\n".join(map(symmath.invert_symop, symmops.split("\n"))))

        return symmops

    def cell():
        return "{} {} {} {} {} {}".format(
                                *parsing_dict["CELL"].strip().split()[1:]
                                )

    def dispatcher(list_matched_objects):
        """fills parsed_dict with key-value pairs"""
        parsing_dict = dict()
        for line in list_matched_objects:
            match_obj = line.pop()
            if match_obj.group('tag') in parsing_dict:
                parsing_dict[match_obj.group('tag')] += \
                        "\n{}".format(match_obj.group('value'))
            else:
                parsing_dict[match_obj.group('tag')] = match_obj.group('value')
        return parsing_dict

    def check_list():
        return parsing_dict['LIST'] == 5

        
    inflip_dict = dict()

    purposes = {
                'Fo': gen_fo4sflip,
                'Fc': gen_fc4sflip,
                'dF': gen_df_4sflip
            }
    assert purpose in purposes.keys()
    
    fpath_fcf = fpath_ins.rsplit(".ins")[0] + ".fcf"
    tags = ['CELL', 'SYMM', 'LATT', 'LIST']
    re_compile_objs = map(lambda tag: \
            re.compile("(?P<tag>{})\\s+(?P<value>\\S+.*)".format(tag)), tags)
    filenames = generators.gen_find(os.path.basename(fpath_ins),
                                    os.path.dirname(fpath_ins))
    fobjects = generators.gen_open(filenames)
    lines = generators.gen_cat(fobjects)
    list_matched_objects = generators.gen_grep(lines, re_compile_objs,
                                                yield_line = False)
    parsing_dict  = dispatcher(list_matched_objects)
    
    inflip_dict['job'] = purpose
    inflip_dict['fname'] = os.path.basename(fpath_ins).rsplit(".ins")[0]
    inflip_dict['cell'] = cell()
    inflip_dict['centers'] = centers()
    inflip_dict['symmetry'] = symmetry()
    inflip_dict['voxel'] = voxel

    with open(fpath_inflip, 'w') as f:
        for line in commands_inflip():
            f.write(line + "\n")
        for line in reflections_inflip():
            f.write(line)


def difference_peaks(fpath_res):
    """Saves peaks from difference Fourier(liested in .res) into peaks.cif"""

    def cell():
        cell_str = "_cell_length_a              {}\n"\
                   "_cell_length_b              {}\n"\
                   "_cell_length_c              {}\n"\
                   "_cell_angle_alpha           {}\n"\
                   "_cell_angle_beta            {}\n"\
                   "_cell_angle_gamma           {}".format(
                                *parsing_dict["CELL"].strip().split()[1:])
        for line in cell_str.split("\n"):
            yield line

    #def group_HM():
    #    yield "_symmetry_space_group_name_H-M    '{}'\n".format(
    #                                                sgnr)
    #                                                    #groupsHM.table[sgnr])
    #    #yield "_symmetry_Int_Tables_number        {}\n".format(sgnr)
    def symops_from_cif():
        yield "loop_\n" 
        yield "_symmetry_equiv_pos_as_xyz\n"
        filenames = generators.gen_find(
                os.path.basename(fpath_res).rsplit(".res")[0] + ".cif",
                os.path.dirname(fpath_res))
        fobjects = generators.gen_open(filenames)
        lines = generators.gen_cat(fobjects)

        
        patt = patt =re.compile(r"('[^,'()]+,[^,'()]+,[^,'()]+')")
        for line in lines:
            mobj = re.search(patt, line)
            if mobj:
                yield line


    def loop_atom():
        yield "loop_\n"
        yield "_atom_site_label\n"
        yield "_atom_site_type_symbol\n"
        yield "_atom_site_fract_x\n"
        yield "_atom_site_fract_y\n"
        yield "_atom_site_fract_z\n"

    def density_peaks():
        for matchobj in parsing_dict["PEAKS"]:
            yield " {}  {}  {}  {}  {}\n".format(
                                                 matchobj.group(1),
                                                 'He',
                                                 matchobj.group(3),
                                                 matchobj.group(4),
                                                 matchobj.group(5),
                                                 matchobj.group(6))

    re_compile_objs = (
                        re.compile("\s*(CELL)(.*)"),
                        re.compile(
                          r'\s*(Q\d+)\s+(\d+)'\
                          r'\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)'\
                          r'\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*'))


    
    parsing_dict = dict()

    filenames = generators.gen_find(os.path.basename(fpath_res),
                                       os.path.dirname(fpath_res))
    fobjects = generators.gen_open(filenames)
    lines = generators.gen_cat(fobjects)
    list_matched_objects = generators.gen_grep(lines, re_compile_objs,
                                                yield_line = False)
    poped_objs = generators.pop_it_fromlist(list_matched_objects)
    
    for obj in poped_objs:
        if obj.group(1) == "CELL":
            parsing_dict["CELL"] = obj.group(2)
        else:
            parsing_dict.setdefault("PEAKS", []).append(obj)

    peaks_fpath = os.path.join(os.path.dirname(fpath_res), "peaks.cif")

    with open(peaks_fpath, 'w') as f:
        f.write("data_{}\n".format(os.path.basename(fpath_res)))
        for line in cell():
            f.write(line + "\n")
        for line in symops_from_cif():
            f.write(line)
        for line in loop_atom():
            f.write(line)
        for line in density_peaks():
            f.write(line)


if __name__ == "__main__":
    difference_peaks("/Users/dima/Projects/flipGUI/tests/organic/benz-01.res")
    #print parse_ins("/Users/dima/Projects/flipGUI/tests/inputfiles/struct.res")
        
