from nlplr.repair.repair_options import RepairOption

import pm4py
from pm4py.algo.filtering.log.attributes import attributes_filter

from typing import List, Dict, Union
from abc import ABC, abstractmethod
from os import path
from dateutil.parser import parse
import time
import logging

logger = logging.getLogger(__name__)


class Model(ABC):
    """Abstract Base Class as an interface for different DataModel implementations"""
    # no abstract methods needed yet because programme does not enforce complete loose coupling
    @abstractmethod
    def __init__(self):
        pass


class TkModel(Model):
    """
    Concrete Implementation for DataModel in MVC architecture

    Parameters
    ----------

    """
    def __init__(self):
        # original file
        self.log = None
        self.file_location = 'test_old'
        self._filename: str = ''
        # content of log
        self.relevant_attributes = []
        self.attributes_list = []
        self.attribute_content = {}

        # content of user choice
        self.selected_attributes = []

        # content for analysis
        self.current_analysis_index = 0
        self.current_analysis = None
        self.analysis_options = None
        self.analysis_information = ''

        # content to repair log
        self.repair_ids = []
        self.repair_dict: Dict[int, RepairOption] = {}

        # content of old analyses
        self.blacklist_repair_options = []  # TODO
        self.whitelist_attribute_values = []  # TODO
        pass

    def setup_analyses(self, analysis_options):
        self.analysis_options = analysis_options

    def preprocess_log(self):
        self._read_attribute_content()
        self._filter_events_and_attribute_content()
        self._insert_eval_labels()

    def _read_attribute_content(self):
        """
        Read content for each attribute and get individual values to store in a dict with the key 'attribute'
        """
        for attribute in self.selected_attributes:
            self.attribute_content[attribute] = attributes_filter.get_attribute_values(self.log, attribute)

    def _filter_events_and_attribute_content(self):
        """
        Semantic augmentation by Rebmann et al. introduces many empty strings or NaN values that are filtered in order
        to increase computing speed
        """
        from numpy import nan
        filtered_attribute_content = {}
        for key, values in self.attribute_content.items():
            new_values = {}
            for k in values.keys():
                if str(k) != 'nan' or str(k) != '' or k != nan:  # solution works but not the best
                    if not isinstance(k, bool):
                        new_values[k.strip()] = values[k]  # strip key to get rid of leading and trailing whitespace
            filtered_attribute_content[key] = new_values
        self.attribute_content = filtered_attribute_content

    def _insert_eval_labels(self):
        """
        Insert attributes after selection for use in tool to be able to evaluate the progress of the tool afterwards, comparing values that were inside before and what it became after repair
        :return:
        """
        for trace in self.log:
            for event in trace:
                for attr in self.selected_attributes:
                    if event.get(attr, False):
                        event[attr] = event[attr].strip()  # strip labels from whitespaces
                        if f'start:{attr}' not in event.keys():  # only insert start variable if it is not available before
                            event[f'start:{attr}'] = event[attr]
                    else:
                        continue
        logger.info('Evaluation labels <key=\'start:{attr}\', value=\'**start_label**\'> were inserted.')

    def reset_repair_data(self):
        self.repair_ids = []
        self.repair_dict = {}

    def get_current_analysis_information(self):
        self.current_analysis = self.analysis_options[self.current_analysis_index]
        return f'({self.current_analysis_index+1} / {len(self.analysis_options)} steps) {self.current_analysis!s}'

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename):
        if new_filename is not None:
            self._filename = new_filename

    def __repr__(self):
        return f'TkEventController({self.model!r}, {self.view!r}'

    def __str__(self):
        return f'TkModel (implemented for TkController and TkView)'
