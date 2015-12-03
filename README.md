# Ideas

Minimalistic GUI for SHELX, which can either be used as a standalone application
or as a part of a bigger project. It is based on few basic ideas:

1. There is no need to reinvent the wheel. It allows you to plug good *existing* solutions for editing, minimization,
Fourier synthesis and visualization in your refinement project

2. Not to overtake control. It does not modify your input files so that you do not lose control over your refinement.
It barely manages data flow between different components to make the refinement process more convenient

3. Keep it simple. You do not need to read any manual to start working with it. You need to know software that implements 
the offered functionality though (see sections 'Current software and library dependencies' and 'What do you need to start') 

# Currently available features

1. Running SHELX/SHELXL refinements
2. Quick access to *.res* *.ins* and *.lst* files with your favourite editor
3. Renaiming *.res* file into *.ins* file 
4. Saving copies of *.ins* file
5. |Fo| *vs.* |Fc| plots
6. Generating electron density maps in *.xplor* format (can be viewed with CHIMERA or VESTA)
7. Full support for VESTA. This allows using VESTA to follow updates in density maps, model and difference peaks 
   in course of refinemet. You can use every feature of VESTA and create your own drawing styles via *.vesta* files
8. Partial support for CHIMERA.

# Current software and library dependencies

1. Software: You need to have SHELX/SHELXL, SUPERFLIP and VESTA/CHIMERA running on your machine.

2. Libraries: You should use Python 2x interpreter to run the software and the following python libraries installed: *numpy*, *scipy*, *matplotlib*.

# Upcoming features

I'm currently writing a part that will allow you to use CHIMERA to follow changes in your model and density maps
during the course of refinement. 

# What do you need to start

The best way to learn the programm is by using it.
Just create a working directory and place there the same set of files you
need to start any shelx refinement (*.ins* and *.hkl*). Open the program (see 'Installation' section), provide the required
paths and just try it out. Follow the messages it prints and changes that occur in your working directory and you will understand everything about its functionality withing few minutes.

## Support for VESTA

IMPORTANT: To be able to use VESTA you should make it a default application to view *.xplor* and *.vesta* files. You should also issue 'LIST 5' and 'ACTA' instructions in your *.ins* file before the refinement. The former instraction generates *.fcf* file for the Fourier synthesis and the latter generates *.cif* file with your model. After that it works as follows:

Assume you have file *ref.ins* with parameters of your refinement

1. First time you make refinement or any kind of Fourier synthesis one of the corresponding *ref_dF.xplor*, *ref_Fo.xplor* or *ref_Fc.xplor* density files will be generated and immediately opened with VESTA. In case of refinement *peaks.cif* and *res.cif* containing information about residual density peaks and your model will be generated additionally

2. After the *.xplor* file is opened you can customize what else would you like to have on top of the electron density by importing any of the *.cif* files, drawing bonds, polyhedra etc. After you are happy with the final result and want to keep the style for further cycles of refinement just save the corresponding *.vesta* file. 

Example: Say you have performed dF synthesis. The file that will be generated and opened is *ref_dF.xplor*. Now you would like to put you model on top, draw some polyhedra and keep this style so that next time you make dF synthesis you not only see the density but also the model with drawn polyhedra. Import *ref.cif*, draw the polyhedra and save the content as *ref_Fo.vesta* file (consult VESTA manual). Next time you will make dF synthesis you style of visualization will be kept and only the density and model parameters will be updated. If later you want to change the style just do so and resave the corresponding *.xplor* file (*ref_dF.xplor* in the given example)

## Support for CHIMERA

Current support for CHIMERA is somewhat limited with respect to what you can do with the style of representation of electron density, your model and updating your model. I will try to do something about it in the nearest future.

IMPORTANT: To be able to use CHIMERA you should issue 'LIST 5' and 'WPDB *n*' instructions in your *.ins* file before refinement. The former instraction generates *.fcf* file for the Fourier synthesis and the latter generates *.pdb* file with your model. After that it works as follows:

Assume you have file *ref.ins* with parameters of your refinement

1. First time you make refinement or any kind of Fourier synthesis one of the corresponding *ref_dF.xplor*, *ref_Fo.xplor* or *ref_Fc.xplor* density files will be generated and immediately opened with CHIMERA. In case of refinement *res.pdb* containing information about your model will be generated additionally

2. Each time you make refinement or Fourier synthesis the screen with the density map will be updated accordingly

3. You can also open your *res.pdb* file on top of the electron density but its content is currently not updated so you
have to reopen it after new cycles of refinement.

#Installation (current state)

IMPORTANT: The current version runs only under OS X operating system.

1. Open the Terminal(the following instructions are given for the bash shell) and navigate to the folder where you want to store the program: *>>cd .../myfolder* 

2. Clone the repository by issuing: *>>git clone https://github.com/3Prophet/flipGUI* 

3. After step 2 you should have *flipGUI* directory in *myfolder*. Navigate there: *>>cd flipGUI*

4. Add path to *flipGUI* folder into the PYTHONPATH variable: *>>export PYTHONPATH="$(pwd)":$PYTHONPATH*

5. Navigate to the flipGUI folder: *>>cd flipGUI*

6. Launch: *>>python app.py* 


