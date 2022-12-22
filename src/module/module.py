"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from .unflattener import unflattener

log = getLogger("module")


def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    try:
        if type(received_data) == list:
            processed_data = []

            for data in received_data:
                restored = unflattener(data)

                # in case of unflattener returning error
                if type(restored) == str:
                    return None, restored

                processed_data.append(restored)

        else:
            processed_data = unflattener(received_data)

            # in case of unflattener returning error
            if type(processed_data) == str:
                return None, processed_data

        return processed_data, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"
