from bp_from_json import blueprint
from bp_from_json import get_machine_recipes_with_one_product
from bp_from_json import get_recipes_with_one_product
from bp_from_json import get_items
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
from bp_functions import add_constant_combinator
from bp_functions import add_filtr_constant_combinator
import math


# ====================================
recipes_for_constant_combinators = (
    "accumulator",
    "advanced-circuit",
    "arithmetic-combinator",
    "artillery-shell",
    "artillery-targeting-remote",
    "artillery-turret",
    "artillery-wagon",
    "assembling-machine-1",
    "assembling-machine-2",
    "assembling-machine-3",
    "atomic-bomb",
    "battery-equipment",
    "battery-mk2-equipment",
    "beacon",
    "belt-immunity-equipment",
    "big-electric-pole",
    "boiler",
    "burner-inserter",
    "burner-mining-drill",
    "cannon-shell",
    "car",
    "cargo-wagon",
    "centrifuge",
    "chemical-plant",
    "cliff-explosives",
    "cluster-grenade",
    "combat-shotgun",
    "concrete",
    "constant-combinator",
    "construction-robot",
    "copper-cable",
    "decider-combinator",
    "defender-capsule",
    "destroyer-capsule",
    "discharge-defense-equipment",
    "discharge-defense-remote",
    "distractor-capsule",
    "effectivity-module",
    "effectivity-module-2",
    "effectivity-module-3",
    "electric-engine-unit",
    "electric-furnace",
    "electric-mining-drill",
    "electronic-circuit",
    "empty-barrel",
    "empty-crude-oil-barrel",
    "energy-shield-equipment",
    "energy-shield-mk2-equipment",
    "engine-unit",
    "exoskeleton-equipment",
    "explosive-cannon-shell",
    "explosive-rocket",
    "explosive-uranium-cannon-shell",
    "express-splitter",
    "express-transport-belt",
    "express-underground-belt",
    "fast-inserter",
    "fast-splitter",
    "fast-transport-belt",
    "fast-underground-belt",
    "fill-crude-oil-barrel",
    "fill-heavy-oil-barrel",
    "fill-light-oil-barrel",
    "fill-lubricant-barrel",
    "fill-petroleum-gas-barrel",
    "fill-sulfuric-acid-barrel",
    "fill-water-barrel",
    "filter-inserter",
    "firearm-magazine",
    "flamethrower",
    "flamethrower-turret",
    "fluid-wagon",
    "flying-robot-frame",
    "fusion-reactor-equipment",
    "gate",
    "green-wire",
    "grenade",
    "gun-turret",
    "hazard-concrete",
    "heat-exchanger",
    "heat-pipe",
    "inserter",
    "iron-chest",
    "iron-gear-wheel",
    "iron-stick",
    "lab",
    "land-mine",
    "landfill",
    "laser-turret",
    "locomotive",
    "logistic-chest-active-provider",
    "logistic-chest-buffer",
    "logistic-chest-passive-provider",
    "logistic-chest-requester",
    "logistic-chest-storage",
    "logistic-robot",
    "long-handed-inserter",
    "low-density-structure",
    "medium-electric-pole",
    "night-vision-equipment",
    "nuclear-reactor",
    "offshore-pump",
    "oil-refinery",
    "personal-laser-defense-equipment",
    "personal-roboport-equipment",
    "personal-roboport-mk2-equipment",
    "piercing-rounds-magazine",
    "piercing-shotgun-shell",
    "pipe",
    "pipe-to-ground",
    "pistol",
    "poison-capsule",
    "power-armor-mk2",
    "power-switch",
    "processing-unit",
    "productivity-module",
    "productivity-module-2",
    "productivity-module-3",
    "programmable-speaker",
    "pump",
    "pumpjack",
    "radar",
    "rail",
    "rail-chain-signal",
    "rail-signal",
    "red-wire",
    "refined-concrete",
    "refined-hazard-concrete",
    "repair-pack",
    "roboport",
    "rocket",
    "rocket-control-unit",
    "rocket-fuel",
    "rocket-launcher",
    "rocket-silo",
    "shotgun",
    "shotgun-shell",
    "slowdown-capsule",
    "small-electric-pole",
    "small-lamp",
    "solar-panel",
    "solar-panel-equipment",
    "speed-module",
    "speed-module-2",
    "speed-module-3",
    "spidertron",
    "spidertron-remote",
    "splitter",
    "stack-filter-inserter",
    "stack-inserter",
    "steam-engine",
    "steam-turbine",
    "steel-chest",
    "steel-furnace",
    "stone-furnace",
    "stone-wall",
    "storage-tank",
    "submachine-gun",
    "substation",
    "tank",
    "train-stop",
    "transport-belt",
    "underground-belt",
    "uranium-cannon-shell",
    "uranium-fuel-cell",
    "uranium-rounds-magazine",
    "wooden-chest",
)


items_for_constant_combinators = {
    "accumulator": 50,
    "arithmetic-combinator": 50,
    "artillery-shell": 4,
    "artillery-targeting-remote": 1,
    "artillery-turret": 10,
    "artillery-wagon": 5,
    "assembling-machine-1": 50,
    "assembling-machine-2": 50,
    "assembling-machine-3": 50,
    "atomic-bomb": 10,
    "battery-equipment": 20,
    "battery-mk2-equipment": 20,
    "beacon": 40,
    "belt-immunity-equipment": 20,
    "big-electric-pole": 50,
    "boiler": 50,
    "burner-inserter": 50,
    "burner-mining-drill": 50,
    "cannon-shell": 200,
    "car": 1,
    "cargo-wagon": 5,
    "centrifuge": 50,
    "chemical-plant": 10,
    "cliff-explosives": 20,
    "cluster-grenade": 100,
    "combat-shotgun": 5,
    "concrete": 200,
    "constant-combinator": 50,
    "construction-robot": 50,
    "decider-combinator": 50,
    "defender-capsule": 100,
    "destroyer-capsule": 100,
    "discharge-defense-equipment": 20,
    "discharge-defense-remote": 1,
    "distractor-capsule": 100,
    "electric-furnace": 50,
    "electric-mining-drill": 50,
    "empty-barrel": 10,
    "energy-shield-equipment": 20,
    "energy-shield-mk2-equipment": 20,
    "exoskeleton-equipment": 20,
    "explosive-cannon-shell": 1400,
    "explosive-rocket": 1000,
    "explosive-uranium-cannon-shell": 200,
    "fast-inserter": 50,
    "filter-inserter": 50,
    "firearm-magazine": 200,
    "flamethrower": 5,
    "flamethrower-ammo": 100,
    "flamethrower-turret": 100,
    "fluid-wagon": 10,
    "fusion-reactor-equipment": 20,
    "gate": 50,
    "green-wire": 200,
    "grenade": 100,
    "gun-turret": 100,
    "hazard-concrete": 100,
    "heat-exchanger": 50,
    "heat-pipe": 50,
    "inserter": 50,
    "iron-chest": 50,
    "lab": 10,
    "land-mine": 100,
    "laser-turret": 200,
    "locomotive": 5,
    "logistic-chest-active-provider": 50,
    "logistic-chest-buffer": 50,
    "logistic-chest-passive-provider": 50,
    "logistic-chest-requester": 50,
    "logistic-chest-storage": 50,
    "logistic-robot": 50,
    "long-handed-inserter": 50,
    "medium-electric-pole": 50,
    "night-vision-equipment": 20,
    "nuclear-reactor": 10,
    "offshore-pump": 20,
    "oil-refinery": 10,
    "personal-laser-defense-equipment": 20,
    "personal-roboport-equipment": 20,
    "personal-roboport-mk2-equipment": 20,
    "piercing-rounds-magazine": 200,
    "piercing-shotgun-shell": 200,
    "pipe": 200,
    "pipe-to-ground": 50,
    "pistol": 5,
    "poison-capsule": 100,
    "power-armor-mk2": 1,
    "power-switch": 50,
    "programmable-speaker": 50,
    "pump": 50,
    "pumpjack": 20,
    "radar": 50,
    "rail": 200,
    "rail-chain-signal": 50,
    "rail-signal": 50,
    "red-wire": 200,
    "refined-concrete": 100,
    "refined-hazard-concrete": 100,
    "repair-pack": 100,
    "rocket": 1800,
    "rocket-launcher": 5,
    "rocket-silo": 1,
    "shotgun": 5,
    "shotgun-shell": 200,
    "slowdown-capsule": 100,
    "small-electric-pole": 50,
    "small-lamp": 50,
    "solar-panel": 50,
    "solar-panel-equipment": 20,
    "spidertron": 1,
    "spidertron-remote": 1,
    "stack-filter-inserter": 50,
    "stack-inserter": 50,
    "steam-engine": 10,
    "steam-turbine": 10,
    "steel-chest": 50,
    "steel-furnace": 50,
    "stone-furnace": 50,
    "stone-wall": 100,
    "storage-tank": 50,
    "submachine-gun": 5,
    "substation": 50,
    "tank": 1,
    "train-stop": 10,
    "uranium-cannon-shell": 200,
    "uranium-rounds-magazine": 1800,
    "wooden-chest": 50,
    # ====================================
    "copper-cable": x,
    "electric-engine-unit": x,
    "electronic-circuit": x,
    "empty-crude-oil-barrel": x,
    "engine-unit": x,
    "express-splitter": x,
    "express-transport-belt": x,
    "express-underground-belt": x,
    "fast-splitter": x,
    "fast-transport-belt": x,
    "fast-underground-belt": x,
    "flying-robot-frame": x,
    "iron-gear-wheel": x,
    "iron-stick": x,
    "landfill": x,
    "low-density-structure": x,
    "roboport": x,
    "rocket-control-unit": x,
    "rocket-fuel": x,
    "splitter": x,
    "transport-belt": x,
    "underground-belt": x,
    "uranium-fuel-cell": x,
}


# ====================================
def get_bp(bp, recipes_for_constant_combinators, recipes):
    x = y = 0.5
    count = 0
    for r1 in recipes_for_constant_combinators:
        if r1 in recipes:
            constant_combinator = add_constant_combinator(bp, x, y)
            add_filtr_constant_combinator(
                constant_combinator, "item", recipes[r1]["product"], 1
            )

        count += 1
        x += 2
        if count % 10 == 0:
            x = 0
            y += 2


######################################
#
# main
if __name__ == "__main__":
    recipes = get_recipes_with_one_product("Factorio 1.1 Vanilla.json")

    # print()
    # print("==================")
    # print("recipes_for_constant_combinators")
    # print()
    # print(recipes_for_constant_combinators)

    bp = blueprint.new_blueprint()
    get_bp(bp, sorted(recipes_for_constant_combinators), recipes)
    label = "constant_combinators"
    filename = "bp-out-vanilla-constant-combinators.ignore"
    bp.set_label_color(1, 0, 1)
    bp.set_label(label)
    print()
    print(label)
    print("==================================")
    print(f"to file: {filename}")
    bp.to_file(filename)
    print(bp.to_str())
    print("==================================")

    print()
    print("==================")
    print("mall7.3 complete.txt.ignore")
    print()
    # get all recipes for the mall
    bp = blueprint.from_file("mall7.3 complete.txt.ignore")
    new_recipes = {}
    entities = bp.get_entities()
    print("######################################")
    for e in entities:
        if e.read_name() in ("stack-filter-inserter", "stack-inserter"):
            if (
                "control_behavior" in e.data
                and "circuit_condition" in e.data["control_behavior"]
            ):
                r = e.data["control_behavior"]["circuit_condition"]["first_signal"].get(
                    "name", None
                )
                constant = e.data["control_behavior"]["circuit_condition"].get(
                    "constant", None
                )
                if r and constant:
                    if r in new_recipes:
                        if new_recipes[r] != constant:
                            print("Warning!")
                            print("\t{}\t{} != {}".format(r, new_recipes[r], constant))
                    else:
                        new_recipes[r] = constant

    for k in sorted(new_recipes.keys()):
        print("'{}': {}, ".format(k, new_recipes[k]))
    print("######################################")

    print()
    print("==================")
    print("не вошли в фильтрующие инсертеры")
    print()
    s1 = set(recipes_for_constant_combinators) - set(new_recipes.keys())
    for r in sorted(s1):
        print("'{}': {}, ".format(r, "x"))

    # .data["control_behavior"]["circuit_condition"]

    # "control_behavior"
    # return {
    #         "circuit_condition": {
    #             "first_signal": {"type": "item", "name": r},
    #             "constant": constant,
    #             "comparator": comparator,
    #         }
    #     }
