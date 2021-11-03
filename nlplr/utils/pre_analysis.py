import nlplr.utils.data_utils as data_utils

import pm4py
from pm4py.algo.filtering.log.attributes import attributes_filter

from typing import List
import logging

logger = logging.getLogger(__name__)


def filter_attributes(log: pm4py.objects.log.log.EventLog):
    attribute_filter = AttributeFilter(log)
    return attribute_filter.get_attribute_values([]), attribute_filter.attributes_list


class AttributeFilter:
    def __init__(self, log: pm4py.objects.log.log.EventLog):
        self.log = log
        self.attributes_list = []
        self.attribtube_not_for_analyis = []
        self.attributes_not_used = ['time:timestamp', 'id']

    def get_attribute_values(self, attribute_not_for_analysis: List[str] = None):
        """
        Retrieves all attributes present in log and removes irrelevant attributes that are selected with original

        Parameters
        ----------
        attribute_not_for_analysis: List[str]
            additional attributes that shall not be analyzed
        """
        self.attributes_list = pm4py.get_attributes(self.log)
        self.remove_irrelevant_attributes(attribute_not_for_analysis)
        self.relevant_attributes = [attribute for attribute in self.attributes_list if
                                    attribute not in self.attributes_not_used]
        logger.info(f'Relevant attributes {self.relevant_attributes}; ({self.attributes_not_used} stripped)')
        return self.relevant_attributes

    def remove_irrelevant_attributes(self, attribute_not_for_analysis):
        self.attributes_not_used.extend(attribute_not_for_analysis)
        for attribute in self.attributes_list:
            test_values_list = attributes_filter.get_attribute_values(self.log, attribute, parameters=None)
            first_test_value = list(test_values_list)[0]
            if isinstance(first_test_value, str):
                if not first_test_value.isnumeric() and not data_utils.is_date(first_test_value):
                    if attribute.split(':')[0] not in ['correct', 'start', 'an']:  # TODO does that fit naming conventions
                        continue
            else:
                continue
            self.attributes_not_used.append(attribute)

    @staticmethod
    def is_date(string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        Parameters
        ----------
        string: str
            str, string to check for date
        fuzzy: bool
            ignore unknown tokens in string if True
        """
        try:
            parse(string, fuzzy=fuzzy)
            return True
        except ValueError:
            return False


