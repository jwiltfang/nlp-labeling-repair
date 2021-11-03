import pm4py
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class LogFilterTraces:
    def __init__(self, o_log):
        self.o_log = o_log

    def filter_traces_for_words(self, selected_words: Dict[str, List[str]]) -> pm4py.objects.log.log.EventLog:
        allowed_values = [a for values in selected_words.values() for a in values]
        filtered_log = pm4py.filter_log(lambda t: self._condition_word_in_trace(t, allowed_values), self.o_log)
        logger.info(f'ContextPreview: {len(filtered_log)} traces remain in filtered log')
        return filtered_log

    @staticmethod
    def _condition_word_in_trace(trace, values: List[str], attr: str = 'concept:name') -> bool:
        """return bool whether one of the values is in event"""
        for event in trace:
            if event[attr] in values:
                # print(event[attr], values)
                return True
