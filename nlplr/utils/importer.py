import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer

import tkinter as tk
from tkinter import filedialog

from typing import Tuple
import os
import time
import logging

logger = logging.getLogger(__name__)


def import_file() -> Tuple[pm4py.objects.log.log.EventLog, str, str]:
    importer = LogImporter()
    return importer.import_log(), importer.file_location, importer.filename


class LogImporter:  # TODO what happens when the filedialog is cancelled
    """select file and import log to work with the file"""

    def __init__(self):
        self._file_location: str = ''
        self._filename: str = ''
        self.log: pm4py.objects.log.log.EventLog = None

    def import_log(self):
        """Import eventlog"""
        self._get_log_file()
        tic = time.perf_counter()
        self.log = self._import_log()

        if self.log:
            toc = time.perf_counter()
            logger.info(f"Import eventlog in {toc - tic} seconds: {self.file_location}")
            return self.log
        else:
            logger.info(f'File does not fulfill requirements: {self.file_location}')

    def _get_log_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(initialdir=None,
                                               title="Select a File ...",
                                               filetypes=(("eventlog files", "*.xes"), ("all files", ".*")))  # no csv at the moment("eventlog files", "*.csv")
        self.file_location = os.path.abspath(file_path)  # easier for other work
        root.destroy()

    def _import_log(self):
        file_suffix = os.path.splitext(self.file_location)[1]
        if file_suffix == '.xes':
            return self._import_xes(self.file_location)
        elif file_suffix == '.csv':
            return self._import_csv(self.file_location)
        else:
            pass

    @staticmethod
    def _import_xes(file_location):
        return xes_importer.apply(file_location)

    @staticmethod
    def _import_csv(file_location):  # TODO
        pass

    @property
    def file_location(self):
        return self._file_location

    @file_location.setter
    def file_location(self, new_location):
        if os.path.exists(new_location):
            self._file_location = new_location
            self.filename = os.path.splitext(os.path.basename(self.file_location))[0]

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):

        self._filename = new_filename
