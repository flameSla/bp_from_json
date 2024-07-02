from bp_from_json import blueprint
from bp_from_json import get_recipes_with_one_product
from bp_from_json import get_items
from bp_from_json import get_entities
from fractions import Fraction
import math
from operator import itemgetter
import sys


# ====================================
def print_productivity():
    for k, v in sorted(productivity.items(), key=lambda x: x[0]):
        print("'{}': Fraction({}),".format(k, float(v)))


productivity = {
    "accumulator": Fraction(1.0),
    "advanced-circuit": Fraction(1.4),
    "artillery-shell": Fraction(1.0),
    "assembling-machine-1": Fraction(1.0),
    "assembling-machine-2": Fraction(1.0),
    "assembling-machine-3": Fraction(1.0),
    "atomic-bomb": Fraction(1.0),
    "battery": Fraction(1.3),
    "battery-equipment": Fraction(1.0),
    "battery-mk2-equipment": Fraction(1.0),
    "beacon": Fraction(1.0),
    "big-electric-pole": Fraction(1.0),
    "chemical-plant": Fraction(1.0),
    "concrete": Fraction(1.0),
    "constant-combinator": Fraction(1.0),
    "construction-robot": Fraction(1.0),
    "copper-cable": Fraction(1.4),
    "copper-plate": Fraction(1.2),
    "effectivity-module": Fraction(1.0),
    "effectivity-module-2": Fraction(1.0),
    "effectivity-module-3": Fraction(1.0),
    "electric-engine-unit": Fraction(1.4),
    "electric-furnace": Fraction(1.0),
    "electronic-circuit": Fraction(1.4),
    "engine-unit": Fraction(1.4),
    "exoskeleton-equipment": Fraction(1.0),
    "explosive-cannon-shell": Fraction(1.0),
    "explosives": Fraction(1.3),
    "express-splitter": Fraction(1.0),
    "express-transport-belt": Fraction(1.0),
    "express-underground-belt": Fraction(1.0),
    "fast-inserter": Fraction(1.0),
    "fast-splitter": Fraction(1.0),
    "fast-transport-belt": Fraction(1.0),
    "fast-underground-belt": Fraction(1.0),
    "firearm-magazine": Fraction(1.0),
    "flamethrower-turret": Fraction(1.0),
    "flying-robot-frame": Fraction(1.4),
    "fusion-reactor-equipment": Fraction(1.0),
    "gun-turret": Fraction(1.0),
    "heat-exchanger": Fraction(1.0),
    "heat-pipe": Fraction(1.0),
    "inserter": Fraction(1.0),
    "iron-gear-wheel": Fraction(1.4),
    "iron-plate": Fraction(1.2),
    "iron-stick": Fraction(1.4),
    "lab": Fraction(1.0),
    "landfill": Fraction(1.0),
    "laser-turret": Fraction(1.0),
    "logistic-chest-active-provider": Fraction(1.0),
    "logistic-chest-passive-provider": Fraction(1.0),
    "logistic-chest-requester": Fraction(1.0),
    "logistic-chest-storage": Fraction(1.0),
    "logistic-robot": Fraction(1.0),
    "long-handed-inserter": Fraction(1.0),
    "low-density-structure": Fraction(1.4),
    "lubricant": Fraction(1.3),
    "medium-electric-pole": Fraction(1.0),
    "nuclear-fuel": Fraction(1.2),
    "nuclear-reactor": Fraction(1.0),
    "offshore-pump": Fraction(1.0),
    "oil-refinery": Fraction(1.0),
    "personal-laser-defense-equipment": Fraction(1.0),
    "personal-roboport-equipment": Fraction(1.0),
    "personal-roboport-mk2-equipment": Fraction(1.0),
    "piercing-rounds-magazine": Fraction(1.0),
    "pipe": Fraction(1.0),
    "pipe-to-ground": Fraction(1.0),
    "plastic-bar": Fraction(1.3),
    "power-armor-mk2": Fraction(1.0),
    "processing-unit": Fraction(1.4),
    "pump": Fraction(1.0),
    "radar": Fraction(1.0),
    "rail": Fraction(1.0),
    "rail-chain-signal": Fraction(1.0),
    "rail-signal": Fraction(1.0),
    "roboport": Fraction(1.0),
    "rocket-control-unit": Fraction(1.4),
    "rocket-fuel": Fraction(1.4),
    "rocket-launcher": Fraction(1.0),
    "rocket-silo": Fraction(1.0),
    "solar-panel": Fraction(1.0),
    "speed-module": Fraction(1.0),
    "speed-module-2": Fraction(1.0),
    "spidertron": Fraction(1.0),
    "splitter": Fraction(1.0),
    "stack-filter-inserter": Fraction(1.0),
    "stack-inserter": Fraction(1.0),
    "steam-turbine": Fraction(1.0),
    "steel-chest": Fraction(1.0),
    "steel-plate": Fraction(1.2),
    "stone-brick": Fraction(1.2),
    "storage-tank": Fraction(1.0),
    "substation": Fraction(1.0),
    "sulfur": Fraction(1.3),
    "sulfuric-acid": Fraction(1.3),
    "train-stop": Fraction(1.0),
    "transport-belt": Fraction(1.0),
    "underground-belt": Fraction(1.0),
    "uranium-fuel-cell": Fraction(1.4),
    "uranium-rounds-magazine": Fraction(1.0),
}

productivity = {}
# ====================================
par_debugging = False


def debug(*args, end="\n"):
    global par_debugging
    if par_debugging:
        print(*args, end=end, file=sys.stderr, flush=True)


# ====================================
class dict_bp(dict):
    def __add__(self, other):
        temp = dict_bp(self)
        for key, value in other.items():
            if key in temp:
                temp[key][1] += value[1]
                temp[key][0] = max(temp[key][0], value[0])  # level
            else:
                temp[key] = value
        return temp

    def __iadd__(self, other):
        for key, value in other.items():
            if key in self:
                self[key][1] += value[1]
                self[key][0] = max(self[key][0], value[0])  # level
            else:
                self[key] = value
        return self


# ====================================
def print_dict(d, dimension=None):
    if dimension is None:
        dimension = ""

    temp = [(k, v[0], v[1]) for k, v in d.items()]
    # print("temp = ", type(temp), temp)
    for k, l, v in sorted(temp, key=itemgetter(1, 0)):
        print("{:34}(level{:3d}) = {:10.3f} {}".format(k, l, float(v), dimension))


# ====================================
def get_all_ingredients(item_name, amount, final_ingredients):

    res = dict_bp()
    if item_name in productivity:
        k = productivity[item_name]
    else:
        k = Fraction(1)
        # print("'{}': Fraction(1.0),".format(item_name))
    for ingredient in recipes[item_name]["ingredients"]:
        # print(ingredient['name'], amount)
        res += recursion_get_all_ingredients(
            ingredient, amount / k, final_ingredients, 0
        )
    # print('-------------------\n', item_name)
    # print_dict(res)
    return res


def recursion_get_all_ingredients(ingredient, amount, final_ingredients, level):
    res = dict_bp()
    level += 1
    debug("recurcive - level = {}".format(level))
    debug("\t", ingredient, amount)
    if isinstance(ingredient, dict):
        res += dict_bp({ingredient["name"]: [level, amount * ingredient["amount"]]})
        if (
            not ingredient["name"] in final_ingredients
            and ingredient["name"] in recipes
        ):
            if ingredient["name"] in productivity:
                k = productivity[ingredient["name"]]
            else:
                k = Fraction(1)
                # print("'{}': Fraction(1.0),".format(ingredient["name"]))
            for i in recipes[ingredient["name"]]["ingredients"]:
                res += recursion_get_all_ingredients(
                    i, ingredient["amount"] * amount / k, final_ingredients, level
                )
    return res


######################################
#
# main
if __name__ == "__main__":
    recipes = get_recipes_with_one_product()
    recipes["space-science-pack"] = {
        "ingredients": [
            {"name": "rocket-part", "type": "item", "amount": Fraction(100, 1000)},
            {"name": "satellite", "type": "item", "amount": Fraction(1, 1000)},
        ],
        "product": "space-science-pack",
    }

    entities = get_entities()

    science = {
        # "automation-science-pack": 1,
        # "logistic-science-pack": 1,
        # "military-science-pack": 1,
        # "chemical-science-pack": 1,
        # "production-science-pack": 1,
        # "utility-science-pack": 1,
        "space-science-pack": 1,
    }

    print(recipes["copper-plate"])

    # final_ingredients = ('iron-plate', 'copper-plate', 'steel-plate', 'plastic-bar', 'stone-brick', 'lubricant')
    final_ingredients = ("iron-plate", "copper-plate", "stone-brick", "lubricant")
    ingredients = dict_bp()
    for item_name, amount in science.items():
        if item_name in recipes:
            ingredients[item_name] = [0, amount]
            ingredients += get_all_ingredients(item_name, amount, final_ingredients)
            # print_dict(ingredients)

    print()
    print_dict(ingredients, "/sec")

    # print([x for x in recipes.keys()])
    # i = []
    # for name, v in recipes.items():
    #     i = [x["name"] for x in v["ingredients"]]
    #     res = False
    #     for a in i:
    #         if "rocket" in a:
    #             res = True
    #             break

    #     if res:
    #         print(name, i)

    # a = {
    #     "ingredients": [
    #         {"name": "rocket-part", "type": "item", "amount": Fraction(100, 1000)},
    #         {"name": "satellite", "type": "item", "amount": Fraction(1, 1000)},
    #     ],
    #     "product": "space-science-pack",
    # }

    def print_crafting_categories():
        print()
        print('==================')
        print('crafting_categories')
        print()
        a = {}
        for e in entities:
            # print(e["name"])
            for b in e.get("crafting_categories", ""):
                if b in a:
                    a[b].append((e["name"], e["speed"]))
                else:
                    a[b] = [(e["name"], e["speed"])]
        print(a)

    print_crafting_categories()
