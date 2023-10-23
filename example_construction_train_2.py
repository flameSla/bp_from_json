"""
construction_train
it is necessary to change the script for the formation of the train by specifying the number of items
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
def add_train(bp, train_number, locomotives, cars, station_name):
    train_car_position = 0

    train_length = (locomotives + cars) * 7 - 1
    number_of_rails = math.ceil(train_length / 2) + 2
    for i in range(number_of_rails):
        rail = entity.new_entity(
            "straight-rail", i * 2 - 1, train_number * 4 + 1, direction=2
        )
        bp.append_entity(rail)

    train_stop = entity.new_entity(
        "train-stop", 7 * train_car_position + 1, train_number * 4 - 1, direction=6
    )
    train_stop.set_station(station_name)
    bp.append_entity(train_stop)

    for i in range(locomotives):
        locomotive = entity.new_entity(
            "locomotive",
            7 * train_car_position + 4,
            train_number * 4 + 1,
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
        train_number * 4 + 1,
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
    pos = 0
    for key, val in filtrs.items():
        inserter = entity.new_entity(
            "stack-inserter", 7 * train_car_position + 1.5 + pos, train_number * 4 - 0.5
        )
        bp.append_entity(inserter)

        requester = entity.new_entity(
            "logistic-chest-requester",
            7 * train_car_position + 1.5 + pos,
            train_number * 4 - 1.5,
        )

        requester.append_request_filters({"index": 1, "name": key, "count": items[key]})

        requester.set_request_from_buffers("true")
        bp.append_entity(requester)

        pos += 1
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
            if slot_count >= 40 or (len(filtrs) >= 6 and new_item):
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
    exchange_str = input("bp to be built:(string or filename.txt)")
    if os.path.exists(exchange_str):
        bp = blueprint.from_file(exchange_str)
    else:
        bp = blueprint.from_string(exchange_str)

    necessary_items_for_construction = bp.get_all_items()
    print("\nbp contains:")
    print(necessary_items_for_construction)

    # "item name": amount
    additional_items = dict_bp({"speed-module-3": 6588, "productivity-module-3": 2557})

    print("\nadditional items:")
    print(additional_items)

    contents = additional_items  # + necessary_items_for_construction
    # contents += bp.get_all_tiles()

    debug("\ncontents:")
    debug(contents)

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
