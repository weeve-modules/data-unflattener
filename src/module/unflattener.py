import os
from logging import getLogger

log = getLogger("unflattener")

__DELIMITER__ = os.getenv("DELIMITER", "/")
__SEARCH_FOR_LISTS__ = bool(os.getenv("SEARCH_FOR_LISTS", "True"))

def unflattener(data):
    try:
        base = {}

        for k, v in data.items():
            fields = k.split(__DELIMITER__)
            temp = base
            for f in fields[:-1]:
                if f not in temp:
                    temp[f] = {}
                temp = temp[f]
            temp[fields[-1]] = v

        if __SEARCH_FOR_LISTS__:
            base = dict_to_list(base)

        return base

    except Exception as e:
        return f"Exception when trying to unflatten data: {data}. Exception: {e}"

def dict_to_list(data):
    if type(data) != dict: # hit a leaf (scalar value)
        return data

    # assume that data is a dict
    if keys_are_digits(data):
        # needs to be transformed into a list
        new_data = list(data.values())
        for i in range(len(new_data)):
            new_data[i] = dict_to_list(new_data[i])
    else:
        # no transformation needed
        new_data = data
        for key in data.keys():
            new_data[key] = dict_to_list(new_data[key])

    return new_data

def keys_are_digits(data):
    for key in list(data.keys()):
        if not key.isdigit():
            return False

    return True




