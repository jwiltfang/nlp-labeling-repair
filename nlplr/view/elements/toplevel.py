from nlplr.view.settings import _TITLE_FONT
import tkinter as tk
from abc import ABC, abstractmethod


class ABCTopLevel(ABC, tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self._setup_frame()
        self._orient_frame()

    @abstractmethod
    def _setup_frame(self):
        pass

    @abstractmethod
    def _orient_frame(self):
        pass

    def run_and_restrict(self):
        """
        Functions to grab focus from main window, so there can be no changes while the toplevel is open and multiple instances are not possible
        """
        self.grab_set()
        self.focus_set()
        self.mainloop()
        self.grab_release()


class TutorialTopLevel(ABCTopLevel):
    def __init__(self, master, controller):
        self.settings = {
            'text': 'Please check out the website https://github.com/jwiltfang/nlp-labeling-repair for how to use this tool and find more information on this client.'
            }
        super().__init__(master, controller)

    def _setup_frame(self):
        self.title('Tutorial')
        self.topl_frame = tk.Frame(self)
        self.repair_choice_legend = tk.Label(self.topl_frame, anchor='w', justify='left', text=self.settings['text'])
        # pack all elements in order

    def _orient_frame(self):
        self.topl_frame.pack(anchor='w', fill='x', expand=True)
        self.repair_choice_legend.pack(anchor='w', fill='x')
