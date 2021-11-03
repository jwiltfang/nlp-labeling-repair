from nlplr.utils import matrix_eval
from nlplr.analysis_NLP.attribute_value import Attribute, AttributeValue
from nlplr.repair.repair_options import RepairOption
from nlplr.analysis_NLP.analysis_options import AnalysisOption

import pm4py
from pm4py.objects.log.log import EventLog

import numpy as np

from typing import Dict, List, Tuple, Union, Any
import logging

logger = logging.getLogger(__name__)


def filter_log_on_given_level(log: EventLog,
                              attribute: str,
                              values: Any,
                              level: str = 'event',
                              retain: bool = False) -> EventLog:
    """
    Filter event log on certain attribute given certain filter on a given level

    Parameters
    ----------
    log
        pm4py eventlog
    attribute
        attribute to filter
    values
        values to be filtered for
    level
        which level should the filter work on (event or case level)
    retain
        if level instance should be kept or not

    Returns
    -------
    filtered_log
        new event log, filtered on conditions above
    """
    filtered_log = pm4py.filter_event_attribute_values(log, attribute, values, level, retain)
    return filtered_log


def generate_sim_matrices(attributes: List[Attribute],
                          name: str,
                          options: AnalysisOption) -> None:
    """
    Calculate the similarity matrices for each attribute and save them within their instance in a dict

    Parameters
    ----------
    attributes
        set of attributes to work with
    name
        key for dict to get correct similarity_matrices back for different analysis purposes
    options
        list of options [model, name, attribute to look for, function]
    """
    for attribute in attributes:
        attribute.build_sim_matrix(name, options)


def get_result_selection(all_sim_matrices: Dict[Attribute, Dict[str, List[np.ndarray]]],
                         options: AnalysisOption,
                         antonym_library) -> Dict[int, RepairOption]:
    repair_selection_dict, repair_id = {}, 0
    for attribute, matrix_content in all_sim_matrices.items():
        for name, matrices in matrix_content.items():
            for i, matrix in enumerate(matrices):
                relevant_indices, relevant_values = matrix_eval.get_results_from_matrix(matrix, options.threshold)
                for index, sim_score in zip(relevant_indices, relevant_values):
                    # attribute value instances for given indices
                    value1, value2 = attribute.attr_values[index[0]], attribute.attr_values[index[1]]
                    correct_value, incorrect_value = _get_repair_values_after_sorting(value1, value2)
                    if correct_value and incorrect_value:
                        # antonym distinction, if there are any antonyms and skip selection
                        antonym_set = _check_antonymy(antonym_library, value1, value2)
                        rep_option = RepairOption(attribute, correct_value, incorrect_value, sim_score, antonym_set, options)
                        if rep_option:
                            repair_selection_dict[repair_id] = rep_option
                        repair_id += 1
                    else:
                        # declaration as correct or incorrect only possible if the count is different
                        continue
    return repair_selection_dict


def _get_repair_values_after_sorting(value1: AttributeValue, value2: AttributeValue) -> Union[Tuple[None, None], Tuple[AttributeValue, AttributeValue]]:
    """Turn possible repair options into RepairOption instances"""
    freq1, freq2 = value1.count, value2.count
    # based on frequency, decide which value should be changed in the original log
    if freq1 == freq2:
        return None, None
    elif freq1 < freq2:
        incorrect_value, correct_value = value1, value2
    else:
        incorrect_value, correct_value = value2, value1

    return correct_value, incorrect_value


def _check_antonymy(antonym_library: Dict[str, List[str]],
                    attr_value1: 'AttributeValue',
                    attr_value2: 'AttributeValue') -> Dict[str, str]:
    """
    Check if there are any shared antonyms within the two values

    Parameters
    ----------
    antonym_library
        set of antonyms derived from verbocean file
    attr_value1:
        first instance of AttributeValue to be compared
    attr_value2
        second instance of AttributeValue to be compared

    Returns
    -------
    total_antonym_set
        set of antonyms that both attr_values 'share'
    """
    total_antonym_set = {}
    total_antonym_set.update(
        get_antonym_from_verbocean_local(antonym_library, attr_value1.spacy_lemmas, attr_value2.spacy_lemmas))
    total_antonym_set.update(
        get_antonyms_of_two_terms_from_wordnet(attr_value1.synsets_right_pos, attr_value2.synsets_right_pos))
    return total_antonym_set


def get_antonyms_of_two_terms_from_wordnet(term1_synsets: Dict[str, List['Synset']],
                                           term2_synsets: Dict[str, List['Synset']]) -> Dict[str, List[str]]:
    """
    Return the antonym both terms and their corresponding synsets share

    Parameters
    ----------
    term1_synsets
        set of synsets for each value in the term
    term2_synsets
        set of synsets for each value in the term

    Returns
    -------
    antonym_library
        key corresponds to the antonym in the other term
    """
    antonym_set = {}
    for key1, syn1 in term1_synsets.items():
        for key2, syn2 in term2_synsets.items():
            lemma1_list, lemma2_list = [], []
            ant1_list, ant2_list = [], []
            for synset1 in syn1:
                for synset2 in syn2:
                    if synset1.pos() == synset2.pos():
                        lemma1_list.extend(set([lemma for lemma in synset1.lemmas()]))
                        lemma2_list.extend(set([lemma for lemma in synset2.lemmas()]))
                        ant1_list.extend(set([ant for lemma in lemma1_list for ant in lemma.antonyms()]))
                        ant2_list.extend(set([ant for lemma in lemma2_list for ant in lemma.antonyms()]))

            if set.intersection(set(lemma1_list), set(ant2_list)):
                lib_key, lib_value = key1, list(key2.split())
                if lib_key in antonym_set.keys():
                    antonym_set[lib_key].extend(lib_value)
                else:
                    antonym_set[lib_key] = lib_value
            if set.intersection(set(lemma2_list), set(ant1_list)):
                lib_key, lib_value = key2, list(key1.split())
                if lib_key in antonym_set.keys():
                    antonym_set[lib_key].extend(lib_value)
                else:
                    antonym_set[lib_key] = lib_value
    return antonym_set


def _line_to_tuple(line: str) -> Tuple[str, str, str, str]:
    """
    Turn line from verbocean into correct observation

    Parameters
    ----------
    line
        line from verbocean that has to be separated and prepared
    """
    start_br = line.find('[')
    end_br = line.find(']')
    conf_delim = line.find('::')
    verb1 = line[:start_br].strip()
    rel = line[start_br + 1: end_br].strip()
    verb2 = line[end_br + 1: conf_delim].strip()
    conf = line[conf_delim: len(line)].strip()
    return verb1, rel, verb2, conf


def get_antonyms_from_verbocean() -> Dict[str, List[str]]:
    """
    Get antonym library based on verbocean.txt
    Relation:   opposite-of returns opposities resembling antonyms for verbs

    Returns
    -------
    antonym_library
        all antonyms from verbocean saved in a dictionary
    """
    input_file = 'data/verbocean.txt'
    rel_to_observation = ["opposite-of"]
    antonym_library = {}
    with open(input_file) as f:
        line = f.readline()
        while line:
            if not line.startswith("#"):
                (verb1, rel, verb2, conf) = _line_to_tuple(line)
                if rel in rel_to_observation:
                    if verb1 in antonym_library:
                        antonym_library[verb1].append(verb2)
                    else:
                        antonym_library[verb1] = [
                            verb2]  # create list with first element if the key is found for the first time
            line = f.readline()
    return antonym_library


def get_synonyms_from_verbocean() -> Dict[str, List[str]]:
    """
    Get synonym library based on verbocean.txt
    Relation:   stronger-than as it often still conveys the same meaning
                similar as it gives synonyms

    Returns
    -------
    synonym_library
        all synonyms from verbocean saved in a dictionary
    """
    # TODO make use of synonyms by verbocean
    input_file = 'data/verbocean.txt'
    rel_to_observation = ["stronger-than", "similar"]
    synonym_library = {}
    with open(input_file) as f:
        line = f.readline()
        while line:
            if not line.startswith("#"):
                (verb1, rel, verb2, conf) = _line_to_tuple(line)
                if rel in rel_to_observation:
                    if verb1 in synonym_library:
                        synonym_library[verb1].append(verb2)
                    else:
                        synonym_library[verb1] = [
                            verb2]  # create list with first element if the key is found for the first time
            line = f.readline()
    return synonym_library


def get_antonym_from_verbocean_local(antonym_library: Dict[str, List[str]],
                                     lemmas1: List[str],
                                     lemmas2: List[str]) -> Dict[str, str]:
    """
    Check if there are 'shared' antonyms between both lemmas within antonym_library and return them
    Returns
    -------
    antonym_set
        set of antonym_dictionary for current values lemmas1 and lemmas2
    """
    antonym_set = {}
    for lemma1 in lemmas1:
        if lemma1 in antonym_library.keys():
            for lemma2 in lemmas2:
                if lemma2 in antonym_library[lemma1]:
                    antonym_set[lemma1] = lemma2
    return antonym_set
