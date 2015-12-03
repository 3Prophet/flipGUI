import Tkinter

from flipGUI.interface import FlipGUI

def main():
    root = Tkinter.Tk()
    root.title('flipGUI')
    app = FlipGUI.FlipGUI(root)
    root.mainloop()



