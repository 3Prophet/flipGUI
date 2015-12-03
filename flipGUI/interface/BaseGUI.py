"""Class that implements some basic functionality of GUI object: runs processes
displays messages and checks paths"""

import Tkinter
import ttk
import subprocess
import os
import sys
import tkFileDialog

class BaseGUI(object):
    """Class for the superflip GUI object"""
    def __init__(self, parent):
        """Class that provides some basic functionality for Tkinter to be 
        inherited by subclusses."""
        #------------- CREATING MAINFRAME--------------------------------------
        self.parent = parent
        self.parent.columnconfigure(0, weight = 1)
        self.parent.rowconfigure(0, weight = 1)


        self.mainframe = ttk.Frame(self.parent, padding = 3)
        self.mainframe.grid(column = 0, row = 0,
                            sticky = ("n", "w", "e", "s"))


        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)

        #------------- OPTIONS FOR OPENING OR SAVING FILES---------------------
        self.file_opt = options = {}
        options['initialdir'] = '/'

        #------------- OPTIONS FOR OPENING A DIRECTORY-------------------------
        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = '/'
        options['mustexist'] = False

    #-----------------FUNCTIONS------------------------------------------------

    def get_dirname(self):
        """Returns directoryname."""
        return tkFileDialog.askdirectory(**self.dir_opt)

    def get_filename(self):
        """Returns a  file name"""
        return tkFileDialog.askopenfilename(**self.file_opt)
    

    def fpath_input_exists(self, fpath, attr):
        """Checks wheather fpath exists and it is a file. attr should be an 
        instance of Tkinter.Text """
        if not os.path.exists(fpath):
            self.display_message(attr, 
                ["\nERROR!",
                "INPUT FILE: '{}' DOES NOT EXIST!\n".format(fpath)])
            sys.exit(1)

        if not os.path.isfile(fpath):
            self.display_message(attr, 
                    ["\nERROR!",
                     "INPUT: '{}' IS NOT A FILE!\n".format(fpath)])
            sys.exit(1)
        return True
    
    def display_message(self, attr, message):
        """Displays a message(iterable object) on an attr that has to be an
        instance of Tkinter.Text. Checks for the presence
        of word 'error' in the message.
        """
        ref2attr = getattr(self, attr)
        error_pattern = "error"
        error_presence = 0

        #discriminates subprocess.PIPE instances from container messages
        if callable(message):
            message_iter = iter(message, "")
        else:
            message_iter = iter(message)

        for line in message_iter:
            if error_pattern in line.lower():
                error_presence = 1
            ref2attr.insert('end',line)
            ref2attr.see('end')
            ref2attr.update_idletasks()
        return error_presence

    def run_process(self, proc_fpath, inp_fpath,  
                    attr = None,
                    redirect_out = False,
                    redirect_err = False,
                    wait = True):
        """Runs a process in and redirects stdout and stderr  to attr, which 
        should be an instance of Tkinter.Text"""
        if not os.path.exists(proc_fpath):
            self.display_message(attr, 
                   ["\nERROR!", 
                    "EXECUTABLE: '{}' DOES NOT EXIST!\n".format(proc_fpath)])

            self.display_message(attr, 
                                ["--SOLUTION: CHECK SOFTWARE PATHS.\n"])
            sys.exit(1)                    

        if not os.path.isfile(proc_fpath):
            self.display_message(attr, 
                    ["\nERROR!", 
                     "EXECUTBLE: '{}' IS NOT A FILE!\n".format(proc_fpath)])
            self.display_message(attr, 
                    ["--SOLUTION: CHECK SOFTWARE PATHS.\n"])
            sys.exit(1)

        process = subprocess.Popen([proc_fpath, inp_fpath],
                                    cwd = os.path.dirname(inp_fpath),
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
        
        if attr and redirect_out:
            exit_status_out =\
                self.display_message('txt_progress', process.stdout.readline)

        if attr and redirect_err:
            exit_status_err =\
                self.display_message('txt_progress', process.stderr.readline)

        if wait:
            process.wait()
        return int(any([exit_status_out, exit_status_err]))   

