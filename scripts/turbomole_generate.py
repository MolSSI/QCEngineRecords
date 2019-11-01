#!/usr/bin/env python3

"""This script generates the record data in the CWD. The created
directories can then be moved to ../qcenginerecords/turbomole."""

from collections import namedtuple
import json
import os
from pathlib import Path

import qcelemental
from qcelemental.testing import compare_values
import qcengine


RecordData = namedtuple("RecordData",
                        "driver input_json output_json stdout outfiles",
)


def get_turbomole_records(driver, mol, method, keywords):
    resi = {
        "molecule": mol,
        "driver": driver,
        "model": {
            "method": method,
            "basis": "def2-SVP",
        },
        "keywords": keywords,
    }

    res = qcengine.compute(resi, "turbomole", raise_error=True)

    resi_ = qcelemental.models.ResultInput(**resi)
    input_json = resi_.json(indent=2)
    output_json = res.json(indent=2)
    rd = RecordData(res.driver, input_json, output_json, res.stdout, res.extras["outfiles"])

    return rd


def h2o():
    mol = qcelemental.models.Molecule.from_data("""
            O 0.000000000000     0.000000000000    -0.068516245955
            H 0.000000000000    -0.790689888800     0.543701278274
            H 0.000000000000     0.790689888800     0.543701278274
    """)
    return "water", mol


def generate_records():
    cases = (
        ("energy", 'hf', {}),
        ("energy", 'pbe0', {"grid": "m5"}),
        ("energy", 'ricc2', {}),
        ("energy", 'rimp2', {}),
        ("gradient", 'hf', {}),
        ("gradient", 'pbe0', {"grid": "m5"}),
        ("gradient", 'ricc2', {}),
        ("gradient", 'rimp2', {}),
    )
    mol_name, mol = h2o()
    for driver, method, keywords in cases:
        rd = get_turbomole_records(driver, mol, method, keywords)
        out_path = Path(f"{mol_name}_{rd.driver}_{method}")

        try:
            os.mkdir(out_path)
        except FileExistsError:
            print(f"Skipped creation of '{str(out_path)}' as it already exists")

        with open(out_path / "input.json", "w") as handle:
            handle.write(rd.input_json)

        with open(out_path / "output.json", "w") as handle:
            handle.write(rd.output_json)

        with open(out_path / "stdout", "w") as handle:
            handle.write(rd.stdout)

        if "gradient" in rd.outfiles:
            with open(out_path / "gradient", "w") as handle:
                handle.write(rd.outfiles["gradient"])


if __name__ == "__main__":
    generate_records()
