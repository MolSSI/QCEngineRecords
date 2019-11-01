import pprint
import json
import qcengine as qcng
inp = {
    "molecule": {
        "geometry": [
            0.0,  0.0,               -0.1294769411935893,
            0.0, -1.494187339479985,  1.0274465079245698,
            0.0,  1.494187339479985,  1.0274465079245698
        ],
        "symbols": ["O", "H", "H"],
    },
    "driver": "gradient",
    "keywords": {},
    "model": {
        "method": "B3LYP-D3",
    }
}

import qcelemental as qcel
from qcengine.programs import intf_dftd3

def format_dict(d):
    o = pprint.pformat(d, compact=True, indent=2, width=100)
    o = o.replace("'", '"')
    o = o.replace("True", "true")
    o = o.replace("False", "false")
    o = o.replace("None", "null")

    return o

print(format_dict(inp))
print("\n------\n")

inp = qcel.models.ResultInput(**inp)
out = intf_dftd3.run_json(inp.json_dict())
out["keywords"] = {}

stdout = out.pop("stdout")
print(stdout)
print("\n------\n")

out = qcel.models.Result(**out)
print(format_dict(out.json_dict()))
#
#print(json.dumps(out.json_dict(), indent=2))


