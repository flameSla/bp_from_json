"""
Space Exploration: colonization of the planet
"""

from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import entity
import sys
import os
import argparse


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


#############################################
def get_bp(contents):

    bp = blueprint.new_blueprint()

    aai_warehouse = entity.new_entity('aai-warehouse', 0, 0)
    for item, amount in contents.items():
        aai_warehouse.update_items({item: amount},
                                   name_verification=False)

    bp.append_entity(aai_warehouse)

    bp.set_label_color(1, 0, 1)
    bp.set_label("Space Exploration: colonization of the planet")

    print('==================================')
    print(bp.to_str())
    print('==================================')


######################################
#
# main
if __name__ == "__main__":

    exchange_str = ''
    parser = argparse.ArgumentParser(
        description="example: python construction_train.py")
    parser.add_argument("-d", "--debug", action="store_true", dest="d",
                        help="debug output on STDERR")
    opt = parser.parse_args()

    exchange_str = input('bp to be built:(string or filename.txt)')
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    necessary_items_for_construction = bp.get_all_items()
    print("\nbp contains:")
    print(necessary_items_for_construction)

    # "item name": amount
    additional_items = dict_bp()
    # additional_items = dict_bp({
    #     "construction-robot": 200,
    #     "logistic-robot": 50,
    #     "radar": 50,
    #     "repair-pack": 100,
    #     "cliff-explosives": 100,
    #     "laser-turret": 50
    # })

    print("\nadditional items:")
    print(additional_items)

    contents = additional_items + necessary_items_for_construction
    # contents += bp.get_all_tiles()

    debug("\ncontents:")
    debug(contents)

    get_bp(contents)
