from nlplr.view.elements.frames.f_general import WindowFrame
from nlplr.view.elements.frames.fe_general import InformationContainer
from nlplr.view.elements.frames.fe_start import SelectAttributesContainer
from nlplr.view.settings import _ACTIVE_BUTTON

import tkinter as tk


class StartFrame(WindowFrame):
    def __init__(self, master: tk.Tk, controller, callbacks, *args, **kwargs):
        """
        Initializes frame to have something to show while nlp_models are loading and user can already select the log

        Parameters
        ----------
        master: tk.Frame
            frame that this object is placed in
        controller
            controller from MVC pattern
        """
        super().__init__(master, controller, callbacks, *args, **kwargs)

    def _setup_frame(self):
        self.information_container = InformationContainer(self, self.controller, self.callbacks, bd=2,
                                                          relief='raised')
        self.import_log_button = tk.Button(self, text='Import Log File {Strg+I}',
                                           command=self.callbacks['import_log'],
                                           activebackground=_ACTIVE_BUTTON)
        self.select_attributes_container = SelectAttributesContainer(self, self.controller, self.callbacks)
        self.start_analysis_button = tk.Button(self,
                                               text='Start Analysis',
                                               activebackground=_ACTIVE_BUTTON,
                                               command=self.callbacks['start_analysis'],
                                               state='disabled')

    def _orient_frame(self):  # TODO import log muss nach obne
        self.information_container.pack(side='top', anchor='nw', fill='both')
        self.import_log_button.pack(side='top', anchor='nw', fill='x')
        self.select_attributes_container.pack(side='top', anchor='w', fill='both', expand=True)
        self.start_analysis_button.pack(side='bottom', anchor='w', fill='x')

    # def update_information_container(self, filename, analysis_information):  # TODO delete
    #     self.information_container.update_information(filename, analysis_information)

    def update_selected_attributes_container(self, relevant_attributes):
        self.select_attributes_container.update_attributes(relevant_attributes)
