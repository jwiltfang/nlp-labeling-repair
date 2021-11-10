from nlplr.utils.context_preview.filter_traces import LogFilterTraces
from nlplr.utils.context_preview.marker import Marker
from nlplr.utils.context_preview.visualizer import HeuristicsGraph

from pm4py.objects.log.log import EventLog

import tkinter as tk
from tkinter import filedialog

from typing import List, Dict
import os
from datetime import datetime
import random


def preview_context(log, save_location, filename, selected_words):
    context_previewer = ContextPreviewer(log, save_location, filename)
    context_previewer.preview_context_pdf(selected_words)


class ContextPreviewer:
    def __init__(self, log: EventLog, save_location: str, filename: str):
        self.log = log  # original log
        self.save_location: str = self._get_save_location(filename)
        self.filename: str = filename

    def preview_context_pdf(self, selected_words: Dict[str, List[str]]):
        correct_word = self.get_correct_word(selected_words)
        temp_save_location = os.path.join(self.save_location, f'graph_{self.filename}.pdf')
        final_save_location = os.path.join(self.save_location, f'mark_{correct_word}_{self.filename}_{self.get_random_digit()}.pdf')

        log_filter = LogFilterTraces(self.log)
        filtered_log = log_filter.filter_traces_for_words(selected_words)

        visualizer = HeuristicsGraph(filtered_log)
        visualizer.run()

        graph_file = visualizer.save_pdf(temp_save_location)

        marker = Marker()
        marker.load_pdf(graph_file)
        marker.mark_words(selected_words)

        mark_file = marker.save_pdf(final_save_location)

        self.open_folder(mark_file)

    @staticmethod
    def get_correct_word(selected_words):
        return str(selected_words['correct'][0])

    @staticmethod
    def open_folder(save_location):
        os.startfile(os.path.abspath(save_location))

    @staticmethod
    def get_current_time():
        now = datetime.now()
        current_time = now.strftime("%H,%M,%S")
        return current_time

    @staticmethod
    def get_random_digit(n=3):
        lower = 10 ** (n - 1)
        upper = 10 ** n - 1
        return random.randint(lower, upper)

    def _get_save_location(self, filename: str, prefix: str = 'rep'):
        root = tk.Tk()
        root.withdraw()
        preview_dir = filedialog.askdirectory(initialdir=None,
                                            title='Select Directory for Preview File')
        root.destroy()
        return os.path.abspath(preview_dir)