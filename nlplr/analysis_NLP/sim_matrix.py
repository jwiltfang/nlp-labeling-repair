from nlplr.analysis_NLP.nlp_models import GloVeModel, SpaCyModel
from nlplr.analysis_NLP import sim_utils

from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from gensim.similarities import SparseTermSimilarityMatrix, MatrixSimilarity, LevenshteinSimilarityIndex, SoftCosineSimilarity

import numpy as np
from abc import ABC, abstractmethod
from typing import List, Dict, Union
import time
import logging
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
logger = logging.getLogger(__name__)


class SimMatrix(ABC):
    """
    Abstract Base class for SimMatrix to ensure that all implementations have the same functionality
    """

    def __init__(self, name: str, content: List[List[str]]) -> None:
        self.name = name
        self.content = content
        self.sim_matrix = None

    def log_info(self, time: float) -> None:
        logger.info(f'Similarity matrix {self.name}, {self.content} in {time} seconds.')  # -> result:\n{self.sim_matrix}')

    @abstractmethod
    def _calc_sim_matrix(self):
        pass


class GloVeSimMatrix(SimMatrix):
    """
    GloVeSimilarityMatrix based on -- missing --  # TODO
    """
    def __init__(self, name: str, content: List[List[str]], glove: GloVeModel, _: str) -> None:
        tic = time.perf_counter()
        super().__init__(name, content)
        self.glove = glove
        self.sim_matrix = self._calc_sim_matrix()

        toc = time.perf_counter()
        self.log_info((toc-tic))

    def _calc_sim_matrix(self) -> np.ndarray:
        """
        Calculate similarity matrix the way gensim intended
        """
        termsim_index = self.glove.similarity_index
        dictionary, documents_doc2bow, tfidf = sim_utils.initialize_tfidf_content(
            self.content)  # tfidf is not used in this implementation
        similarity_matrix = SparseTermSimilarityMatrix(termsim_index, dictionary)
        docsim_index = SoftCosineSimilarity(documents_doc2bow, similarity_matrix)

        score_list = []
        for query in self.content:
            sims = docsim_index[dictionary.doc2bow(query)]
            score_list.append(sims.tolist())
        sim_matrix = np.asarray(score_list, dtype=object)
        return sim_matrix


class OpenGloVeSimMatrix(SimMatrix):
    """
    OpenGloVeSimilarityMatrix can use any function defined in glove model
    """
    def __init__(self, name: str, content: List[List[str]], glove: GloVeModel, function: str) -> None:
        tic = time.perf_counter()
        super().__init__(name, content)
        self.glove = glove
        self.function = sim_utils._check_function(self.glove, function)
        self.sim_matrix = self._calc_sim_matrix()

        toc = time.perf_counter()
        self.log_info((toc - tic))

    def _calc_sim_matrix(self) -> np.ndarray:
        """
        Returns the similarity matrix based on glove_algorithm calc_similarity_list
        """
        return sim_utils.abstract_calc_sim_matrix(self.name, self.content, self.function)


# TODO does not work currently
class TfIdfSimMatrix(SimMatrix):
    """
    TfIdfSimMatrix based on term frequency-inverse document frequency
    """
    def __init__(self, name: str, content: List[List[str]], glove: GloVeModel, _: str) -> None:
        tic = time.perf_counter()
        # initialization and complete calculation
        super().__init__(name, content)
        self.glove = glove
        self.sim_matrix = self._calc_sim_matrix()

        toc = time.perf_counter()
        self.log_info((toc - tic))

    def _calc_sim_matrix(self) -> np.ndarray:
        dictionary, documents_doc2bow, tfidf = sim_utils.initialize_tfidf_content(self.content)
        tfidf_corpus = [tfidf[document] for document in documents_doc2bow]

        docsim_index = MatrixSimilarity(tfidf_corpus, num_features=len(dictionary))
        sim_matrix = self.generate_tfidf_sim_matrix(documents_doc2bow, docsim_index)
        return sim_matrix

    @staticmethod
    def generate_tfidf_sim_matrix(documents_doc2bow: List[str], docsim_index: MatrixSimilarity) -> np.ndarray:
        """
        from computed cosine or soft cosine similarity generate readable sim_matrix

        Parameters
        ----------
        documents_doc2bow
            all documents adapted to bag-of-words
        docsim_index
            -- missing --

        Returns
        -------
        sim_matrix
            results of similarity queries
        """
        score_list = []
        for query in documents_doc2bow:
            sim_scores = docsim_index[query]
            score_list.append(sim_scores)
        sim_matrix = np.asarray(score_list)
        return sim_matrix


class SpaCySimMatrix(SimMatrix):
    def __init__(self, name: str, content: List[List[str]], nlp: SpaCyModel, function: str) -> None:
        tic = time.perf_counter()
        super().__init__(name, content)
        self.nlp = nlp
        self.function = sim_utils._check_function(self.nlp, function)
        self.sim_matrix = self._calc_sim_matrix()

        toc = time.perf_counter()
        self.log_info((toc - tic))

    def _calc_sim_matrix(self) -> np.ndarray:
        """
        Returns the similarity matrix based on glove_algorithm calc_similarity_list

        abstract_calc_sim_matrix(name, content, func_matrix, func_vec)
        """
        return sim_utils.abstract_calc_sim_matrix(self.name, self.content, self.function)


class LevenshteinSimMatrix(SimMatrix):
    def __init__(self, name: str, content: Union[List[str], List[List[str]]], _1: str, _2: str) -> None:
        tic = time.perf_counter()
        # initialization and complete calculation
        super().__init__(name, content)
        self.sim_matrix = self._calc_sim_matrix()

        toc = time.perf_counter()
        self.log_info((toc - tic))

    def _calc_sim_matrix(self) -> np.ndarray:
        score_list = []
        for query in self.content:
            sim_scores = sim_utils.calc_levenshtein_sim(query, self.content)
            score_list.append(sim_scores)
        sim_matrix = np.asarray(score_list)
        return sim_matrix


# unit test
if __name__ == '__main__':
    from nlp_models import GloVeModel, SpaCyModel
    glove = GloVeModel()
    content = ['Start file', 'End file', 'Change my life']
    contents = [string.split(' ') for string in content]
    glove_sim_matrix = GloVeSimMatrix('name', contents, glove)

    print(glove_sim_matrix.sim_matrix)
    print(glove_sim_matrix.name)
    print(glove_sim_matrix.content)

    nlp = SpaCyModel()
    content = ['Start file', 'End file', 'Change my life']
    contents = [string.lower().split(' ') for string in content]
    spacy_matrix = SpaCySimMatrix('name', contents, glove, 'calc_similarity_difference_list')

    print(spacy_matrix.sim_matrix)
    print(spacy_matrix.name)
    print(spacy_matrix.content)
