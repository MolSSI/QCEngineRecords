import os
import json
import qcelemental as qcel
import qcengine as qcng

from qcelemental.util import serialize

molecule_name = "water" 
drivers = ["energy", "gradient", "hessian"]
keywords = {}
model = {"method": "HF", "basis": "6-31g"}
program = "qchem"

config = qcng.get_config()
temporary_directory = os.path.join(os.getcwd(), "build")
os.makedirs(temporary_directory, exist_ok=True)

for driver in drivers:
    folder_name = os.path.join(temporary_directory, f"{model['method'].lower()}_{molecule_name}_{driver}")
    os.makedirs(folder_name, exist_ok=True)

    input_model = {
        "molecule": qcng.get_molecule(molecule_name),
        "keywords": keywords,
        "model": model,
        "driver": driver,
    }
    input_model = qcel.models.ResultInput(**input_model)

    with open(os.path.join(folder_name, "input.json"), "w") as handle:
        handle.write(serialize(input_model, 'json'))


    # Save generated infiles
    prog = qcng.get_program(program)
    inputs = prog.build_input(input_model, config)
    with open(os.path.join(folder_name, "infiles.msgpack"), "wb") as handle:
        handle.write(serialize(inputs["infiles"], 'msgpack-ext'))

    # Save outfiles
    ret = prog.execute(inputs)
    with open(os.path.join(folder_name, "outfiles.msgpack"), "wb") as handle:
        handle.write(serialize(ret[1]["outfiles"], 'msgpack-ext'))

    # Save result
    result = prog.parse_output(ret[1]["outfiles"], input_model)
    with open(os.path.join(folder_name, "output.json"), "w") as handle:
        handle.write(serialize(result, 'json'))

