import math
import json
import sys
import itertools
from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import entity
from fractions import Fraction

full_stack = True

recipes_for_mall = (
    "accumulator",
    "air-pump",
    "air-pump-2",
    "air-pump-3",
    "air-pump-4",
    "antron",
    "arithmetic-combinator",
    "artillery-targeting-remote",
    "artillery-turret",
    "artillery-wagon",
    "assembling-machine-1",
    "assembling-machine-2",
    "assembling-machine-3",
    "assembling-machine-4",
    "assembling-machine-5",
    "assembling-machine-6",
    "basic-splitter",
    "basic-transport-belt",
    "basic-underground-belt",
    "battery-equipment",
    "battery-mk2-equipment",
    "battery-mk3-equipment",
    "battery-mk4-equipment",
    "battery-mk5-equipment",
    "battery-mk6-equipment",
    "beacon",
    "beacon-2",
    "beacon-3",
    "belt-immunity-equipment",
    "big-electric-pole",
    "big-electric-pole-2",
    "big-electric-pole-3",
    "big-electric-pole-4",
    "bob-area-mining-drill-1",
    "bob-area-mining-drill-2",
    "bob-area-mining-drill-3",
    "bob-area-mining-drill-4",
    "bob-armoured-cargo-wagon",
    "bob-armoured-cargo-wagon-2",
    "bob-armoured-fluid-wagon",
    "bob-armoured-fluid-wagon-2",
    "bob-armoured-locomotive",
    "bob-armoured-locomotive-2",
    "bob-artillery-turret-2",
    "bob-artillery-turret-3",
    "bob-artillery-wagon-2",
    "bob-artillery-wagon-3",
    "bob-burner-generator",
    "bob-cargo-wagon-2",
    "bob-cargo-wagon-3",
    "bob-character-balanced-2",
    "bob-character-builder",
    "bob-character-builder-2",
    "bob-character-engineer",
    "bob-character-fighter",
    "bob-character-fighter-2",
    "bob-character-miner",
    "bob-character-miner-2",
    "bob-character-prospector",
    "bob-distillery",
    "bob-distillery-2",
    "bob-distillery-3",
    "bob-distillery-4",
    "bob-distillery-5",
    "bob-fluid-wagon-2",
    "bob-fluid-wagon-3",
    "bob-greenhouse",
    "bob-gun-turret-2",
    "bob-gun-turret-3",
    "bob-gun-turret-4",
    "bob-gun-turret-5",
    "bob-laser-turret-2",
    "bob-laser-turret-3",
    "bob-laser-turret-4",
    "bob-laser-turret-5",
    "bob-locomotive-2",
    "bob-locomotive-3",
    "bob-logistic-zone-expander",
    "bob-logistic-zone-expander-2",
    "bob-logistic-zone-expander-3",
    "bob-logistic-zone-expander-4",
    "bob-logistic-zone-interface",
    "bob-mining-drill-1",
    "bob-mining-drill-2",
    "bob-mining-drill-3",
    "bob-mining-drill-4",
    "bob-overflow-valve",
    "bob-plasma-turret-1",
    "bob-plasma-turret-2",
    "bob-plasma-turret-3",
    "bob-plasma-turret-4",
    "bob-plasma-turret-5",
    "bob-power-armor-mk3",
    "bob-power-armor-mk4",
    "bob-power-armor-mk5",
    "bob-pump-2",
    "bob-pump-3",
    "bob-pump-4",
    "bob-pumpjack-1",
    "bob-pumpjack-2",
    "bob-pumpjack-3",
    "bob-pumpjack-4",
    "bob-robo-charge-port",
    "bob-robo-charge-port-2",
    "bob-robo-charge-port-3",
    "bob-robo-charge-port-4",
    "bob-robo-charge-port-large",
    "bob-robo-charge-port-large-2",
    "bob-robo-charge-port-large-3",
    "bob-robo-charge-port-large-4",
    "bob-robochest",
    "bob-robochest-2",
    "bob-robochest-3",
    "bob-robochest-4",
    "bob-roboport-2",
    "bob-roboport-3",
    "bob-roboport-4",
    "bob-small-inline-storage-tank",
    "bob-small-storage-tank",
    "bob-sniper-turret-1",
    "bob-sniper-turret-2",
    "bob-sniper-turret-3",
    "bob-storage-tank-all-corners",
    "bob-storage-tank-all-corners-2",
    "bob-storage-tank-all-corners-3",
    "bob-storage-tank-all-corners-4",
    "bob-tank-2",
    "bob-tank-3",
    "bob-topup-valve",
    "bob-valve",
    "boiler",
    "boiler-2",
    "boiler-3",
    "boiler-4",
    "boiler-5",
    "brass-chest",
    "brass-pipe",
    "brass-pipe-to-ground",
    "bronze-pipe",
    "bronze-pipe-to-ground",
    "burner-assembling-machine",
    "burner-inserter",
    "burner-mining-drill",
    "burner-reactor",
    "burner-reactor-2",
    "car",
    "cargo-wagon",
    "centrifuge",
    "centrifuge-2",
    "centrifuge-3",
    "ceramic-pipe",
    "ceramic-pipe-to-ground",
    "character",
    "chemical-plant",
    "chemical-plant-2",
    "chemical-plant-3",
    "chemical-plant-4",
    "cliff-explosives",
    "cluster-grenade",
    "combat-shotgun",
    "constant-combinator",
    "copper-cable",
    "copper-pipe",
    "copper-pipe-to-ground",
    "copper-tungsten-pipe",
    "copper-tungsten-pipe-to-ground",
    "decider-combinator",
    "electric-chemical-furnace",
    "electric-chemical-mixing-furnace",
    "electric-chemical-mixing-furnace-2",
    "electric-furnace",
    "electric-furnace-2",
    "electric-furnace-3",
    "electric-mining-drill",
    "electric-mixing-furnace",
    "electrolyser",
    "electrolyser-2",
    "electrolyser-3",
    "electrolyser-4",
    "electrolyser-5",
    "electronics-machine-1",
    "electronics-machine-2",
    "electronics-machine-3",
    "empty-barrel",
    "empty-canister",
    "energy-shield-equipment",
    "energy-shield-mk2-equipment",
    "energy-shield-mk3-equipment",
    "energy-shield-mk4-equipment",
    "energy-shield-mk5-equipment",
    "energy-shield-mk6-equipment",
    "exoskeleton-equipment",
    "exoskeleton-equipment-2",
    "exoskeleton-equipment-3",
    "explosive-rocket",
    "express-filter-inserter",
    "express-inserter",
    "express-splitter",
    "express-stack-filter-inserter",
    "express-stack-inserter",
    "express-transport-belt",
    "express-underground-belt",
    "fast-accumulator",
    "fast-accumulator-2",
    "fast-accumulator-3",
    "fast-inserter",
    "fast-splitter",
    "fast-transport-belt",
    "fast-underground-belt",
    "filter-inserter",
    "flamethrower",
    "flamethrower-turret",
    "fluid-chemical-furnace",
    "fluid-furnace",
    "fluid-generator",
    "fluid-generator-2",
    "fluid-generator-3",
    "fluid-mixing-furnace",
    "fluid-reactor-2",
    "fluid-reactor-from-fluid-furnace",
    "fluid-wagon",
    "fusion-reactor-equipment",
    "fusion-reactor-equipment-2",
    "fusion-reactor-equipment-3",
    "fusion-reactor-equipment-4",
    "gas-canister",
    "gate",
    "gilded-copper-cable",
    "green-wire",
    "grenade",
    "gun-turret",
    "hazard-concrete",
    "heat-exchanger",
    "heat-exchanger-2",
    "heat-exchanger-3",
    "heat-exchanger-4",
    "heat-pipe",
    "heat-pipe-2",
    "heat-pipe-3",
    "heat-pipe-4",
    "heavy-armor",
    "heavy-spidertron",
    "hydrazine-generator",
    "inserter",
    "insulated-cable",
    "iron-chest",
    "iron-stick",
    "lab",
    "lab-2",
    "lab-alien",
    "lab-module",
    "land-mine",
    "landfill",
    "large-accumulator-2",
    "large-accumulator-3",
    "laser-turret",
    "light-armor",
    "locomotive",
    "logistic-chest-active-provider",
    "logistic-chest-active-provider-2",
    "logistic-chest-active-provider-3",
    "logistic-chest-buffer",
    "logistic-chest-buffer-2",
    "logistic-chest-buffer-3",
    "logistic-chest-passive-provider",
    "logistic-chest-passive-provider-2",
    "logistic-chest-passive-provider-3",
    "logistic-chest-requester",
    "logistic-chest-requester-2",
    "logistic-chest-requester-3",
    "logistic-chest-storage",
    "logistic-chest-storage-2",
    "logistic-chest-storage-3",
    "logistic-spidertron",
    "long-handed-inserter",
    "mech-armor-plate",
    "mech-brain",
    "mech-foot",
    "mech-frame",
    "mech-hip",
    "mech-knee",
    "mech-leg",
    "mech-leg-segment",
    "medium-electric-pole",
    "medium-electric-pole-2",
    "medium-electric-pole-3",
    "medium-electric-pole-4",
    "modular-armor",
    "night-vision-equipment",
    "night-vision-equipment-2",
    "night-vision-equipment-3",
    "nitinol-pipe",
    "nitinol-pipe-to-ground",
    "nuclear-reactor",
    "nuclear-reactor-2",
    "nuclear-reactor-3",
    "offshore-pump",
    "oil-boiler",
    "oil-boiler-2",
    "oil-boiler-3",
    "oil-boiler-4",
    "oil-refinery",
    "oil-refinery-2",
    "oil-refinery-3",
    "oil-refinery-4",
    "personal-laser-defense-equipment",
    "personal-laser-defense-equipment-2",
    "personal-laser-defense-equipment-3",
    "personal-laser-defense-equipment-4",
    "personal-laser-defense-equipment-5",
    "personal-laser-defense-equipment-6",
    "personal-roboport-antenna-equipment",
    "personal-roboport-antenna-equipment-2",
    "personal-roboport-antenna-equipment-3",
    "personal-roboport-antenna-equipment-4",
    "personal-roboport-chargepad-equipment",
    "personal-roboport-chargepad-equipment-2",
    "personal-roboport-chargepad-equipment-3",
    "personal-roboport-chargepad-equipment-4",
    "personal-roboport-equipment",
    "personal-roboport-mk2-equipment",
    "personal-roboport-mk3-equipment",
    "personal-roboport-mk4-equipment",
    "personal-roboport-robot-equipment",
    "personal-roboport-robot-equipment-2",
    "personal-roboport-robot-equipment-3",
    "personal-roboport-robot-equipment-4",
    "piercing-shotgun-shell",
    "pipe",
    "pipe-to-ground",
    "plastic-pipe",
    "plastic-pipe-to-ground",
    "player-boots",
    "player-boots-2",
    "player-brain",
    "player-brain-2",
    "player-frame",
    "player-frame-2",
    "player-gloves",
    "player-gloves-2",
    "player-head",
    "player-head-2",
    "player-power-core",
    "poison-capsule",
    "power-armor",
    "power-armor-mk2",
    "power-switch",
    "programmable-speaker",
    "pump",
    "pumpjack",
    "radar",
    "radar-2",
    "radar-3",
    "radar-4",
    "radar-5",
    "rail",
    "rail-chain-signal",
    "rail-signal",
    "red-filter-inserter",
    "red-stack-filter-inserter",
    "red-stack-inserter",
    "red-wire",
    "refined-concrete",
    "refined-hazard-concrete",
    "reinforced-gate",
    "reinforced-wall",
    "repair-pack",
    "repair-pack-2",
    "repair-pack-3",
    "repair-pack-4",
    "repair-pack-5",
    "rifle",
    "roboport",
    "roboport-antenna-1",
    "roboport-antenna-2",
    "roboport-antenna-3",
    "roboport-antenna-4",
    "roboport-chargepad-1",
    "roboport-chargepad-2",
    "roboport-chargepad-3",
    "roboport-chargepad-4",
    "roboport-door-1",
    "roboport-door-2",
    "roboport-door-3",
    "roboport-door-4",
    "rocket",
    "rocket-launcher",
    "rocket-silo",
    "shotgun",
    "shotgun-shell",
    "slow-accumulator",
    "slow-accumulator-2",
    "slow-accumulator-3",
    "small-electric-pole",
    "small-lamp",
    "sniper-rifle",
    "solar-panel",
    "solar-panel-2",
    "solar-panel-3",
    "solar-panel-equipment",
    "solar-panel-equipment-2",
    "solar-panel-equipment-3",
    "solar-panel-equipment-4",
    "solar-panel-large",
    "solar-panel-large-2",
    "solar-panel-large-3",
    "solar-panel-small",
    "solar-panel-small-2",
    "solar-panel-small-3",
    "spidertron",
    "spidertron-cannon",
    "spidertron-remote",
    "splitter",
    "stack-filter-inserter",
    "stack-inserter",
    "steam-assembling-machine",
    "steam-engine",
    "steam-engine-2",
    "steam-engine-3",
    "steam-engine-4",
    "steam-engine-5",
    "steam-inserter",
    "steam-mining-drill",
    "steam-turbine",
    "steam-turbine-2",
    "steam-turbine-3",
    "steel-chemical-furnace",
    "steel-chest",
    "steel-furnace",
    "steel-mixing-furnace",
    "steel-pipe",
    "steel-pipe-to-ground",
    "stone-chemical-furnace",
    "stone-furnace",
    "stone-mixing-furnace",
    "stone-pipe",
    "stone-pipe-to-ground",
    "stone-wall",
    "storage-tank",
    "storage-tank-2",
    "storage-tank-3",
    "storage-tank-4",
    "submachine-gun",
    "substation",
    "substation-2",
    "substation-3",
    "substation-4",
    "tank",
    "tankotron",
    "tinned-copper-cable",
    "titanium-chest",
    "titanium-pipe",
    "titanium-pipe-to-ground",
    "train-stop",
    "transport-belt",
    "tungsten-pipe",
    "tungsten-pipe-to-ground",
    "turbo-filter-inserter",
    "turbo-inserter",
    "turbo-splitter",
    "turbo-stack-filter-inserter",
    "turbo-stack-inserter",
    "turbo-transport-belt",
    "turbo-underground-belt",
    "ultimate-splitter",
    "ultimate-transport-belt",
    "ultimate-underground-belt",
    "underground-belt",
    "vehicle-battery-1",
    "vehicle-battery-2",
    "vehicle-battery-3",
    "vehicle-battery-4",
    "vehicle-battery-5",
    "vehicle-battery-6",
    "vehicle-belt-immunity-equipment",
    "vehicle-big-turret-1",
    "vehicle-big-turret-2",
    "vehicle-big-turret-3",
    "vehicle-big-turret-4",
    "vehicle-big-turret-5",
    "vehicle-big-turret-6",
    "vehicle-engine",
    "vehicle-fusion-cell-1",
    "vehicle-fusion-cell-2",
    "vehicle-fusion-cell-3",
    "vehicle-fusion-cell-4",
    "vehicle-fusion-cell-5",
    "vehicle-fusion-cell-6",
    "vehicle-fusion-reactor-1",
    "vehicle-fusion-reactor-2",
    "vehicle-fusion-reactor-3",
    "vehicle-fusion-reactor-4",
    "vehicle-fusion-reactor-5",
    "vehicle-fusion-reactor-6",
    "vehicle-laser-defense-1",
    "vehicle-laser-defense-2",
    "vehicle-laser-defense-3",
    "vehicle-laser-defense-4",
    "vehicle-laser-defense-5",
    "vehicle-laser-defense-6",
    "vehicle-motor",
    "vehicle-roboport",
    "vehicle-roboport-2",
    "vehicle-roboport-3",
    "vehicle-roboport-4",
    "vehicle-roboport-antenna-equipment",
    "vehicle-roboport-antenna-equipment-2",
    "vehicle-roboport-antenna-equipment-3",
    "vehicle-roboport-antenna-equipment-4",
    "vehicle-roboport-chargepad-equipment",
    "vehicle-roboport-chargepad-equipment-2",
    "vehicle-roboport-chargepad-equipment-3",
    "vehicle-roboport-chargepad-equipment-4",
    "vehicle-roboport-robot-equipment",
    "vehicle-roboport-robot-equipment-2",
    "vehicle-roboport-robot-equipment-3",
    "vehicle-roboport-robot-equipment-4",
    "vehicle-shield-1",
    "vehicle-shield-2",
    "vehicle-shield-3",
    "vehicle-shield-4",
    "vehicle-shield-5",
    "vehicle-shield-6",
    "vehicle-solar-panel-1",
    "vehicle-solar-panel-2",
    "vehicle-solar-panel-3",
    "vehicle-solar-panel-4",
    "vehicle-solar-panel-5",
    "vehicle-solar-panel-6",
    "void-pump",
    "water-miner-1",
    "water-miner-2",
    "water-miner-3",
    "water-miner-4",
    "water-miner-5",
    "water-pump",
    "water-pump-2",
    "water-pump-3",
    "water-pump-4",
    "wooden-chest",
    "yellow-filter-inserter",
)


groups = (
    "ammo",
    "armor",
    "bob-assembly-machine",
    "bob-cargo-wagon",
    "bob-chemical-machine",
    "bob-electrolyser-machine",
    "bob-electronic-components",
    "bob-energy-accumulator",
    "bob-energy-boiler",
    "bob-energy-fluid-generator",
    "bob-energy-heat-exchanger",
    "bob-energy-oil-boiler",
    "bob-energy-solar-panel",
    "bob-energy-steam-engine",
    "bob-fluid-wagon",
    "bob-greenhouse",
    "bob-intermediates",
    "bob-locomotive",
    "bob-logistic-roboport",
    "bob-logistic-roboport-charge",
    "bob-logistic-roboport-chest",
    "bob-logistic-roboport-zone",
    "bob-logistic-tier-0",
    "bob-logistic-tier-1",
    "bob-logistic-tier-2",
    "bob-logistic-tier-3",
    "bob-logistic-tier-4",
    "bob-logistic-tier-5",
    "bob-pump",
    "bob-refinery-machine",
    "bob-roboport-parts-antenna",
    "bob-roboport-parts-charge",
    "bob-roboport-parts-door",
    "bob-smelting-machine",
    "bob-storage-tank",
    "bodies",
    "body-parts",
    "capsule",
    "circuit-network",
    "defensive-structure",
    "energy",
    "energy-pipe-distribution",
    "equipment",
    "extraction-machine",
    "gun",
    "intermediate-product",
    "logistic-chests-2",
    "logistic-chests-3",
    "logistic-network",
    "mech-parts",
    "military-equipment",
    "module-beacon",
    "pipe",
    "pipe-to-ground",
    "production-machine",
    "smelting-machine",
    "space-related",
    "storage",
    "terrain",
    "tool",
    "train-transport",
    "transport",
    "vehicle-equipment",
)


groups2 = (
    ("bob-electronic-components",),
    (
        "bob-roboport-parts-antenna",
        "bob-roboport-parts-charge",
        "bob-roboport-parts-door",
        "bob-logistic-roboport",
        "bob-logistic-roboport-zone",
        "bob-logistic-roboport-charge",
        "bob-logistic-roboport-chest",
    ),
    (
        "storage",
        "logistic-network",
        "logistic-chests-2",
        "logistic-chests-3",
        "bob-storage-tank",
    ),
    (
        "production-machine",
        "bob-greenhouse",
        "extraction-machine",
        "smelting-machine",
        "bob-smelting-machine",
        "bob-assembly-machine",
        "bob-electrolyser-machine",
        "bob-chemical-machine",
        "bob-refinery-machine",
        "module-beacon",
    ),
    (
        "pipe",
        "pipe-to-ground",
        "energy-pipe-distribution",
        "bob-pump",
    ),
    (
        "circuit-network",
        "intermediate-product",
        "bob-intermediates",
        "terrain",
        "tool",
        "space-related",
    ),
    ("defensive-structure",),
    (
        "bodies",
        "body-parts",
        "armor",
        "gun",
        "ammo",
        "capsule",
        "equipment",
        "military-equipment",
    ),
    (
        "transport",
        "train-transport",
        "bob-locomotive",
        "bob-cargo-wagon",
        "bob-fluid-wagon",
        "mech-parts",
        "vehicle-equipment",
    ),
    (
        "bob-logistic-tier-0",
        "bob-logistic-tier-1",
        "bob-logistic-tier-2",
        "bob-logistic-tier-3",
        "bob-logistic-tier-4",
        "bob-logistic-tier-5",
    ),
    (
        "energy",
        "bob-energy-boiler",
        "bob-energy-oil-boiler",
        "bob-energy-heat-exchanger",
        "bob-energy-steam-engine",
        "bob-energy-solar-panel",
        "bob-energy-accumulator",
        "bob-energy-fluid-generator",
    ),
)


# ====================================
par_debugging = False


def debug(*args, end="\n"):
    global par_debugging
    if par_debugging:
        print(*args, end=end, file=sys.stderr, flush=True)


# ====================================
def get_recipes():
    global par_debugging
    # par_debugging = True

    # read json file
    with open("BobMod.json", "r", encoding="utf8") as read_file:
        json_all = json.load(read_file)

    # json -> dist()
    for a in (e for e in json_all["entities"] if "assembling-machine-6" in e["name"]):
        crafting_categories = a["crafting_categories"]

    # for r in json_all["recipes"]:
    #     print("r = ", type(r), r)
    #     raise Exception("Stop")

    recipes = dict()
    names = []
    for recipe in (
        r for r in json_all["recipes"] if r["category"] in crafting_categories
    ):
        names.append(recipe["name"])
        debug(names[-1])
        if len(recipe["products"]) == 1:
            for ingredient in recipe["ingredients"]:
                ingredient["amount"] = Fraction(
                    ingredient["amount"], recipe["products"][0]["amount"]
                )
            recipes[recipe["name"]] = {
                "category": recipe["category"],
                "subgroup": recipe["subgroup"],
                "ingredients": recipe["ingredients"],
                "product": recipe["products"][0]["name"],
            }

    debug("len(names) = {} - len(recipes) = {}".format(len(names), len(recipes)))
    print("ATTENTION: these recipes are ignored")
    diff = set(names) - set(recipes.keys())
    print(diff)
    print("len(diff) = {}".format(len(diff)))
    print()

    return recipes


# ====================================
def get_items():
    # read json file
    with open("BobMod.json", "r", encoding="utf8") as read_file:
        json_all = json.load(read_file)

    # json -> dist()
    items = dict_bp()
    for i in json_all["items"]:
        items[i["name"]] = float(i["stack"])  # items["wooden-chest"] = 50.0

    return items


# ====================================
def add_assembling_machine_2(bp, x, y, recipe, speed):
    assembly = entity.new_entity("assembling-machine-2", x, y)
    if recipe:
        assembly.set("recipe", recipe)
    if speed:
        assembly.update_items({"speed-module-3": 4}, name_verification=False)
    bp.append_entity(assembly)
    return assembly


# ====================================
def get_iningredients(recipe):
    amount = 1
    if recipe:
        ingredients = [
            (i["name"], i["amount"] * amount)
            for i in recipes[recipe]["ingredients"]
            if i["name"] in items
        ]
    else:
        ingredients = []

    return ingredients


# ====================================
def add_passive_provider(bp, x, y, bar=None):
    passive_provider = entity.new_entity("logistic-chest-passive-provider", x, y)
    if bar is not None:
        passive_provider.set("bar", bar)
    bp.append_entity(passive_provider)
    return passive_provider


# ====================================
def add_red_filter_inserter(
    bp, x, y, direction, recipe, circuit_condition=None, connection=None
):
    inserter = entity.new_entity("red-filter-inserter", x, y)
    inserter.set("direction", direction)
    if recipe:
        r = recipes[recipe]["product"]
        f = list()
        f.append({"index": 1, "name": r})
        inserter.set("filters", f)
    if circuit_condition is not None:
        inserter.set("control_behavior", circuit_condition)
    if connection is not None:
        inserter.set("connections", connection)
    bp.append_entity(inserter)
    return inserter


# ====================================
def add_red_inserter(bp, x, y, direction):
    inserter = entity.new_entity("red-inserter", x, y)
    inserter.set("direction", direction)
    bp.append_entity(inserter)
    return inserter


# ====================================
def new_connection(entity_number):
    return {"1": {"red": [{"entity_id": entity_number}]}}


# ====================================
def new_circuit_condition(recipe):
    if recipe:
        r = recipes[recipe]["product"]
        if r != recipe:
            debug(r, recipe)
        return {
            "circuit_condition": {
                "first_signal": {"type": "item", "name": r},
                "constant": items[r],
                "comparator": "<",
            }
        }
    else:
        return None


# ====================================
def add_logistic_chest_requester(bp, x, y, ingredient=None):
    requester = entity.new_entity("logistic-chest-requester", x, y)
    if ingredient is not None:
        if isinstance(ingredient, tuple):
            name, amount = ingredient
            amount = get_amount(amount, name)
            requester.append_request_filters(
                {"index": 1, "name": name, "count": amount}
            )
        elif isinstance(ingredient, list):
            for index, ing in enumerate(ingredient, start=1):
                name, amount = ing
                amount = get_amount(amount, name)
                requester.append_request_filters(
                    {"index": index, "name": name, "count": amount}
                )
    bp.append_entity(requester)
    return requester


# ====================================
def update_request_filters(entity, ingredient):
    index = len(entity.read("request_filters")) + 1
    if isinstance(ingredient, tuple):
        name, amount = ingredient
        amount = get_amount(amount, name)
        entity.append_request_filters({"index": index, "name": name, "count": amount})
    elif isinstance(ingredient, list):
        for ing in ingredient:
            name, amount = ing
            amount = get_amount(amount, name)
            entity.append_request_filters(
                {"index": index, "name": name, "count": amount}
            )
            index += 1


# ====================================
def add_small_electric_pole(bp, x, y):
    pole = entity.new_entity("small-electric-pole", x, y)
    bp.append_entity(pole)
    return pole


# ====================================
def compress(ingredients1, ingredients2):
    temp = []
    temp.extend(ingredients1)
    temp.extend(ingredients2)
    return temp


# ====================================
def get_amount(amount, name):
    if full_stack:
        return math.ceil(items[name] / 4 / 2) * 4
    else:
        return math.ceil(amount / 4) * 4


# ====================================
def add_assembly_machine(bp, x0, y0, recipe1, recipe2, recipe3, recipe4):
    ingredients1 = get_iningredients(recipe1)
    ingredients2 = get_iningredients(recipe2)
    ingredients3 = get_iningredients(recipe3)
    ingredients4 = get_iningredients(recipe4)

    # assembly + passive_provider
    add_assembling_machine_2(bp, x0 + 1.5, y0 + 1.5, recipe1, False)
    add_assembling_machine_2(bp, x0 + 4.5, y0 + 1.5, recipe2, False)
    add_assembling_machine_2(bp, x0 + 1.5, y0 + 7.5, recipe3, False)
    add_assembling_machine_2(bp, x0 + 4.5, y0 + 7.5, recipe4, False)

    requesters = []
    passive_provider = add_passive_provider(bp, x0 + 2.5, y0 + 4.5)
    cs = new_circuit_condition(recipe1)
    c = new_connection(passive_provider.read_entity_number())
    add_red_filter_inserter(bp, x0 + 2.5, y0 + 3.5, 1, recipe1, cs, c)
    add_red_inserter(bp, x0 + 1.5, y0 + 3.5, 4)
    cs = new_circuit_condition(recipe3)
    c = new_connection(passive_provider.read_entity_number())
    add_red_filter_inserter(bp, x0 + 2.5, y0 + 5.5, 4, recipe3, cs, c)
    add_red_inserter(bp, x0 + 1.5, y0 + 5.5, 1)
    requesters.append(add_logistic_chest_requester(bp, x0 + 1.5, y0 + 4.5))
    pole1 = add_small_electric_pole(bp, x0 + 0.5, y0 + 4.5)

    passive_provider = add_passive_provider(bp, x0 + 3.5, y0 + 4.5)
    cs = new_circuit_condition(recipe2)
    c = new_connection(passive_provider.read_entity_number())
    add_red_filter_inserter(bp, x0 + 3.5, y0 + 3.5, 1, recipe2, cs, c)
    add_red_inserter(bp, x0 + 4.5, y0 + 3.5, 4)
    cs = new_circuit_condition(recipe4)
    c = new_connection(passive_provider.read_entity_number())
    add_red_filter_inserter(bp, x0 + 3.5, y0 + 5.5, 4, recipe4, cs, c)
    add_red_inserter(bp, x0 + 4.5, y0 + 5.5, 1)
    requesters.append(add_logistic_chest_requester(bp, x0 + 4.5, y0 + 4.5))
    pole2 = add_small_electric_pole(bp, x0 + 5.5, y0 + 4.5)
    pole1.set("neighbours", [pole2.read_entity_number()])
    pole2.set("neighbours", [pole1.read_entity_number()])

    ingredients = compress(ingredients1, ingredients3)
    update_request_filters(requesters[0], ingredients)

    ingredients = compress(ingredients2, ingredients4)
    update_request_filters(requesters[1], ingredients)


# ====================================
def get_bp(bp, recipes_for_bp):
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

        add_assembly_machine(bp, x, y, r1, r2, r3, r4)
        count += 1
        x += 7
        if count % 10 == 0:
            x = 0
            y += 10


######################################
#
# main
if __name__ == "__main__":
    recipes = get_recipes()
    items = get_items()

    # print(len(recipes))
    # bp = blueprint.new_blueprint()
    # x = y = 0
    # for count, recipe in enumerate(recipes.keys(), start=1):
    #     add_assembling_machine_2(bp, x, y, recipe, False)
    #     x += 4
    #     if count % 40 == 0:
    #         x = 0
    #         y += 4

    # label = "all"
    # bp.set_label_color(1, 0, 1)
    # bp.set_label(label)
    # print()
    # print(label)
    # print("==================================")
    # print(bp.to_str())
    # print("==================================")

    # # get all recipes for the mall
    # bp = blueprint.from_file("mall-bob.txt.ignore")
    # new_recipes = set()
    # entities = bp.get_entities()
    # print("######################################")
    # for e in entities:
    #     if e.read_name() == "assembling-machine-2":
    #         if e.read_recipe() and e.read_recipe() not in recipes_for_mall:
    #             new_recipes.add(e.read_recipe())

    # for r in sorted(new_recipes):
    #     print("'{}',".format(r))
    # print("######################################")

    # print(len(recipes))
    # bp = blueprint.new_blueprint()
    # x = y = 0
    # # for count, recipe in enumerate(recipes.keys(), start=1):
    # for count, recipe in enumerate(recipes_for_mall, start=1):
    #     add_assembling_machine_2(bp, x, y, recipe, False)
    #     x += 4
    #     if count % 40 == 0:
    #         x = 0
    #         y += 4

    # label = "all"
    # bp.set_label_color(1, 0, 1)
    # bp.set_label(label)
    # print()
    # print(label)
    # print("==================================")
    # print(bp.to_str())
    # print("==================================")

    bp = blueprint.new_blueprint()
    get_bp(bp, recipes_for_mall)
    label = "mall"
    filename = "bp-out-BobMod.ignore"
    bp.set_label_color(1, 0, 1)
    bp.set_label(label)
    print()
    print(label)
    print("==================================")
    print(f"to file: {filename}")
    bp.to_file(filename)
    print("==================================")

    modules = (
        "speed-module",
        "speed-module-2",
        "speed-module-3",
        "speed-module-4",
        "speed-module-5",
        "speed-module-6",
        "speed-module-7",
        "speed-module-8",
        "effectivity-module",
        "effectivity-module-2",
        "effectivity-module-3",
        "effectivity-module-4",
        "effectivity-module-5",
        "effectivity-module-6",
        "effectivity-module-7",
        "effectivity-module-8",
        "productivity-module",
        "productivity-module-2",
        "productivity-module-3",
        "productivity-module-4",
        "productivity-module-5",
        "productivity-module-6",
        "productivity-module-7",
        "productivity-module-8",
    )
    bp = blueprint.new_blueprint()
    get_bp(bp, modules)
    label = "mall"
    filename = "bp-out-BobMod.ignore"
    bp.set_label_color(1, 0, 1)
    bp.set_label(label)
    print()
    print(label)
    print("==================================")
    # print(f"to file: {filename}")
    print(bp.to_str())
    print("==================================")

    # sorting recipes by groups
    subgroups = tuple(r["subgroup"] for r in recipes.values())  # all subgroups
    recipes_for_mall2 = {}  # { subgroup: [ recipes ] }

    print(sorted(groups))
    for subgroup in sorted(groups):
        recipes_for_mall2[subgroup] = [
            r for r in recipes_for_mall if recipes[r]["subgroup"] == subgroup
        ]

    book = blueprint.new_blueprint_book()
    index = 0
    for group in groups2:
        recipes_sub = list(
            itertools.chain.from_iterable(
                [r for s, r in recipes_for_mall2.items() if s in group]
            )
        )
        index += 1
        bp = blueprint.new_blueprint()
        get_bp(bp, recipes_sub)
        bp.set_label_color(1, 0, 1)
        bp.set_label(subgroup)
        book.append_bp(bp, index)

    label = "mall"
    book.set_label(label)
    filename = "bp-out-BobMod.ignore"

    print()
    print(label)
    print("==================================")
    print(f"to file: {filename}")
    book.to_file(filename)
    print("==================================")

    print("len(recipes_for_mall) = ", len(recipes_for_mall))
