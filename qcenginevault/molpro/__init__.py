import os

MOLPRO_INFO = {
    "base_folder": os.path.dirname(os.path.abspath(__file__)),
    "required_files": [
        "input.json",
        "example.mol",
        "example.out",
        "example.xml",
    ],
    "test_cases": {}
}

for dirname, subdirs, file_list in os.walk(MOLPRO_INFO["base_folder"]):
    if dirname == MOLPRO_INFO["base_folder"]:
        continue

    MOLPRO_INFO["test_cases"][os.path.basename(dirname)] = file_list
