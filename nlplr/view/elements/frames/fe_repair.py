from nlplr.repair.repair_options import RepairOption
from nlplr.view.elements.frames.fe_general import BaseFrame
from nlplr.view.settings import _ACTIVE_BUTTON
# from nlplr.view.elements.frames.f_repair import RepairOptionViewClass

import nlplr.utils.data_utils as data_utils

import tkinter as tk
from tkinter import ttk

from typing import Dict, List

import logging

logger = logging.getLogger(__name__)


class RepairOptionViewClass:
    def __init__(self, repair_dict):
        self.repair_dict = repair_dict
        # get correct data
        self.correct_listbox_values = self.get_listbox_values()
        self.frame_data_values = self.get_frame_values()

    def get_listbox_values(self) -> List[str]:
        correct_value_list, index = [], 0
        for iid, repair_option in self.repair_dict.items():
            if repair_option.cor_value.orig_value not in correct_value_list:
                correct_value_list.append(repair_option.cor_value.orig_value)
                index += 1
        return correct_value_list

    def get_frame_values(self) -> List[Dict[int, RepairOption]]:
        incorrect_frames_list = []
        for index, correct_value in enumerate(self.correct_listbox_values):
            frames_dict = {}
            for iid, repair_option in self.repair_dict.items():
                if repair_option.cor_value.orig_value == correct_value:
                    frames_dict[iid] = repair_option
            incorrect_frames_list.append(frames_dict)
        return incorrect_frames_list

    def __repr__(self):
        return f'RepairOptionViewClass(listbox: {self.correct_listbox_values}, frames: {self.frame_data_values})'


class RepairSelectionFrame(BaseFrame):
    def __init__(self, master: tk.Frame, controller, callbacks, repair_dict, *args, **kwargs):
        self.repair_ids = []
        self.blacklist_ids = []
        self.repair_value_class = RepairOptionViewClass(repair_dict)
        # self.correct_value_dict = self.get_listbox_values()
        # self.incorrect_frames_dict = self.get_frame_values()
        super().__init__(master, controller, callbacks, *args, **kwargs)

    def _setup_frame(self):
        self.selection_container = tk.Frame(self)
        # container for selecting the correct values from listbox
        self.listbox_container = tk.Frame(self.selection_container)
        self.listbox_title_label = tk.Label(self.listbox_container, text='Select presumably correct value.', pady=2,
                                            bg='#0078d7', fg='white', relief='raised', bd=2)
        self.listbox = tk.Listbox(self.listbox_container, selectmode='single', width=30)
        self.vsb = ttk.Scrollbar(self.listbox_container, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.vsb.set)

        self._current_list_selection = 0
        self.correct_listbox_values = self.repair_value_class.correct_listbox_values
        for index, cor_value in enumerate(self.correct_listbox_values):
            self.listbox.insert(tk.END, cor_value)
        self.listbox.bind("<<ListboxSelect>>", self.listbox_callback)
        # container for one correct value to select fitting wrong values
        self.option_selection_container = tk.Frame(self.selection_container)
        self.frames = {}
        self.incorrect_values_dict = self.repair_value_class.frame_data_values
        for index, values in enumerate(self.incorrect_values_dict):  # only get values from dict -> RepairOptions
            # all frames in the same location, top frame is visible, stack frames on top of each other
            index_and_length = {'index': index, 'list_len': len(self.correct_listbox_values)}
            frame = ValueSelectionContainer(self.option_selection_container, self.controller, self.callbacks, index_and_length, values)
            self.frames[index] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(0)
        # container for click actions
        self.bottom_button_container = tk.Frame(self)
        self.run_repair_button = tk.Button(self.bottom_button_container,
                                           text='Run Repair',
                                           activebackground=_ACTIVE_BUTTON,
                                           command=self.run_repair,
                                           state='normal')
        self.run_next_analysis_button = tk.Button(self.bottom_button_container,
                                                  text='Next Analysis',
                                                  activebackground=_ACTIVE_BUTTON,
                                                  command=self.run_next_analysis,
                                                  state='normal')
        self.export_log_button = tk.Button(self.bottom_button_container,
                                           text='Export Log',
                                           activebackground=_ACTIVE_BUTTON,
                                           command=self.export_log,
                                           state='normal')

    def _orient_frame(self):
        self.selection_container.pack(anchor='nw', fill='both', expand=True)
        # listbox element
        self.listbox_container.pack(side='left', fill='y')
        self.listbox_title_label.pack(side='top', fill='x', anchor='nw')
        self.vsb.pack(side='left', fill='y')
        self.listbox.pack(side='left', fill='both')
        # container that contains all frames connected to cnotrol -> listbox
        self.option_selection_container.pack(side='left', fill='both', expand=True)
        self.option_selection_container.grid_columnconfigure(0, weight=1)
        self.option_selection_container.grid_rowconfigure(0, weight=1)
        # all buttons to actually run repair
        self.bottom_button_container.pack(side='bottom', anchor='sw', fill='x')
        self.export_log_button.pack(side='left')
        self.run_next_analysis_button.pack(side='right')
        self.run_repair_button.pack(side='right')

    def show_frame(self, page_index: int):
        """Show a frame for the given page name"""
        try:
            frame = self.frames[page_index]
            frame.tkraise()
        except KeyError as ke:
            logger.error(f'KeyError: {ke}')

    def listbox_callback(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            if index == self.current_list_selection:  # only act if new line selected
                return
            else:
                self.current_list_selection = index
                self.callbacks['select_listbox_value'](self.current_list_selection)
                return index
        else:
            return

    def export_log(self):
        self.callbacks['export_log']()

    def run_repair(self):
        repair_items, blacklist_items = [], []
        for frame in self.frames.values():
            repair_ids, blacklist_ids = frame.return_repair_ids()
            repair_items.extend(repair_ids)
            blacklist_items.extend(blacklist_ids)
        self.callbacks['run_repair'](repair_items, blacklist_items)

    def run_next_analysis(self):
        self._disable_all_buttons()
        self.callbacks['run_next_analysis']()

    def _disable_all_buttons(self):
        state = 'disabled'
        self.export_log_button.config(state=state)
        self.run_repair_button.config(state=state)
        self.run_next_analysis_button.config(state=state)
        for frame in self.frames.values():
            frame.reset_repair_elements_button.config(state=state)
            frame.clear_selection_button.config(state=state)
            frame.preview_context_button.config(state=state)
            frame.selection_to_repair_button.config(state=state)
            frame.discard_elements_button.config(state=state)
            frame.next_value_button.config(state=state)

    @property
    def current_list_selection(self):
        return self._current_list_selection

    @current_list_selection.setter
    def current_list_selection(self, new_selection):
        if isinstance(new_selection, int):
            self._current_list_selection = new_selection


class ValueSelectionContainer(BaseFrame):
    def __init__(self, master: tk.Frame, controller, callbacks, index_and_len: Dict[str, int], repair_options: Dict[int, RepairOption], *args,
                 **kwargs):
        # data to be returned for repair
        self.index_and_len = index_and_len
        self.repair_items = []
        self.blacklist_items = []
        # repair options for selection
        self.repair_options = repair_options
        self.first_correct_value_collection = self.repair_options[list(self.repair_options.keys())[0]]
        self.test_cor_values: Dict[str, str] = self.first_correct_value_collection.cor_repair_dict  # TODO
        self.test_inc_values: Dict[str, str] = self.first_correct_value_collection.inc_repair_dict
        self.treeview_headers = list(self.test_inc_values.keys())

        self.cor_value = self.test_cor_values['correct value']
        self.value_label_dict = {}
        self.counter = 0
        super().__init__(master, controller, callbacks, *args, **kwargs)

    def _setup_frame(self):
        # container for currently selected value
        self.current_value_information_container = tk.Frame(self, width=100)
        self.title_label_cor = tk.Label(self.current_value_information_container, text='Current value to review.',
                                        pady=2, bg='#0078d7', fg='white', relief='raised', bd=2)
        self.content_frame = tk.Frame(self.current_value_information_container)
        r = 0
        for key, value in self.test_cor_values.items():
            key_label = tk.Label(self.content_frame, text=key)
            value_label = tk.Label(self.content_frame, text=value)

            key_label.grid(row=r, column=0, sticky='w')
            value_label.grid(row=r, column=1, sticky='w')
            r += 1
        # only allow context preview for attribute 'concept:name'
        self.preview_context_button_state = 'normal'
        if self.test_cor_values['attribute'] != 'concept:name':
            self.preview_context_button_state = 'disabled'

        self.preview_context_button = tk.Button(self.current_value_information_container,
                                                text='Preview Context',
                                                activebackground=_ACTIVE_BUTTON,
                                                command=self.preview_context,
                                                state=self.preview_context_button_state)

        # container for incorrect values option (treeview selection)
        self.incorrect_options_value_container = tk.Frame(self)
        self.title_label_inc = tk.Label(self.incorrect_options_value_container, text='Possible incorrect values',
                                        pady=2, bg='#0078d7', fg='white', relief='raised', bd=2)

        self.tree_container = tk.Frame(self.incorrect_options_value_container)
        # treestyle adaptable
        self.treestyle = ttk.Style()
        self.treestyle.theme_use('clam')
        self.treestyle.configure('Treeview', background='white', rowheight=20, fieldbackground='lightgrey')
        self.treestyle.map('Treeview', background=[('selected', '#0078d7')])
        # treeview elements
        self.tree = ttk.Treeview(self.tree_container, columns=self.treeview_headers, show="headings",
                                 selectmode='extended', displaycolumns=self.treeview_headers)
        # self.tree = ttk.Treeview(self.tree_container, show='headings', selectmode='extended')
        self.vsb = ttk.Scrollbar(self.tree_container, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.tree.tag_configure('default', background='white')
        self.tree.tag_configure('repair', background='lightgreen')
        self.tree.tag_configure('blacklist', background='lightpink')

        self.button_container = tk.Frame(self.incorrect_options_value_container)
        self.clear_selection_button = tk.Button(self.button_container,
                                                text='Clear Selection',
                                                activebackground=_ACTIVE_BUTTON,
                                                command=self.clear_selection,
                                                state='normal')
        self.reset_repair_elements_button = tk.Button(self.button_container,
                                                      text='Reset Frame',
                                                      activebackground=_ACTIVE_BUTTON,
                                                      command=self.reset_repair_elements,
                                                      state='normal')
        self.discard_elements_button = tk.Button(self.button_container,
                                                 text='Discard Elements',
                                                 activebackground=_ACTIVE_BUTTON,
                                                 command=self.discard_elements,
                                                 state='normal')
        self.selection_to_repair_button = tk.Button(self.button_container,
                                                    text='Elements To Repair',
                                                    activebackground=_ACTIVE_BUTTON,
                                                    command=self.selection_to_repair,
                                                    state='normal')
        self.next_value_button = tk.Button(self.button_container,
                                           text='Next Value from Listbox',
                                           activebackground=_ACTIVE_BUTTON,
                                           command=self.next_listbox_value,
                                           state='normal')
        if self.index_and_len['index']+1 == self.index_and_len['list_len']:
            self.next_value_button.config(state='disabled')

        # TODO test
        self.fill_tree()

    def _orient_frame(self):
        # correct values left side
        self.current_value_information_container.pack(side='left', anchor='nw', fill='y')
        self.title_label_cor.pack(side='top', fill='x')
        self.content_frame.pack(anchor='nw', fill='both')
        self.preview_context_button.pack(anchor='nw')
        # incorrect values right side
        self.incorrect_options_value_container.pack(side='left', fill='both', expand=True)
        self.title_label_inc.pack(side='top', fill='x')
        # treeview
        self.tree_container.pack(side='top', fill='both', expand=True)
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)
        self.tree.grid(column=0, row=0, sticky='nsew')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')
        # button container for actions in treeview
        self.button_container.pack(anchor='w', fill='x')
        self.clear_selection_button.pack(side='left')
        self.reset_repair_elements_button.pack(side='left')
        self.next_value_button.pack(side='right')
        self.selection_to_repair_button.pack(side='right')
        self.discard_elements_button.pack(side='right')

    def fill_tree(self):
        self.tree.config(columns=self.treeview_headers)
        index = 1
        for col in self.treeview_headers:
            index_str = f'#{index}'
            self.tree.heading(index_str, text=col.title(), anchor='nw')
            # self.tree.column(index_str)
            index += 1
            # if col in ['sim_score', 'suggested occurence', 'original occurence']:
            #     # numeric columns can be sorted by values
            #     self.tree.heading(index, text=col.title(), command=lambda c=col: self.sortby(c, 1))
            # else:
            #     self.tree.heading(index, text=col.title(), anchor='w')
            # # adjust the column's width to the header string
        for repair_id, repair_option in self.repair_options.items():
            values_per_line = list(repair_option.inc_repair_dict.values())
            self.tree.insert(parent='', index='end', iid=repair_id, values=values_per_line)

    def preview_context(self):  # TODO
        incorrect_values = self._get_incorrect_values_selection()
        if incorrect_values:
            self.callbacks['preview_context']([self.cor_value], incorrect_values)

    def _get_incorrect_values_selection(self):
        incorrect_values = []
        for iid in self.repair_items:
            tree_item = self.tree.item(iid)
            inc_value = tree_item['values'][1]
            incorrect_values.append(inc_value)
        if incorrect_values:
            return incorrect_values

    # button actions
    def discard_selection2(self):
        selection = self.tree.selection()
        if selection:
            self._discard_elements(selection)
        else:
            self._discard_elements(self.tree.get_children())

    def discard_elements(self):
        self.simple_button_action(self._discard_elements)

    def reset_repair_elements(self):
        self.simple_button_action(self._reset_repair_elements)

    def selection_to_repair(self):
        self.simple_button_action(self._selection_to_repair)

    def clear_selection(self):
        self.simple_button_action(self._clear_selection)

    def next_listbox_value(self):
        self.callbacks['select_listbox_value']((self.index_and_len['index']+1))

    def simple_button_action(self, fn):
        selection = self.tree.selection()
        if not selection:
            selection = self.tree.get_children()
        for item in selection:
            fn(item)

    def _discard_elements(self, item):
        if item not in self.blacklist_items:
            self.blacklist_items.append(item)
        if item in self.repair_items:
            self.repair_items.remove(item)
        self.tree.item(item, tag='blacklist')
        self.tree.selection_remove(item)

    def _selection_to_repair(self, item):
        if item not in self.repair_items:
            self.repair_items.append(item)
        if item in self.blacklist_items:
            self.blacklist_items.remove(item)
        self.tree.item(item, tag='repair')
        self.tree.selection_remove(item)

    def _reset_repair_elements(self, item):
        if item in self.repair_items:
            self.repair_items.remove(item)
        if item in self.blacklist_items:
            self.blacklist_items.remove(item)
        self.tree.item(item, tag='default')
        self.tree.selection_remove(item)

    def _clear_selection(self, item):
        self.tree.selection_remove(item)

    # return values from frame
    def return_repair_ids(self):
        return self.repair_items, self.blacklist_items


class TreeviewSelection(BaseFrame):
    def __init__(self, master: tk.Frame, controller, callbacks, *args, **kwargs):
        self.repair_items = []
        self.blacklist_items = []
        super().__init__(master, controller, callbacks, *args, **kwargs)
        self._build_tree()  # TODO get it going

    def _setup_frame(self):
        # create a treeview with dual scrollbars
        self.tree_container = tk.Frame(self)
        self._create_treeview(self.tree_container)

    def _orient_frame(self):
        self.tree_container.pack(fill='both', expand=True)
        self.tree.grid(column=0, row=0, sticky='nsew')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='ew')
        self.tree_container.grid_columnconfigure(0, weight=1)
        self.tree_container.grid_rowconfigure(0, weight=1)

    def _create_treeview(self, master: tk.Frame):
        """
        Creation and adaption of treeview bundled in this function for better resuability
        (has to be implemented for each frame as the packing on the interface happens within the function
        """
        self.treestyle = ttk.Style()
        self.treestyle.theme_use('clam')
        self.treestyle.configure('Treeview', background='white', rowheight=20,
                                 fieldbackground='lightgrey')
        self.treestyle.map('Treeview', background=[('selected', '#0078d7')])

        # TODO test ------------------------------------------------------------
        self.tree = ttk.Treeview(master, show='headings', selectmode='extended')
        # TODO -----------------------------------------------------------------
        self.vsb = ttk.Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(master, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree.tag_configure('repair', background='lightgreen')
        self.tree.tag_configure('blacklist', background='lightpink')

        # self.tag_colors = ['#ffffff', '#e9e9e9', '#d4d4d4', '#bfbfbf', '#aaaaaa', '#969696', '#838383', '#707070',
        #                    '#5d5d5d']  # white to grey color scheme; green and white highlights for selected values
        # self.green_color = 'lightgreen'
        # self.red_color = 'lightpink'
        # self.tag_colors = ['lightgreen', '#cfe9b5', '#ebebd3', '#f2efec', 'white', '#f6f8f4', '#e4f6f4', '#dfcff8',
        #                    'lightpink']
        # self.tag_prios = ['prio8', 'prio7', 'prio6', 'prio5', 'prio4', 'prio3', 'prio2', 'prio1', 'prio0']
        # self.current_prio = 0
        # for tag_name, color in zip(self.tag_prios, self.tag_colors):
        #     self.tree.tag_configure(tag_name, background=color)
        # self.tree.tag_configure('high', background='lightgreen')
        # self.tree.tag_configure('middle', background='white')
        # self.tree.tag_configure('low', background='lightpink')

        self.tree.focus()

    def _build_tree(self):
        # self.treeview_headers = self.controller.get_treeview_headers()
        # self.tree = ttk.Treeview(master, columns=self.treeview_headers, show="headings",
        #                          selectmode='extended')  # displaycolumns=self.treeview_headers[:]

        self.treeview_headers = ['sim_score', 'test', 'test_value', 'attibute']
        self.tree.config(columns=self.treeview_headers)
        for index, col in enumerate(self.treeview_headers):
            index = f'#{index}'
            if col in ['sim_score', 'suggested occurence', 'original occurence']:
                # numeric columns can be sorted by values
                self.tree.heading(index, text=col.title(), command=lambda c=col: self.sortby(c, 1))
            else:
                self.tree.heading(index, text=col.title(), anchor='w')
            # adjust the column's width to the header string
            self.tree.column(index)

        # TODO test insertion of values
        for i in range(10):
            self.tree.insert("", 0, text=i)

            # TODO sortby category float value

    def update_treeview_content(self, repair_dict: Dict[int, RepairOption]):
        for key, repair_option in repair_dict.items():
            values_per_line = list(repair_option.repair_dict.values())
            # TODO integrate tags for values above certain
            tag = self._get_tag_for_treeview_line(repair_option.result, repair_option.threshold)
            self.tree.insert(parent='', index='end', iid=key, values=values_per_line, tags=tag)

    def _get_tag_for_treeview_line(self, sim_value, threshold):
        """
        Color support to make it information more readable # TODO
        :param sim_value:
        :return:
        """
        max_threshold = 1
        green_area = max_threshold - threshold
        tag = self.tag_prios[-1]  # originally lowest tag
        for tag_name in self.tag_prios:
            if sim_value > max_threshold:
                tag = (tag_name,)
                return tag
            else:
                max_threshold -= green_area / len(self.tag_prios)
        return tag

    def selection_to_repair(self):
        selection = self.tree.selection()
        for item in selection:
            self.tree.tag_has('repair', item)
            self.repair_items.append(item)
        print(selection)

    def selection_to_blacklist(self):
        selection = self.tree.selection()
        for item in selection:
            self.tree.tag_has('blacklist', item)
            self.blacklist_items.append(item)

    def clear_selection(self):
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def delete_entire_list(self, *args):
        for item in self.tree.get_children():
            # TODO just have ids saved in a different list
            self.tree.delete(item)  # TODO

    def delete_selection(self):
        for selected_item in self.tree.selection():
            # TODO just have ids saved in a different list
            self.tree.delete(selected_item)

    def select_all(self):
        self.tree.selection_set(self.tree.get_children())

    def select_prio_items(self):
        iid_list = []
        for iid in self.tree.get_children():
            tag_list = self.tree.item(iid, 'tags')
            if self.tag_prios[self.current_prio] in tag_list:  # select all items that have current prio
                iid_list.append(iid)
        self.tree.selection_set(iid_list)
        self.current_prio += 1
        if self.current_prio > len(self.tag_prios):  # when all prios have been checked, disable the button
            self.update_button('select_green_items_button', 'disabled')
        self.select_green_items_button.config(text=f'Select Next Priority {self.current_prio}')

    def get_indices_for_repair(self):
        repair_ids = self.tree.selection()
        for element in repair_ids:
            self.tree.detach(element)
        return repair_ids

    def reattach_repair_ids(self):
        if self.repair_ids:
            for element in self.repair_ids[-1]:
                self.tree.reattach(element, '', 0)
            del self.repair_ids[-1]

    def return_final_repair_ids(self):
        final_repair_ids = []
        for repair_list in self.repair_ids:
            final_repair_ids.extend(repair_list)
        return final_repair_ids

    def select_to_repair(self):
        # TODO first collect the repair_ids in frame and then give it to model
        #  possibility to make them reappear or hide them from view
        #  detach and reattach for hiding the values, need to make sure how to save these values
        self.repair_ids.append(self.get_indices_for_repair())
        print(self.repair_ids)
        self.update_button('run_repair_button', 'normal')
        self.update_button('run_analysis_button', 'disabled')
        self.update_button('export_button', 'disabled')

    def sortby(self, col, descending, *args):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        # if the data to be sorted is numeric change to float
        data = data_utils.change_numeric(data)
        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            self.tree.move(item[1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        self.tree.heading(col, command=lambda c=col: self.sortby(c, not descending))
