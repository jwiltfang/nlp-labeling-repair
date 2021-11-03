import tkinter as tk
from abc import abstractmethod, ABC


class WindowFrame(ABC, tk.Frame):
    def __init__(self, master, controller, callbacks, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.callbacks = callbacks
        self._setup_frame()
        self.statusbar = tk.Label(self, bd=2, relief='ridge', anchor='sw', bg='gray', fg='white')
        self.statusbar.pack(side='bottom', anchor='sw', fill='x')
        self._orient_frame()

    @abstractmethod
    def _setup_frame(self):
        """initialize elements that will be placed within the frame"""
        pass

    @abstractmethod
    def _orient_frame(self):
        """alignment and packing of frame elements"""
        pass

    def update_information_container(self, filename, analysis_information):
        self.information_container.update_information(filename, analysis_information)

    def update_button(self, element=None, btn: str = '', state: str = 'normal'):  # TODO does it work
        if element:
            element_in_frame = getattr(self, element)
            element_in_frame.update_button(btn, state)
        else:
            button = getattr(self, btn)
            button.config(state=state)

    def update_statusbar(self, status):
        self.statusbar.config(text=status)
