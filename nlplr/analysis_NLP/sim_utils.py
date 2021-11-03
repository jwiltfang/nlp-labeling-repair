from nlplr.analysis_NLP.nlp_models import GloVeModel, SpaCyModel
from nlplr.utils import label_utils

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities.levenshtein import levsim

import numpy as np
import logging
import time
from typing import List, Callable, Tuple, Any, Union

logger = logging.getLogger(__name__)
logger.disabled = False


def _check_function(model: Union[GloVeModel, SpaCyModel], function: str) -> Callable[[List[str], List[str]], float]:
    assert isinstance(function, str), 'Function values has to be passed as a string'
    function = getattr(model, function)
    return function


def abstract_calc_sim_matrix(name: str,
                             content: List[List[str]],
                             func_vec: Callable[[List[str], List[str]], float]) -> np.ndarray:
    """
    Abstract version to calculate similarity matrix based on varying similarity functions / algorithms

    Parameters
    ----------
    name
        name of matrix
    content
        content to compare similarity for
    func_vec
        function for similarity_scores

    Returns
    -------
    sim_matrix
        result of appending vectors of similarity scores
    """
    tic = time.perf_counter()
    score_list = []
    for query in content:
        sim_scores = abstract_calc_sim(query, content, func_vec)
        score_list.append(sim_scores)
    sim_matrix = np.asarray(score_list)
    toc = time.perf_counter()
    logger.info(f'SimilarityMatrix {name} has been calculated in {toc - tic} seconds')
    return sim_matrix


def abstract_calc_sim(query: List[str],
                      content: List[List[str]],
                      func_vec: Callable[[List[str], List[str]], float]) -> List[float]:
    """
    Calculate the sim_scores for every query compared to each element of content

    Parameters
    ----------
    query
        element to compare to every element of content
    content
        content to compare similarity for
    func_vec
            function for similarity_scores

    Returns
    -------
    sim_scores
        similarity scores
    """
    sim_scores = []
    for i in content:
        if i and query:
            sim_value = func_vec(query, i)
            sim_scores.append(sim_value)
        else:
            sim_scores.append(float(0))
    return sim_scores


def initialize_tfidf_content(content: List[List[str]]) -> Tuple[Any, Any, Any]:
    """
    Initilialize content for GloVeSimMatrix and TfIdfSimMatrix and turn it into bag-of-words

    Parameters
    ----------
    content
        content to compare similarity for

    Returns
    -------
    dictionary
        -- missing --
    documents_doc2bow
        -- missing --
    tfidf
        -- missing --
    """
    dictionary = Dictionary(content)
    documents_doc2bow = [dictionary.doc2bow(document) for document in content]
    tfidf = TfidfModel(documents_doc2bow)  # combination for keyword smartirs (e.g. = 'apc' possible)  TODO find out what special characters change
    return dictionary, documents_doc2bow, tfidf


def calc_levenshtein_sim(t1: Union[str, List[str]],
                         content: Union[List[str],  List[List[str]]],
                         len_threshold: int = 17) -> List[float]:
    """
    Calculates the levenshtein similarity of one term against all other terms in content
    Both str and List[str] can be entered into this function as a term

    Parameters
    ----------
    t1
        base term to be compared
    content
        other values that t1 is compared to
    len_threshold
        term length to which only full results are calculated

    Returns
    -------
    result_lev_sim
        list of levenshtein similarity values
    """
    # TODO filters could be added that integrate the number of strings in one term
    result_lev_sim = []
    if isinstance(t1, list):
        result_lev_sim = _calc_levenshtein_distance_list(result_lev_sim, t1, content, len_threshold)
    elif isinstance(t1, str):
        result_lev_sim = _calc_levenshtein_distance_str(result_lev_sim, t1, content, len_threshold)
    return result_lev_sim


def _calc_levenshtein_distance_str(result_lev_sim: List[float],
                                   t1: str,
                                   content: List[str],
                                   len_threshold: int) -> List[float]:
    """
    Implementation of levenshtein distance with t1: str as input
    """
    for t2 in content:
        fixed_t1, fixed_t2 = label_utils.difference_of_str_both(t1, t2)
        result_real = levsim(t1, t2)  # full strings
        result_diff = levsim(fixed_t1, fixed_t2)  # different strings
        # filter results
        if len(t1) < len_threshold:  # if the string is short itself
            appending, condition = result_real, 1
        elif abs(len(t1) - len(fixed_t1)) < len(t1) / 2:  # if more than half the letters are fixed
            appending, condition = result_diff, 2
        elif abs(len(fixed_t1) - len(fixed_t2)) <= 3:  # difference compare length of fixed_values
            appending, condition = result_diff, 3
        else:  # all other values should take the minimal value
            appending, condition = min(result_real, result_diff), 4

        result_lev_sim.append(min(appending,
                                  1.0))  # all values above 1.0 will be decreased to 1 in order to make sense with all other calculations
    return result_lev_sim


def _calc_levenshtein_distance_list(result_lev_sim: List[float],
                                    t1: List[str],
                                    content: List[List[str]],
                                    len_threshold: int) -> List[float]:
    """
    Implementation of levenshtein distance with t1: List[str] as input
    """
    for t2 in content:
        fixed_t1, fixed_t2 = label_utils.difference_of_list_both(t1, t2)
        result_real = levsim(' '.join(t1), ' '.join(t2))
        result_diff = levsim(' '.join(fixed_t1), ' '.join(fixed_t2))
        # filter results
        if len(t1) < len_threshold:  # if the string is short itself
            appending, condition = result_real, 1
        elif abs(len(t1) - len(fixed_t1)) < len(t1) / 2:  # if more than half the letters are fixed
            appending, condition = result_diff, 2
        elif abs(len(fixed_t1) - len(fixed_t2)) <= 3:  # difference compare length of fixed_values
            appending, condition = result_diff, 3
        else:  # all other values should take the minimal value
            appending, condition = min(result_real, result_diff), 4

        result_lev_sim.append(min(appending,
                                  1.0))  # all values above 1.0 will be decreased to 1 in order to make sense with all other calculations
    return result_lev_sim
