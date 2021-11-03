from nlplr.view.elements.frames.fe_general import BaseFrame
from nlplr.view.settings import _ACTIVE_BUTTON

import tkinter as tk

import logging

logger = logging.getLogger(__name__)


class SelectAttributesContainer(BaseFrame):
    def __init__(self, master: tk.Frame, controller, callbacks, *args, **kwargs):
        super().__init__(master, controller, callbacks, *args, **kwargs)
        self.attributes = None
        self.selected_attributes = None

    def _setup_frame(self):
        self.selection_label = tk.Label(self, text='Please select the attributes that you want to correct.', anchor='w')
        self.selection_box = tk.Listbox(self, selectmode=tk.MULTIPLE, height=4)
        self.select_button = tk.Button(self, text='Confirm Selection', command=self.select_attributes, state='disabled')

    def _orient_frame(self):
        self.selection_label.pack(anchor='w', fill='x')
        self.selection_box.pack(anchor='w', fill='both', expand=True)
        self.select_button.pack(anchor='w', fill='x')

    def update_attributes(self, attributes):
        self.attributes = attributes
        for val in self.attributes:
            self.selection_box.insert(tk.END, val)

    def select_attributes(self):
        self.selected_attributes = [self.attributes[i] for i in self.selection_box.curselection()]  # tuple turned into list of strings
        if self.selected_attributes:
            self._udpate_content_selection_label()
            self.callbacks['confirm_attribute_selection'](self.selected_attributes)

    def _udpate_content_selection_label(self):
        self.selection_label.config(text=f'Attributes Selected: {self.selected_attributes}')
        self.selection_box.pack_forget()
        self.select_button.pack_forget()
