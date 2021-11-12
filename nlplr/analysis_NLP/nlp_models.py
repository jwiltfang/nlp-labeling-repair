from nlplr.utils import exe_utils
from nlplr.utils.label_utils import difference_of_list_both, difference_of_str_both

import spacy
import gensim.models.keyedvectors
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors, WordEmbeddingSimilarityIndex
from gensim.scripts.glove2word2vec import glove2word2vec

from abc import ABC, abstractmethod
import numpy as np
from statistics import mean
from typing import List, Dict, Tuple
import logging
import time
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TODO create meaningful classes that make sense and are interchangeably useful; instance of each model with different
#  pre_settings when __init__ and all similarity functions or similarity_matrix maybe generalized somewhere else

# File locations
_glove_file = 'data/glove.6B.100d.txt'  # 400k vectors, 100dim
_spacy_file_sm = 'en_core_web_sm'  # no word vectors included, so not recommended
_spacy_file_md = 'en_core_web_md'  # 685k keys, 20k unique vectors (300 dimensions)


class Model(ABC):
    """
    Class Model contains abstract basic functions for all models
    If different implementations for the different NLP approaches are needed, the input is standardized for better usage

    Parameters
    ----------
    name
        name of model
    """

    def __init__(self, name: str) -> None:
        self.name = name
        logger.info(f'{self.name!r} model initializing ...')

    def _prep_list_elements(self, list1: List[str], list2: List[str]) -> List[float]:
        full_sim = self.calc_similarity_list(list1, list2)
        diff_sim = self.calc_similarity_difference_list(list1, list2)
        return [full_sim, diff_sim]

    def _prep_str_elements(self, str1: str, str2: str) -> List[float]:
        full_sim = self.calc_similarity_str(str1, str2)
        diff_sim = self.calc_similarity_difference_str(str1, str2)
        return [full_sim, diff_sim]

    @staticmethod
    def _str_to_list(str1: str, str2: str) -> Tuple[List[str], List[str]]:
        list1, list2 = str1.split(' '), str2.split(' ')
        return list1, list2

    @staticmethod
    def _list_to_str(list1: List[str], list2: List[str]) -> Tuple[str, str]:
        separator = ' '
        str1, str2 = separator.join(list1), separator.join(list2)
        return str1, str2

    def calc_combine_filter_list(self, list1, list2):
        len_threshold = 4

        fixed_list1, fixed_list2 = difference_of_list_both(list1, list2)
        full_sim, diff_sim = self._prep_list_elements(list1, list2)
        if len(list1) < len_threshold and len(list2) < len_threshold:  # if the list is short itself
            appending, condition = full_sim, 1
        elif abs(len(list1) - len(fixed_list1)) < len(list1) / 2:  # if more than half the words are fixed
            appending, condition = diff_sim, 2
        elif abs(len(fixed_list1) - len(fixed_list2)) < 3:  # only if two or less words are different
            appending, condition = diff_sim, 3
        else:  # all other values should take the minimal value
            appending, condition = min(full_sim, diff_sim), 4

        # if appending > 0.3:  # for debugging
        #     print(f'{full_sim}, {diff_sim}, {list1}, {list2}, {appending}, {condition}')
        return appending

    def calc_combine_max_list(self, list1, list2) -> float:
        return max(self._prep_list_elements(list1, list2))

    def calc_combine_min_list(self, list1, list2) -> float:
        return min(self._prep_list_elements(list1, list2))

    def calc_combine_avg_list(self, list1, list2) -> float:
        return mean(self._prep_list_elements(list1, list2))

    def calc_combine_max_str(self, str1: str, str2: str) -> float:
        return self.calc_combine_max_list(self._str_to_list(str1, str2))

    def calc_combine_min_str(self, str1, str2):
        list1, list2 = str1.split(' '), str2.split(' ')
        return self.calc_combine_min_list(list1, list2)

    def calc_combine_avg_str(self, str1, str2):
        list1, list2 = str1.split(' '), str2.split(' ')
        return self.calc_combine_min_list(list1, list2)

    @abstractmethod
    def _load_model(self, model_file):
        pass

    @abstractmethod
    def calc_similarity_list(self, list1, list2):
        pass

    @abstractmethod
    def calc_similarity_str(self, str1, str2):
        pass

    @abstractmethod
    def calc_similarity_difference_list(self, list1, list2):
        pass

    @abstractmethod
    def calc_similarity_difference_str(self, str1, str2):
        pass

    @abstractmethod
    def find_most_similar(self, value_list: list, depth: int):
        pass


class GloVeModel(Model):  # TODO what is the correct docstring for class attributes, # TODO useful? wmd_similarit
    """
    GloVe model (based on Word2Vec)
    """

    # model: None / gensim.models.keyedvectors.Word2VecKeyedVectors
    # similarity_index: Any

    def __init__(self, name: str = 'glove',
                 model_file: str = _glove_file) -> None:
        """
        Parameters
        ----------
        name: str
            name of model (logging purposes)
        model_file: str
            filepath for pre-trained model
        """
        super().__init__(name)
        self._load_model(model_file)

    def __repr__(self):
        return 'SpaCy model'

    def _load_model(self, model_file: str):
        """
        Load GloVe model from file_location

        Parameters
        ----------
        model_file: str
            file_location of model

        Returns
        -------
        model_glove: gensim.models.keyedvectors.Word2VecKeyedVectors
            loaded model (not trainable)
        """
        # TODO make choice available for GloVe model
        try:
            tic = time.perf_counter()
            # model_file = exe_utils.resource_path(model_file)
            binary = self.check_if_binary(model_file)
            if not binary:
                glove_file, model_file = model_file, get_tmpfile('glove.word2vec.txt')
                _ = glove2word2vec(glove_file, model_file)
            self.model = KeyedVectors.load_word2vec_format(model_file, binary=binary)
            self.similarity_index = WordEmbeddingSimilarityIndex(self.model)
            toc = time.perf_counter()
            
            logger.info(f'GloVe model loaded in {toc - tic:0.4f} seconds')
        except FileNotFoundError:
            logger.exception('GloVe Model could not be loaded.')
        except:
            logger.exception('Test')

    @staticmethod
    def check_if_binary(filepath: str) -> bool:
        if filepath.endswith('.txt'):
            return False
        else:  # considering bin as only other option
            return True

    def calc_similarity_list(self, list1, list2):
        # TODO make function calc_similarity_value that decides within the function which type it is working with
        """
        Compute n_similarity between two lists

        Parameters
        ----------
        list1: List[str]
            string to be evaluated (elements of string saved in a list)
        list2: List[str]
            string to be evaluated (elements of string saved in a list)

        Returns
        -------
        similarity_score: float
            result of similarity calculation
        """
        if list1 and list2:
            return self.model.n_similarity(list1, list2)
        else:
            return 0

    def calc_similarity_str(self, str1, str2):
        """
        Compute n_similarity between two strings, adaption to lists necessary

        Parameters
        ----------
        str1: str
            string to be evaluated
        str2: str
            string to be evaluated

        Returns
        -------
        similarity_score: float
            result of similarity calculation
        """
        list1, list2 = str1.split(' '), str2.split(' ')
        return self.calc_similarity_list(list1, list2)

    def calc_similarity_difference_str(self, str1, str2):
        """
        Compute n_similarity between two strings, but the strings are first stripped of shared values

        Parameters
        ----------
        str1: str
            string to be evaluated
        str2: str
            string to be evaluated

        Returns
        -------
        similarity_score: float
            result of similarity calculation
        """
        fixed_str1, fixed_str2 = difference_of_str_both(str1, str2)
        return self.calc_similarity_str(fixed_str1, fixed_str2)

    def calc_similarity_difference_list(self, list1, list2):
        """
        Compute n_similarity between two lists, but lists are first stripped of shared values

        Parameters
        ----------
        list1: List[str]
            string to be evaluated (elements of string saved in a list)
        list2: List[str]
            string to be evaluated (elements of string saved in a list)

        Returns
        -------
        similarit_score: float
            result of similarity calculation
        """
        fixed_list1, fixed_list2 = difference_of_list_both(list1, list2)
        return self.calc_similarity_list(fixed_list1, fixed_list2)

    def find_most_similar(self, value_list: list, depth: int = 10):
        """
        Find similar words from a given value_list

        Parameters
        ----------
        value_list: List[str]
            sequence of strings
        depth: int
            depth of how far top-N similar words are searched

        Returns
        -------
        similar_words: Dict[str, List[str]]
            {key: element from value_list, value: top-N similar words with score}
        """
        tic = time.perf_counter()
        similar_words = {}
        for i in value_list:
            similar_words[i] = self.model.most_similar(str(i), topn=depth)
        toc = time.perf_counter()
        logger.info(f'The \'find_similar_words\' process found similar words in {toc - tic} seconds')
        return similar_words


class SpaCyModel(Model):
    """
    SpaCy functions for preprocessing and model
    """
    model: spacy.lang

    def __init__(self, name: str = 'spacy',
                 model_file: str = 'en_core_web_md'):
        """
        Parameters
        ----------
        name: str
            name of model (logging purposes)
        model_file: str
            filepath for pre-trained model
        """
        super().__init__(name)
        self._load_model(model_file)

    def _load_model(self, model_file: str) -> spacy.lang:
        """
        Different approach than Word2Vec

        Parameters
        ----------
        model_file: str
            file_location of model

        Returns
        -------
        nlp: spacy.lang.en.English
            loaded spacy model (not trainable)
        """
        try:
            tic = time.perf_counter()
            self.model = spacy.load(model_file)
            toc = time.perf_counter()
            logger.info(f'SpaCy Model loaded in {toc - tic:0.4f} seconds')
        except:
            logger.exception('SpaCy model could not be loaded.')

    def calc_similarity_str(self, str1: str, str2: str) -> float:
        """
        Compute symmetric vector similarity between two strings

        Parameters
        ----------
        str1: str
            string to evaluate
        str2: str
            string to evaluate

        Returns
        -------
        sim_result: float
            result of similarity calculation
        """
        if str1 and str2:
            return self.model(str1).similarity(self.model(str2))
        else:
            return 0

    def calc_similarity_list(self, list1: list, list2: list) -> float:
        """
        Compute symmetric vector similarity between two lists

        Parameters
        ----------
        list1: List[str]
            string to be evaluated (elements of string saved in a list)
        list2: List[str]
            string to be evaluated (elements of string saved in a list)

        Returns
        -------
        similarit_score: float
            result of similarity calculation
        """
        separator = ' '
        str1, str2 = separator.join(list1), separator.join(list2)
        return self.calc_similarity_str(str1, str2)

    def calc_similarity_difference_str(self, str1, str2):
        """
        Compute n_similarity between two strings, but the strings are first stripped of shared values

        Parameters
        ----------
        str1: str
            string to evaluate
        str2: str
            string to evaluate

        Returns
        -------
        sim_result: float
            result of similarity calculation
        """
        fixed_str1, fixed_str2 = difference_of_str_both(str1, str2)
        return self.calc_similarity_str(fixed_str1, fixed_str2)

    def calc_similarity_difference_list(self, list1, list2):
        """
        Compute n_similarity between two lists, but lists are first stripped of shared values

        Parameters
        ----------
        list1: List[str]
            string to be evaluated (elements of string saved in a list)
        list2: List[str]
            string to be evaluated (elements of string saved in a list)

        Returns
        -------
        similarit_score: float
            result of similarity calculation
        """
        fixed_list1, fixed_list2 = difference_of_list_both(list1, list2)
        return self.calc_similarity_list(fixed_list1, fixed_list2)

    def filter_stopwords_and_lemmatize(self, string1):  # Implemented in AttributeValue class
        """
        Normal string is filtered to not contain SpaCy stopwords and words are lemmatized for better comparison

        Parameters
        ----------
        string1: str
            list to evaluate

        Returns
        -------
        filtered_doc: List[str]
            lemmatized list that is filtered from OOV / stopwords
        """
        return [[token.lemma_, token.pos_] for token in self.model(string1) if not token.is_stop or token.is_oov]

    def find_most_similar(self, value_list: List[str], depth: int = 10) -> Dict[str, List[str]]:
        """
        Find similar words from a given value_list

        Parameters
        ----------
        value_list
            sequence of strings
        depth
            depth of how far top-N similar words are searched

        Returns
        -------
        similar_words
            {key: element from value_list, value: top-N similar words with score}
        """
        """
        Find similar words from a given value_list

        :param (list) value_list: sequence of strings
        :param (int) depth: depth of how far top-N similar words are searched

        :return (dict) similar_words: {key: element from value_list, value: top-N similar words with score}
        """
        similar_words = {}
        for word in value_list:
            ms = self.model.vocab.vectors.most_similar(
                np.asarray([self.model.vocab.vectors[self.model.vocab.strings[word]]]), n=depth)
            words = [self.model.vocab.strings[w] for w in ms[0][0]]
            distances = ms[2][0].tolist()  # turn array to list for zipping
            similar_words[word] = list(zip(words, distances))
        return similar_words


# unit test successful
if __name__ == '__main__':
    tic = time.perf_counter()
    logger.info('-----New entry!-----')
    glove = GloVeModel('glove', _glove_file)
    print(glove.calc_similarity_str('submit', 'send'))
    # word2vec = GloVeModel('word2vec', _word2vec_file)
    # print(word2vec.calc_similarity_str('submit', 'send'))

    nlp = SpaCyModel('spacy', _spacy_file_md)
    print(nlp.calc_similarity_str('submit', 'send'))

    ms_glove = glove.find_most_similar(['test', 'permit'], depth=10)
    print(ms_glove)
    ms_nlp = nlp.find_most_similar(['test', 'permit'], depth=10)
    print(ms_nlp)
    # very different results
    toc = time.perf_counter()
    logger.info(f'Test resulted in {toc - tic} seconds')
