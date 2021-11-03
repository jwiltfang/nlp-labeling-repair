from typing import Dict, List, Tuple
from re import sub


def preprocess_value(value):  # TODO add preprocessing for noise and others, inspiration on the web
    """
    Preprocess value with regex to clear noise and data

    Parameters
    ----------
    value: str
        string to be preprocessed

    Returns
    -------
    preprocessed: str
        value that is already filtered from tokens that are not in
    """
    value = value.split('_')
    value = str(' '.join(value)).lower().split(' ')
    preprocessed = []
    for v in value:
        v = sub(r'<img[^<>]+(>|$)', ' image_token ', v)
        v = sub(r'<[^<>]+(>|$)', ' ', v)
        # noinspection RegExpDuplicateCharacterInClass
        v = sub(r'[img_assist[^]]*?]', ' ', v)
        v = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|%[0-9a-fA-F][0-9a-fA-F])+', ' url_token ', v)
        preprocessed.append(v)
    preprocessed_str = ' '.join(preprocessed)
    return preprocessed_str.lower()  # return result as a lowered string


def difference_of_list(value, other_value):
    """
    Compare two value lists and return a set for each list that does not include shared values, RETURN ONE LIST

    Parameters
    ----------
    value: List[str]
        list to be compared to other list (most often some certain properties)
    other_value: List[str]
        other list for comparison

    Returns
    -------
    fixed_list: List[str]
        contains only single list only with elements that are NOT in other_value
    """
    return [i for i in value if i not in other_value]


def difference_of_list_both(value, other_value):
    """
    Compare two value lists and return a set for each list that does not include shared values, RETURN BOTH LISTS

    Parameters
    ----------
    value: List[str]
        list to be compared to other list (most often some certain properties)
    other_value: List[str]
        other list for comparison

    Returns
    -------
    fixed_lists: Tuple[List[str]]
        contains both lists only with elements that are NOT in other_value
    """
    return difference_of_list(value, other_value), difference_of_list(other_value, value)


def difference_of_str(value, other_value):
    """
    Compare two strings of given property and return a string that does not include shared values

    Parameters
    ----------
    value: str
        string to be compared
    other_value: str
        other string for comparison

    Returns
    -------
    fixed_str: str
        contains only single string only with elements that are NOT in other_value
    """
    fixed_list = difference_of_list(value.split(' '), other_value.split(' '))
    return ' '.join(fixed_list)


def difference_of_str_both(value, other_value):
    """
    Compare two strings of given property and return a string that does not include shared values, RETURN BOTH STRINGS

    Parameters
    ----------
    value: str
        string to be compared
    other_value: str
        other string for comparison

    Returns
    -------
    fixed_strs: Tuple[str]
        contains both strings only with elements that are NOT in other_value
    """
    return difference_of_str(value, other_value), difference_of_str(other_value, value)