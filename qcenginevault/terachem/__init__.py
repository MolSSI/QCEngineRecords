import os

TERACHEM_INFO = {
    "base_folder": os.path.dirname(os.path.abspath(__file__)),
    "required_files": [
        "input.json",
        "example.in",
        "example.out",
        "geometry.xyz",
    ],
    "test_cases": {}
}

for dirname, subdirs, file_list in os.walk(TERACHEM_INFO["base_folder"]):
    if dirname == TERACHEM_INFO["base_folder"]:
        continue
    elif "pycache" in dirname:
        continue

    TERACHEM_INFO["test_cases"][os.path.basename(dirname)] = file_list
