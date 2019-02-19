import pytest

import qcenginevault as qcev
import qcelemental as qcel


def test_list_programs():
    assert "molpro" in qcev.list_programs()
    assert "terachem" in qcev.list_programs()


# Build out a list of all tests and validate
validation_tests = []
for program in qcev.list_programs():
    validation_tests.extend((program, case) for case in qcev.list_test_cases(program))


@pytest.mark.parametrize("program, test_case", validation_tests)
def test_validate_test_case(program, test_case):

    filenames = qcev.get_test_case_filenames(program, test_case)
    required_filesnames = qcev.get_required_files(program)

    # Check all required files are present
    assert filenames.keys() == set(required_filesnames), "Missing required files for testing."

    # Ensure the `input.json` is valid
    model = qcel.models.ResultInput.parse_file(filenames["input.json"])
