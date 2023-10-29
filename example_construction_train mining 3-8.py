"""
construction_train
"""

from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import entity
from bp_from_json import get_items
import sys
import os
import argparse
import math
import uuid
import enum


#############################################
def debug(*args):
    if opt.d:
        print(*args, file=sys.stderr, flush=True)


#############################################
@enum.unique
class type_of_train(enum.Enum):
    requester_trains = 1
    filtered_trains = 2


#############################################
def get_y(train_number):
    return train_number * 6


#############################################
def add_train(bp, train_number, locomotives, cars, station_name):
    train_car_position = 0

    train_length = (locomotives + cars) * 7 - 1
    number_of_rails = math.ceil(train_length / 2) + 2
    for i in range(number_of_rails):
        rail = entity.new_entity(
            "straight-rail", i * 2 - 1, get_y(train_number) + 1, direction=2
        )
        bp.append_entity(rail)

    train_stop = entity.new_entity(
        "train-stop", 7 * train_car_position + 1, get_y(train_number) - 1, direction=6
    )
    train_stop.set_station(station_name)
    bp.append_entity(train_stop)

    for i in range(locomotives):
        locomotive = entity.new_entity(
            "locomotive",
            7 * train_car_position + 4,
            get_y(train_number) + 1,
            orientation=0.75,
        )
        locomotive.update_items({"nuclear-fuel": 3}, name_verification=False)
        bp.append_entity(locomotive)
        train_car_position += 1

    return train_car_position


#############################################
def create_wagon(train_car_position, train_number):
    return entity.new_entity(
        "cargo-wagon",
        7 * train_car_position + 4,
        get_y(train_number) + 1,
        orientation=0.75,
    )


#############################################
def wagon_close_slots(cargo_wagon, slot_count):
    if slot_count < 40:
        cargo_wagon.set_inventory_bar(slot_count)
    while slot_count < 40:
        cargo_wagon.set_inventory_filter(
            {"index": slot_count + 1, "name": "linked-chest"}
        )
        slot_count += 1


#############################################
def append_chests(bp, filtrs, train_car_position, train_number, items):
    for i, (key, val) in enumerate(filtrs.items()):
        if i <= 5:
            x1 = 7 * train_car_position + 1.5 + i
            y1 = get_y(train_number) - 0.5
            y2 = get_y(train_number) - 1.5
            d = 1
        elif i <= 11:
            x1 = 7 * train_car_position + 1.5 + i - 6
            y1 = get_y(train_number) + 2.5
            y2 = get_y(train_number) + 3.5
            d = 4
        inserter = entity.new_entity("stack-inserter", x1, y1)
        inserter.set("direction", d)
        bp.append_entity(inserter)

        requester = entity.new_entity(
            "logistic-chest-requester",
            x1,
            y2,
        )

        requester.append_request_filters({"index": 1, "name": key, "count": items[key]})

        requester.set_request_from_buffers("true")
        bp.append_entity(requester)

    filtrs.clear()


#############################################
def requester_trains(
    bp, contents, train_number, train_car_position, locomotives, cars, station_name
):
    cargo_wagon = create_wagon(train_car_position, train_number)

    slot_count = 0
    items = get_items()
    for item, amount in contents.items():
        stack_size = items[item]

        if item == "landfill":
            # for landfill, we start a new train,
            #   so it's easier to remove these trains from the bp
            bp.append_entity(cargo_wagon)
            train_number += 1
            train_car_position = add_train(
                bp, train_number, locomotives, cars, station_name
            )
            slot_count = 0
            cargo_wagon = create_wagon(train_car_position, train_number)

        while amount > 0:
            slots = math.ceil(amount / stack_size)
            if slot_count + slots > 40:
                add_items = (40 - slot_count) * stack_size
                amount -= add_items
                cargo_wagon.update_items({item: add_items}, name_verification=False)
                # Add a new wagon
                train_car_position += 1
                if train_car_position >= locomotives + cars:
                    train_number += 1
                    train_car_position = add_train(
                        bp, train_number, locomotives, cars, station_name
                    )

                bp.append_entity(cargo_wagon)
                slot_count = 0
                cargo_wagon = create_wagon(train_car_position, train_number)

            else:
                cargo_wagon.update_items({item: amount}, name_verification=False)
                amount = 0
                slot_count += slots

    bp.append_entity(cargo_wagon)
    bp.set_icons(1, "virtual", "signal-B")
    bp.set_icons(2, "item", "construction-robot")


#############################################
def filtered_trains(
    bp, contents, train_number, train_car_position, locomotives, cars, station_name
):
    cargo_wagon = create_wagon(train_car_position, train_number)

    slot_count = 0
    filtrs = dict_bp()
    items = get_items()
    for item, amount in contents.items():
        stack_size = items[item]
        slots = math.ceil(amount / stack_size)

        if item == "landfill":
            # for landfill, we start a new train,
            #   so it's easier to remove these trains from the bp
            wagon_close_slots(cargo_wagon, slot_count)
            append_chests(bp, filtrs, train_car_position, train_number, items)
            bp.append_entity(cargo_wagon)
            train_number += 1
            train_car_position = add_train(
                bp, train_number, locomotives, cars, station_name
            )
            slot_count = 0
            cargo_wagon = create_wagon(train_car_position, train_number)

        for _ in range(slots):
            new_item = item not in filtrs
            if slot_count >= 40 or (len(filtrs) >= 12 and new_item):
                # Add a new wagon
                wagon_close_slots(cargo_wagon, slot_count)
                append_chests(bp, filtrs, train_car_position, train_number, items)

                train_car_position += 1
                if train_car_position >= locomotives + cars:
                    train_number += 1
                    train_car_position = add_train(
                        bp, train_number, locomotives, cars, station_name
                    )

                bp.append_entity(cargo_wagon)
                slot_count = 0
                cargo_wagon = create_wagon(train_car_position, train_number)

            cargo_wagon.set_inventory_filter({"index": slot_count + 1, "name": item})
            filtrs += {item: 1}

            slot_count += 1

    wagon_close_slots(cargo_wagon, slot_count)
    append_chests(bp, filtrs, train_car_position, train_number, items)

    bp.append_entity(cargo_wagon)
    bp.set_icons(1, "virtual", "signal-B")
    bp.set_icons(2, "item", "logistic-chest-requester")


#############################################
def get_bp(locomotives, cars, contents, station_name, type_of_Train):
    bp = blueprint.new_blueprint()

    train_number = 0
    train_car_position = add_train(bp, train_number, locomotives, cars, station_name)

    if type_of_Train == type_of_train.requester_trains:
        requester_trains(
            bp,
            contents,
            train_number,
            train_car_position,
            locomotives,
            cars,
            station_name,
        )
    elif type_of_Train == type_of_train.filtered_trains:
        filtered_trains(
            bp,
            contents,
            train_number,
            train_car_position,
            locomotives,
            cars,
            station_name,
        )

    bp.set_label_color(1, 0, 1)
    bp.set_label(f"{locomotives}-{cars} construction_train")

    print("==================================")
    print(str(type_of_Train))
    print(bp.to_str())
    print("==================================")


######################################
#
# main
if __name__ == "__main__":
    exchange_str = ""
    parser = argparse.ArgumentParser(
        description="example: python construction_train.py"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", dest="d", help="debug output on STDERR"
    )
    opt = parser.parse_args()

    locomotives = input("locomotives:")
    cars = input("cars:")
    # exchange_str = input('bp to be built:(string or filename.txt)')
    exchange_str = r"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"
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    necessary_items_for_construction = bp.get_all_items()
    print("\nbp contains:")
    print(necessary_items_for_construction)

    # "item name": amount
    additional_items = dict_bp(
        {
            "construction-robot": 50,
            "logistic-robot": 50,
            "roboport": 10,
            "radar": 50,
            "repair-pack": 100,
            "cliff-explosives": 40,
            "laser-turret": 50,
            "express-transport-belt": 2000,
            "express-underground-belt": 200,
            "express-splitter": 50,
            "stack-inserter": 50,
            "fast-inserter": 50,
            "filter-inserter": 50,
            "electric-mining-drill": 250,
            "speed-module": 750,
            "medium-electric-pole": 50,
        }
    )

    print("\nadditional items:")
    print(additional_items)

    contents = additional_items + necessary_items_for_construction
    contents += bp.get_all_tiles()

    contents2 = dict_bp(contents)
    contents2["fast-transport-belt"] = contents2.pop("express-transport-belt", None)
    contents2["fast-underground-belt"] = contents2.pop("express-underground-belt", None)
    contents2["fast-splitter"] = contents2.pop("express-splitter", None)

    debug("\ncontents:")
    debug(contents)
    debug("\ncontents:")
    debug(contents2)


    print()
    print('==================')
    print('blue')
    print()
    station_name = str(uuid.uuid4())
    get_bp(
        int(locomotives),
        int(cars),
        contents,
        station_name,
        type_of_train.requester_trains,
    )
    get_bp(
        int(locomotives),
        int(cars),
        contents,
        station_name,
        type_of_train.filtered_trains,
    )

    print()
    print('==================')
    print('red')
    print()
    station_name = str(uuid.uuid4())
    get_bp(
        int(locomotives),
        int(cars),
        contents2,
        station_name,
        type_of_train.requester_trains,
    )
    get_bp(
        int(locomotives),
        int(cars),
        contents2,
        station_name,
        type_of_train.filtered_trains,
    )
