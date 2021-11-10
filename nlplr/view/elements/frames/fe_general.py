from nlplr.view.settings import _TITLE_FONT, _ACTIVE_BUTTON
from nlplr.utils import exe_utils

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import ImageTk, Image

from abc import ABC, abstractmethod
from typing import List
import logging

logger = logging.getLogger(__name__)


class BaseFrame(ABC, tk.Frame):
    def __init__(self, master: tk.Frame, controller, callbacks, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.callbacks = callbacks
        self._setup_frame()
        self._orient_frame()

    @abstractmethod
    def _setup_frame(self):
        pass

    @abstractmethod
    def _orient_frame(self):
        pass

    def update_button(self, btn: str, state: str):
        button = getattr(self, btn)
        button.config(state=state)


class InformationContainer(BaseFrame):  # TODO update useful information for the current analysis (what happens, how, when, why)
    def __init__(self, master: tk.Frame, controller, callbacks, *args, **kwargs):
        """
        Information container class that can be reused in different frames
        :param master:
        """
        self.filename = ''
        self.analysis_step_information = ''
        super().__init__(master, controller, callbacks, *args, **kwargs)

    def _setup_frame(self):
        self.header_container = tk.Frame(self)
        self.current_file_label = tk.Label(self.header_container,
                                           text=('Current File: ' + str(self.filename)), anchor='w', pady=6)
        self.current_analysis_label = tk.Label(self.header_container,
                                               text=('Analysis: ' + str(self.analysis_step_information)), anchor='w', pady=6)

        self.logo_container = tk.Frame(self)
        self.logo_panel = LogoPanel(self.logo_container, self.controller, self.callbacks)

    def _orient_frame(self):
        self.header_container.pack(side='left', anchor='w', fill='x', expand=True)
        self.current_file_label.pack(anchor='w', fill='x')
        self.current_analysis_label.pack(anchor='w', fill='x')
        self.logo_container.pack(side='left', expand=False)
        self.logo_panel.pack()

    def update_information(self, file_location, analysis_infomartion):
        self.update_current_file_label(file_location)
        self.update_analysis_step_information(analysis_infomartion)

    def update_current_file_label(self, filename):
        self.current_file_label.config(text=('Current File: ' + str(filename)))

    def update_analysis_step_information(self, analysis_step):
        self.current_analysis_label.config(text=('Analysis step: ' + str(analysis_step)))


class LogoPanel(BaseFrame):
    def __init__(self, master: tk.Frame, controller, callbacks, *args, **kwargs):
        """
        Logo class that can be reused in different frames
        :param master:
        """
        self.logo = Image.open(exe_utils.resource_path('nlplr/view/elements/icons/logo.PNG'))
        super().__init__(master, controller, callbacks, *args, **kwargs)

    def _setup_frame(self):
        self.logo_resized = self.logo.resize((128, 72), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo_resized)
        self.logo_panel = tk.Label(self, image=self.logo)

    def _orient_frame(self):
        self.logo_panel.pack(anchor='w')
