import fitz
from typing import Dict, List

import logging

logger = logging.getLogger(__name__)


class Marker:
    def __init__(self):
        self.doc = None
        self.rect_size_add = (-20, -10, 20, 10)
        self.point_move = (20, 10)
        self.stroke_color = (0, 0, 1)
        self.fill_color_correct = (0, 1, 0)
        self.fill_color_incorrect = (1, 0, 0)
        self.text_correct = 'correct value (stays unchanged)'
        self.text_incorrect = 'incorrect value (is changed)'
        self.icon = 'Help'
        self.setting = {'rect_size_add': (-20, -10, 20, 10),
                        'point_move': (20, 10),
                        'stroke_color': (0, 0, 1),
                        'fill_color_correct': (0, 1, 0),
                        'fill_color_incorrect': (1, 0, 0),
                        'text_incorrect': 'correct value (stays unchanged)',
                        'text_correct': 'incorrect value (is changed)',
                        'icon': 'Help'}

    def load_pdf(self, filepath: str):
        """open file to work with pdf in fitz"""
        self.doc = fitz.open(filepath)

    def save_pdf(self, save_location: str):
        self.doc.save(save_location)
        self.doc.close()
        return save_location

    def mark_words(self, selected_words: Dict[str, List[str]]):
        logger.info(f'preview for {selected_words}')
        for page in self.doc:
            # correct word
            for word in selected_words['correct']:
                rect, point = self.get_word_geometry(page, word)
                if rect:
                    self.mark_correct_word(page, rect, point)

            # incorrect word
            for word in selected_words['incorrect']:
                rect, point = self.get_word_geometry(page, word)
                if rect:
                    self.mark_incorrect_word(page, rect, point)

    def get_word_geometry(self, page, word):
        """return left_upper_point for alignment"""
        try:
            quads = page.search_for(word, quads=True)[0]  # quads returns the points of each corner of the element
            rect = quads.rect + self.rect_size_add  # increase size
            point = quads[3] + self.point_move  # moved to the side of the element
            return rect, point
        except IndexError as ie:
            logger.error(f'Index Error: {ie}')
            return None, None

    def mark_correct_word(self, page, rect, point):
        annot1 = self._add_text_annot(page, point, self.text_correct)
        annot2 = self._add_rect_annot(page, rect, stroke_color=self.stroke_color, fill_color=self.fill_color_correct)

    def mark_incorrect_word(self, page, rect, point):
        annot1 = self._add_text_annot(page, point, self.text_incorrect)
        annot2 = self._add_rect_annot(page, rect, stroke_color=self.stroke_color, fill_color=self.fill_color_incorrect)

    @staticmethod
    def _add_text_annot(page, point, text_value, icon='Help'):
        annot = page.addTextAnnot(point, text_value, icon=icon)
        return annot

    @staticmethod
    def _add_rect_annot(page, rect, width=1, dashes=(1, 2), stroke_color=(0, 0, 1), fill_color=(0, 0, 1), opacity=0.5):
        annot = page.addRectAnnot(rect)
        annot.set_border(width=width, dashes=dashes)
        annot.set_colors(stroke=stroke_color, fill=fill_color)
        annot.update(opacity=opacity)
        return annot

    @staticmethod
    def _add_freetext_annot(page, rect, text_value, alignment=(100, 0, 100, 0)):
        """align freetext to the right"""
        freetext_rect = rect + alignment
        annot = page.addFreetextAnnot(freetext_rect, text_value)
        return annot