from typing import List


class AnalysisOption:
    def __init__(self,
                 name: str = 'open',
                 model: str = 'leven',
                 preprocessing: str = 'preprocessed_value',
                 fn: str = '_',
                 threshold: float = 0.5):
        self._name = name
        self._model = model
        self._preprocessing = preprocessing
        self._fn = fn
        self._threshold = threshold

    def transform_to_orig_version_build_sim_matrix(self):  # TODO deprecate this necessity
        """necessary to work with original implementation of attribute value"""
        return self.model, self.name, self.preprocessing, self.fn

    @property
    def name(self):
        return self._name

    @ property
    def model(self):
        return self._model

    @property
    def preprocessing(self):
        return self._preprocessing

    @property
    def fn(self):
        return self._fn

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, new_treshold):
        if 0 < new_threshold < 1:
            self._threshold = new_treshold

    def __repr__(self):
        return f'AnalysisOption(name: {self._name!r}, model: {self._model!r}, preprocessing: {self._preprocessing!r}, fn: {self._fn!r}, threshold: {self._threshold!r})'

    def __str__(self):
        return f'Analysis option {self.name!r} with model {self._model!r}; preprocessing {self._preprocessing!r}; fn {self._fn!r}; threshold: {self._threshold!r}'


class AnalysisOptionsContainer:
    def __init__(self):
        self._options: List[AnalysisOption] = list()

    def add_options(self, options):
        self._options += options

    def __getitem__(self, item):
        return self._options[item]

    def __iter__(self):
        return AnalysisOptionsIterator(self)

    def __len__(self):
        return len(self._options)

    def __repr__(self):
        return f'{len(self)} options included'


class AnalysisOptionsIterator:
    """Iterator class for AnalysisOptions"""
    def __init__(self, container):
        self._container = container
        self._index = 0

    def __next__(self):
        """Returns the next value from team object's lists"""
        if self._index < (len(self._container._options)):
            result = self._container._options[self._index]
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration


if __name__ == '__main__':

    analysis_options = AnalysisOptionsContainer()
    options = [AnalysisOption('gram_lev', 'leven', 'preprocessed_value', threshold=0.5),
               AnalysisOption('open', 'sem_glove', 'glove_tokens', 'calc_similarity_list', threshold=0.5)]
    analysis_options.add_options(options)
    for option in analysis_options:
        print(option)
        if option.name == 'gram_lev':
            print('test_sucessful')
            print(option)

    current_option = analysis_options[1]
    print(f'{current_option.model!r}', current_option.name)

    print(len(analysis_options))
    print(f'{analysis_options!r}')