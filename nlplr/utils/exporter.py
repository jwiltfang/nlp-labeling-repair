import pm4py
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

import tkinter as tk
from tkinter import filedialog

from typing import Tuple
import os
import time
import logging

logger = logging.getLogger(__name__)


def export_file(log, filename, prefix='rep'):
    exporter = LogExporter(filename)
    exporter.export_log(log, prefix)


class LogExporter:
    """
    Export event log in .xes format after the necessary changes have been done

    Parameters
    ----------
    repaired_log
        eventlog to be exported
    new_filename
        filepath where the repaired event log is meant to be saved
    """
    def __init__(self, filename: str):
        self.save_location: str = ''
        self.filename = filename

    def export_log(self, log, prefix: str = 'rep'):
        """Import eventlog"""
        tic = time.perf_counter()
        self._get_save_location(self.filename, prefix)
        try:
            if self.save_location.endswith('.xes'):
                self._export_xes(log, self.save_location)
            elif self.save_location.endswith('.csv'):
                self._export_csv(log, self.save_location)
            else:
                return
            toc = time.perf_counter()
            logger.info(f'The event log was exported and saved at {self.save_location} in {toc - tic} seconds.')
        except FileNotFoundError as fe:
            pass  # TODO

    def _get_save_location(self, filename: str, prefix: str = 'rep'):
        root = tk.Tk()
        root.withdraw()
        export_filename = filedialog.asksaveasfilename(initialdir=None,  # TODO
                                                       initialfile=f'{prefix}_{filename}',
                                                       defaultextension='.xes',
                                                       title='Save File after Repair',
                                                       filetypes=(("eventlog files", "*.xes"), ("all files", ".*")))  # no cvs ("eventlog files", "*.csv")
        self.save_location = os.path.abspath(export_filename)  # easier for other work
        root.destroy()

    @staticmethod
    def _export_xes(repaired_log: pm4py.objects.log.log.EventLog, new_filename: str) -> None:
        xes_exporter.apply(repaired_log, new_filename)

    @staticmethod
    def _export_csv(repaired_log: pm4py.objects.log.log.EventLog, new_filename: str) -> None:
        dataframe = log_converter.apply(repaired_log, variant=log_converter.Variants.TO_DATA_FRAME)
        dataframe.to_csv(new_filename)
