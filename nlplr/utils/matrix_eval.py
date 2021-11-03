import numpy as np
from typing import Dict, List, Tuple
import logging
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
logger = logging.getLogger(__name__)


def round_matrix(a, decimals: int = 4):
    """
    Round array in-line

    :param (np.nadarray) a: array to work on
    :param (int) decimals: characteristic of rounding
    """
    np.around(a, decimals)


def set_diagonal_to_zero(a):
    """
    Checks if array is dimensioned symmetrically and fills diagonal with 0

    :param (np.ndarray) a: array to work on
    """
    np.fill_diagonal(a, float(0))


def round_and_diagonal_zero(a, decimals: int = 4):
    """
    Diagonal is set to zero and rounded to the given decimal count

    :param (np.nadarray) a: array to work on
    :param (int) decimals: characteristic of rounding
    """
    set_diagonal_to_zero(a)
    round_matrix(a, decimals)


def get_value_by_index(a, index):
    """
    Get value of a array by its index

    :param (np.ndarray) a:
    :param (list) index:

    :return (float) value:
    """
    if a.ndim == 2:
        return a[index[0]][index[1]]
    else:
        logger.info('The given matrix does ')


def get_value_list_by_indices(a, indices):
    """
    Return a list of values of array a given by the indices

    :param (np.ndarray) a: array to work on
    :param (List[List]) indices:

    :return (List[float])
    """
    return [get_value_by_index(a, index) for index in indices]


def get_sorted_indices(a):
    """
    Return the indices sorted by value in descending order

    :param (np.ndarray) a: array

    :return (np.ndarray): indices
    """
    flat_index = (-a).argsort(axis=None, kind='stable')  # get max indices with stable sort
    j = np.unravel_index(flat_index, a.shape)  # unflatten the indices
    return np.vstack(j).T


def get_length_to_threshold(a, var, threshold):
    """
    Return length of sorted indices

    :param a: array
    :param (np.ndarray) var: array of sorted indices
    :param (float) threshold: value that each element of a has to be above

    :return (int) length:
    """
    list_above = [element for element in list(var) if a[element[0]][element[1]] > threshold]
    return len(list_above)


def get_max_indices_above_threshold(a, threshold):
    """
    Only returns the indices of the array a which values are above the given threshold
    :param (np.ndarray) a: array to work on
    :param (float) threshold: value to check if it is necessary for analysis
    :return (np.ndarray): indices that are interesting
    """
    var = get_sorted_indices(a)
    len_indices = get_length_to_threshold(a, var, threshold)
    return var[:len_indices]


def get_results_from_matrix(a: np.ndarray, threshold: float) -> Tuple[np.ndarray, List[float]]:
    """
    Return max values and corresponding indices

    Parameters
    ----------
    a: np.ndarray
        matrix of which the maximum should be found
    threshold: float
        minimal value each matrix element needs to have to be looked into

    Returns
    -------
    max_indices, max_values: Tuple[np.ndarray, List[float]]
        relevant indices; corresponding values
    """
    upper_triangle = np.triu(a)  # filter only upper triangle
    round_and_diagonal_zero(upper_triangle)
    max_indices = get_max_indices_above_threshold(upper_triangle, threshold)
    max_values = get_value_list_by_indices(a, max_indices)
    return max_indices, max_values
