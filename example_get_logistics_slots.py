"""
example_get_logistics_slots
"""

from bp_from_json import blueprint
from bp_from_json import dict_bp
import sys
import os
import argparse


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


######################################
#
# main
if __name__ == "__main__":
    exchange_str = ""
    parser = argparse.ArgumentParser(
        description="example: example_get_logistics_slots.py"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="d", help="debug output on STDERR"
    )
    opt = parser.parse_args()

    items = []
    with open(
        r"D:\GitHub\factorio-logistics-requests\src\player_all_items_to_zero.h", "r"
    ) as f:
        for line in f.readlines():
            lile = line.rstrip()
            line = line.replace("max = 0", "max = {}")
            line = line.replace("min = 0", "min = {}")
            items.append(line)
    # print("items = ", type(items), items)

    exchange_str = input("bp to be slots:(string or filename.txt)")
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    necessary_items = bp.get_all_items()
    print("\nbp contains:")
    print(necessary_items)
    m = input("multiplicity? [1]:")
    for k, v in necessary_items.items():
        found_string = tuple(x for x in items if '"{}"'.format(k) in x)
        if len(found_string) == 1:
            print(found_string[0].replace("{}", str(int(v) * int(m))).rstrip())
        else:
            print("!!!!!!!!!!!!!!!!!!!")
            print(found_string)
            print()
