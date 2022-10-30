import os
from logging import getLogger

log = getLogger("unflattener")

__PARENTNESS__ = os.getenv("PARENTNESS", "/")
__SEARCH_FOR_LISTS__ = bool(os.getenv("SEARCH_FOR_LISTS", "True"))

def unflattener(data):
    try:
        base = {}

        for k, v in data.items():
            fields = k.split(__PARENTNESS__)
            temp = base
            for f in fields[:-1]:
                if f not in temp:
                    temp[f] = {}
                temp = temp[f]
            temp[fields[-1]] = v

        if __SEARCH_FOR_LISTS__:
            base = checkDataForLists(base)

        return base

    except Exception as e:
        return f"Exception when trying to unflatten data: {data}. Exception: {e}"

def checkDataForLists(data):
    try:
        for k, v in data.items():
            if type(v) == dict:
                all_digits = True
                for ck in list(v.keys()):
                    if not ck.isdigit():
                        all_digits = False

                if all_digits:
                    objects_copy = data[k]
                    data[k] = []

                    for ck in list(objects_copy.keys()):
                        data[k].append(checkDataForLists(objects_copy[ck]))
        return data

    except Exception as e:
        return f"Exception when trying to search for lists in data: {data}. Exception: {e}"