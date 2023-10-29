from bp_from_json import entity
import math


# ====================================
def get_iningredients(recipe, recipes, items, amount=1):
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
def add_machine(bp, name, x, y, recipe, name_of_modules="", number_of_modules=0):
    # name = "assembling-machine-2"
    assembly = entity.new_entity(name, x, y)
    if recipe:
        assembly.set("recipe", recipe)
    if name_of_modules:
        assembly.update_items(
            {name_of_modules: number_of_modules}, name_verification=False
        )
    bp.append_entity(assembly)
    return assembly


# ====================================
def add_passive_provider(bp, x, y, bar=None):
    passive_provider = entity.new_entity("logistic-chest-passive-provider", x, y)
    if bar is not None:
        passive_provider.set("bar", bar)
    bp.append_entity(passive_provider)
    return passive_provider


# ====================================
def add_filter_inserter(
    bp, name, x, y, direction, recipe, recipes, circuit_condition=None, connection=None
):
    inserter = entity.new_entity(name, x, y)
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
def add_inserter(bp, name, x, y, direction):
    inserter = entity.new_entity(name, x, y)
    inserter.set("direction", direction)
    bp.append_entity(inserter)
    return inserter


# ====================================
def new_connection(entity_number):
    return {"1": {"red": [{"entity_id": entity_number}]}}


# ====================================
def new_circuit_condition(recipe, recipes, constant, comparator="<"):
    if recipe:
        r = recipes[recipe]["product"]
        return {
            "circuit_condition": {
                "first_signal": {"type": "item", "name": r},
                "constant": constant,
                "comparator": comparator,
            }
        }
    else:
        return None


# ====================================
def get_stack_size(recipe, recipes, items):
    return items[recipes[recipe]["product"]]


# ====================================
def add_logistic_chest_requester(bp, x, y, ingredient=None, func_get_amount=None):
    requester = entity.new_entity("logistic-chest-requester", x, y)
    if ingredient is not None:
        if isinstance(ingredient, tuple):
            name, amount = ingredient
            amount = func_get_amount(amount, name)
            requester.append_request_filters(
                {"index": 1, "name": name, "count": amount}
            )
        elif isinstance(ingredient, list):
            for index, ing in enumerate(ingredient, start=1):
                name, amount = ing
                amount = func_get_amount(amount, name)
                requester.append_request_filters(
                    {"index": index, "name": name, "count": amount}
                )
    bp.append_entity(requester)
    return requester


# ====================================
def update_request_filters(entity, ingredient, func_get_amount):
    index = len(entity.read("request_filters")) + 1
    if isinstance(ingredient, tuple):
        name, amount = ingredient
        amount = func_get_amount(amount, name)
        entity.append_request_filters({"index": index, "name": name, "count": amount})
    elif isinstance(ingredient, list):
        for ing in ingredient:
            name, amount = ing
            amount = func_get_amount(amount, name)
            entity.append_request_filters(
                {"index": index, "name": name, "count": amount}
            )
            index += 1


# ====================================
def add_entity(bp, name, x, y):
    pole = entity.new_entity(name, x, y)
    bp.append_entity(pole)
    return pole


# ====================================
def get_amount(amount, name, items, full_stack=True):
    if full_stack:
        return math.ceil(items[name] / 4 / 2) * 4
    else:
        return math.ceil(amount / 4) * 4
