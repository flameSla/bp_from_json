from bp_from_json import blueprint
from bp_from_json import entity
from bp_from_json import v2_0_34


# from typing import Any
from typing import List
from typing import Dict
from typing import Tuple


# ====================================
Wire_circuit_green = 2
Wire_circuit_red = 1
Wire_combinator_input_green = 2
Wire_combinator_input_red = 1
Wire_combinator_output_green = 4
Wire_combinator_output_red = 3
Wire_pole_copper = 5
Wire_power_switch_left_copper = 5
Wire_power_switch_right_copper = 6


# ====================================
font = (
    (
        "xxxx",
        "x .x",
        "x. x",
        "x..x",
        "x .x",
        "x. x",
        "xxxx",
    ),
    (
        "...x",
        ". xx",
        ".x x",
        "x..x",
        ". .x",
        ".. x",
        "...x",
    ),
    (
        "xxxx",
        ". .x",
        ".. x",
        "...x",
        ". x.",
        ".x .",
        "xxxx",
    ),
    (
        "xxxx",
        ". x.",
        ".x .",
        "xxxx",
        ". x.",
        ".x .",
        "x...",
    ),
    (
        "x..x",
        "x .x",
        "x. x",
        "xxxx",
        ". .x",
        ".. x",
        "...x",
    ),
    (
        "xxxx",
        "x ..",
        "x. .",
        "xxxx",
        ". .x",
        ".. x",
        "xxxx",
    ),
    (
        "...x",
        ". x.",
        ".x .",
        "xxxx",
        "x .x",
        "x. x",
        "xxxx",
    ),
    (
        "xxxx",
        ". x.",
        ".x .",
        "x...",
        "x ..",
        "x. .",
        "x...",
    ),
    (
        "xxxx",
        "x .x",
        "x. x",
        "xxxx",
        "x .x",
        "x. x",
        "xxxx",
    ),
    (
        "xxxx",
        "x .x",
        "x. x",
        "xxxx",
        ". x.",
        ".x .",
        "x...",
    ),
)


# ====================================
# Creating a table of virtual signals
# When creating display segments, we will use the signals from this table
def get_signals() -> List:
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    for quality in ("normal", "uncommon", "rare", "epic", "legendary"):
        for letter in alphabet:
            res.append(
                {
                    "type": "virtual",
                    "quality": quality,
                    "name": "signal-{}".format(letter),
                }
            )
    return res


# ====================================
# used when creating a constant combinator
def get_filter(index, signal_type, name, quality, count) -> Dict:
    return {
        "index": index,
        "type": signal_type,
        "name": name,
        "quality": quality,
        "comparator": "=",
        "count": count,
    }


# ====================================
# used when creating a lamp
def get_control_behavior_for_lamp(signal_type, name, quality, constant) -> Dict:
    return {
        "circuit_enabled": True,
        "circuit_condition": {
            "first_signal": {"type": signal_type, "quality": quality, "name": name},
            "constant": constant,
            "comparator": "<",
        },
    }


# ====================================
def add_filtr_constant_combinator(section, filtr):
    section["filters"].append(filtr)


# ====================================
def add_section_constant_combinator(constant_combinator: entity, index) -> Dict:
    sections = constant_combinator.data["control_behavior"]["sections"]["sections"]
    section = {"index": index, "filters": []}
    sections.append(section)
    return section


# ====================================
def add_constant_combinator(bp: blueprint, x, y) -> entity:
    constant_combinator = entity.new_entity("constant-combinator", x, y)
    constant_combinator.set("control_behavior", {"sections": {"sections": []}})
    bp.append_entity(constant_combinator)
    return constant_combinator


# ====================================
def add_arithmetic_combinator(bp: blueprint, x, y, direction=None) -> entity:
    arithmetic_combinator = entity.new_entity("arithmetic-combinator", x, y, direction)
    arithmetic_combinator.set("control_behavior", {"arithmetic_conditions": {}})
    bp.append_entity(arithmetic_combinator)
    return arithmetic_combinator


# ====================================
def add_medium_electric_pole(bp: blueprint, x, y, direction=None) -> entity:
    medium_electric_pole = entity.new_entity("medium-electric-pole", x, y, direction)
    bp.append_entity(medium_electric_pole)
    return medium_electric_pole


# ====================================
def get_segments(font: Tuple) -> Dict:
    signals = get_signals()

    width = len(font[0][0])
    height = len(font[0])

    res: Dict = {}
    res["width"] = width
    res["height"] = height
    res["segments"] = []

    font2: List = ["".join(a) for a in font]

    if not all([len(font2[0]) == len(a) for a in font2]):
        print()
        for letter in font2:
            print(">{}<".format(letter))
        raise Exception(
            "Incorrect font. The size of one of the letters is different from the others."
        )

    index = 0
    for segment in range(len(font2[0])):
        segment_dict: Dict = {}
        segment_dict["enabled"] = True
        constant = 0
        for letter in range(len(font2)):
            bit = font2[letter][segment]
            if bit == " ":
                # The lamp is not needed
                # checking that the entire column is equal to " "
                if not all([a[segment] == " " for a in font2]):
                    print()
                    for letter in font2:
                        print(">{}<".format(letter))
                    raise Exception(
                        "Incorrect font. the entire column should be equal to ' '"
                    )

                segment_dict["enabled"] = False
                break
            elif bit == "x":
                constant += 1 << (31 - letter)

        constant = constant - 2**32 if constant >= 2**31 else constant

        if segment_dict["enabled"]:
            index += 1
            signal = signals.pop(0)
            signal_type = signal["type"]
            name = signal["name"]
            quality = signal["quality"]
            segment_dict["filter"] = get_filter(
                index, signal_type, name, quality, constant
            )
            segment_dict["control_behavior"] = get_control_behavior_for_lamp(
                signal_type, name, quality, 0
            )
        res["segments"].append(segment_dict)

    # print(res)
    # print(len(res))
    return res


# ====================================
def add_display(bp: blueprint, segments: Dict, start_pos: complex):
    def get_pos_from_index(index: int, width: int) -> complex:
        y = index // width
        x = index % width
        return complex(x, y)

    def is_position_correct(pos: complex, width: int, height: int) -> bool:
        x = pos.real
        y = pos.imag
        return (x >= 0) and (x <= width) and (y >= 0) and (y <= height)

    def get_index_from_pos(pos: complex, width: int) -> int:
        x = pos.real
        y = pos.imag
        return int(x + y * width)

    width = segments["width"]
    height = segments["height"]
    # adding lamps
    entity_number_for_lamps = []
    for index in range(len(segments["segments"])):
        segment = segments["segments"][index]
        if segment["enabled"]:
            pos = start_pos + get_pos_from_index(index, width)
            lamp = entity.new_entity("small-lamp", pos.real, pos.imag)
            lamp.data["control_behavior"] = segment["control_behavior"]
            bp.append_entity(lamp)
            entity_number_for_lamps.append(lamp.read_entity_number())
        else:
            entity_number_for_lamps.append(-1)

    # adding wires for lamps
    offsets = (
        # offset table for finding the nearest lamp
        -1 + 0j,
        +0 - 1j,
        -1 - 1j,
        +1 - 1j,
        +1 + 0j,
        +1 + 1j,
        +0 + 1j,
        -1 + 1j,
    )

    wires = []
    first_lamp = True  # we skip the first lamp, there is nothing to connect it with
    for cur_index in range(len(entity_number_for_lamps)):
        entity_number_1 = entity_number_for_lamps[cur_index]
        if entity_number_1 > 0:  # skip the empty cells
            if first_lamp:
                first_lamp = False
                continue
            else:
                # looking for the closest lamp to the current lamp
                for offset in offsets:
                    pos = get_pos_from_index(cur_index, width) + offset
                    if is_position_correct(pos, width, height):
                        index_0 = get_index_from_pos(pos, width)
                        entity_number_0 = entity_number_for_lamps[index_0]
                        if entity_number_0 > 0:
                            wires.append(
                                [
                                    entity_number_0,
                                    Wire_circuit_green,
                                    entity_number_1,
                                    Wire_circuit_green,
                                ]
                            )
                            break

    if "wires" in bp.obj:
        bp.obj["wires"].extend(wires)
    else:
        bp.obj["wires"] = wires

    pos = start_pos + 2 - 1j
    constant_combinator = add_constant_combinator(bp, pos.real, pos.imag)
    section = add_section_constant_combinator(constant_combinator, 1)
    for segment in (s for s in segments["segments"] if s["enabled"]):
        add_filtr_constant_combinator(section, segment["filter"])

    pos = start_pos + 0.5 - 1j
    arithmetic_combinator_1 = add_arithmetic_combinator(bp, pos.real, pos.imag, 12)
    control_behavior = arithmetic_combinator_1.data["control_behavior"]
    conditions = control_behavior["arithmetic_conditions"]
    conditions["first_signal"] = {"type": "virtual", "name": "signal-each"}
    conditions["second_signal"] = {"type": "virtual", "name": "signal-N"}
    conditions["operation"] = "<<"
    conditions["output_signal"] = {"type": "virtual", "name": "signal-each"}
    conditions["first_signal_networks"] = {"red": False, "green": True}
    conditions["second_signal_networks"] = {"red": True, "green": False}

    pos -= 1j
    arithmetic_combinator_2 = add_arithmetic_combinator(bp, pos.real, pos.imag, 12)
    control_behavior = arithmetic_combinator_2.data["control_behavior"]
    conditions = control_behavior["arithmetic_conditions"]
    conditions["first_signal"] = {"type": "virtual", "name": "signal-each"}
    conditions["second_constant"] = 10
    conditions["operation"] = "%"
    conditions["output_signal"] = {"type": "virtual", "name": "signal-N"}

    pos -= 1j
    arithmetic_combinator_3 = add_arithmetic_combinator(bp, pos.real, pos.imag, 12)
    control_behavior = arithmetic_combinator_3.data["control_behavior"]
    conditions = control_behavior["arithmetic_conditions"]
    conditions["first_signal"] = {"type": "virtual", "name": "signal-each"}
    conditions["second_constant"] = 10
    conditions["operation"] = "/"
    conditions["output_signal"] = {"type": "virtual", "name": "signal-N"}

    entity_number_for_lamp = [e for e in entity_number_for_lamps if e > 0][0]
    bp.obj["wires"].append(
        [
            entity_number_for_lamp,
            Wire_circuit_green,
            arithmetic_combinator_1.read_entity_number(),
            Wire_combinator_output_green,
        ]
    )
    bp.obj["wires"].append(
        [
            constant_combinator.read_entity_number(),
            Wire_circuit_green,
            arithmetic_combinator_1.read_entity_number(),
            Wire_combinator_input_green,
        ]
    )
    bp.obj["wires"].append(
        [
            arithmetic_combinator_1.read_entity_number(),
            Wire_combinator_input_red,
            arithmetic_combinator_2.read_entity_number(),
            Wire_combinator_output_red,
        ]
    )
    bp.obj["wires"].append(
        [
            arithmetic_combinator_2.read_entity_number(),
            Wire_combinator_input_red,
            arithmetic_combinator_3.read_entity_number(),
            Wire_combinator_input_red,
        ]
    )

    pos_pole_west = start_pos - 1
    pos_pole_east = start_pos + width
    if (pos_pole_east - pos_pole_west).real > 7:
        raise Exception("The distance between the poles is more than 7")

    pole_west = add_medium_electric_pole(bp, pos_pole_west.real, pos_pole_west.imag)
    pole_east = add_medium_electric_pole(bp, pos_pole_east.real, pos_pole_east.imag)
    bp.obj["wires"].append(
        [
            arithmetic_combinator_3.read_entity_number(),
            Wire_combinator_input_red,
            pole_east.read_entity_number(),
            Wire_circuit_red,
        ]
    )
    bp.obj["wires"].append(
        [
            arithmetic_combinator_3.read_entity_number(),
            Wire_combinator_output_red,
            pole_west.read_entity_number(),
            Wire_circuit_red,
        ]
    )
    bp.obj["wires"].append(
        [
            pole_east.read_entity_number(),
            Wire_pole_copper,
            pole_west.read_entity_number(),
            Wire_pole_copper,
        ]
    )

    def add_poles(start_pole: entity, height):
        x, y = start_pole.get_pos().get_tuple()
        end_y = y + height - 1

        additional_pole_is_needed = True
        while additional_pole_is_needed:
            next_y = end_y if end_y - y <= 7 else y + 7
            additional_pole_is_needed = False if end_y - y <= 7 else True

            new_pole = add_medium_electric_pole(bp, x, next_y)
            bp.obj["wires"].append(
                [
                    start_pole.read_entity_number(),
                    Wire_pole_copper,
                    new_pole.read_entity_number(),
                    Wire_pole_copper,
                ]
            )
            start_pole = new_pole
            y = next_y

    add_poles(pole_east, height)
    add_poles(pole_west, height)

    bp.obj["snap-to-grid"] = {"x": width + 1, "y": height + 3}


######################################
#
# main
if __name__ == "__main__":

    bp = blueprint.new_blueprint(v2_0_34)

    segments = get_segments(font)
    add_display(bp, segments, 0.5 + 0.5j)
    label = "display"
    bp.set_label_color(1, 0, 1)
    bp.set_label(label)

    print()
    print(label)
    print("==================================")
    print(bp.to_str())
    print("==================================")
