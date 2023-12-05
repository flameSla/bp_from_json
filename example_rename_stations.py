import os
from bp_from_json import blueprint


modified_bps = []


# ====================================
def input_def(text, default):
    str = input(text + "[" + default + "]:")
    return str if str else default


# ====================================
class renamer:
    def __init__(self):
        self.dictionary_for_renaming = {
            "[L] [item=iron-ore] 4-Stop": "[L] 4-Stop",
            "[L] [item=copper-ore] 4-Stop": "[L] 4-Stop",
            "[L] [item=coal] 4-Stop": "[L] 4-Stop",
            "[L] [item=stone] 4-Stop": "[L] 4-Stop",
            "[L] [item=uranium-ore] 4-Stop": "[L] 4-Stop",
            "[Exit Check Full Cargo] [item=iron-ore]": "[Exit Check Full Cargo]",
            "[Exit Check Full Cargo] [item=copper-ore]": "[Exit Check Full Cargo]",
            "[Exit Check Full Cargo] [item=coal]": "[Exit Check Full Cargo]",
            "[Exit Check Full Cargo] [item=stone]": "[Exit Check Full Cargo]",
            "[Exit Check Full Cargo] [item=uranium-ore]": "[Exit Check Full Cargo]",
        }

    def is_the_name_to_be_renamed(self, name):
        return name in self.dictionary_for_renaming

    def rename(self, name):
        return self.dictionary_for_renaming.get(name, None)


# ====================================
def get_filename(bp):
    return "{} [index={:03d}]".format(bp.read_label(), bp.data.get("index", 0))


# ====================================
def get_path(bps):
    path = "root/"
    for bp in bps:
        if bp.is_blueprint_book():
            path += get_filename(bp) + "/"
    return path


# ====================================
def rename_stations_in_the_bp(bp, bp_name, renamer_for_bp):
    bp_name_is_displayed = False
    for entity in bp.get_entities():
        if "train-stop" in entity.read_name():
            old_name = entity.read("station")
            if renamer_for_bp.is_the_name_to_be_renamed(old_name):
                if not bp_name_is_displayed:
                    print()
                    print("Renaming stations")
                    print()
                    print(bp_name)
                    bp_name_is_displayed = True
                    modified_bps.append(bp_name)
                entity.set_station(renamer_for_bp.rename(old_name))
                print("\t{} -> {}".format(old_name, entity.read("station")))
                if str(entity.read("station")) == "[Exit Check Full Cargo]":
                    # entity.data["control_behavior"]["read_stopped_train"] = True
                    # entity.data["control_behavior"]["train_stopped_signal"] = {
                    #     "type": "virtual",
                    #     "name": "signal-T",
                    # }

                    # id = entity.data["connections"]["1"]["green"][0]["entity_id"]
                    # programmable_speaker = [e for e in bp.get_entities() if e.data["entity_number"] == id][0]
                    # programmable_speaker.data['control_behavior']["circuit_condition"]["first_signal"]["name"] = "signal-everything"
                    pass
                else:
                    pass
                    # print("{} == {}".format(entity.read("station"), "[Exit Check Full Cargo]"))


# ====================================
def changing_schedules_in_the_bp(bp, bp_name, renamer_for_bp):
    bp_name_is_displayed = False
    if "schedules" in bp.obj:
        for schedule in bp.obj["schedules"]:
            name_for_adding_station = ""
            position_for_adding_a_station = -1
            for i in range(len(schedule.get("schedule", []))):
                s = schedule["schedule"][i]
                old_name = s.get("station", "")
                if renamer_for_bp.is_the_name_to_be_renamed(old_name):
                    if "[Exit Check Full Cargo]" in old_name:
                        name_for_adding_station = old_name
                        position_for_adding_a_station = i
                    if not bp_name_is_displayed:
                        print()
                        print("Changing schedules")
                        print()
                        print(bp_name)
                        bp_name_is_displayed = True
                        modified_bps.append(bp_name)
                    s["station"] = renamer_for_bp.rename(old_name)
                    print("\t{} -> {}".format(old_name, s["station"]))
            if name_for_adding_station:
                # [Exit Check Full Cargo] [Waiting] [item=iron-ore]
                name_for_adding_station = name_for_adding_station.replace("[Exit Check Full Cargo]", "[Waiting]")
                schedule["schedule"].insert(
                    position_for_adding_a_station + 1,
                    {"station": name_for_adding_station},
                )


################################################################
#
# main
if __name__ == "__main__":
    renaming_for_stations = renamer()

    exchange_str = input_def("bp:(string or filename.txt)", "bp.txt")
    if os.path.exists(exchange_str):
        with open(exchange_str, "r") as f:
            exchange_str = f.read()

    book = blueprint.from_string(exchange_str)
    bps = book.get_all_bp()
    for i in range(len(bps)):
        bp, path = bps[i]
        if not bp.is_blueprint_book():
            # "blueprint"
            # "upgrade_planner"
            # "deconstruction_planner"
            bp_name = get_path(path) + get_filename(bp)
            # print("blueprint: {}".format(bp_name))

            rename_stations_in_the_bp(bp, bp_name, renaming_for_stations)
            changing_schedules_in_the_bp(bp, bp_name, renaming_for_stations)

        else:
            # bp_name = get_path(path) + get_filename(bp)
            # print("blueprint book: {}".format(bp_name))
            pass

    print()
    print("==================")
    print("modified_bps")
    print()
    for bp in modified_bps:
        print(bp)

    # print(bp.to_str())
    book.set_label(book.read_label() + " - renamed stations")
    book.to_file("bp_out.ignore")
