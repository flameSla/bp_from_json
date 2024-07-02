from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import get_recipes_with_one_product
from bp_from_json import get_items
import math
import sys
from fractions import Fraction

from bp_functions import add_machine
from bp_functions import add_inserter
from bp_functions import add_entity


par_debugging = False


# ====================================
def debug(*args, end="\n"):
    global par_debugging
    if par_debugging:
        print(*args, end=end, file=sys.stderr, flush=True)


# ====================================
def new_request(name, amount):
    return {"name": name, "amount": Fraction(amount, 1)}


# ====================================
def get_requests(requests, request, final_ingredients):
    debug("get_requests")
    debug("\t:{}".format(request))
    debug()
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

    add_machine(bp, "assembling-machine-1", x0 + 1.5, y0 + 1.5, item)
    add_entity(bp, "steel-chest", x0 + 2.5, y0 + 4.5)
    add_inserter(bp, "inserter", x0 + 2.5, y0 + 3.5, 1)

    steel_chests = []
    for chest in range(chests):
        steel_chests.append(add_entity(bp, "steel-chest", x0 + 0.5 + chest, y0 + 4.5))
        # add_inserter(bp, "inserter", x0 + 0.5 + chest, y0 + 3.5, 4)

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
def get_bp(recipe, amount, requests):
    bp = blueprint.new_blueprint()
    item = recipes[recipe]["product"]
    bp.set_icons(1, "item", item)
    try:
        tier = int(item.split("-")[-1])
    except ValueError:
        tier = 1
    bp.set_label("{}x[item={}]-{}".format(amount, item, tier))
    bp.set_description("{}x{}".format(amount, recipe))
    count = 0
    x = y = 0
    for item, amount in requests.items():
        if count == 1:
            x += 4
        else:
            x += 3
        add_assembly_machine_ver2(bp, x, y, item, amount)
        count += 1

    return bp


######################################
#
# main
if __name__ == "__main__":
    recipes = get_recipes_with_one_product("BobMod.json")
    items = get_items("BobMod.json")

    final_ingredients = (
        "oxygen",
        "stone",
        "stone-brick",
        "iron-plate",
        "copper-plate",
        "steel-plate",
        "zinc-plate",
        "aluminium-plate",
        "brass-alloy",
        "invar-alloy",
        "nickel-plate",
        "stone-furnace",
        "pipe",
    )

    request_for_production = (
        ("steam-engine-2", 40, 0),
        ("steam-engine-3", 40, 1),
        ("steam-engine-4", 40, 2),
        ("steam-engine-2", 108, 6),
        ("steam-engine-3", 108, 7),
        ("steam-engine-4", 108, 8),
        ("fluid-reactor-from-fluid-furnace", 12, 12),
        ("fluid-reactor-2", 12, 13),
        ("heat-exchanger", 27, 14),
        ("heat-exchanger-2", 27, 15),
        ("heat-exchanger-3", 27, 16),
        ("bob-gun-turret-3", 300, 20),
        ("bob-gun-turret-4", 300, 21),
    )

    par_debugging = False
    book = blueprint.new_blueprint_book()
    book.set_label("mall-on-construction-bots")
    book.set_description("by flame_Sla")
    for item, amount, index in request_for_production:
        # print()
        # print("==================")
        # print(item)
        # print()
        requests = dict_bp({item: amount})
        # get_requests(requests, new_request(item, amount), final_ingredients)
        debug(requests)
        book.append_bp(get_bp(item, amount, requests), index)

    print()
    print("==================")
    print("book")
    print()
    print(book.to_str())
    print("==================")

    request_for_production2 = (
        ("steam-engine-2", 56, 0, False),
        ("steam-engine-3", 56, 1, False),
        ("heat-exchanger-2", 14, 2, True),
        ("heat-pipe", 43, 3, False),
        ("burner-reactor", 15, 4, True),
    )

    par_debugging = False
    book = blueprint.new_blueprint_book()
    book.set_label("mall-on-construction-bots")
    book.set_description("by flame_Sla")
    for item, amount, index, go_to_final_ingredient in request_for_production2:
        debug()
        debug("==================")
        debug(item)
        debug()
        requests = dict_bp({item: amount})
        if go_to_final_ingredient:
            get_requests(requests, new_request(item, amount), final_ingredients)
        debug(requests)
        book.append_bp(get_bp(item, amount, requests), index)

    print()
    print("==================")
    print("book")
    print()
    print(book.to_str())
    print("==================")
