"""Implementation of flipGUI"""

import Tkinter 
import ttk
import subprocess
import os
import sys
import fnmatch
import numpy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,\
                                                    NavigationToolbar2TkAgg
import flipGUI.routines.shelx
import flipGUI.routines.tkhandlers
from flipGUI.interface import BaseGUI
from flipGUI.interface import Chimera, Vesta

class FlipGUI(BaseGUI.BaseGUI, object):
    """Class for the superflip GUI object"""
    def __init__(self, parent):
        """Initializing widgets"""
        super(FlipGUI, self).__init__(parent)

        #------------------------CREATING NOTEBOOK WITH PANELS-----------------

        self.nbook = ttk.Notebook(self.mainframe)

        self.f_paths = ttk.Frame(self.nbook, padding = 5)
        self.f_jobs = ttk.Frame(self.nbook, padding = 5)
        self.f_jobs.columnconfigure(1, weight = 1)
        self.f_jobs.rowconfigure(1, weight = 1)
        self.f_jobs.update_idletasks()

        self.nbook.add(self.f_paths, text = "Paths and locations")
        self.nbook.add(self.f_jobs, text = "Jobs")
        self.nbook.grid(row = 0, column = 0, sticky = ("w","s","n","e"))
        self.nbook.columnconfigure(0, weight = 1)
        self.nbook.rowconfigure(0, weight = 1)

        #-------------- ENTRY VARIABLES----------------------------------------
        
        self._path_superflip = Tkinter.StringVar()
        self._path_editor = Tkinter.StringVar()
        self._path_shelx = Tkinter.StringVar()
        self._path_visual = Tkinter.StringVar()
        self._path_ins = Tkinter.StringVar()
        self._voxel = Tkinter.StringVar()

        self._path_superflip.set("")
        self._path_shelx.set("")
        self._path_editor.set("")
        self._path_visual.set("")
        self._path_ins.set("")
        self._voxel.set("AUTO")

        #--------------CHIMERA SERVER/VESTA------------------------------------------
        self._visual = None        
              
        #--------------COMMON BUTTONS------------------------------------------
        #Name of the file to store defaults
        self._path2defaults = 'defaults'
        
        self.f_combut = ttk.Frame(self.mainframe, padding = (20,5,10,5))
        self.f_combut.grid(row = 1, column =0, sticky = ("n", "w", "e", "s"))

        #Button for loading defaults
        self.b_loaddef = ttk.Button(self.f_combut, width = 15, 
                                            text = "Load from defaults",
                                            command = lambda caller = self:\
            flipGUI.routines.tkhandlers.loader(caller, caller._path2defaults))
        self.b_loaddef.grid(row = 0, column = 0)
        
        #Button for saving defaults
        self.b_savedef = ttk.Button(self.f_combut, width = 14,
                                        text = "Save to defaults",
                                        command = lambda caller = self,\
                                            fpath = self._path2defaults,
                                            attributes = (
                                                        '_path_superflip',
                                                        '_path_shelx',
                                                        '_path_editor',
                                                        '_path_visual',
                                                        '_path_ins'
                                                        ):\
                flipGUI.routines.tkhandlers.handler(caller, fpath, attributes))
        self.b_savedef.grid(row = 0, column = 1)
        
        self.b_exit = ttk.Button(self.f_combut , text = "EXIT",
                                    command = self.destroy)
        self.b_exit.grid(row = 0, column = 2)
        
        #--------------LOADING DEFAULTS FOR SOFTWARE AND .ins FILE PATHS-------

        
        #initialization of default vaues
        #flipGUI.routines.tkhandlers.loader(self, self._path2defaults)


        #--------ASSEMBLING NOTEBOOK PAGE PATHS AND LOCATIONS------------------

        labelframe_titles_paths = ("Software paths (binaries)", "Locations")

        label_software_titles = ("Superflip", "SHELX/SHELXL", "Editor", "Chimera/Vesta")
        entry_software_textvar = \
                (self._path_superflip, self._path_shelx, self._path_editor,
                                        self._path_visual)

        button_software_text = ("Select" , "Select", "Select", "Select")
        button_software_commands = map(lambda textvar:\
                                            lambda attr = textvar:\
                                            attr.set(self.get_filename()),
                                            entry_software_textvar)

        label_locations_titles = ("Your .ins file",)
        entry_locations_titles = (self._path_ins,)

        button_locations_text = ("select",)
        button_locations_commands = (lambda attr = self._path_ins:\
                                            attr.set(self.get_filename()),)
        l_e_b_dict = dict(
                        zip(labelframe_titles_paths,
                            (zip(label_software_titles,
                                entry_software_textvar,
                                button_software_text,
                                button_software_commands),
                             zip(label_locations_titles,
                                 entry_locations_titles,
                                 button_locations_text,
                                 button_locations_commands))))


        for lf_row, lf_title in enumerate(labelframe_titles_paths):
            lf = ttk.Labelframe(self.f_paths, text = lf_title, padding = 10)
            lf.grid(row = lf_row, column = 0, sticky = "we")

            for leb_row, l_e_b in enumerate(l_e_b_dict[lf_title]):
                l = ttk.Label(lf, text = l_e_b[0], padding = (0, 20, 0, 15))
                l.grid(row = leb_row, column = 0)

                e = ttk.Entry(lf, width = 20, textvariable = l_e_b[1],
                                                    justify = "right")
                e.grid(row = leb_row, column = 1)

                b = ttk.Button(lf, width = 6, text = l_e_b[2], 
                                            command = l_e_b[3])
                b.grid(row = leb_row, column = 2, sticky = ("e", "w"))
                               
        #--------ASSEMBLING NOTEBOOK PAGE JOBS---------------------------------

        self.f_editing = ttk.Frame(self.f_jobs)
        self.f_editing.grid(row = 0, column = 0, sticky = ("n","e","s","w"))

        self.f_progress = ttk.Frame(self.f_jobs)
        self.f_progress.grid(row = 0, column = 1, rowspan =2,
                                                sticky = ("n","e","s","w"))
        self.f_progress.rowconfigure(1, weight = 1)
        self.f_progress.columnconfigure(0, weight = 1)
        
        labelframe_titles_jobs = ("Editing", "Refinement", "Density maps")

        button_editing_text = ("Open .ins", "Open .res", "Open .lst")
        button_editing_commands = (lambda proc = self.open_with_editor,\
                                          attr = 'txt_progress':\
                                          proc(self.ins_fpath,attr),
                                   lambda proc = self.open_with_editor,\
                                          attr = 'txt_progress':\
                                          proc(self.res_fpath,attr),
                                   lambda proc = self.open_with_editor,\
                                          attr = 'txt_progress':\
                                          proc(self.lst_fpath,attr))
        

        button_refinement_text = ("Refine", ".res -> .ins", "duplicate .ins",
                                                                 "plot Fo/Fc" )
        button_refinement_commands = \
                    map(lambda proc: \
                                lambda attr = 'txt_progress': proc(attr),\
                    (self.refine,self.res2ins, self.copy_ins, self.plot_fo_fc))
        
        button_maps_text = ('Fo', 'Fc', 'dF')
        button_maps_commands = \
                    map(lambda job: \
                                lambda attr = 'txt_progress':\
                                    self.fourier(attr, job, self._voxel.get()),
                    ('Fo', 'Fc', 'dF'))

        l_b_dict = dict(
                        zip(labelframe_titles_jobs,
                            (zip(button_editing_text,
                                 button_editing_commands),
                             zip(button_refinement_text,
                                 button_refinement_commands),
                             zip(button_maps_text,
                                 button_maps_commands))))

        #Dictionary for buttons
        self.button_dict = dict()

        for lf_row, lf_title in enumerate(labelframe_titles_jobs):
            lf = ttk.Labelframe(self.f_editing, text = lf_title, padding = 10)
            lf.grid(row = lf_row, column = 0, sticky = ("n", "s"), padx = 5)

            for b_row, b_c in enumerate(l_b_dict[lf_title]):
                b = ttk.Button(lf, width = 10, text = b_c[0], 
                                                command = b_c[1])
                b.grid(row = b_row, column = 0)
                self.button_dict[b_c[0]] = b

        #adding VOXEL entry
        self.lf_voxel = ttk.Labelframe(self.f_editing, text = "VOXEL", 
                                                    padding = (20, 5))
        self.lf_voxel.grid(row = 3, column = 0, sticky = ("w", "e"), padx = 5)

        self.e_voxel = ttk.Entry(self.lf_voxel, width = 10, 
                        textvariable = self._voxel, justify = "center" )
        self.e_voxel.grid(row = 0, column = 0, sticky = ("n", "s", "w", "e"))
 
        #-------------CREATING TEXT PANEL TO REDIRECT OUTPUT-------------------
        
        self.lf_progress = ttk.Labelframe(self.f_progress, 
                                        text = "Progress pane", padding = 10)
        self.lf_progress.grid(row = 0, column = 0, rowspan = 5,
                                                    sticky = ("n","e","w","s"))
                       
        self.lf_progress.columnconfigure(0, weight = 1)
        self.lf_progress.rowconfigure(0, weight = 1)                       
                       
        
        self.txt_progress = Tkinter.Text(self.lf_progress, height = 10)
        self.txt_progress.insert("1.0", "flipGUI v.0.1 >>\n")
        self.txt_progress.grid(row = 0, column = 0, sticky = ("n","w","e","s"))
        
        self.s_bar_y = ttk.Scrollbar(self.lf_progress, orient = "vertical",
                                 command = self.txt_progress.yview)
        self.s_bar_y.grid(row = 0, column = 1, sticky = ("n", "s"))
        self.txt_progress['yscrollcommand'] = self.s_bar_y.set
        
        self.s_bar_x = ttk.Scrollbar(self.lf_progress, orient = "horizontal",
                             command = self.txt_progress.xview)
        self.s_bar_x.grid(row = 1, column = 0, sticky = ("e", "w"))
        self.txt_progress['xscrollcommand'] = self.s_bar_x.set        
        
        
        #------------SAVING DEFAULTS WHEN CLOSING APP--------------------------
        
        self.parent.protocol("WM_DELETE_WINDOW", 
                lambda caller = self: caller.destroy())
       

        #self.parent.protocol("WM_DELETE_WINDOW", 
        #         lambda caller = self,
        #                fpath = self._path2defaults,
        #                attributes = (
        #                            '_path_superflip',
        #                            '_path_shelx',
        #                            '_path_editor',
        #                            '_path_ins'
        #                            ):\
        #        flipGUI.routines.tkhandlers.handler(caller, fpath, attributes))
        
    #-------------METHODS------------------------------------------------------

    @property
    def tag(self):
        return os.path.basename(self._path_ins.get()).rsplit(".ins")[0]

    @property
    def home_dir(self):
        return os.path.dirname(self._path_ins.get())

    @property
    def ins_fname(self):
        return self.tag + ".ins"  
    
    @property
    def res_fname(self):
        return self.tag + ".res"

    @property
    def lst_fname(self):
        return self.tag + ".lst"

    @property
    def fcf_fname(self):
        return self.tag + ".fcf"
    
    @property
    def ins_fpath(self):
        return os.path.join(self.home_dir, self.ins_fname)

    @property
    def res_fpath(self):
        return os.path.join(self.home_dir, self.res_fname)

    @property
    def fcf_fpath(self):
        return os.path.join(self.home_dir, self.fcf_fname)

    @property
    def lst_fpath(self):
        return os.path.join(self.home_dir, self.lst_fname)
    
    @property
    def inflip_fpath(self):
        return os.path.join(self.home_dir, self.tag + "_fourier.inflip")

    @property
    def visual_fpath(self):
        return self._path_visual.get()



    def destroy(self):
        try:
            self._visual.terminate()
        except:
            pass
        self.parent.destroy()

    def open_with_editor(self, fpath, attr):
        """Opens file designated with fpath with the editor"""
        try:
            self.fpath_input_exists(fpath, attr)
            self.run_process(self._path_editor.get(), 
                        fpath,
                        attr,
                        redirect_out = True,
                        redirect_err = True,
                        wait = False)
        except SystemExit:
            return 1

    def refine(self, attr):
        """Runs flipGUI.routines.shelx"""
        try:
            self.fpath_input_exists(self._path_ins.get(), attr)
        except SystemExit:
            self.display_message(attr, ["--REASON: .ins FILE IS MISSING!\n"])
            return 1
        try:
            #self._chimera.save_session(self)

            self.run_process(self._path_shelx.get(), 
                        os.path.join(self.home_dir, self.tag),
                        attr,
                        redirect_out = True,
                        redirect_err = True,
                        wait = True)
            #generating cif with residual density peaks
            flipGUI.routines.shelx.difference_peaks(self.res_fpath)

            #running difference fourier
            self.button_dict['dF'].invoke()

        except SystemExit:
            return 1

    def res2ins(self, attr):
        """Copies content of .res file into .ins file """
        try:
            self.fpath_input_exists(self.res_fpath, attr)
        except SystemExit:
            self.display_message(attr, ["--REASON: .res FILE IS MISSING!\n"])
            return 1

        ins_filename = self.ins_fname
        res_filename = self.tag + ".res"
        working_dir = self.home_dir
        
        process = subprocess.Popen(["cp", res_filename, ins_filename],
                                   cwd = working_dir,
                                   stderr = subprocess.PIPE)
        process.wait()

        if process.communicate()[1] != "":
            getattr(self, attr).insert('end', process.communicate()[1])
            getattr(self, attr).see('end')
            return 1

        self.display_message(attr,
                            ["\n.res file is copied into .ins file!\n"])

    def copy_ins(self, attr):
        """creates numbered copy of .ins file"""
        try:
            self.fpath_input_exists(self.ins_fpath, attr)
        except SystemExit:
            self.display_message(attr, 
                                 ["--REASON: .ins FILE IS MISSING!\n"])
            return 1

        ins_filename =  self.ins_fname 
        working_dir = self.home_dir
        pattern = ins_filename + "COPY*"
        copy_numbers = []
        copy_nr = 1
        
        files = os.listdir(working_dir)
        matches = fnmatch.filter(files, pattern)
        
        if matches != []:
            for m in matches:
                copy_numbers.append(int(m.split("COPY")[1]))
            copy_nr = max(copy_numbers) + 1        
      
        process = subprocess.Popen(["cp",ins_filename,
                                    ins_filename + "COPY" + str(copy_nr)],
                                    cwd = working_dir)
        process.wait()

        self.txt_progress.insert('end',"\nA " + "'"+ ins_filename +
        "COPY" + str(copy_nr) + "'" + " file has been created\n")
        self.txt_progress.see('end')

    def plot_fo_fc(self, attr):
        """plots Fo vs. Fc from .fcf generated with LIST 5 command"""
        try:
            self.fpath_input_exists(self.fcf_fpath, attr)
        except SystemExit:
            self.display_message(attr, ["--REASON: .fcf FILE IS MISSING!\n"])
            self.display_message(attr, 
                                ["--SOLUTION: ISSUE 'LIST 5' COMMAND IN YOUR"\
                                " .ins FILE AND RUN <Refine>!\n"])

            return 1

        root = Tkinter.Tk()
        root.wm_title('|Fo|vs.|Fc|')

        fo_fc_table = list(flipGUI.routines.shelx.gen_fo_fc_2plot(
                                                            self.fcf_fpath))

        maxf_list =  map(max, (zip(*fo_fc_table)))
        minf_list = map(min, (zip(*fo_fc_table)))
        maxf = max(maxf_list)
        minf = min(minf_list)
        #plotting Fo vs Fc-----------------------------------------------------
        fo_fc_array = numpy.array(fo_fc_table, dtype = numpy.float)
        ref_line = numpy.array([[minf, minf] , [maxf, maxf]])

        fig = matplotlib.figure.Figure(figsize = (6, 6), dpi = 100)

        sp = fig.add_subplot(111)
        sp.plot(fo_fc_array[:, 0], fo_fc_array[:, 1], 'o',
                                     markerfacecolor = 'None',  markersize = 5)
        sp.hold('True')
        sp.plot(ref_line[:, 0], ref_line[:, 1],'b-')
        sp.hold('False')
        sp.axis('scaled')

        font = {'family' : 'arial', 'size' : 20}

        sp.set_xlabel(r'$|F_{obs}|$', fontdict = font)
        sp.set_ylabel(r'$|F_{calc}|$', fontdict = font)
        sp.axis([minf, maxf, minf, maxf])
        sp.grid()
        sp.tick_params(axis = 'both', which = 'major', labelsize = 12)

        canvas = FigureCanvasTkAgg(fig, master = root)
        canvas.show()
        canvas.get_tk_widget().pack(side = Tkinter.TOP, fill = Tkinter.BOTH,
                                                                    expand = 1)
        canvas._tkcanvas.pack(side = Tkinter.TOP, fill = Tkinter.BOTH,
                                                                    expand = 1)
        Tkinter.mainloop()

    def fourier(self, attr, job, voxel = 'AUTO'):
        """Fo synthesis"""
        try:
            self.fpath_input_exists(self.ins_fpath, attr)
        except SystemExit:
            self.display_message(attr, ["--REASON: .ins FILE IS MISSING!\n"])
            return 1
        try:
            self.fpath_input_exists(self.fcf_fpath, attr)
        except SystemExit:
            self.display_message(attr, ["--REASON: .fcf FILE IS MISSING!\n"])
            self.display_message(attr, 
                                ["--SOLUTION: ISSUE 'LIST 5' COMMAND IN YOUR "\
                                ".ins FILE AND RUN <Refine>!\n"])

            return 1
        
        flipGUI.routines.shelx.gen_inflip_from_ins(self._path_ins.get(),
                                            self.inflip_fpath, 
                                            job,
                                            self._voxel.get())

        try:
            exit_status = self.run_superflip(attr)
        except SystemExit:
            return 1

        if not exit_status:

            path_visual_lower = self._path_visual.get().lower()

            if "chimera" in path_visual_lower:
                if not self._visual or isinstance(self._visual, 
                        Vesta.Vesta):
                    self._visual = Chimera.Chimera()

            if "vesta" in path_visual_lower: 
                if not self._visual or isinstance(self._visual,
                        Chimera.Chimera):
                    self._visual = Vesta.Vesta()


            self._visual.update(self, job)                

            self.display_message(attr, 
            ["\nDensity map from {} synthesis was saved into '{}'!\n".format(
                job, "{}_{}.xplor".format(self.tag, job)
                )])
            self.display_message(attr, 
                    ["\nIF YOU WOULD LIKE SMOOTHER DENSITY MAPS "\
                    "MODIFY 'VOXEL' ENTRY. \n",
                     "--THERE HAVE TO BE EITHER 3 SPACE SEPARATED "\
                     "NUMBERS OR 'AUTO'\n",
                     "--CONSULT SUPERFLIP MANUAL.\n"])
        else:
            self.display_message(attr, 
                    ["\n--PROBABLE SOLUTION: CHECK 'VOXEL' FIELD\n",
                     "--THERE HAVE TO BE EITHER 3 SPACE SEPARATED "\
                     "NUMBERS OR 'AUTO'\n",
                     "--CONSULT SUPERFLIP MANUAL.\n"])

    def run_superflip(self, attr):
        """Runs superflip"""
        try:
            self.fpath_input_exists(self.inflip_fpath, attr)
        except SystemExit:
            return 1
        try:
            exit_status = self.run_process(self._path_superflip.get(),
                                        self.inflip_fpath,
                                        attr,
                                        redirect_out = True,
                                        redirect_err = True)
        except SystemExit:
            return 1
        return exit_status
   
    
    
