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
import math


# ====================================
def get_amount(amount, name):
    # global items
    full_stack = True
    if full_stack:
        return math.ceil(get_stack_size(name, recipes, items) / 4 / 2) * 4
    else:
        return math.ceil(amount / 4) * 4


# ====================================
def merge_and_convert_to_list(ingredients1, ingredients2):
    temp = list(ingredients1)
    temp.extend(ingredients2)
    return temp


# ====================================
def add_assembly_machine(
    bp, x0, y0, recipe1, recipe2, recipe3, recipe4, recipes, items
):
    ingredients1 = get_iningredients(recipe1, recipes, items)
    ingredients2 = get_iningredients(recipe2, recipes, items)
    ingredients3 = get_iningredients(recipe3, recipes, items)
    ingredients4 = get_iningredients(recipe4, recipes, items)

    # assembly + passive_provider
    add_machine(bp, "assembling-machine-2", x0 + 1.5, y0 + 1.5, recipe1)
    add_machine(bp, "assembling-machine-2", x0 + 4.5, y0 + 1.5, recipe2)
    add_machine(bp, "assembling-machine-2", x0 + 1.5, y0 + 7.5, recipe3)
    add_machine(bp, "assembling-machine-2", x0 + 4.5, y0 + 7.5, recipe4)

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

    ingredients = merge_and_convert_to_list(ingredients1, ingredients3)
    update_request_filters(requesters[0], ingredients, get_amount)

    ingredients = merge_and_convert_to_list(ingredients2, ingredients4)
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


######################################
#
# main
if __name__ == "__main__":
    recipes_for_mall = get_machine_recipes_with_one_product("Factorio 1.1 Vanilla.json")
    recipes = get_recipes_with_one_product("Factorio 1.1 Vanilla.json")
    items = get_items()
    # for r in sorted(recipes_for_mall.keys()):
    #     print(f"\t'{r}',")

    bp = blueprint.new_blueprint()
    get_bp(bp, recipes_for_mall.keys(), recipes, items)
    label = "mall"
    filename = "bp-out-vanilla-mall.ignore"
    bp.set_label_color(1, 0, 1)
    bp.set_label(label)
    print()
    print(label)
    print("==================================")
    print(f"to file: {filename}")
    bp.to_file(filename)
    # print(bp.to_str())
    print("==================================")
