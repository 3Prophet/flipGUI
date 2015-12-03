"""Tests whether flipGUI.inerface.FlipGUI.FlipGUI class intercepts error 
messages coming from the fact that both 'Software paths' and path
to .inp file are not given"""

import shutil
import os
import sys
import subprocess
import time

from flipGUI.interface import FlipGUI

def test_noinputs_editor(button_editing, flipgui):
    for button in button_editing:
        assert 1 == flipgui.button_dict[button].invoke()

def test_noinputs_refinement(button_refinement, flipgui):
    for button in button_refinement:
        assert 1 == flipgui.button_dict[button].invoke()

def test_noinputs_maps(button_maps, flipgui):
    for button in button_maps:
        assert 1 == flipgui.button_dict[button].invoke()

def test_false_softpaths_editor(empty_dir, button_editing, flipgui):
    flipgui._path_editor.set(empty_dir)
    for button in button_editing:
        assert 1 == flipgui.button_dict[button].invoke()
