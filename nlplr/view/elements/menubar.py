import tkinter as tk
from nlplr.view.elements.toplevel import TutorialTopLevel, AboutTopLevel, ReferencesTopLevel


class Menubar(tk.Menu):
    def __init__(self, master, controller):
        tk.Menu.__init__(self, master)
        self.controller = controller
        # bindings and accelerators have to match
        self.bindings = {
            'restart': '<Control-r>',
            'import': '<Control-i>',
            'analysis': '<Control-a>',
            'settings': '<Control-s>',
            'tutorial': '<Control-t>'
        }
        self.accelerators = {
            'restart': 'Strg+R',
            'import': 'Strg+I',
            'analysis': 'Strg+A',
            'settings': 'Strg+S',
            'tutorial': 'Strg+T',
            'exit': 'Alt+F4'
        }
        self.settings = {

        }
        self.setup()

    def setup(self, *args):
        self.file_cascade()
        # self.analysis_cascade()
        self.help_cascade()

    def file_cascade(self, *args):
        # FILEMENU cascade
        self.filemenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=self.filemenu)
        # select log file for analysis
        self.filemenu.add_command(label="Import File", accelerator=self.accelerators['import'], command=self.import_file)
        self.bind_all(self.bindings['import'], self.import_file)
        # restart program
        self.filemenu.add_command(label="Restart", accelerator=self.accelerators['restart'], command=self.restart)
        self.bind_all(self.bindings['restart'], self.restart)

        self.filemenu.add_separator()
        # close window and program
        self.filemenu.add_command(label="Exit", accelerator=self.accelerators['exit'], command=quit)

    def analysis_cascade(self, *args):
        # ANALYSISMENU cascade
        self.analysismenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Analysis", menu=self.analysismenu)
        # select log file for analysis
        self.analysismenu.add_command(label="Run Analysis", accelerator=self.accelerators['analysis'], command=self.run_analysis)
        self.bind_all(self.bindings['analysis'], self.run_analysis)
        # restart program
        self.analysismenu.add_command(label="Settings", accelerator=self.accelerators['settings'], command=self.change_settings)
        self.bind_all(self.bindings['settings'], self.change_settings)

    def help_cascade(self, *args):
        # HELPMENU cascade
        self.helpmenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", menu=self.helpmenu)
        # show tutorial toplevel
        self.helpmenu.add_command(label="Tutorial", accelerator=self.accelerators['tutorial'], command=self.tutorial)
        self.bind_all(self.bindings['tutorial'], self.tutorial)

        self.helpmenu.add_separator()
        # show about toplevel
        self.helpmenu.add_command(label="About", command=self.about)
        # show references toplevel
        self.helpmenu.add_command(label="Libraries", command=self.references)

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

    def about(self, *args):
        self.about_toplevel = AboutTopLevel(self, self.controller)
        self.about_toplevel.run_and_restrict()

    def references(self, *args):
        self.references_toplevel = ReferencesTopLevel(self, self.controller)
        self.references_toplevel.run_and_restrict()