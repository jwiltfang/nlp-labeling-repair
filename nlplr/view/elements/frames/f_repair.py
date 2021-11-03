from nlplr.view.elements.frames.f_general import WindowFrame
from nlplr.view.elements.frames.fe_general import InformationContainer
from nlplr.view.elements.frames.fe_repair import RepairSelectionFrame

from nlplr.repair.repair_options import RepairOption

import tkinter as tk
from typing import Dict


class RepairFrame(WindowFrame):
    def __init__(self, master, controller, callbacks, repair_dict: Dict[int, RepairOption], *args, **kwargs):
        # scramble data for listbox and selection_frames in RepairSelectionFrame
        self.repair_dict: Dict[int, RepairOption] = repair_dict

        super().__init__(master, controller, callbacks, *args, **kwargs)

    def _setup_frame(self):
        """
        Main function to setup the frame for RepairSelectFrame, inlcuding all containers and their packing
        """
        self.main_frame = tk.Frame(self)
        self.information_container = InformationContainer(self.main_frame, self.controller, self.callbacks, bd=2, relief='raised')
        self.repair_selection_container = RepairSelectionFrame(self.main_frame, self.controller, self.callbacks, self.repair_dict)  # .repair_view_class)

    def _orient_frame(self):
        self.main_frame.pack(fill='both', expand=True)
        self.information_container.pack(anchor='nw', fill='x')
        self.repair_selection_container.pack(anchor='nw', fill='both', expand=True)



    def __repr__(self):
        return f'RepairFrame(based on tk.Frame to show {repair_dict!r})'
