import pytest

import qcenginerecords as qcev
import qcelemental as qcel


def test_list_programs():
    assert "molpro" in qcev.list_programs()
    assert "entos" in qcev.list_programs()
    assert "terachem" in qcev.list_programs()
    assert "turbomole" in qcev.list_programs()


# Build out a list of all tests and validate
validation_tests = []
for program in qcev.list_programs():
    info = qcev.get_info(program)

    for case in qcev.list_test_cases(program):
        validation_tests.append(pytest.param(info, case, id="{}-{}".format(program, case)))


@pytest.mark.parametrize("info, test_case", validation_tests)
def test_validate_test_case(info, test_case):

    filenames = qcev.get_test_case_filenames(info.program, test_case)

    # Check all required files are present
    assert filenames.keys() >= info.required_files, "Missing required files for testing."
    assert filenames.keys() <= (info.required_files | info.optional_files), "Unknown files found."

    # Ensure the `input.json` is valid
    qcel.models.ResultInput.parse_file(filenames["input.json"])

    # Ensure the `output.json` is valid
    # qcel.models.Result.parse_file(filenames["output.json"])
