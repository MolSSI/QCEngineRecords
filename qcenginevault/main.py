import os

from .molpro import MOLPRO_INFO

INFO = {"molpro": MOLPRO_INFO}


def list_programs():
    """
    List programs for which test cases exist.
    """
    return list(INFO)


def list_test_cases(program):
    """
    List all available test cases for a given program.
    """

    return list(INFO[program]["test_cases"])


def get_required_files(program):
    """
    Return the required files for a given program.
    """

    return INFO[program]["required_files"].copy()


def get_test_case_filenames(program, test_case):
    """
    Get the full filenames for all files in a given test case.
    """

    filenames = {}
    for f in INFO[program][test_case]:
        filenames[f] = os.path.join(INFO[program]["base_folder"], test_case, f)

    return filenames
