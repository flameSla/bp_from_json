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
