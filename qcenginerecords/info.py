import os
from typing import Dict, List, Set
from pydantic import BaseModel

_basedir = os.path.dirname(os.path.abspath(__file__))

INFO = {}


class ProgramTests(BaseModel):
    program: str
    base_folder: str
    required_files: Set[str]
    optional_files: Set[str]
    test_cases: Dict[str, Set[str]]

    class Config:
        allow_mutation = False

    def list_test_cases(self):
        return list(self.test_cases.keys())

    def get_test_data(self, test):

        ret = {}
        for fn in self.test_cases[test]:
            with open(os.path.join(self.base_folder, test, fn), 'r') as handle:
                ret[fn] = handle.read()

        return ret


def find_tests(path):
    ret = {}
    for dirname, subdirs, file_list in os.walk(path):
        if dirname == path:
            continue
        elif "pycache" in dirname:
            continue

        ret[os.path.basename(dirname)] = set(file_list)
    return ret


def build_test_info(program, required_files, optional_files=None):
    if optional_files is None:
        optional_files = set()

    path = os.path.join(_basedir, program)
    tests = find_tests(path)
    required_files = required_files | {"input.json", "output.json"}

    ret = ProgramTests(
        program=program,
        base_folder=path,
        required_files=required_files,
        optional_files=optional_files,
        test_cases=tests)
    return ret


# Molpro
INFO["molpro"] = build_test_info("molpro", {
    "dispatch.mol",
    "dispatch.out",
    "dispatch.xml",
})

# Entos
INFO["entos"] = build_test_info("entos", {
    "dispatch.in",
    "dispatch.out"
})

INFO["terachem"] = build_test_info("terachem", {
    "tc.in",
    "tc.out",
    "geometry.xyz",
})

INFO["dftd3"] = build_test_info(
    "dftd3", {
        "stdout",
    }, optional_files={"dftd3_gradient"})
