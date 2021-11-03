class IncorrectMultipleOptionsError(Exception):
    def __init__(self, options, option):
        self.options = options
        self.option = option
        self.message = f"One option list was not correct: {self.option} within entire options {self.options}"
        super().__init__(self.message)


class IncorrectSingleOptionError(Exception):
    def __init__(self, options):
        self.options = options
        self.message = f"Single option is meant to have 4 elements: {self.options} has {len(self.options)} elements"
        super().__init__(self.message)


class IncorrectOptionInputError(Exception):
    def __init__(self, options):
        self.options = options
        self.message = f"Only strings are meant to be in {self.options}."
        super().__init__(self.message)


class IncorrectOptionTypeError(Exception):
    def __init__(self, options):
        self.options = options
        self.message = f"Options have to be of type list and not {type(self.options)}."
        super().__init__(self.message)