from nlplr.view.elements.window import Window

from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class View(ABC):
    """Abstract Base Class as an interface for different View implementations"""
    @abstractmethod
    def setup(self, controller):
        pass

    @abstractmethod
    def start_main_loop(self):
        pass


class TkView(View):
    """Concrete Implementation of of a View with tkinter"""
    def setup(self, controller):
        self.controller = controller
        # setup tkinter window
        self.root = Window(self.controller)

    def start_main_loop(self):
        # start the loop
        logger.info('Window started ...')
        self.root.mainloop()
