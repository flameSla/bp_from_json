import argparse
import base64
import json
import os
import sys
import zlib
from bp_from_json import blueprint
from bp_from_json import dict_bp
from fractions import Fraction

# from urllib.parse import quote, unquote
# import networkx as nx
# import matplotlib.pyplot as plt
# from netgraph import Graph


#############################################
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
    ################################
    "electric-mining-drill": Fraction(1.0),
    "small-electric-pole": Fraction(1.0),
    "arithmetic-combinator": Fraction(1.0),
    "decider-combinator": Fraction(1.0),
    "small-lamp": Fraction(1.0),
    "logistic-chest-buffer": Fraction(1.0),
    "filter-inserter": Fraction(1.0),
    "speed-module-3": Fraction(1.0),
    "electric-mining-drill": Fraction(1.0),
    "programmable-speaker": Fraction(1.0),
    "small-lamp": Fraction(1.0),
    "decider-combinator": Fraction(1.0),
    "arithmetic-combinator": Fraction(1.0),
    "logistic-chest-buffer": Fraction(1.0),
    "filter-inserter": Fraction(1.0),
    "productivity-module-3": Fraction(1.0),
    "productivity-module-2": Fraction(1.0),
    "productivity-module": Fraction(1.0),
    ################################
    "cargo-wagon": Fraction(1.0),
    "locomotive": Fraction(1.0),
    "boiler": Fraction(1.0),
    "stone-furnace": Fraction(1.0),
    "steel-furnace": Fraction(1.0),
    "wooden-chest": Fraction(1.0),
}


#############################################
nuclear_power_plant_1120MW = {
    "accumulator": 4,
    "heat-exchanger": 112,
    "heat-pipe": 200,
    "landfill": 4701,
    "logistic-chest-active-provider": 8,
    "logistic-chest-requester": 8,
    "medium-electric-pole": 8,
    "nuclear-reactor": 8,
    "offshore-pump": 12,
    "pipe": 12,
    "pipe-to-ground": 4,
    "pump": 10,
    "radar": 1,
    "roboport": 2,
    "solar-panel": 4,
    "stack-inserter": 16,
    "steam-turbine": 224,
    "substation": 22,
}


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


#############################################
# https://stackoverflow.com/questions/46351275/using-pako-deflate-with-python
#
def pako_inflate_raw(data):
    decompress = zlib.decompressobj(-15)
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    return decompressed_data


def pako_deflate_raw(data):
    compress = zlib.compressobj(
        zlib.Z_DEFAULT_COMPRESSION,
        zlib.DEFLATED,
        -15,
        memLevel=8,
        strategy=zlib.Z_DEFAULT_STRATEGY,
    )
    # compressed_data = compress.compress(js_string_to_byte(js_encode_uri_component(data)))
    compressed_data = compress.compress(js_string_to_byte(data))
    compressed_data += compress.flush()
    return compressed_data


def js_encode_uri_component(data):
    return quote(data, safe="~()*!.'")


def js_decode_uri_component(data):
    return unquote(data)


def js_string_to_byte(data):
    return bytes(data, "iso-8859-1")


def js_bytes_to_string(data):
    return data.decode("iso-8859-1")


def js_btoa(data):
    return base64.b64encode(data)


def js_atob(data):
    return base64.b64decode(data)


########################################
def input_def(text, default):
    str = input(text + "[" + default + "]:")
    return str if str else default


#############################################
def get_recipes():
    # read json file
    with open("Factorio 1.1 Vanilla.json", "r") as read_file:
        json_all = json.load(read_file)

    # json -> dist()
    recipes = dict()
    for recipe in json_all["recipes"]:
        if len(recipe["products"]) == 1:
            for ingredient in recipe["ingredients"]:
                ingredient["amount"] = Fraction(
                    ingredient["amount"], recipe["products"][0]["amount"]
                )
            recipes[recipe["name"]] = recipe["ingredients"]

    return recipes


#############################################
def get_ingredients_graph(
    G, ingredient, amount, final_ingredients, ingredient_name=None
):
    debug("recurcive")
    debug("\t", ingredient, amount)

    if ingredient_name:
        if "consumption" in G.edges[ingredient["name"], ingredient_name]:
            G.edges[ingredient["name"], ingredient_name]["consumption"] += float(
                amount * ingredient["amount"]
            )
        else:
            G.edges[ingredient["name"], ingredient_name]["consumption"] = float(
                amount * ingredient["amount"]
            )

    if not ingredient["name"] in final_ingredients and ingredient["name"] in recipes:
        if ingredient["name"] in productivity:
            k = productivity[ingredient["name"]]
        else:
            k = Fraction(1)
            print("'{}': Fraction(1.0),".format(ingredient["name"]))
        for i in recipes[ingredient["name"]]:
            G.add_edge(i["name"], ingredient["name"])
            get_ingredients_graph(
                G,
                i,
                ingredient["amount"] * amount / k,
                final_ingredients,
                ingredient["name"],
            )


#############################################
def get_all_ingredients(item_name, amount, final_ingredients):
    res = dict_bp()
    if item_name in productivity:
        k = productivity[item_name]
    else:
        k = Fraction(1)
        print("'{}': Fraction(1.0),".format(item_name))
    for ingredient in recipes[item_name]:
        # print(ingredient['name'], amount)
        res += recursion_get_all_ingredients(ingredient, amount / k, final_ingredients)
    # print('-------------------\n', item_name)
    # print_dict(res)
    return res


#############################################
def recursion_get_all_ingredients(ingredient, amount, final_ingredients):
    res = dict_bp()
    debug("recurcive")
    debug("\t", ingredient, amount)
    if isinstance(ingredient, dict):
        res += dict_bp({ingredient["name"]: amount * ingredient["amount"]})
        if (
            not ingredient["name"] in final_ingredients
            and ingredient["name"] in recipes
        ):
            if ingredient["name"] in productivity:
                k = productivity[ingredient["name"]]
            else:
                k = Fraction(1)
                print("'{}': Fraction(1.0),".format(ingredient["name"]))
            for i in recipes[ingredient["name"]]:
                res += recursion_get_all_ingredients(
                    i, ingredient["amount"] * amount / k, final_ingredients
                )
    return res


#############################################
def print_dict(d, dimension=None):
    if dimension is None:
        dimension = ""
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        print("{:34} = {:10.3f} {}".format(k, float(v), dimension))


#############################################
class Build:
    def __init__(self, name, text_message, default_value, recipes, final_ingredients):
        self.name = name
        self.recipes = recipes
        self.final_ingredients = final_ingredients

        exchange_str = input_def(text_message, default_value)
        if os.path.exists(exchange_str):
            bp = blueprint.from_file(exchange_str)
        else:
            bp = blueprint.from_string(exchange_str)

        self.necessary_items_for_construction = bp.get_all_items()
        debug()
        debug("==================")
        debug(
            json.dumps(self.necessary_items_for_construction, indent=4, sort_keys=True)
        )
        debug()

        ingredients = dict_bp()
        for item_name, amount in self.necessary_items_for_construction.items():
            if item_name in self.recipes:
                ingredients += get_all_ingredients(item_name, amount, ())
        ingredients += self.necessary_items_for_construction

        self.ingredients_compact = dict_bp()
        for ingredient in self.final_ingredients:
            self.ingredients_compact[ingredient] = ingredients.get(ingredient, 0)

    def add(self, b):
        self.ingredients_compact += b.ingredients_compact
        self.name += " + " + b.name

    def get_ingredients_compact(self):
        return self.ingredients_compact

    def compare(self, B):
        i1 = self.ingredients_compact
        i2 = B.get_ingredients_compact()

        print()
        print(
            "{:10}   {:>15}   {:>15}".format(
                "",
                self.name,
                B.name,
            )
        )
        for ingredient in self.final_ingredients:
            times_more = i1[ingredient] / i2[ingredient]
            if i2[ingredient] > i1[ingredient]:
                times_more = 1 / times_more

            print(
                "{:10}   {:15.3f} / {:15.3f} times_more = {:15.3f}".format(
                    ingredient,
                    float(i1[ingredient]),
                    float(i2[ingredient]),
                    float(times_more),
                )
            )


######################################
#
# main
if __name__ == "__main__":
    # print_productivity()

    exchange_str = ""
    parser = argparse.ArgumentParser(
        description="example: example_mining_comparison.py"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="d", help="debug output on STDERR"
    )
    opt = parser.parse_args()
    # opt.d = True

    recipes = get_recipes()
    final_ingredients = ("copper-ore", "iron-ore", "coal", "stone")

    # mining_1 = Build(
    #     "mining-1",
    #     "mining-1 BP (string or filename.txt)",
    #     "mining_1.txt",
    #     recipes,
    #     final_ingredients,
    # )
    # mining_2 = Build(
    #     "mining-2",
    #     "mining-2 BP (string or filename.txt)",
    #     "mining_2.txt",
    #     recipes,
    #     final_ingredients,
    # )
    cell500spm = Build(
        "cell500spm",
        "cell500spm BP (string or filename.txt)",
        "cell500spm.txt",
        recipes,
        final_ingredients,
    )

    # mining_1.compare(mining_2)
    # mining_2.compare(cell500spm)

    print()
    print("==================")
    print("Модули-ремни")
    print()

    ass_NaOida = Build(
        "mashinesT3_NaOida",
        "cell500spm BP (string or filename.txt)",
        "ass-NaOida.txt.ignore",
        recipes,
        final_ingredients,
    )

    modules_NaOida = Build(
        "modules_NaOida",
        "cell500spm BP (string or filename.txt)",
        "modules-NaOida.txt.ignore",
        recipes,
        final_ingredients,
    )

    modules_Sla = Build(
        "modules_Sla",
        "cell500spm BP (string or filename.txt)",
        "modules-Sla.txt.ignore",
        recipes,
        final_ingredients,
    )

    belts_Sla = Build(
        "belts_Sla",
        "cell500spm BP (string or filename.txt)",
        "belts-Sla.txt.ignore",
        recipes,
        final_ingredients,
    )

    cell500spm.compare(ass_NaOida)
    ass_NaOida.add(modules_NaOida)

    # modules_Sla.compare(modules_NaOida)
    # belts_Sla.compare(modules_Sla)
    belts_Sla.add(modules_Sla)
    belts_Sla.compare(ass_NaOida)

    # print()
    # print('|{:<30}|'.format('left aligned'))
    # print('|{:>30}|'.format('right aligned'))
    # print('|{:^30}|'.format('centered'))
    # print('|{:*^30}|'.format('centered'))
