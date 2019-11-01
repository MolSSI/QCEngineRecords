import pytest

import qcenginerecords as qcer
import qcelemental as qcel


def test_list_programs():
    assert "molpro" in qcer.list_programs()
    assert "entos" in qcer.list_programs()
    assert "terachem" in qcer.list_programs()
    assert "turbomole" in qcer.list_programs()


# Build out a list of all tests and validate
validation_tests = []
for program in qcer.list_programs():
    info = qcer.get_info(program)

    for case in qcer.list_test_cases(program):
        validation_tests.append(pytest.param(info, case, id="{}-{}".format(program, case)))


@pytest.mark.parametrize("info, test_case", validation_tests)
def test_validate_test_case(info, test_case):

    filenames = qcer.get_test_case_filenames(info.program, test_case)

    # Check all required files are present
    assert filenames.keys() >= info.required_files, "Missing required files for testing."
    assert filenames.keys() <= (info.required_files | info.optional_files), "Unknown files found."

    # Ensure the `input.json` is valid
    qcel.models.ResultInput.parse_file(filenames["input.json"])

    # Ensure the `output.json` is valid
    qcel.models.Result.parse_file(filenames["output.json"])
