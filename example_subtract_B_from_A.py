from pathlib import Path
from bp_from_json import blueprint
from bp_from_json import get_blueprint


# ====================================
def input_def(text, default):
    str = input(text + "[" + default + "]:")
    return str if str else default


# ====================================
def substract(A, B):
    A.normalize_entities()
    B.normalize_entities()
    result = []

    B_dict = {}
    for e in B.get_entities():
        pos = e.get_pos().get_tuple()
        B_dict[pos] = e
    # print()
    # print('==================')
    # print('B_dict')
    # print()
    # print('B_dict = ', type(B_dict), B_dict)

    for e in A.get_entities():
        pos = e.get_pos()
        key = pos.get_tuple()
        # we copy the rails forcibly (bp borders)
        if e.read_name() != "straight-rail" and key in B_dict:
            line = "[{:010.2f}, {:010.2f}]".format(pos.read_x(), pos.read_y())
            if e == B_dict[key]:
                # line += " - entities are equal ( {} )".format(e.read_name())
                pass
            else:
                if e.read_name() == "small-electric-pole":
                    # The differences are only in the "entity_number" & "neighbours"
                    pass
                elif "assembling-machine" in e.read_name():
                    if e.read_recipe() != B_dict[key].read_recipe():
                        line += (
                            " - entities are not equal {} != {} recipe: {}, {}".format(
                                e.read_name(),
                                B_dict[key].read_name(),
                                e.read_recipe(),
                                B_dict[key].read_recipe(),
                            )
                        )
                        print(line)
                        print()
                elif e.read_name() in ("steel-furnace", "stone-furnace") and B_dict[key].read_name() in ("steel-furnace", "stone-furnace"):
                    pass
                else:
                    line += " - entities are not equal {} != {}\n{}\n{}".format(
                        e.read_name(), B_dict[key].read_name(), e.data, B_dict[key].data
                    )
                    print(line)
                    print()
        else:
            result.append(e.data)

    bp = blueprint.new_blueprint()
    bp.obj["entities"] = result
    return bp


######################################
#
# main
if __name__ == "__main__":
    bp_A = get_blueprint("bp A (string or filename.txt)", "example_subtract_A.ignore")
    if not bp_A.is_blueprint:
        raise Exception("it only works with blueprints")

    bp_B = get_blueprint("bp B (string or filename.txt)", "example_subtract_B.ignore")
    if not bp_B.is_blueprint:
        raise Exception("it only works with blueprints")

    bp = substract(bp_A, bp_B)
    bp.to_file("example_subtract_result.ignore")
