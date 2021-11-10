from nlplr.model.model import Model, TkModel
from nlplr.view.view import View, TkView
from nlplr.view.elements.frames.f_repair import RepairFrame

from nlplr.analysis_NLP.analysis import AnalysisModule
from nlplr.analysis_NLP.nlp_models import GloVeModel, SpaCyModel

from nlplr.repair.repair_new import RepairTool
from nlplr.utils import importer, pre_analysis, exporter
from nlplr.utils.context_preview import previewer

import tkinter

from abc import ABC, abstractmethod
import time
import logging

logger = logging.getLogger(__name__)


class Controller(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        pass


class TkEventController(Controller):
    """
    Controller responsible for all main functionality of the programme, conntecting both the front end (View) and the backend (Model)
    TkEventController is ideally implemented to work with TkModel and TkView

    Parameters
    ----------
    model
        Data Model
    view
        front-end package
    """
    def __init__(self):
        logger.info('controller creation')
        super().__init__()
        self.model = TkModel()
        self.view = TkView()

        self._frame = None
        self.eval = True
        self.nlp = None
        self.glove = None

        self.preview_save_location = 'context_pdfs'
        logger.info('controller created')

    def start(self, analysis_options=None):
        self.model.setup_analyses(analysis_options)
        self.view.setup(self)
        self.update_content_before_anything()
        self.view.start_main_loop()  # main function that keeps the frontend running and reactive

    # EventHandler to deal with user input
    # ------------------------------------
    # def handle_click_...(self):
    # return_value1, ... = some_action()
    # --- model data setter
    # self.model.something = return_value1
    # self.model ...
    # --- update content in frontend
    # self.update_content_...()

    def handle_click_import_log(self):
        log, file_location, filename = importer.import_file()
        if log:
            self.model.log = log
            self.model.file_location = file_location
            self.model.filename = filename

            relevant_attributes, attributes_list = pre_analysis.filter_attributes(self.model.log)
            self.model.relevant_attributes = relevant_attributes
            self.model.attributes_list = attributes_list

            self.update_content_after_import_log()

    def handle_click_confirm_selected_attributes(self, selected_attributes):
        self.model.selected_attributes = selected_attributes
        self.model.preprocess_log()
        self.update_content_after_attributes_selected()

    def handle_click_start_analysis(self):
        self.update_content_before_start_analysis()
        self._setup_models()  # one time setup for NLP models
        self.handle_click_run_next_analysis()

    def handle_click_run_next_analysis(self):
        self._run_next_analysis()

    def handle_click_run_repair(self, repair_ids, blacklist_ids):
        logger.info(f'repair_ids: {repair_ids}')
        self.repair_tool = RepairTool()
        self.model.log = self.repair_tool.repair_log(self.model.log, repair_ids, self.model.repair_dict)
        self.update_content_after_repair()

    def handle_click_export_context_preview(self, correct_value, incorrect_values):
        selected_words = {
            'correct': correct_value,
            'incorrect': incorrect_values
            }
        cont_previewer = previewer.ContextPreviewer(self.model.log, self.preview_save_location, self.model.filename)
        cont_previewer.preview_context_pdf(selected_words)

    def handle_click_export_log(self):
        exporter.export_file(self.model.log, self.model.filename)  # optional prefix

    # ContentUpdater for frontend view
    # --------------------------------
    # def update_content_...(self):
    # self.frame.update_...(self.model.something, ...)
    # self.view.root.switch_frame(...)
    # ...

    def update_content_before_anything(self):
        self.frame.update_statusbar('Waiting for file upload ...')

    def update_content_after_import_log(self):
        self.frame.update_information_container(self.model.file_location, '(analysis not yet started ...)')
        self.frame.update_selected_attributes_container(self.model.relevant_attributes)
        self.frame.update_statusbar('Please select the relevant_attributes')
        self.frame.update_button(btn='import_log_button', state='disabled')
        self.frame.update_button('select_attributes_container', 'select_button', 'normal')

    def update_content_after_attributes_selected(self):
        self.frame.update_statusbar('Analysis ready to go ...')
        self.frame.update_button(btn='start_analysis_button', state='normal')

    def update_content_before_start_analysis(self):
        self.frame.update_statusbar('Please wait until analysis has finished ...')

    def update_content_after_run_analysis(self):
        self.view.root.switch_to_repair_frame(self.model.repair_dict)
        self.frame.update_information_container(self.model.file_location, self.model.get_current_analysis_information())
        self.frame.update_statusbar('Please select lines to be repaired or skip to next step ...')

    def update_content_after_last_analysis(self):
        self.frame.update_information_container(self.model.file_location, 'no more analyses available, please restart the tool!')
        self.frame.update_statusbar('Please restart the tool for a new log to analyse.')

    def update_content_after_repair(self):
        self.frame.update_statusbar('Selection was registered and log is being repaired.')

    def update_content_after_preview_export(self):
        self.frame.update_statusbar('Please find the preview context pdfs in the designated folder.')

    def update_content_after_export(self):
        pass

    def _run_next_analysis(self):
        option_index = self.model.current_analysis_index
        if option_index < len(self.model.analysis_options):
            # reset old repair data
            self.model.reset_repair_data()
            self.analysis = AnalysisModule(self, self.nlp, self.glove, self.model.analysis_options[option_index])
            self.model.repair_dict = self.analysis.start(self.model.attribute_content)
            self.update_content_after_run_analysis()
            self.model.current_analysis_index += 1
        else:
            self.update_content_after_last_analysis()

    def _setup_models(self):
        if self.nlp is None:
            tic = time.perf_counter()
            self.nlp = SpaCyModel('spacy')
            self.glove = GloVeModel('glove')
            toc = time.perf_counter()
            logger.info(f'Models setup in {toc - tic} seconds')
        else:
            pass

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame: tkinter.Frame):
        self._frame = new_frame

    def __repr__(self):
        return f'TkEventController({self.model!r}, {self.view!r}'

    def __str__(self):
        return f'TkEventController: Model, View'
