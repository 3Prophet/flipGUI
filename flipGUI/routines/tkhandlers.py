"""Handling opening and closing event for Tk application(saving and loading
defaults)"""

def handler(caller, fpath, attributes):
    """Saves selected attributes of the caller class into a file before closing
    the Tkinter GUI"""
    with open(fpath, "w") as f:
        for attribute in attributes:
            f.write("{} {}\n".format(attribute, getattr(caller, attribute).get()))
    #caller.parent.destroy()

def loader(caller, fpath):
    """Loads attributes from the file where they are stored in the form:
    attribute value"""
    try:
        with open(fpath, "r") as f:
            for line in f:
                attr_value =line.strip().split()
                if len(attr_value) == 1:
                    attr, value = attr_value[0], ""
                else:
                    attr, value = attr_value[0], attr_value[1]
                getattr(caller, attr).set(value)
    except:
        pass

