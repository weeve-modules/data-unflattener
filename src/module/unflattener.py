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
            # wrap base object into an extra dictionary to use recursion in check_data_for_lists
            wrapped_base = {
                "wrapped-base-root": base
            }
            base = check_data_for_lists(wrapped_base)["wrapped-base-root"]

        return base

    except Exception as e:
        return f"Exception when trying to unflatten data: {data}. Exception: {e}"

def check_data_for_lists(data):
    try:
        for k, v in data.items():
            if type(v) == dict:
                all_digits = keys_are_digits(v)

                if all_digits:
                    objects_copy = data[k]
                    data[k] = []

                    for ck in list(objects_copy.keys()):
                        data[k].append(check_data_for_lists(objects_copy[ck]))
                else:
                    data[k] = check_data_for_lists(data[k])

        return data

    except Exception as e:
        return f"Exception when trying to search for lists in data: {data}. Exception: {e}"

def keys_are_digits(data):
    for key in list(data.keys()):
        if not key.isdigit():
            return False

    return True




