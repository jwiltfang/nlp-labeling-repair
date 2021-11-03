from nlplr.analysis_NLP.analysis_options import AnalysisOption
from nlplr.analysis_NLP.attribute_value import AttributeValue, Attribute


class RepairOption:
    def __init__(self,
                 attribute=None,
                 cor_value=None,
                 inc_value=None,
                 result: float = None,
                 antonyms=None,
                 analysis_option=None):
        self._attribute: Attribute = attribute
        self.attribute_str = self.attribute.attr
        self._cor_value: AttributeValue = cor_value
        self._inc_value: AttributeValue = inc_value
        self._result = result
        self._antonyms = antonyms
        self._analysis_option: AnalysisOption = analysis_option
        self._threshold = self.analysis_option.threshold
        self.cor_repair_dict = {
            'attribute': self.attribute_str,
            'correct value': self.cor_value.orig_value,
            'correct processed': getattr(self.cor_value, self.analysis_option.preprocessing),
            'correct freq': self.cor_value.count,
        }
        self.inc_repair_dict = {
            'attribute': self.attribute_str,
            'incorrect value': self.inc_value.orig_value,
            'incorrect processed': getattr(self.inc_value, self.analysis_option.preprocessing),
            'incorrect freq': self.inc_value.count,
            'NLP result': self.result,
            'antonyms': self.antonyms,
        }
        self.repair_dict = {
            'attribute': self.attribute_str,
            'correct value': self.cor_value.orig_value,
            'incorrect value': self.inc_value.orig_value,
            'model': self.analysis_option.model
        }

    def get_treeview_headers(self):
        return self.inc_repair_dict.keys()

    @property
    def attribute(self):
        return self._attribute

    @property
    def cor_value(self):
        return self._cor_value

    @property
    def inc_value(self):
        return self._inc_value

    @property
    def result(self):
        return self._result

    @property
    def antonyms(self):
        return self._antonyms

    @property
    def analysis_option(self):
        return self._analysis_option

    @property
    def threshold(self):
        return self._threshold

    def __eq__(self, other):
        if isinstance(other, RepairOption):
            return self.cor_value == other.cor_value and self.inc_value == other.inc_value
        return False

    def __repr__(self):
        return f'RepairOption(correct: {self.cor_value!r}, incorrect: {self.inc_value!r}'