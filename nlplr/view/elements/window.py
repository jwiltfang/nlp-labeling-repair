from nlplr.view.elements.menubar import Menubar
from nlplr.view.elements.frames.f_start import StartFrame
from nlplr.view.elements.frames.f_repair import RepairFrame
from nlplr.utils import exe_utils

import tkinter as tk
import logging

logger = logging.getLogger(__name__)


class Window(tk.Tk):
    """
    Implementation for a basic tkinter main window

    Handles the general functions regarding the entire window, its properties, short-cuts etc.
    """
    def __init__(self, controller, *args, **kwargs):  # TODO use more hotkeys and make it more useable by standard settings
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.frame = None
        self.settings = {
            'geometry': '1000x600',
            'title': 'NLP Log Repair Client',
            'iconfile': 'nlplr/view/elements/icons/icon.png', # exe_utils.resource_path(
            'full_screen_state': False
        }
        self.bindings = {
            'toggle_full_screen': '<F11>',
            'quit_full_screen': '<Escape>'
        }
        self.callbacks = {
            'import_log': self.import_log,
            'confirm_attribute_selection': self.confirm_attribute_selection,
            'start_analysis': self.start_analysis,
            'run_repair': self.run_repair,
            'run_next_analysis': self.run_next_analysis,
            'export_log': self.export_log,
            'whitelist_correct_value': self.whitelist_correct_value,
            'preview_context': self.preview_context,
            'select_listbox_value': self.select_listbox_value,
        }
        self.setup()

    # TODO do button actions
    def import_log(self):
        self.controller.handle_click_import_log()

    def confirm_attribute_selection(self, selected_attributes):
        self.controller.handle_click_confirm_selected_attributes(selected_attributes)

    def start_analysis(self):
        self.controller.handle_click_start_analysis()

    def run_repair(self, repair_items, blacklist_items):
        self.controller.handle_click_run_repair(repair_items, blacklist_items)

    def run_next_analysis(self):
        self.controller.handle_click_run_next_analysis()

    def export_log(self):
        self.controller.handle_click_export_log()

    def whitelist_correct_value(self):
        pass

    def preview_context(self, cor_value, incorrect_values):
        self.controller.handle_click_export_context_preview(cor_value, incorrect_values)

    def select_listbox_value(self, index):
        self.frame.repair_selection_container.show_frame(index)

    def setup(self):
        self.attributes('-fullscreen', self.settings['full_screen_state'])
        # self.fullScreenState = False
        self.iconphoto(False, tk.PhotoImage(file=self.settings['iconfile']))

        self.geometry(self.settings['geometry'])
        self.title(self.settings['title'])

        # hotkeys for application
        self.bind(self.bindings['toggle_full_screen'], self.toggle_full_screen)
        self.bind(self.bindings['quit_full_screen'], self.quit_full_screen)
        self.config(menu=Menubar(self, self.controller))

        self.switch_frame(StartFrame(self, self.controller, self.callbacks))

    def switch_to_repair_frame(self, repair_dict):
        self.switch_frame(RepairFrame(self, self.controller, self.callbacks, repair_dict=repair_dict))

    def switch_frame(self, frame_class):
        """
        Destroys the current top frame and builds the next one on top

        Parameters
        ----------
        frame_class
            frame that fills the entire window
        """
        new_frame = frame_class
        # new_frame = frame_class(self, self.controller, self.callbacks)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(anchor='nw', fill='both', expand=True)
        self.controller.frame = new_frame

    def toggle_full_screen(self, *args):
        if not self.settings['full_screen_state']:
            self.geometry(self.settings['geometry'])
        self.settings['full_screen_state'] = not self.settings['full_screen_state']
        self.attributes("-fullscreen", self.settings['full_screen_state'])

    def quit_full_screen(self, *args):
        self.settings['full_screen_state'] = False
        self.attributes("-fullscreen", self.settings['full_screen_state'])
        self.geometry(self.settings['geometry'])
