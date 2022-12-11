#
# Get requests for chests
#

import argparse
import math
import json
import sys
from bp_from_json import blueprint
from bp_from_json import entity
from bp_from_json import get_items
from fractions import Fraction


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


#############################################
def get_recipes():
    # read json file
    with open('Factorio 1.1 Vanilla.json', 'r') as read_file:
        json_all = json.load(read_file)

    # json -> dist()
    recipes = dict()
    for recipe in json_all['recipes']:
        if len(recipe['products']) == 1:
            for ingredient in recipe['ingredients']:
                ingredient['amount'] = Fraction(ingredient['amount'],
                                                recipe['products'][0]['amount'])
            recipes[recipe['name']] = recipe['ingredients']

    return recipes


#############################################
def print_dict(d, dimension=None):
    if dimension is None:
        dimension = ''
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        print('{:34} = {:10.3f} {}'.format(k, float(v), dimension))


#############################################
requests = {
    "wooden-chest": 10,
    "iron-chest": 10,
    "steel-chest": 10,
    "storage-tank": 10,
    "transport-belt": 10,
    "underground-belt": 10,
    "splitter": 10,
    "fast-transport-belt": 10,
    "fast-underground-belt": 10,
    "fast-splitter": 10,
    "express-transport-belt": 10,
    "express-underground-belt": 10,
    "express-splitter": 10,
    "burner-inserter": 10,
    "inserter": 10,
    "long-handed-inserter": 10,
    "fast-inserter": 10,
    "filter-inserter": 10,
    "stack-inserter": 10,
    "stack-filter-inserter": 10,
    "small-electric-pole": 10,
    "medium-electric-pole": 10,
    "big-electric-pole": 10,
    "substation": 10,
    "pipe": 10,
    "pipe-to-ground": 10,
    "pump": 10,
    "rail": 10,
    "train-stop": 10,
    "rail-signal": 10,
    "rail-chain-signal": 10,
    "locomotive": 10,
    "cargo-wagon": 10,
    "fluid-wagon": 10,
    "artillery-wagon": 10,
    "car": 10,
    "tank": 10,
    "spidertron": 1,
    "spidertron-remote": 1,
    "logistic-robot": 10,
    "construction-robot": 10,
    "logistic-chest-active-provider": 10,
    "logistic-chest-passive-provider": 10,
    "logistic-chest-storage": 10,
    "logistic-chest-buffer": 10,
    "logistic-chest-requester": 10,
    "roboport": 10,
    "small-lamp": 10,
    "red-wire": 10,
    "green-wire": 10,
    "arithmetic-combinator": 10,
    "decider-combinator": 10,
    "constant-combinator": 10,
    "power-switch": 10,
    "programmable-speaker": 10,
    "stone-brick": 10,
    "concrete": 10,
    "hazard-concrete": 10,
    "refined-concrete": 10,
    "refined-hazard-concrete": 10,
    "landfill": 10,
    "cliff-explosives": 10,
    "repair-pack": 10,
    "boiler": 10,
    "steam-engine": 10,
    "solar-panel": 10,
    "accumulator": 10,
    "nuclear-reactor": 1,
    "heat-pipe": 10,
    "heat-exchanger": 10,
    "steam-turbine": 10,
    "electric-mining-drill": 10,
    "offshore-pump": 10,
    "pumpjack": 10,
    "stone-furnace": 10,
    "steel-furnace": 10,
    "electric-furnace": 10,
    "assembling-machine-1": 10,
    "assembling-machine-2": 10,
    "assembling-machine-3": 10,
    "oil-refinery": 10,
    "chemical-plant": 10,
    "centrifuge": 10,
    "lab": 10,
    "rocket-silo": 1,
    "beacon": 10,
    "speed-module": 10,
    "speed-module-2": 10,
    "speed-module-3": 10,
    "effectivity-module": 10,
    "effectivity-module-2": 10,
    "effectivity-module-3": 10,
    "productivity-module": 10,
    "productivity-module-2": 10,
    "productivity-module-3": 10,
    "submachine-gun": 1,
    "rocket-launcher": 10,
    "shotgun": 10,
    "combat-shotgun": 1,
    "flamethrower": 10,
    "land-mine": 10,
    "firearm-magazine": 100,
    "piercing-rounds-magazine": 100,
    "uranium-rounds-magazine": 100,
    "shotgun-shell": 100,
    "piercing-shotgun-shell": 100,
    "cannon-shell": 10,
    "explosive-cannon-shell": 10,
    "uranium-cannon-shell": 10,
    "explosive-uranium-cannon-shell": 10,
    "artillery-shell": 10,
    "rocket": 100,
    "explosive-rocket": 100,
    "atomic-bomb": 10,
    "flamethrower-ammo": 10,
    "grenade": 10,
    "cluster-grenade": 10,
    "poison-capsule": 10,
    "slowdown-capsule": 10,
    "defender-capsule": 10,
    "distractor-capsule": 10,
    "destroyer-capsule": 10,
    "light-armor": 1,
    "heavy-armor": 1,
    "modular-armor": 1,
    "power-armor": 1,
    "power-armor-mk2": 1,
    "solar-panel-equipment": 10,
    "fusion-reactor-equipment": 1,
    "battery-equipment": 10,
    "battery-mk2-equipment": 1,
    "belt-immunity-equipment": 1,
    "exoskeleton-equipment": 10,
    "personal-roboport-equipment": 10,
    "personal-roboport-mk2-equipment": 1,
    "night-vision-equipment": 1,
    "energy-shield-equipment": 10,
    "energy-shield-mk2-equipment": 10,
    "personal-laser-defense-equipment": 10,
    "discharge-defense-equipment": 1,
    "discharge-defense-remote": 1,
    "stone-wall": 10,
    "gate": 10,
    "gun-turret": 10,
    "laser-turret": 10,
    "flamethrower-turret": 10,
    "artillery-turret": 10,
    "artillery-targeting-remote": 1,
    "radar": 10,
    "battery": 10,
    "explosives": 10,
    "copper-cable": 10,
    "iron-stick": 10,
    "iron-gear-wheel": 10,
    "empty-barrel": 10,
    "electronic-circuit": 10,
    "advanced-circuit": 10,
    "processing-unit": 10,
    "engine-unit": 10,
    "electric-engine-unit": 10,
    "flying-robot-frame": 10,
    "rocket-control-unit": 10,
    "low-density-structure": 10,
    "uranium-fuel-cell": 10,
    "automation-science-pack": 100,
    "logistic-science-pack": 100,
    "military-science-pack": 100,
    "chemical-science-pack": 100,
    "production-science-pack": 100,
    "utility-science-pack": 100}


######################################
def select_chest(slots, request):
    if slots > 48:
        raise Exception("{}: slots > 48".format(request))
    elif slots > 32:
        res = 'steel-chest'

    elif slots > 16:
        res = 'iron-chest'
    else:
        res = 'wooden-chest'

    return res


######################################
#
# main
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="example: python construction_train.py")
    parser.add_argument("-d", "--debug", action="store_true", dest="d",
                        help="debug output on STDERR")
    opt = parser.parse_args()
    # opt.d = True

    recipes = get_recipes()
    items = get_items()

    book1 = blueprint.new_blueprint_book()
    book2 = blueprint.new_blueprint_book()
    for request, amount in requests.items():
        ingredients = [(i['name'], i['amount']*amount) for i in recipes[request] if i['name'] in items]
        debug(ingredients)
        slots = 0
        for item, amount in ingredients:
            stack_size = items[item]
            slots += math.ceil(amount/stack_size)
        debug('slots = ', slots)
        bp1 = blueprint.new_blueprint()
        bp2 = blueprint.new_blueprint()
        chest = entity.new_entity(select_chest(slots, request), 0, 0)
        requester = entity.new_entity('logistic-chest-requester', 0, 0)
        index = 0
        for item, amount in ingredients:
            index += 1
            debug(index, item, math.ceil(amount))
            chest.update_items({item: math.ceil(amount)},
                               name_verification=False)
            requester.append_request_filters({"index": index,
                                              "name": item,
                                              "count": math.ceil(amount)})
        bp1.append_entity(chest)
        bp1.set_label(str(requests[request]))
        bp1.set_icons(1, 'item', request)
        bp2.append_entity(requester)
        bp2.set_label(str(requests[request]))
        bp2.set_icons(1, 'item', request)
        debug('=== chest ========================')
        debug(bp1.to_str())
        debug('==================================')
        debug('=== requester ========================')
        debug(bp2.to_str())
        debug('==================================')
        book1.append_bp(bp1)
        book2.append_bp(bp2)

    print('=== chest ========================')
    print(book1.to_str())
    print('==================================')
    print('=== requester ========================')
    print(book2.to_str())
    print('==================================')
