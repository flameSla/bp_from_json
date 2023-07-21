"""
construction_train
"""

from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import entity
from bp_from_json import get_items
import sys
import os
import argparse
import math

import json


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


#############################################
def create_chest(chest_position, row_number):
    return entity.new_entity(
        "steel-chest", chest_position, row_number, orientation=0.75
    )


#############################################
def requester_chests(bp, contents, row_number, chests):
    chest_position = 0
    chest = create_chest(chest_position, row_number)

    slot_count = 0
    # read json file
    # items = get_items()
    # Bob-Mod
    with open('BobMod.json', 'r', encoding='utf8') as read_file:
        json_items = json.load(read_file)

    # json -> dist()
    items = dict_bp()
    for i in json_items['items']:
        items[i['name']] = float(i['stack'])  # items["wooden-chest"] = 50.0

    for item, amount in contents.items():
        if item == 'red-inserter':
            item = 'long-handed-inserter'

        if item in items:
            stack_size = items[item]
        else:
            raise Exception("Unknown item ({})".format(item))
            # stack_size = 0

        if item == "landfill":
            # for landfill, we start a new train,
            #   so it's easier to remove these trains from the bp
            bp.append_entity(chest)
            chest_position += 1
            slot_count = 0
            chest = create_chest(chest_position, row_number)

        while amount > 0:
            try:
                slots = math.ceil(amount / stack_size)
            except ZeroDivisionError:
                slots = 0

            if slot_count + slots > 48:
                add_items = (48 - slot_count) * stack_size
                amount -= add_items
                chest.update_items({item: add_items}, name_verification=False)
                # Add a new wagon
                chest_position += 1
                if chest_position >= chests:
                    row_number += 1
                    chest_position = 0

                bp.append_entity(chest)
                slot_count = 0
                chest = create_chest(chest_position, row_number)

            else:
                chest.update_items({item: amount}, name_verification=False)
                amount = 0
                slot_count += slots

    bp.append_entity(chest)
    bp.set_icons(1, "virtual", "signal-B")
    bp.set_icons(2, "item", "construction-robot")


#############################################
def get_bp(chests, contents):
    bp = blueprint.new_blueprint()

    row_number = 0
    requester_chests(bp, contents, row_number, chests)

    bp.set_label_color(1, 0, 1)
    bp.set_label("construction_chests")

    print("==================================")
    print(bp.to_str())
    print("==================================")


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

    chests = input("how many chests are there in a row? (4):")
    exchange_str = input("bp to be built:(string or filename.txt)")
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    necessary_items_for_construction = bp.get_all_items()
    print("\nbp contains:")
    print(necessary_items_for_construction)

    # "item name": amount
    additional_items = dict_bp(
        {
            "construction-robot": 1350,
            "logistic-robot": 350,
            "radar": 50,
            "repair-pack": 100,
            "cliff-explosives": 100,
            "laser-turret": 50,
        }
    )
    additional_items = dict_bp()

    print("\nadditional items:")
    print(additional_items)

    contents = additional_items + necessary_items_for_construction
    contents += bp.get_all_tiles()

    debug("\ncontents:")
    debug(contents)

    get_bp(int(chests), contents)
