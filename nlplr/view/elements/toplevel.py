from nlplr.view.settings import _TITLE_FONT
import tkinter as tk
from abc import ABC, abstractmethod


class ABCTopLevel(ABC, tk.Toplevel):
    def __init__(self, master, controller):
        tk.Toplevel.__init__(self, master)
        self.controller = controller
        self._setup_frame()
        self._orient_frame()

    @abstractmethod
    def _setup_frame(self):
        pass

    @abstractmethod
    def _orient_frame(self):
        pass

    def run_and_restrict(self):
        """
        Functions to grab focus from main window, so there can be no changes while the toplevel is open and multiple instances are not possible
        """
        self.grab_set()
        self.focus_set()
        self.mainloop()
        self.grab_release()


class AboutTopLevel(ABCTopLevel):
    def __init__(self, master, controller):
        self.description_text = "This project was created by two students of the University of Bayreuth during the project seminar \"H2 Software-Projektseminar Wintersemester 2020/21\"" \
                                " organized by the Chair BWL VII and the Professorships DEM, NIM, WPM.\n" \
                                "The scope of the project was to establish a repair engine to clean wrong activity labels within process event logs using NLP (\"Natural Language Processing\")" \
                                "methods. The project with the support of Dominik Fischer shall determine first indications whether further research in this area is promising."

        super().__init__(master, controller)

    def _setup_frame(self):
        self.title('About the project')
        # self.resizable(True, False)
        self.topl_frame = tk.Frame(self)

        self.description = tk.Text(self.topl_frame)
        self.description.insert(tk.END, self.description_text)

        self.label = tk.Label(self, text='Jasper Wiltfang, Version 0.1.')

    def _orient_frame(self):
        self.topl_frame.pack(anchor='w', fill='x', expand=True)
        self.description.pack(fill='both')
        self.label.pack()


class ReferencesTopLevel(ABCTopLevel):
    def __init__(self, master, controller):
        self.description_text = "The used references will be added in the future."
        super().__init__(master, controller)

    def _setup_frame(self):
        self.title('References')
        self.topl_frame = tk.Frame(self)

        self.description = tk.Text(self.topl_frame)
        self.description.insert(tk.END, self.description_text)

        self.label = tk.Label(self, text='(C) Copyright by University of Bayreuth')

    def _orient_frame(self):
        self.topl_frame.pack(anchor='w', fill='x', expand=True)
        self.description.pack(fill='both')
        self.label.pack()


class TutorialTopLevel(ABCTopLevel):
    def __init__(self, master, controller):
        self.settings = {
            'text': 'Theoretical Assumption: Decreasing probability of correct assignment of Original Label if occurence is lower than Suggested Label.\n' \
                    'Numerical values can be sorted manually by clicking on column title.\n\n'
                    'Glove Result: similarity value based on glove model_glove\n'
                    'Tfidf result: similarity value based on \'term frequency - inverted document fequency\'\n'
                    'Depth: depth of analysis; 2 -> second highest value of sorted similarity based on glove\n\n'
                    '\'Occurence\' counts total appearance within event eventlog.\n'
                    '\'Original Label\' will be replaced by \'Suggested Label\' in repaired event eventlog.'

        }
        self.description_text = "The used references will be added in the future."
        super().__init__(master, controller)

    def _setup_frame(self):
        self.title('References')
        self.topl_frame = tk.Frame(self)
        self.legend_title = tk.Label(self.topl_frame, text='Legend of used expressions above:', font=_TITLE_FONT, anchor='w')
        self.repair_choice_legend = tk.Label(self.topl_frame, anchor='w', justify='left', text=self.settings['text'])
        self.repair_message = tk.Label(self.topl_frame, anchor="w", justify='left',
                                       text='Select lines where suggestions make sense.\nPress Strg / Ctrl for multi-selection.',
                                       pady=2, bg='#0078d7', fg='white', relief='raised', bd=2)
        self.label = tk.Label(self, text='(C) Copyright by University of Bayreuth', relief='raised')
        # pack all elements in order

    def _orient_frame(self):
        self.topl_frame.pack(anchor='w', fill='x', expand=True)
        self.legend_title.pack(anchor='w', fill='x')
        self.repair_choice_legend.pack(anchor='w', fill='x')
        self.repair_message.pack(side='top', fill='x')
        self.label.pack()
