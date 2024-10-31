from bp_from_json import entity
import math


# ====================================
def get_iningredients(recipe, recipes, items, amount=1):
    ingredients = {}
    if recipe:
        for i in recipes[recipe]["ingredients"]:
            if i["name"] in items:
                ingredients[i["name"]] = i["amount"] * amount

    return ingredients


# ====================================
def add_filtr_constant_combinator(constant_combinator, type, name, count, index=None):
    if index is None:
        min_index = 0
        for f in constant_combinator.data["control_behavior"]["filters"]:
            min_index = max(min_index, f.get("index", 0))
        index = min_index + 1

    constant_combinator.data["control_behavior"]["filters"].append(
        {"signal": {"type": type, "name": name}, "count": count, "index": index}
    )


# ====================================
def add_constant_combinator(bp, x, y):
    constant_combinator = entity.new_entity("constant-combinator", x, y)
    constant_combinator.set("control_behavior", {"filters": []})
    bp.append_entity(constant_combinator)
    return constant_combinator


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
    if recipe:
        if recipe in recipes:
            item_name = recipes[recipe]["product"]
        else:
            item_name = recipe

        if item_name in items:
            return items[item_name]
        else:
            return 0
    else:
        return None


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
    elif isinstance(ingredient, dict):
        for name, amount in ingredient.items():
            amount = func_get_amount(amount, name)
            entity.append_request_filters(
                {"index": index, "name": name, "count": amount}
            )
            index += 1
    else:
        print("ingredient = ", type(ingredient), ingredient)
        raise Exception("unknown type")


# ====================================
def add_entity(bp, name, x, y):
    e = entity.new_entity(name, x, y)
    bp.append_entity(e)
    return e


# ====================================
def get_amount(amount, name, items, full_stack=True):
    if full_stack:
        return math.ceil(items[name] / 4 / 2) * 4
    else:
        return math.ceil(amount / 4) * 4


######################################
#
# main
if __name__ == "__main__":
    func_list = [
        name
        for (name, obj) in vars().items()
        if hasattr(obj, "__class__") and obj.__class__.__name__ == "function"
    ]

    for line in func_list:
        print(f"from bp_functions import {line}")

"""
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
from bp_functions import get_amount
"""
