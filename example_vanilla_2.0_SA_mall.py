from bp_from_json import blueprint
from bp_from_json import get_recipes_with_one_product
from bp_from_json import get_items
from bp_from_json import v1_1_110
from bp_functions import get_iningredients
from bp_functions import add_machine
from bp_functions import add_passive_provider
from bp_functions import add_filter_inserter
from bp_functions import add_inserter
from bp_functions import new_connection
from bp_functions import new_circuit_condition
from bp_functions import get_stack_size
from bp_functions import add_logistic_chest_requester
from bp_functions import update_request_filters
from bp_functions import add_entity
import json
import math
from fractions import Fraction

crafting_categories = {
    "pressing": ("assembling-machine-2", 0.75),
    "crafting-with-fluid-or-metallurgy": ("assembling-machine-2", 0.75),
    "metallurgy-or-assembling": ("assembling-machine-2", 0.75),
    "parameters": ("assembling-machine-2", 0.75),
    "organic-or-hand-crafting": ("assembling-machine-2", 0.75),
    "organic-or-assembling": ("assembling-machine-2", 0.75),
    # "organic-or-chemistry": ("chemical-plant", 1),
    "crafting": ("assembling-machine-2", 0.75),
    "basic-crafting": ("assembling-machine-2", 0.75),
    "advanced-crafting": ("assembling-machine-2", 0.75),
    "electronics": ("assembling-machine-2", 0.75),
    "crafting-with-fluid": ("assembling-machine-2", 0.75),
    "electronics-with-fluid": ("assembling-machine-2", 0.75),
    "electronics-or-assembling": ("assembling-machine-2", 0.75),
    "cryogenics-or-assembling": ("assembling-machine-2", 0.75),
    # "chemistry": ("chemical-plant", 1),
    # "chemistry-or-cryogenics": ("chemical-plant", 1),
    # "centrifuging": ("centrifuge", 1),
}
crafting_categories_keys = crafting_categories.keys()

recipes_for_mall = {
    "accumulator": 0,
    "active-provider-chest": 1,
    "advanced-circuit": 2,
    "agricultural-tower": 3,
    "arithmetic-combinator": 4,
    "artificial-jellynut-soil": 5,
    "artificial-yumako-soil": 6,
    "artillery-shell": 7,
    "artillery-turret": 8,
    "artillery-wagon": 9,
    "assembling-machine-1": 10,
    "assembling-machine-2": 11,
    "assembling-machine-3": 12,
    "asteroid-collector": 13,
    "atomic-bomb": 14,
    "automation-science-pack": 15,
    "barrel": 16,
    "battery-equipment": 17,
    "battery-mk2-equipment": 18,
    "battery-mk3-equipment": 19,
    "beacon": 20,
    "belt-immunity-equipment": 21,
    "big-electric-pole": 22,
    "biochamber": 23,
    "biolab": 24,
    "boiler": 25,
    "buffer-chest": 26,
    "bulk-inserter": 27,
    "burner-inserter": 28,
    "burner-mining-drill": 29,
    "cannon-shell": 30,
    "capture-robot-rocket": 31,
    "car": 32,
    "cargo-bay": 33,
    "cargo-landing-pad": 34,
    "cargo-wagon": 35,
    "centrifuge": 36,
    "chemical-plant": 37,
    "chemical-science-pack": 38,
    "cliff-explosives": 39,
    "cluster-grenade": 40,
    "combat-shotgun": 41,
    "concrete": 42,
    "constant-combinator": 43,
    "construction-robot": 44,
    "copper-cable": 45,
    "crude-oil-barrel": 46,
    "crusher": 47,
    "cryogenic-plant": 48,
    "decider-combinator": 49,
    "defender-capsule": 50,
    "destroyer-capsule": 51,
    "discharge-defense-equipment": 52,
    "display-panel": 53,
    "distractor-capsule": 54,
    "efficiency-module": 55,
    "efficiency-module-2": 56,
    "efficiency-module-3": 57,
    "electric-engine-unit": 58,
    "electric-furnace": 59,
    "electric-mining-drill": 60,
    "electromagnetic-plant": 61,
    "electronic-circuit": 62,
    "energy-shield-equipment": 63,
    "energy-shield-mk2-equipment": 64,
    "engine-unit": 65,
    "exoskeleton-equipment": 66,
    "explosive-cannon-shell": 67,
    "explosive-rocket": 68,
    "explosive-uranium-cannon-shell": 69,
    "express-loader": 70,
    "express-splitter": 71,
    "express-transport-belt": 72,
    "express-underground-belt": 73,
    "fast-inserter": 74,
    "fast-loader": 75,
    "fast-splitter": 76,
    "fast-transport-belt": 77,
    "fast-underground-belt": 78,
    "firearm-magazine": 79,
    "fission-reactor-equipment": 80,
    "flamethrower": 81,
    "flamethrower-turret": 82,
    "fluid-wagon": 83,
    "fluoroketone-cold-barrel": 84,
    "fluoroketone-hot-barrel": 85,
    "flying-robot-frame": 86,
    "foundation": 87,
    "foundry": 88,
    "fusion-reactor-equipment": 89,
    "gate": 90,
    "grenade": 91,
    "gun-turret": 92,
    "hazard-concrete": 93,
    "heat-exchanger": 94,
    "heat-interface": 95,
    "heat-pipe": 96,
    "heating-tower": 97,
    "heavy-armor": 98,
    "heavy-oil-barrel": 99,
    "holmium-plate": 100,
    "ice-platform": 101,
    "infinity-chest": 102,
    "infinity-pipe": 103,
    "inserter": 104,
    "iron-chest": 105,
    "iron-gear-wheel": 106,
    "iron-stick": 107,
    "lab": 108,
    "land-mine": 109,
    "landfill": 110,
    "laser-turret": 111,
    "light-armor": 112,
    "light-oil-barrel": 113,
    "lightning-rod": 114,
    "loader": 115,
    "locomotive": 116,
    "logistic-robot": 117,
    "logistic-science-pack": 118,
    "long-handed-inserter": 119,
    "low-density-structure": 120,
    "lubricant-barrel": 121,
    "mech-armor": 122,
    "medium-electric-pole": 123,
    "military-science-pack": 124,
    "modular-armor": 125,
    "night-vision-equipment": 126,
    "nuclear-reactor": 127,
    "nutrients-from-biter-egg": 128,
    "nutrients-from-fish": 129,
    "nutrients-from-spoilage": 130,
    "offshore-pump": 131,
    "oil-refinery": 132,
    "overgrowth-jellynut-soil": 133,
    "overgrowth-yumako-soil": 134,
    "passive-provider-chest": 135,
    "personal-laser-defense-equipment": 136,
    "personal-roboport-equipment": 137,
    "personal-roboport-mk2-equipment": 138,
    "petroleum-gas-barrel": 139,
    "piercing-rounds-magazine": 140,
    "piercing-shotgun-shell": 141,
    "pipe": 142,
    "pipe-to-ground": 143,
    "pistol": 144,
    "poison-capsule": 145,
    "power-armor": 146,
    "power-armor-mk2": 147,
    "power-switch": 148,
    "processing-unit": 149,
    "production-science-pack": 150,
    "productivity-module": 151,
    "productivity-module-2": 152,
    "productivity-module-3": 153,
    "programmable-speaker": 154,
    "pump": 155,
    "pumpjack": 156,
    "quality-module": 157,
    "quality-module-2": 158,
    "quality-module-3": 159,
    "radar": 160,
    "rail": 161,
    "rail-chain-signal": 162,
    "rail-ramp": 163,
    "rail-signal": 164,
    "rail-support": 165,
    "railgun-ammo": 166,
    "recycler": 167,
    "refined-concrete": 168,
    "refined-hazard-concrete": 169,
    "repair-pack": 170,
    "requester-chest": 171,
    "roboport": 172,
    "rocket": 173,
    "rocket-fuel": 174,
    "rocket-launcher": 175,
    "rocket-silo": 176,
    "rocket-turret": 177,
    "selector-combinator": 178,
    "shotgun": 179,
    "shotgun-shell": 180,
    "slowdown-capsule": 181,
    "small-electric-pole": 182,
    "small-lamp": 183,
    "solar-panel": 184,
    "solar-panel-equipment": 185,
    "space-platform-foundation": 186,
    "space-platform-starter-pack": 187,
    "space-science-pack": 188,
    "speed-module": 189,
    "speed-module-2": 190,
    "speed-module-3": 191,
    "spidertron": 192,
    "splitter": 193,
    "stack-inserter": 194,
    "steam-engine": 195,
    "steam-turbine": 196,
    "steel-chest": 197,
    "steel-furnace": 198,
    "stone-furnace": 199,
    "stone-wall": 200,
    "storage-chest": 201,
    "storage-tank": 202,
    "submachine-gun": 203,
    "substation": 204,
    "sulfuric-acid-barrel": 205,
    "tank": 206,
    "thruster": 207,
    "toolbelt-equipment": 208,
    "train-stop": 209,
    "transport-belt": 210,
    "tungsten-carbide": 211,
    "turbo-loader": 212,
    "underground-belt": 213,
    "uranium-cannon-shell": 214,
    "uranium-fuel-cell": 215,
    "uranium-rounds-magazine": 216,
    "utility-science-pack": 217,
    "water-barrel": 218,
    "wood-processing": 219,
    "wooden-chest": 220,
}


# ====================================
def get_amount(amount, name):
    # global items
    full_stack = True
    if full_stack:
        return math.ceil(get_stack_size(name, recipes, items) / 4 / 2) * 4
    else:
        return math.ceil(amount / 4) * 4


# ====================================
def merge_and_convert_to_dict(ingredients1, ingredients2=None):
    def add_to_dict(d1, d2):
        if d2 is not None:
            for k, v in d2.items():
                if k in items:
                    if k in d1:
                        d1[k] += v
                    else:
                        d1[k] = v

    temp = {}
    add_to_dict(temp, ingredients1)
    add_to_dict(temp, ingredients2)

    return temp


# ====================================
def get_machine_name(recipe):
    if recipe:
        machine_name = crafting_categories[recipes[recipe]["category"]][0]
    else:
        machine_name = "assembling-machine-2"
    return machine_name


# ====================================
def add_assembly_machine(
    bp, x0, y0, recipe1, recipe2, recipe3, recipe4, recipes, items
):
    ingredients1 = get_iningredients(recipe1, recipes, items)
    ingredients2 = get_iningredients(recipe2, recipes, items)
    ingredients3 = get_iningredients(recipe3, recipes, items)
    ingredients4 = get_iningredients(recipe4, recipes, items)

    # assembly + passive_provider
    add_machine(bp, get_machine_name(recipe1), x0 + 1.5, y0 + 1.5, recipe1)
    add_machine(bp, get_machine_name(recipe2), x0 + 4.5, y0 + 1.5, recipe2)
    add_machine(bp, get_machine_name(recipe3), x0 + 1.5, y0 + 7.5, recipe3)
    add_machine(bp, get_machine_name(recipe4), x0 + 4.5, y0 + 7.5, recipe4)

    requesters = []
    passive_provider = add_passive_provider(bp, x0 + 2.5, y0 + 4.5)
    constant = get_stack_size(recipe1, recipes, items)
    cs = new_circuit_condition(recipe1, recipes, constant, "<")
    c = new_connection(passive_provider.read_entity_number())
    add_filter_inserter(
        bp, "filter-inserter", x0 + 2.5, y0 + 3.5, 1, recipe1, recipes, cs, c
    )
    add_inserter(bp, "fast-inserter", x0 + 1.5, y0 + 3.5, 4)
    constant = get_stack_size(recipe3, recipes, items)
    cs = new_circuit_condition(recipe3, recipes, constant, "<")
    c = new_connection(passive_provider.read_entity_number())
    add_filter_inserter(
        bp, "filter-inserter", x0 + 2.5, y0 + 5.5, 4, recipe3, recipes, cs, c
    )
    add_inserter(bp, "fast-inserter", x0 + 1.5, y0 + 5.5, 1)
    requesters.append(add_logistic_chest_requester(bp, x0 + 1.5, y0 + 4.5))
    pole1 = add_entity(bp, "small-electric-pole", x0 + 0.5, y0 + 4.5)

    passive_provider = add_passive_provider(bp, x0 + 3.5, y0 + 4.5)
    constant = get_stack_size(recipe2, recipes, items)
    cs = new_circuit_condition(recipe2, recipes, constant, "<")
    c = new_connection(passive_provider.read_entity_number())
    add_filter_inserter(
        bp, "filter-inserter", x0 + 3.5, y0 + 3.5, 1, recipe2, recipes, cs, c
    )
    add_inserter(bp, "fast-inserter", x0 + 4.5, y0 + 3.5, 4)
    constant = get_stack_size(recipe4, recipes, items)
    cs = new_circuit_condition(recipe4, recipes, constant, "<")
    c = new_connection(passive_provider.read_entity_number())
    add_filter_inserter(
        bp, "filter-inserter", x0 + 3.5, y0 + 5.5, 4, recipe4, recipes, cs, c
    )
    add_inserter(bp, "fast-inserter", x0 + 4.5, y0 + 5.5, 1)
    requesters.append(add_logistic_chest_requester(bp, x0 + 4.5, y0 + 4.5))
    pole2 = add_entity(bp, "small-electric-pole", x0 + 5.5, y0 + 4.5)
    pole1.set("neighbours", [pole2.read_entity_number()])
    pole2.set("neighbours", [pole1.read_entity_number()])

    ingredients = merge_and_convert_to_dict(ingredients1, ingredients3)
    update_request_filters(requesters[0], ingredients, get_amount)

    ingredients = merge_and_convert_to_dict(ingredients2, ingredients4)
    update_request_filters(requesters[1], ingredients, get_amount)


# ====================================
def get_bp(bp, recipes_for_bp, recipes, items):
    all_recipe = list(recipes_for_bp)
    x = y = count = 0
    while True:

        def get_recipe():
            if all_recipe:
                r = all_recipe.pop()
                return r
            else:
                return ""

        r1 = get_recipe()
        r2 = get_recipe()
        r3 = get_recipe()
        r4 = get_recipe()

        if r1 == "" and r2 == "" and r3 == "" and r4 == "":
            break

        add_assembly_machine(bp, x, y, r1, r2, r3, r4, recipes, items)
        count += 1
        x += 7
        if count % 10 == 0:
            x = 0
            y += 10


# ====================================
def add_assembly_machine_ver2(bp, x0, y0, recipe1, recipes, items):
    ingredients1 = get_iningredients(recipe1, recipes, items)

    # assembly + passive_provider
    add_machine(bp, get_machine_name(recipe1), x0 + 1.5, y0 + 1.5, recipe1)
    # "recipe_quality": "normal"

    requesters = []
    passive_provider = add_passive_provider(bp, x0 + 2.5, y0 + 4.5)
    constant = get_stack_size(recipe1, recipes, items)
    cs = new_circuit_condition(recipe1, recipes, constant, "<")
    c = new_connection(passive_provider.read_entity_number())
    add_filter_inserter(
        bp, "filter-inserter", x0 + 2.5, y0 + 3.5, 1, recipe1, recipes, cs, c
    )
    add_inserter(bp, "fast-inserter", x0 + 1.5, y0 + 3.5, 4)
    requesters.append(add_logistic_chest_requester(bp, x0 + 1.5, y0 + 4.5))

    ingredients = merge_and_convert_to_dict(ingredients1)
    update_request_filters(requesters[0], ingredients, get_amount)


# ====================================
def get_bp_one_machine(book, recipes_for_bp, recipes, items):
    all_recipe = list(recipes_for_bp)
    x = y = count = 0
    for r1 in recipes_for_bp:
        bp = blueprint.new_blueprint()
        add_assembly_machine_ver2(bp, x, y, r1, recipes, items)
        icon_name = recipes[r1]["product"]
        icon_type = "item" if icon_name in items else "fluid"
        bp.set_icons(1, icon_type, icon_name)
        bp.set_label(str(recipes_for_mall[r1]))
        book.append_bp(bp)
        count += 1
        x += 4
        if count % 10 == 0:
            x = 0
            y += 7


def get_machine_recipes_with_one_product_SA(name_of_the_json_file):
    # read json file
    with open(name_of_the_json_file, "r", encoding="utf8") as read_file:
        json_all = json.load(read_file)

    recipes = dict()
    names = []
    for recipe in (
        r for r in json_all["recipes"] if r["category"] in crafting_categories_keys
    ):
        names.append(recipe["name"])
        if len(recipe["products"]) == 1:
            for ingredient in recipe["ingredients"]:
                ingredient["amount"] = Fraction(
                    ingredient["amount"], recipe["products"][0]["amount"]
                )
            recipes[recipe["name"]] = {
                "ingredients": recipe["ingredients"],
                "product": recipe["products"][0]["name"],
                "category": recipe["category"],
                "energy": recipe["energy"] / recipe["products"][0]["amount"],
            }
            n1 = recipe["name"]
            n2 = recipe["products"][0]["name"]
            if n1 != n2:
                print()
                print("ATTENTION")
                print(f"recipe '{n1}' -> product '{n2}'")

    print()
    print("len(names) = {} - len(recipes) = {}".format(len(names), len(recipes)))
    print("ATTENTION: these recipes are ignored")
    diff = set(names) - set(recipes.keys())
    print(diff)
    print("len(diff) = {}".format(len(diff)))
    print()

    return recipes


######################################
#
# main
if __name__ == "__main__":
    # recipes_for_mall = get_machine_recipes_with_one_product_SA(
    #     "Factorio 2.0 SA Vanilla.json"
    # )
    # print("######################################")
    # for n, r in enumerate(sorted(recipes_for_mall.keys())):
    #     print("'{}': {},".format(r, n))
    # print("######################################")

    recipes = get_recipes_with_one_product("Factorio 2.0 SA Vanilla.json")
    items = get_items("Factorio 2.0 SA Vanilla.json")

    print("######################################")
    print(recipes["stack-inserter"])
    print("######################################")

    print(v1_1_110)

    bp = blueprint.new_blueprint(version=v1_1_110)
    get_bp(bp, recipes_for_mall, recipes, items)
    label = "mall"
    filename = "bp-out-vanilla-2.0-SA-mall_1.ignore"
    bp.set_label_color(1, 0, 1)
    bp.set_label(label)
    print()
    print(label)
    print("==================================")
    print(f"to file: {filename}")
    bp.to_file(filename)
    # print(bp.to_str())
    print("==================================")

    book = blueprint.new_blueprint_book(version=v1_1_110)
    get_bp_one_machine(book, recipes_for_mall, recipes, items)
    label = "mall-1"
    filename = "bp-out-vanilla-2.0-SA-mall_2.ignore"
    book.set_label_color(1, 0, 1)
    book.set_label(label)
    print()
    print(label)
    print("==================================")
    print(f"to file: {filename}")
    book.to_file(filename)
    # print(book.to_str())
    print("==================================")
