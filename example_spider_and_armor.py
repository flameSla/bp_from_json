from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import get_recipes_with_one_product
from bp_from_json import get_items
import math
from fractions import Fraction
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


# ====================================
def new_request(name, amount):
    return {"name": name, "amount": Fraction(amount, 1)}


# ====================================
def get_requests(requests, request, final_ingredients):
    # print("get_requests")
    # print("\t:{}".format(request))
    # print()
    for ingredient in recipes[request["name"]]["ingredients"]:
        if ingredient["name"] not in final_ingredients:
            amount = request["amount"] * ingredient["amount"]
            name = ingredient["name"]
            requests += dict_bp({name: amount})

            get_requests(requests, new_request(name, amount), final_ingredients)


# ====================================
def add_assembly_machine_ver2(bp, x0, y0, item, amount):
    slots = 0
    for ingredient in recipes[item]["ingredients"]:
        a = int(amount * ingredient["amount"])
        n = ingredient["name"]
        stack_size = items[n]
        slots += math.ceil(a / stack_size)
    chests = math.ceil(slots / 48)
    if chests > 2:
        raise Exception("{}={}: chest={} > 2".format(item, amount, chests))

    add_machine(bp, "assembling-machine-2", x0 + 1.5, y0 + 1.5, item)
    add_entity(bp, "steel-chest", x0 + 2.5, y0 + 4.5)
    add_inserter(bp, "fast-inserter", x0 + 2.5, y0 + 3.5, 1)

    steel_chests = []
    for chest in range(chests):
        steel_chests.append(add_entity(bp, "steel-chest", x0 + 0.5 + chest, y0 + 4.5))
        add_inserter(bp, "fast-inserter", x0 + 0.5 + chest, y0 + 3.5, 4)

    for ingredient in recipes[item]["ingredients"]:
        if ingredient["name"] in final_ingredients or True:
            a = math.ceil((amount * ingredient["amount"] / chests))
            n = ingredient["name"]
            for chest in range(chests):
                steel_chests[chest].update_items({n: a}, name_verification=False)
        else:
            print("")
            print("Error !!!")
            print("item = ", ingredient["name"])
            raise Exception("Неверный рецепт в запросе")


# ====================================
def get_bp(item, amount, requests):
    bp = blueprint.new_blueprint()
    bp.set_icons(1, "item", item)
    bp.set_label("{}x[item={}]".format(amount, item))
    x = y = 0
    for item, amount in requests.items():
        add_assembly_machine_ver2(bp, x, y, item, amount)
        x += 3

    return bp


######################################
#
# main
if __name__ == "__main__":
    recipes = get_recipes_with_one_product()
    items = get_items()
    final_ingredients = (
        "copper-ore",
        "iron-ore",
        "coal",
        "stone",
        "raw-fish",
        "plastic-bar",
        "iron-plate",
        "copper-plate",
        "steel-plate",
        "iron-gear-wheel",
        "processing-unit",
        "advanced-circuit",
        "electronic-circuit",
        "electric-engine-unit",
        "radar",
        "battery",
    )

    request_for_production = (
        ("power-armor-mk2", 1, 0),
        ("solar-panel-equipment", 32, 1),
        ("fusion-reactor-equipment", 1, 2),
        ("exoskeleton-equipment", 3, 3),
        ("battery-mk2-equipment", 10, 4),
        ("personal-laser-defense-equipment", 13, 6),
        ("personal-roboport-mk2-equipment", 1, 7),
        ("spidertron", 1, 12),
        ("spidertron-remote", 1, 13),
        ("battery-equipment", 4, 14),
        ("productivity-module-3", 4, 18),
    )

    book = blueprint.new_blueprint_book()
    book.set_label("mk2+spider")
    book.set_description("by flame_Sla")
    for item, amount, index in request_for_production:
        print()
        print("==================")
        print(item)
        print()
        requests = dict_bp({item: amount})
        get_requests(requests, new_request(item, amount), final_ingredients)
        print(requests)
        book.append_bp(get_bp(item, amount, requests), index)

    print()
    print("==================")
    print("book")
    print()
    print(book.to_str())
    print("==================")
