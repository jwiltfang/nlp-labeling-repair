from nlplr.analysis_NLP.attribute_value import AttributeValue
from nlplr.repair.repair_options import RepairOption

from pm4py.objects.log.log import EventLog

from typing import List, Dict, Union
import time
import logging

logger = logging.getLogger(__name__)


class RepairTool:
    def __init__(self):
        self.repair_ids: List[int] = []
        self.repair_conditions: List[RepairOption] = []

        self.changed_entries = 0
        self.changed_events = 0

    def repair_log(self, log, repair_ids: List[int], repair_options: Dict[int, RepairOption]) -> EventLog:
        """
        Repair log based on selected conditions
        -> Conditions are being sorted by occurence and update the log to an ideally better standard

        Parameters
        ----------
        log
            original event log
        repair_ids
            all ids that have to be changed now
        repair_options
            set of possible repair options

        Returns
        -------
        repaired_log
            log where all selected conditions where repaired
        """
        if repair_ids:
            self._get_repair_conditions(repair_ids, repair_options)
            self._sort_conditions_by_occurence()
            return self._update_events(log)
        return log

    def _get_repair_conditions(self, repair_ids: List[int], repair_options: Dict[int, RepairOption]):
        """
        Return pre-filtered repair conditions
        """
        self.repair_conditions = []
        for rep_id in repair_ids:
            self.repair_conditions.append(repair_options[int(rep_id)])

    def _sort_conditions_by_occurence(self):
        sorted_repair_conditions = sorted(
            sorted(self.repair_conditions, key=lambda rep_option: rep_option.inc_value.count),
            key=lambda rep_option: rep_option.cor_value.count)
        self.repair_conditions = sorted_repair_conditions

    def _update_events(self, log: EventLog) -> EventLog:
        """
        Update the event log with the repair conditions
        -> additional attribute labels simplify the evaluation of the event log
        """
        tic = time.perf_counter()
        analysis_name = self.repair_conditions[0].analysis_option
        log.attributes[f'an:{analysis_name}:changes'] = self.repair_conditions
        for trace in log:
            for event in trace:
                event_changed = False  # report if any changes were made in the program
                # print(f'Event: {event}')
                # print('test')
                # if event['concept:name'] == 'Permit ABBROVED':
                #     print('2:', event)
                # if event.get('concept:name') == 'Permit ABBROVED ':
                #     print('1:', event)
                for condition in self.repair_conditions:
                    condition = condition.repair_dict
                    attr_name = condition.get('attribute')
                    orig_value = condition.get('incorrect value')
                    sugg_value = condition.get('correct value')
                    analysis_name = condition.get('model')
                    if event.get(attr_name) == orig_value:
                        event[attr_name] = sugg_value
                        event[f'an:{analysis_name}:{attr_name}'] = sugg_value
                        event_changed = True
                        self.changed_entries += 1

                if event_changed:
                    self.changed_events += 1
        toc = time.perf_counter()
        logger.info(f'The repair has changed {self.changed_entries} entries in {self.changed_events} events in {toc - tic} seconds.')

        return log
