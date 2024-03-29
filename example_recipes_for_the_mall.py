import math
import json
import sys
from bp_from_json import blueprint
from bp_from_json import entity
from bp_from_json import get_items
from fractions import Fraction


full_stack = True


recipes_for_mall_2 = {
    "wooden-chest": 10,
    "radar": 10,
    "land-mine": 10,
    "stone-wall": 10,
    "empty-barrel": 10,
    "spidertron": 0.5,
    "logistic-robot": 10,
    "construction-robot": 10,
    "roboport": 10,
    "lab": 10,
    "rocket-silo": 0.1,
    "electric-furnace": 10,
    "steel-furnace": 10,
    "stone-furnace": 10,
    "steam-turbine": 10,
    "heat-exchanger": 5,
    "heat-pipe": 10,
    "nuclear-reactor": 1,
    "centrifuge": 2,
    "solar-panel": 10,
    "accumulator": 10,
    "small-electric-pole": 10,
    "medium-electric-pole": 10,
    "big-electric-pole": 10,
    "substation": 10,
    "red-wire": 10,
    "green-wire": 10,
    "arithmetic-combinator": 10,
    "decider-combinator": 10,
    "constant-combinator": 10,
    "power-switch": 10,
    "programmable-speaker": 10,
    "small-lamp": 10,
    "train-stop": 10,
    "rail-signal": 10,
    "rail-chain-signal": 10,
    "locomotive": 10,
    "cargo-wagon": 10,
    "fluid-wagon": 10,
    "artillery-wagon": 2,
    "artillery-turret": 2,
    "shotgun-shell": 10,
    "poison-capsule": 10,
    "grenade": 10,
    "car": 1,
    "iron-chest": 10,
    "burner-inserter": 10,
    "repair-pack": 10,
    "gate": 10,
    "cliff-explosives": 10,
    "spidertron-remote": 10,
    "oil-refinery": 10,
    "chemical-plant": 10,
    "storage-tank": 10,
    "pump": 10,
    "offshore-pump": 10,
    "pumpjack": 10,
    "electric-mining-drill": 10,
    "burner-mining-drill": 10,
    "steam-engine": 10,
    "boiler": 10,
    "solar-panel-equipment": 10,
    "belt-immunity-equipment": 10,
    "night-vision-equipment": 10,
    "exoskeleton-equipment": 10,
    "personal-roboport-equipment": 10,
    "personal-roboport-mk2-equipment": 2,
    "discharge-defense-remote": 1,
    "discharge-defense-equipment": 1,
    "personal-laser-defense-equipment": 10,
    "battery-equipment": 10,
    "battery-mk2-equipment": 10,
    "energy-shield-equipment": 10,
    "energy-shield-mk2-equipment": 10,
    "fusion-reactor-equipment": 1,
    "power-armor-mk2": 1,
    "artillery-targeting-remote": 1,
    "flamethrower": 10,
    "rocket-launcher": 10,
    "combat-shotgun": 10,
    "shotgun": 10,
    "submachine-gun": 10,
    "pistol": 1,
    "destroyer-capsule": 10,
    "distractor-capsule": 10,
    "defender-capsule": 10,
    "piercing-shotgun-shell": 10,
    "slowdown-capsule": 10,
    "cluster-grenade": 10,
    "tank": 1,
}


recipes_for_mall_b12 = {
    "copper-cable": 10,
    "iron-stick": 10,
    "iron-gear-wheel": 10,
    # ====================================
    "electronic-circuit": 10,
    "advanced-circuit": 10,
    "processing-unit": 10,
    # ====================================
    "pipe": 10,
    "pipe-to-ground": 10,
    # ====================================
    "effectivity-module": 10,
    "effectivity-module-2": 10,
    "effectivity-module-3": 10,
    "productivity-module": 10,
    "productivity-module-2": 10,
    "productivity-module-3": 10,
    "speed-module": 10,
    "speed-module-2": 10,
    "speed-module-3": 10,
    # ====================================
    "engine-unit": 10,
    "electric-engine-unit": 10,
    "flying-robot-frame": 10,
    # ====================================
    "assembling-machine-1": 10,
    "assembling-machine-2": 10,
    "assembling-machine-3": 10,
    # ====================================
    "splitter": 10,
    "fast-splitter": 10,
    "express-splitter": 10,
    "transport-belt": 10,
    "fast-transport-belt": 10,
    "express-transport-belt": 10,
    "underground-belt": 10,
    "fast-underground-belt": 10,
    "express-underground-belt": 10,
    # ====================================
    "logistic-chest-passive-provider": 10,
    "logistic-chest-active-provider": 10,
    "logistic-chest-requester": 10,
    "logistic-chest-storage": 10,
    "logistic-chest-buffer": 10,
    "steel-chest": 10,
    # ====================================
    "inserter": 10,
    "long-handed-inserter": 10,
    "fast-inserter": 10,
    "stack-inserter": 10,
    "filter-inserter": 10,
    "stack-filter-inserter": 10,
    # ====================================
    "rocket-control-unit": 10,
    "low-density-structure": 10,
    # ====================================
    "gun-turret": 10,
    "laser-turret": 10,
    "flamethrower-turret": 10,
    "atomic-bomb": 5,
    "artillery-shell": 10,
    "rocket": 10,
    "explosive-rocket": 10,
    "cannon-shell": 10,
    "explosive-cannon-shell": 10,
    "uranium-cannon-shell": 10,
    "explosive-uranium-cannon-shell": 10,
    "firearm-magazine": 10,
    "piercing-rounds-magazine": 10,
    "uranium-rounds-magazine": 10,
    # ====================================
    "rail": 10,
    "rocket-fuel": 10,
    "uranium-fuel-cell": 10,
    "beacon": 10,
    "landfill": 10,
    "concrete": 10,
    "refined-concrete": 10,
    "hazard-concrete": 10,
    "refined-hazard-concrete": 10,
}


items_that_may_be_damaged = (
    "steel-chest",
    "pipe",
    "laser-turret",
    "fast-underground-belt",
    "stone-wall",
    "solar-panel",
    "splitter",
    "inserter",
    "fast-splitter",
    "transport-belt",
    "fast-inserter",
    "assembling-machine-1",
    "assembling-machine-2",
    "radar",
    "stack-inserter",
    "fast-transport-belt",
    "underground-belt",
    "storage-tank",
    "stone-furnace",
)
# ====================================
par_debugging = False


def debug(*args, end="\n"):
    global par_debugging
    if par_debugging:
        print(*args, end=end, file=sys.stderr, flush=True)


# ====================================
def get_amount(amount, name):
    if full_stack:
        return math.ceil(items[name] / 4) * 4 * 2
    else:
        return math.ceil(amount / 4) * 4


# ====================================
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


# ====================================
def print_dict(d, dimension=None):
    if dimension is None:
        dimension = ""
    for k, v in sorted(d.items(), key=lambda x: x[0]):
        print("{:34} = {:10.3f} {}".format(k, float(v), dimension))


# ====================================
def add_assembling_machine_3(bp, x, y, recipe, speed):
    assembly = entity.new_entity("assembling-machine-3", x, y)
    if recipe:
        assembly.set("recipe", recipe)
    if speed:
        assembly.update_items({"speed-module-3": 4}, name_verification=False)
    bp.append_entity(assembly)
    return assembly


# ====================================
def new_connection(entity_number):
    return {"1": {"red": [{"entity_id": entity_number}]}}


# ====================================
def new_circuit_condition(recipe):
    return {
        "circuit_condition": {
            "first_signal": {"type": "item", "name": recipe},
            "constant": items[recipe],
            "comparator": "<",
        }
    }


# ====================================
def add_stack_filter_inserter(
    bp, x, y, direction, recipe, circuit_condition=None, connection=None
):
    inserter = entity.new_entity("stack-filter-inserter", x, y)
    inserter.set("direction", direction)
    if recipe:
        f = list()
        f.append({"index": 1, "name": recipe})
        inserter.set("filters", f)
    if circuit_condition is not None:
        inserter.set("control_behavior", circuit_condition)
    if connection is not None:
        inserter.set("connections", connection)
    bp.append_entity(inserter)
    return inserter


# ====================================
def add_passive_provider(bp, x, y, bar=None):
    passive_provider = entity.new_entity("logistic-chest-passive-provider", x, y)
    if bar is not None:
        passive_provider.set("bar", bar)
    bp.append_entity(passive_provider)
    return passive_provider


# ====================================
def add_stack_inserter(bp, x, y, direction):
    inserter = entity.new_entity("stack-inserter", x, y)
    inserter.set("direction", direction)
    bp.append_entity(inserter)
    return inserter


# ====================================
def add_logistic_chest_requester(bp, x, y, ingredient):
    requester = entity.new_entity("logistic-chest-requester", x, y)
    if isinstance(ingredient, tuple):
        name, amount = ingredient
        amount = get_amount(amount, name)
        requester.append_request_filters({"index": 1, "name": name, "count": amount})
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
def if_quantity_is_more_than_5_sort_and_compress(ingredients):
    if len(ingredients) > 5:
        ingredients = sorted(ingredients, key=lambda tup: tup[1], reverse=True)
        reset = True
        while reset:
            reset = False
            debug("Warning")
            for j in range(5, len(ingredients)):
                i, a = ingredients[j]
                debug("i = ", type(i), i)
                if i in items_that_may_be_damaged:
                    t = ingredients.pop(j)
                    debug("ingredients = ", type(ingredients), ingredients)
                    ingredients.insert(0, t)
                    debug("ingredients = ", type(ingredients), ingredients)
                    reset = True
        temp = ingredients[0:4]
        temp.append(list(ingredients[5:]))
        return temp
    else:
        return ingredients


# ====================================
def sort_and_compress(ingredients):
    global par_debugging
    # par_debugging = True
    if ingredients:
        there_are_items_that_can_be_damaged = False
        for j in range(len(ingredients)):
            i, a = ingredients[j]
            if i in items_that_may_be_damaged:
                t = ingredients.pop(j)
                ingredients.insert(0, t)
                there_are_items_that_can_be_damaged = True
                break
        if there_are_items_that_can_be_damaged:
            temp = []
            temp.append(ingredients[0])
            if ingredients[1:]:
                if len(ingredients) == 2:
                    temp.append(ingredients[1])
                else:
                    temp.append(list(ingredients[1:]))
            return temp
        else:
            temp = []
            temp.append(list(ingredients))
            return temp
    else:
        return ingredients


# ====================================
def add_assembly_machine(bp, x0, y0, recipe, amount, speed):
    coordinates = (
        (1.5, -0.5, 1, 1.5, -1.5),
        (2.5, -0.5, 1, 2.5, -1.5),
        (0.5, 3.5, 4, 0.5, 4.5),
        (1.5, 3.5, 4, 1.5, 4.5),
        (2.5, 3.5, 4, 2.5, 4.5),
    )

    # assembly + passive_provider
    add_assembling_machine_3(bp, x0 + 1.5, y0 + 1.5, recipe, speed)
    add_stack_filter_inserter(bp, x0 + 0.5, y0 - 0.5, 4, recipe)
    add_passive_provider(bp, x0 + 0.5, y0 - 1.5, bar=1)

    ingredients = [
        (i["name"], i["amount"] * amount) for i in recipes[recipe] if i["name"] in items
    ]

    ingredients = if_quantity_is_more_than_5_sort_and_compress(ingredients)
    # logistic-chest-requester
    i = 0
    for ingredient in ingredients:
        x1, y1, d, x2, y2 = coordinates[i]
        add_stack_inserter(bp, x0 + x1, y0 + y1, d)
        add_logistic_chest_requester(bp, x0 + x2, y0 + y2, ingredient)
        i += 1


# ====================================
def add_assembly_machine_2(bp, x0, y0, recipe1, amount1, recipe2, amount2, speed):
    if recipe1:
        ingredients1 = [
            (i["name"], i["amount"] * amount1)
            for i in recipes[recipe1]
            if i["name"] in items
        ]
    else:
        ingredients1 = []

    if recipe2:
        ingredients2 = [
            (i["name"], i["amount"] * amount2)
            for i in recipes[recipe2]
            if i["name"] in items
        ]
    else:
        ingredients2 = []

    if len(ingredients1) <= 4 and len(ingredients2) <= 3:
        block_type_2 = True
    else:
        block_type_2 = False

    coordinates = (
        (0.5, 3.5, 4, 0.5, 4.5),
        (1.5, 3.5, 4, 1.5, 4.5),
        (2.5, 3.5, 4, 2.5, 4.5),
        (2.5, -0.5, 1, 2.5, -1.5),
        (0.5, -0.5, 1, 0.5, -1.5),
    )
    coordinates2 = (
        (0.5, 5.5, 1, 0.5, 4.5),
        (1.5, 5.5, 1, 1.5, 4.5),
        (2.5, 5.5, 1, 2.5, 4.5),
        (2.5, 9.5, 4, 2.5, 10.5),
        (0.5, 9.5, 4, 0.5, 10.5),
    )

    # assembly + passive_provider
    add_assembling_machine_3(bp, x0 + 1.5, y0 + 1.5, recipe1, speed)
    add_stack_filter_inserter(bp, x0 + 1.5, y0 - 0.5, 4, recipe1)
    add_passive_provider(bp, x0 + 1.5, y0 - 1.5, bar=1)
    add_assembling_machine_3(bp, x0 + 1.5, y0 + 7.5, recipe2, speed)
    add_stack_filter_inserter(bp, x0 + 1.5, y0 + 9.5, 1, recipe2)
    add_passive_provider(bp, x0 + 1.5, y0 + 10.5, bar=1)

    ingredients1 = if_quantity_is_more_than_5_sort_and_compress(ingredients1)
    ingredients2 = if_quantity_is_more_than_5_sort_and_compress(ingredients2)
    # logistic-chest-requester
    i = 0
    e = [None, None, None, None, None]
    for ingredient in ingredients1:
        x1, y1, d, x2, y2 = coordinates[i]
        add_stack_inserter(bp, x0 + x1, y0 + y1, d)
        requester = add_logistic_chest_requester(bp, x0 + x2, y0 + y2, ingredient)
        # 3 chests shared by two machine
        if i < 3:
            e[i] = requester
        i += 1

    i = 1 if block_type_2 else 0
    for ingredient in ingredients2:
        x1, y1, d, x2, y2 = coordinates2[i]
        add_stack_inserter(bp, x0 + x1, y0 + y1, d)
        if e[i] is None:
            add_logistic_chest_requester(bp, x0 + x2, y0 + y2, ingredient)
        else:
            update_request_filters(e[i], ingredient)
        i += 1

    if block_type_2:
        for x1, y1 in ((0.5, -0.5), (0.5, 5.5), (0.5, 9.5)):
            pole = entity.new_entity("medium-electric-pole", x0 + x1, y0 + y1)
            bp.append_entity(pole)


# ====================================
def add_assembly_machine_2_ver2(bp, x0, y0, recipe1, amount1, recipe2, amount2, speed):
    if recipe1:
        ingredients1 = [
            (i["name"], i["amount"] * amount1)
            for i in recipes[recipe1]
            if i["name"] in items
        ]
    else:
        ingredients1 = []

    if recipe2:
        ingredients2 = [
            (i["name"], i["amount"] * amount2)
            for i in recipes[recipe2]
            if i["name"] in items
        ]
    else:
        ingredients2 = []

    coordinates = (
        (1.5, 3.5, 4, 1.5, 4.5),
        (2.5, 3.5, 4, 2.5, 4.5),
    )
    coordinates2 = (
        (1.5, 5.5, 1, 1.5, 4.5),
        (2.5, 5.5, 1, 2.5, 4.5),
    )

    # assembly + passive_provider
    passive_provider = add_passive_provider(bp, x0 + 0.5, y0 + 4.5)
    if recipe1:
        cs = new_circuit_condition(recipe1)
        c = new_connection(passive_provider.read_entity_number())
        add_stack_filter_inserter(bp, x0 + 0.5, y0 + 3.5, 1, recipe1, cs, c)
    if recipe2:
        cs = new_circuit_condition(recipe2)
        c = new_connection(passive_provider.read_entity_number())
        add_stack_filter_inserter(bp, x0 + 0.5, y0 + 5.5, 4, recipe2, cs, c)

    add_assembling_machine_3(bp, x0 + 1.5, y0 + 1.5, recipe1, speed)
    add_assembling_machine_3(bp, x0 + 1.5, y0 + 7.5, recipe2, speed)

    ingredients1 = sort_and_compress(ingredients1)
    ingredients2 = sort_and_compress(ingredients2)
    debug("ingredient1 = ", type(ingredients1), ingredients1)
    debug("ingredient2 = ", type(ingredients2), ingredients2)

    # only one request chest
    compact_version = (
        True if len(ingredients1) <= 1 and len(ingredients2) <= 1 else False
    )
    # logistic-chest-requester
    i = 0
    e = [None, None]
    for ingredient in ingredients1:
        if not compact_version and isinstance(ingredient, list) and i == 0:
            i += 1
        x1, y1, d, x2, y2 = coordinates[i]
        if isinstance(ingredient, tuple):
            name, amount = ingredient
            add_stack_filter_inserter(bp, x0 + x1, y0 + y1, d, name)
        else:
            add_stack_inserter(bp, x0 + x1, y0 + y1, d)
        # 2 chests shared by two machine
        e[i] = add_logistic_chest_requester(bp, x0 + x2, y0 + y2, ingredient)
        i += 1

    i = 0
    for ingredient in ingredients2:
        if not compact_version and isinstance(ingredient, list) and i == 0:
            i += 1
        x1, y1, d, x2, y2 = coordinates2[i]
        if isinstance(ingredient, tuple):
            name, amount = ingredient
            add_stack_filter_inserter(bp, x0 + x1, y0 + y1, d, name)
        else:
            add_stack_inserter(bp, x0 + x1, y0 + y1, d)
        if e[i] is None:
            add_logistic_chest_requester(bp, x0 + x2, y0 + y2, ingredient)
        else:
            update_request_filters(e[i], ingredient)
        i += 1


######################################
#
# main
if __name__ == "__main__":
    recipes = get_recipes()
    items = get_items()

    # # get all recipes for the mall
    # bp = blueprint.from_file("mall-Megamall-in-one_v7.1.txt")
    # new_recipes = set()
    # entities = bp.get_entities()
    # print("######################################")
    # for e in entities:
    #     if e.read_name() == "assembling-machine-3":
    #         if e.read_recipe() and e.read_recipe() not in recipes_for_mall_2.keys():
    #             new_recipes.add(e.read_recipe())

    # for r in new_recipes:
    #     print("'{}': 1, ".format(r))
    # print("######################################")

    # all_ingredients = set()
    # for request, amount in recipes_for_mall_2.items():
    #     ingredients = [
    #         (i["name"], i["amount"] * amount)
    #         for i in recipes[request]
    #         if i["name"] in items
    #     ]
    #     for item, amount in ingredients:
    #         all_ingredients.add(item)
    # for request, amount in recipes_for_mall_b12.items():
    #     ingredients = [
    #         (i["name"], i["amount"] * amount)
    #         for i in recipes[request]
    #         if i["name"] in items
    #     ]
    #     for item, amount in ingredients:
    #         all_ingredients.add(item)
    # print()
    # print("==================")
    # print("all_ingredients")
    # print()
    # for item in all_ingredients:
    #     print(f"'{item}',")
    # print("==================")

    bp = blueprint.new_blueprint()
    x = y = 0
    for recipe, amount in recipes_for_mall_b12.items():
        add_assembly_machine(bp, x, y, recipe, amount, False)
        x += 4

    bp.set_label_color(1, 0, 1)
    bp.set_label("mall b12")
    print()
    print("mall b12")
    print("==================================")
    print(bp.to_str())
    print("==================================")

    par_debugging = False
    number_of_ingredients_in_the_recipe = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
    }
    for request, amount in recipes_for_mall_2.items():
        ingredients = [
            (i["name"], i["amount"] * amount)
            for i in recipes[request]
            if i["name"] in items
        ]
        slots = 0
        all_ingredients = set()
        for item, amount in ingredients:
            stack_size = items[item]
            slots += math.ceil(amount / stack_size)
            all_ingredients.add(item)
        if slots >= 10:
            debug(request, ingredients, "slots = ", slots)

        if len(ingredients) <= 3:
            number_of_ingredients_in_the_recipe[3].append(request)
        elif len(ingredients) == 4:
            number_of_ingredients_in_the_recipe[4].append(request)
        else:
            number_of_ingredients_in_the_recipe[5].append(request)

    debug()
    debug(len(number_of_ingredients_in_the_recipe[3]))
    debug(len(number_of_ingredients_in_the_recipe[4]))
    debug(len(number_of_ingredients_in_the_recipe[5]))
    debug()
    debug(number_of_ingredients_in_the_recipe)

    bp = blueprint.new_blueprint()
    x = y = 0
    i = 10
    while True:

        def get_recipe():
            global i
            while True:
                if i <= 0:
                    return 0, ""
                elif len(number_of_ingredients_in_the_recipe[i]):
                    r = number_of_ingredients_in_the_recipe[i].pop()
                    return i, r
                else:
                    i -= 1

        l, r1 = get_recipe()
        if l != 4:
            l, r2 = get_recipe()
        else:
            r2 = number_of_ingredients_in_the_recipe[3].pop()

        if r1 == "" and r2 == "":
            break

        a1 = recipes_for_mall_2.get(r1, 0)
        a2 = recipes_for_mall_2.get(r2, 0)

        add_assembly_machine_2(
            bp,
            x,
            y,
            r1,
            a1,
            r2,
            a2,
            True,
        )

        x += 4

    bp.set_label_color(1, 0, 1)
    bp.set_label("mall 2")
    print()
    print("mall 2")
    print("==================================")
    print(bp.to_str())
    print("==================================")

    recipes_items_less_than_equal_to_1 = []
    recipes_items_more_than_1 = []
    for request, amount in recipes_for_mall_2.items():
        ingredients = [
            (i["name"], i["amount"] * amount)
            for i in recipes[request]
            if i["name"] in items
        ]
        slots = 0
        i = 0
        for item, amount in ingredients:
            if item in items_that_may_be_damaged:
                i += 1
        if i > 1 and len(ingredients) > i:
            recipes_items_more_than_1.append(request)
        else:
            recipes_items_less_than_equal_to_1.append(request)

    print()
    print("==================")
    print("error")
    print(recipes_items_more_than_1)
    # print()
    # print("==================")
    # print("")
    # print(recipes_items_less_than_equal_to_1)

    bp = blueprint.new_blueprint()
    x = y = 0
    while True:

        def get_recipe():
            if len(recipes_items_less_than_equal_to_1):
                r = recipes_items_less_than_equal_to_1.pop()
                return r
            else:
                return ""

        r1 = get_recipe()
        r2 = get_recipe()
        a1 = recipes_for_mall_2.get(r1, 0)
        a2 = recipes_for_mall_2.get(r2, 0)

        if r1 == "" and r2 == "":
            break

        add_assembly_machine_2_ver2(
            bp,
            x,
            y,
            r1,
            a1,
            r2,
            a2,
            True,
        )

        x += 4

    for r in recipes_items_more_than_1:
        add_assembling_machine_3(bp, x + 1.5, y + 1.5, r, True)

    bp.set_label_color(1, 0, 1)
    bp.set_label("mall ver2")
    print()
    print("mall ver2")
    print("==================================")
    print(bp.to_str())
    print("==================================")

    all_ingredients = set()
    for request, amount in recipes_for_mall_2.items():
        ingredients = [
            (i["name"], i["amount"] * amount)
            for i in recipes[request]
            if i["name"] in items
        ]
        for item, amount in ingredients:
            all_ingredients.add(item)
    for request, amount in recipes_for_mall_b12.items():
        ingredients = [
            (i["name"], i["amount"] * amount)
            for i in recipes[request]
            if i["name"] in items
        ]
        for item, amount in ingredients:
            all_ingredients.add(item)

    bp = blueprint.new_blueprint()
    x0 = y0 = 0
    for i in all_ingredients:
        add_passive_provider(bp, x0 + 0.5, y0 + 0.5)
        add_passive_provider(bp, x0 + 0.5, y0 + 4.5)
        add_passive_provider(bp, x0 + 1.5, y0 + 0.5)
        add_passive_provider(bp, x0 + 1.5, y0 + 4.5)

        add_stack_inserter(bp, x0 + 0.5, y0 + 1.5, 4)
        add_stack_inserter(bp, x0 + 1.5, y0 + 1.5, 4)
        add_stack_inserter(bp, x0 + 0.5, y0 + 3.5, 1)
        add_stack_inserter(bp, x0 + 1.5, y0 + 3.5, 1)

        infinity_chest = entity.new_entity("infinity-chest", x0 + 0.5, y0 + 2.5)
        s = {
            "remove_unfiltered_items": False,
            "filters": [
                {
                    "name": i,
                    "count": 24,
                    "mode": "at-least",
                    "index": 1,
                }
            ],
        }
        infinity_chest.set("infinity_settings", s)
        bp.append_entity(infinity_chest)
        infinity_chest = entity.new_entity("infinity-chest", x0 + 1.5, y0 + 2.5)
        s = {
            "remove_unfiltered_items": False,
            "filters": [
                {
                    "name": i,
                    "count": 24,
                    "mode": "at-least",
                    "index": 1,
                }
            ],
        }
        infinity_chest.set("infinity_settings", s)
        bp.append_entity(infinity_chest)

        x0 += 2

    bp.set_label_color(1, 0, 1)
    bp.set_label("inf")
    print()
    print("inf")
    print("==================================")
    print(bp.to_str())
    print("==================================")
