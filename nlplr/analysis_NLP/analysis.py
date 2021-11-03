from nlplr.analysis_NLP import analysis_utils
from nlplr.analysis_NLP.analysis_options import AnalysisOption
from nlplr.analysis_NLP.attribute_value import Attribute
from nlplr.analysis_NLP.nlp_models import GloVeModel, SpaCyModel
from nlplr.repair.repair_options import RepairOption

import numpy as np
from typing import List, Dict, Tuple, Any, Union
from abc import ABC, abstractmethod
import time
import logging

logger = logging.getLogger(__name__)


class Analysis(ABC):
    def __init__(self, controller) -> None:
        self.controller = controller

    @abstractmethod
    def start(self, attribute_content):
        pass


class AnalysisModule(Analysis):
    """
    AnalysisModule correcting grammatical and synonymous errors

    Parameters
    ----------
    nlp
        spacy Model
    glove
        KeyedVectors model
    name
        name of this analysis instance
    options
        configuration options for the analysis
    threshold
        configuration under which the results are filtered
    controller
        main controller for the full program
    """

    def __init__(self,
                 controller,
                 nlp: SpaCyModel,
                 glove: GloVeModel,
                 analysis_option: AnalysisOption):
        super().__init__(controller)
        self.nlp = nlp
        self.glove = glove
        # analysis setup
        self.analysis_option = analysis_option
        self.name = self.analysis_option.name
        self.threshold = self.analysis_option.threshold

        self.attributes = []
        # self.treeview_headers = self.controller.get_treeview_headers() TODO
        self.antonym_library = analysis_utils.get_antonyms_from_verbocean()

    def start(self, attribute_content: Dict[str, Dict[str, int]]) -> Dict[int, RepairOption]:
        """
        Fully automatic process to use AnalysisModule for grammar analysis

        Parameters
        ----------
        attribute_content
            content to be analyzed {attr1: {'attr_value1': count, ...}, attr2: ...}

        Returns
        -------
        repair_dict
            repair_dict is passed to treeview for selection of useful results
        """
        tic = time.perf_counter()
        self._initialize_attributes(attribute_content)
        repair_dict = self._get_results_per_analysis(self.name, self.attributes, self.analysis_option)
        toc = time.perf_counter()
        logger.info(f'AnalysisModule took {toc - tic} seconds for syntax analysis.')
        return repair_dict

    def _initialize_attributes(self, attribute_content: Dict[str, Dict[str, int]]) -> None:
        """
        Initialize attribute content as Attribute classes containing AttributeValue classes itself for deeper analysis


        Parameters
        ----------
        attribute_content
            content to be analyzed {attr1: {'attr_value1': count, ...}, attr2: ...}
        """
        tic = time.perf_counter()
        for attr, values in attribute_content.items():
            self.attributes.append(Attribute(attr, values, self.nlp, self.glove))
        toc = time.perf_counter()
        logger.info(f'AttributeValue instances were initialized in {toc - tic} seconds')

    def _get_results_per_analysis(self,
                                  name: str,
                                  attributes: List[Attribute],
                                  options: AnalysisOption) \
            -> Dict[int, RepairOption]:
        """
        Generate the similarity matrices, return the results and filter them
         -> preparation for frontend to show results in readable manner

        Parameters
        ----------
        name
            name of analysis step
        attributes
            list of all attributes that were filtered from original log
        options
            configuration options to build matrices
        thresholds
            values to filter matrices by

        Returns
        -------
        repair_selection_dict
            result selection filtered with threshold and prepared to be used in
        """
        analysis_utils.generate_sim_matrices(attributes, name, options)
        all_sim_matrices = {attribute: attribute.matrix_content for attribute in self.attributes}
        repair_selection_dict = analysis_utils.get_result_selection(all_sim_matrices, options, self.antonym_library)
        return repair_selection_dict
