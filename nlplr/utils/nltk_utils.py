import nltk
from nltk.corpus import wordnet

from typing import List, Dict


def pos_tag_wordnet(text: List) -> List:  # TODO connect this with spacy for better checks and if they do not agree, change to spacy with the use of nltks naming
    """Create pos_tag with wordnet format

        :rtype: object
        :param (List) text: string to be nltk_pos_tagged for syntactic similar synonyms

        :return (List[List[str, 'pos_tag']]) tagged_text: str values with according nltk_pos_tag
    """
    pos_tagged_text = nltk.pos_tag(text)
    # map the pos tagging output with wordnet output
    tagged_text = []
    wordnet_map = {
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "J": wordnet.ADJ,
        "R": wordnet.ADV
    }
    for (word, pos_tag) in pos_tagged_text:
        tagged_text.append((word, wordnet_map.get(pos_tag[0])) if pos_tag[0] in wordnet_map.keys() else (word, wordnet.NOUN))
    return tagged_text


def get_nltk_synsets(nltk_pos_tokens) -> Dict[str, List[str]]:
    """
    Return list of all synsets with right pos tag for each token

    :return Dict[str, List[str]] synsets_right_pos:
    """
    synsets_right_pos = {}
    for token, pos in nltk_pos_tokens:
        synsets_right_pos[token] = wordnet.synsets(token, pos=pos)
    return synsets_right_pos


def get_nltk_data(synsets_right_pos) -> object:
    """
    Combine all three function from below to only iterate synsets_right_pos once
    ------------
    Return only lemmas from all synsets, double values deleted through set

    :return Dict[str, List] lemmas_set
    -----
    Return the antonyms from all synsets, double values deleted through set

    :return Dict[str, List] antonyms_set
    -----
    Return the hypernyms_set of the synsets (more abstract term)

    :return Dict[str, List] hypernyms_set:
    """
    lemmas_set = {}
    antonyms_set = {}
    hypernyms_set = {}
    for token, synsets in synsets_right_pos.items():
        # synonym lemmas
        lemmas_set[token] = list(set([lemma for syn in synsets for lemma in syn.lemmas()]))
        # antonyms
        antonyms = []
        for syn in synsets:
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.extend(lemma.antonyms())  # extend because lemma.antonyms() is an iterable
        antonyms_set[token] = list(set(antonyms))
        # hypernyms
        hypernyms_set[token] = list(set([hypernym for syn in synsets for hypernym in syn.hypernyms()]))
    return lemmas_set, antonyms_set, hypernyms_set


"""NLTK functions and model"""  # TODO explain difference of calculations


def nltk_calc_wup_similarity(synset1: 'Synset', synset2: 'Synset') -> float:
    """
    Compute symmetric vector similarity between document lists (easy to handle when all models take same input)

    :param ('Synset') synset2: synset to evaluate
    :param ('Synset') synset1: sysnet to evaluate

    :return (float) sim_result: similarity score between string sequences
    """
    return synset1.wup_similarity(synset2)


def nltk_calc_path_similarity(synset1: 'Synset', synset2: 'Synset') -> float:
    """
    Compute symmetric vector similarity between document lists (easy to handle when all models take same input)

    :param ('Synset') synset2: synset to evaluate
    :param ('Synset') synset1: sysnet to evaluate

    :return (float) sim_result: similarity score between string sequences
    """
    return synset1.path_similarity(synset2)


def nltk_calc_lch_similarity(synset1: 'Synset',
                             synset2: 'Synset') -> float:  # not used because it does not return values between 0 and 1
    """
    Compute symmetric vector similarity between document lists (easy to handle when all models take same input)

    :param ('Synset') synset2: synset to evaluate
    :param ('Synset') synset1: sysnet to evaluate

    :return (float) sim_result: similarity score between string sequences
    """
    return synset1.lch_similarity(synset2)


# TODO more similarities with information content
# wordnet_ic = nltk.corpus.reader.wordnet.WordNetCorpsReader.ic(wordnet)