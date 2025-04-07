"""
Aquilo
"""

from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import entity
from bp_from_json import get_items
from bp_from_json import input_def
import sys
import os
import argparse
import math
import uuid
import enum


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


thermal_power = {
    "pumpjack": 50,
    "pipe-to-ground": 150,
    "pipe": 1,
    "heat-pipe": 0,
    "medium-electric-pole": 0,
    "roboport": 300,
    "beacon": 400,
    "heating-tower": 0,
    "bulk-inserter": 50,
    "cryogenic-plant": 100,
    "big-electric-pole": 0,
    "express-transport-belt": 10,
    "express-underground-belt": 150,
    "substation": 0,
    "chemical-plant": 100,
    "recycler": 100,
    "storage-tank": 100,
    "infinity-pipe": 0,
    "constant-combinator": 0,
    "pump": 30,
    "turbo-underground-belt": 200,
    "long-handed-inserter": 50,
    "turbo-transport-belt": 10,
    "offshore-pump": 0,
    "fusion-generator": 0,
    "requester-chest": 0,
    "fusion-reactor": 0,
    "passive-provider-chest": 0,
    "rocket-silo": 300,
    "cargo-bay": 0,
    "assembling-machine-3": 100,
    "stack-inserter": 50,
    "electric-furnace": 100,
    "electromagnetic-plant": 100,
    "turbo-splitter": 40,
    "steel-chest": 0,
    "cargo-landing-pad": 0,
    "storage-chest": 0,
    "active-provider-chest": 0,
    "nuclear-reactor": 0,
    "express-splitter": 40,
    "infinity-chest": 0,
    "heat-exchanger": 0,
    "steam-turbine": 50,
    "buffer-chest": 0,
}


######################################
#
# main
if __name__ == "__main__":
    exchange_str = ""
    parser = argparse.ArgumentParser(
        description="example: python construction_train.py"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="d", help="debug output on STDERR"
    )
    opt = parser.parse_args()

    exchange_str = input_def("bp (string or filename.txt):", "Aquilo.txt.ignore")
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    all_items = bp.get_all_items()
    print("all_items = ", type(all_items), all_items)
    print()
    print("==================")
    print("")
    print()
    print("\nbp contains:")
    print(all_items)

    total = 0
    for k, v in all_items.items():
        if k in thermal_power:
            print(
                '"{}" -> {} * {} = {}'.format(
                    k, v, thermal_power[k], v * thermal_power[k]
                )
            )
            total += v * thermal_power[k]
        else:
            print('"{}": ???,'.format(k))
    print("total:", total)
