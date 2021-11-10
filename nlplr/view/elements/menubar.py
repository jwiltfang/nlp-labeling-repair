import tkinter as tk
from nlplr.view.elements.toplevel import TutorialTopLevel

class Menubar(tk.Menu):
    def __init__(self, master, controller):
        tk.Menu.__init__(self, master)
        self.controller = controller
        # bindings and accelerators have to match
        self.setup()

    def setup(self, *args):
        self.file_cascade()
        # self.analysis_cascade()
        self.help_cascade()

    def file_cascade(self, *args):
        # FILEMENU cascade
        self.filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=self.filemenu)
        # close window and program
        self.filemenu.add_command(label="Exit", command=quit)

    def help_cascade(self, *args):
        # HELPMENU cascade
        self.helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=self.helpmenu)
        # show tutorial toplevel
        self.helpmenu.add_command(label="Tutorial", command=self.tutorial)

    def run_analysis(self, *args):
        self.controller.handle_click_run_analysis()

    def change_settings(self, *args):
        self.controller.handle_click_settings()

    def import_file(self, *args):
        self.controller.handle_click_import_file()

    def restart(self, *args):
        self.controller.handle_click_restart()

    def tutorial(self, *args):
        self.tutorial_toplevel = TutorialTopLevel(self, self.controller)
        self.tutorial_toplevel.run_and_restrict()