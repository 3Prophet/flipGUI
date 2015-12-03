"""Collection of generators for parsing of file lines"""

import os
import fnmatch
import re

def gen_find(filepat, top, dig_recursive = None):
    """Yields files starting from top that do match filepat. Can walk
    reqursively through the directories"""
    for path, dirlist, filelist in os.walk(top):
        if not dig_recursive:
            dirlist = []
        for fname in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, fname)

def gen_open(filenames):
    """Yields fileobjects"""
    for name in filenames:
        yield open(name)

def gen_cat(sources):
    """Can be used for yielding lines from a bunch of file objects"""
    for s in sources:
        for line in s:
            yield line

def gen_grep(lines, re_compile_objects, yield_line = True):
    """Yields either lines that match one of the re.compile objects
    or result of applying re.compile_object.search(line). 
    re_compile_objects is a list of objects re.compile. If yield_line
    is set to False the program yields list of matchins search objects,
    that correspond to patterns in re_compile_objects! If there is a single 
    pattern use pop_it_fromlist afterwards
    to yield that single matching object"""
    for line in lines:
        re_search_list = filter (lambda res: True if res else False,
                map(lambda obj: getattr(obj,"search")(line), 
                    re_compile_objects))
        if re_search_list:
            if yield_line:
                yield line
            else:
                yield re_search_list

def pop_it_fromlist(re_search_lists):
    """If each of re_search lists contains just one object it yields that
    object"""
    for re_search_list in re_search_lists:
        re_search = re_search_list.pop()
        yield re_search

def gen_values(re_search_objs):
    for re_search in re_search_objs:
        yield re_search.groups()

def gen_typed_values(types, re_search_groups):
    for group_list in re_search_groups:
        yield map(lambda type_value_pair:
                type_value_pair[0](type_value_pair[1]),                
                zip(types, group_list))


def gen_dicts(keys, values_sequence):
    """generates dictionary for the result of passing a line through
    gen_search_objs"""
    for values in values_sequence:
        yield dict(zip(keys, values))

def numbers_from_flines(fpath, pattern, types):
    """Generalized procedure for parsing lines of the file
    according to patttern and converting them to types.
    pattern is instance of re.compile,
    types - tuple or list with types to which parsed fields have to be
    converted"""
    filenames = gen_find(os.path.basename(fpath), 
                                   os.path.dirname(fpath))
    fobjects = gen_open(filenames)
    lines = gen_cat(fobjects)
    re_search_lists = gen_grep(lines, [pattern], yield_line = False)

    pop_re_search = pop_it_fromlist(re_search_lists)

    values = gen_values(pop_re_search)
    typed_values = gen_typed_values(types, values)
    for typed_values_collection in typed_values:
        yield typed_values_collection


def dicts_from_flines(fpath, pattern, keys, types):
    """This creates dictionary for the line parsed according to 
    numbers_from_lines. Keys are a list or tuple of keys"""
    values = numbers_from_flines(fpath, pattern, types)
    for values_dict in gen_dicts(keys, values):
        yield values_dict
        
if __name__ == "__main__":
    pass
