from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    Parameters
    ----------
    string: str
        str, string to check for date
    fuzzy: bool
        ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def is_numeric(s):
    """test if a string is numeric"""
    for c in s:
        if c in "1234567890-.":
            return True
        else:
            return False


def change_numeric(data):
    """if the data to be sorted is numeric change to float"""
    new_data = []
    if is_numeric(data[0][0]):
        # change child to a float
        for child, col in data:
            new_data.append((float(child), col))
        return new_data
    return data
