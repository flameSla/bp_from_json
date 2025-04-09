from bp_from_json import blueprint
from bp_from_json import v2_0_34
from bp_from_json import list_of_qualities


# bp_text = """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"""

upgrade_planner_text = """0eNqNjsEKwjAQRP9lzimI1ULyKyKy0LUE0k1Mt2op+XeTQ++edmZ3lnk71jRlGvmRAolwhtuxsKqXaWl6ppQ4V3nb8cxxbjvdEsOBRb1uMBCam180CncfCgHFQON/UYPXSqFdHTJlbr9eRv7Cncq9GeXaenB2B6fBu3L5KHDX4Wwv1tbR237oS/kBNRFH1A=="""

all_items_1 = [
    [
        [("wooden-chest", "entity")],
        [("wooden-chest", "iron-chest", "entity"), ("iron-chest", "entity")],
        [("iron-chest", "entity")],
        [("steel-chest", "entity")],
        [
            ("wooden-chest", "steel-chest", "entity"),
            ("iron-chest", "steel-chest", "entity"),
            ("steel-chest", "entity"),
        ],
        [("active-provider-chest", "entity")],
        [("passive-provider-chest", "entity")],
        [("storage-chest", "entity")],
        [("buffer-chest", "entity")],
        [("requester-chest", "entity")],
    ],
    [[("storage-tank", "entity")], [("pump", "entity")]],
    # "transport-belt", "entity",
    # "fast-transport-belt", "entity",
    # "express-transport-belt", "entity",
    # "turbo-transport-belt", "entity",
    # "underground-belt", "entity",
    # "fast-underground-belt", "entity",
    # "express-underground-belt", "entity",
    # "turbo-underground-belt", "entity",
    # "splitter", "entity",
    # "fast-splitter", "entity",
    # "express-splitter", "entity",
    # "turbo-splitter", "entity",
    [
        [("burner-inserter", "entity")],
        [("inserter", "entity")],
        [("long-handed-inserter", "entity")],
        [
            ("burner-inserter", "fast-inserter", "entity"),
            ("inserter", "fast-inserter", "entity"),
            ("fast-inserter", "entity"),
            ("bulk-inserter", "fast-inserter", "entity"),
        ],
        [("stack-inserter", "fast-inserter", "entity")],
        [("fast-inserter", "entity")],
        [
            ("burner-inserter", "bulk-inserter", "entity"),
            ("inserter", "bulk-inserter", "entity"),
            ("fast-inserter", "bulk-inserter", "entity"),
            ("bulk-inserter", "entity"),
        ],
        [("stack-inserter", "bulk-inserter", "entity")],
        [("bulk-inserter", "entity")],
        [("fast-inserter", "stack-inserter", "entity")],
        [("bulk-inserter", "stack-inserter", "entity")],
        [("stack-inserter", "entity")],
    ],
    [
        [("small-electric-pole", "entity")],
        [
            ("small-electric-pole", "medium-electric-pole", "entity"),
            ("medium-electric-pole", "entity"),
        ],
        [("medium-electric-pole", "entity")],
        [("big-electric-pole", "entity")],
        [("substation", "entity")],
    ],
    # "pipe", "entity",
    # "pipe-to-ground", "entity",
    #
    # "straight-rail", "entity",
    # "rail-ramp", "entity",
    # "rail-support", "entity",
    # "train-stop", "entity",
    # "rail-signal", "entity",
    # "rail-chain-signal", "entity",
    [
        [("locomotive", "entity")],
        [("cargo-wagon", "entity")],
        [("fluid-wagon", "entity")],
        [("artillery-wagon", "entity")],
        [("car", "entity")],
        [("tank", "entity")],
        [("spidertron", "entity")],
    ],
    [[("roboport", "entity")]],
    # "small-lamp", "entity",
    # "arithmetic-combinator", "entity",
    # "decider-combinator", "entity",
    # "selector-combinator", "entity",
    # "constant-combinator", "entity",
    # "power-switch", "entity",
    # "programmable-speaker", "entity",
    # "display-panel", "entity",
]


all_items_2 = [
    [[("solar-panel", "entity")], [("accumulator", "entity")]],
    [
        [("boiler", "entity")],
        [("steam-engine", "entity")],
        [("heating-tower", "entity")],
        [("nuclear-reactor", "entity")],
        [("heat-pipe", "entity")],
        [("heat-exchanger", "entity")],
        [("steam-turbine", "entity")],
        [("fusion-reactor", "entity")],
        [("fusion-generator", "entity")],
    ],
    [
        [("burner-mining-drill", "entity")],
        [("electric-mining-drill", "entity")],
        [("big-mining-drill", "entity")],
        [("offshore-pump", "entity")],
        [("pumpjack", "entity")],
    ],
    [
        [("stone-furnace", "entity")],
        [("steel-furnace", "stone-furnace", "entity"), ("stone-furnace", "entity")],
        [("steel-furnace", "entity")],
        [("stone-furnace", "steel-furnace", "entity"), ("steel-furnace", "entity")],
        [("electric-furnace", "entity")],
        [("foundry", "entity")],
        [("recycler", "entity")],
        [("agricultural-tower", "entity")],
        [("biochamber", "entity")],
        [("captive-biter-spawner", "entity")],
        [("assembling-machine-1", "entity")],
        [
            ("assembling-machine-1", "entity"),
            ("assembling-machine-2", "assembling-machine-1", "entity"),
            ("assembling-machine-3", "assembling-machine-1", "entity"),
        ],
        [("assembling-machine-2", "entity")],
        [
            ("assembling-machine-1", "assembling-machine-2", "entity"),
            ("assembling-machine-2", "entity"),
            ("assembling-machine-3", "assembling-machine-2", "entity"),
        ],
        [("assembling-machine-3", "entity")],
        [
            ("assembling-machine-1", "assembling-machine-3", "entity"),
            ("assembling-machine-2", "assembling-machine-3", "entity"),
            ("assembling-machine-3", "entity"),
        ],
        [("oil-refinery", "entity")],
        [("chemical-plant", "entity")],
        [("centrifuge", "entity")],
        [("electromagnetic-plant", "entity")],
        [("cryogenic-plant", "entity")],
        [("lab", "entity")],
        [("biolab", "entity")],
    ],
    [[("lightning-rod", "entity")], [("lightning-collector", "entity")]],
    [[("beacon", "entity")]],
    [
        [("speed-module", "item")],
        [
            ("speed-module", "item"),
            ("speed-module-2", "speed-module", "item"),
            ("speed-module-3", "speed-module", "item"),
        ],
        [("speed-module-2", "item")],
        [
            ("speed-module", "speed-module-2", "item"),
            ("speed-module-2", "item"),
            ("speed-module-3", "speed-module-2", "item"),
        ],
        [("speed-module-3", "item")],
        [
            ("speed-module", "speed-module-3", "item"),
            ("speed-module-2", "speed-module-3", "item"),
            ("speed-module-3", "item"),
        ],
        [("efficiency-module", "item")],
        [
            ("efficiency-module", "item"),
            ("efficiency-module-2", "efficiency-module", "item"),
            ("efficiency-module-3", "efficiency-module", "item"),
        ],
        [("efficiency-module-2", "item")],
        [
            ("efficiency-module", "efficiency-module-2", "item"),
            ("efficiency-module-2", "item"),
            ("efficiency-module-3", "efficiency-module-2", "item"),
        ],
        [("efficiency-module-3", "item")],
        [
            ("efficiency-module", "efficiency-module-3", "item"),
            ("efficiency-module-2", "efficiency-module-3", "item"),
            ("efficiency-module-3", "item"),
        ],
        [("quality-module", "item")],
        [
            ("quality-module", "item"),
            ("quality-module-2", "quality-module", "item"),
            ("quality-module-3", "quality-module", "item"),
        ],
        [("quality-module-2", "item")],
        [
            ("quality-module", "quality-module-2", "item"),
            ("quality-module-2", "item"),
            ("quality-module-3", "quality-module-2", "item"),
        ],
        [("quality-module-3", "item")],
        [
            ("quality-module", "quality-module-3", "item"),
            ("quality-module-2", "quality-module-3", "item"),
            ("quality-module-3", "item"),
        ],
        [("productivity-module", "item")],
        [
            ("productivity-module", "item"),
            ("productivity-module-2", "productivity-module", "item"),
            ("productivity-module-3", "productivity-module", "item"),
        ],
        [("productivity-module-2", "item")],
        [
            ("productivity-module", "productivity-module-2", "item"),
            ("productivity-module-2", "item"),
            ("productivity-module-3", "productivity-module-2", "item"),
        ],
        [("productivity-module-3", "item")],
        [
            ("productivity-module", "productivity-module-3", "item"),
            ("productivity-module-2", "productivity-module-3", "item"),
            ("productivity-module-3", "item"),
        ],
        [
            ("speed-module", "item"),
            ("speed-module-2", "speed-module", "item"),
            ("speed-module-3", "speed-module", "item"),
            ("efficiency-module", "item"),
            ("efficiency-module-2", "efficiency-module", "item"),
            ("efficiency-module-3", "efficiency-module", "item"),
            ("quality-module", "item"),
            ("quality-module-2", "quality-module", "item"),
            ("quality-module-3", "quality-module", "item"),
            ("productivity-module", "item"),
            ("productivity-module-2", "productivity-module", "item"),
            ("productivity-module-3", "productivity-module", "item"),
        ],
        [
            ("speed-module", "speed-module-2", "item"),
            ("speed-module-2", "item"),
            ("speed-module-3", "speed-module-2", "item"),
            ("efficiency-module", "efficiency-module-2", "item"),
            ("efficiency-module-2", "item"),
            ("efficiency-module-3", "efficiency-module-2", "item"),
            ("quality-module", "quality-module-2", "item"),
            ("quality-module-2", "item"),
            ("quality-module-3", "quality-module-2", "item"),
            ("productivity-module", "productivity-module-2", "item"),
            ("productivity-module-2", "item"),
            ("productivity-module-3", "productivity-module-2", "item"),
        ],
        [
            ("speed-module", "speed-module-3", "item"),
            ("speed-module-2", "speed-module-3", "item"),
            ("speed-module-3", "item"),
            ("efficiency-module", "efficiency-module-3", "item"),
            ("efficiency-module-2", "efficiency-module-3", "item"),
            ("efficiency-module-3", "item"),
            ("quality-module", "quality-module-3", "item"),
            ("quality-module-2", "quality-module-3", "item"),
            ("quality-module-3", "item"),
            ("productivity-module", "productivity-module-3", "item"),
            ("productivity-module-2", "productivity-module-3", "item"),
            ("productivity-module-3", "item"),
        ],
    ],
    [
        [("speed-module", "item")],
        [
            ("speed-module", "item"),
            ("speed-module-2", "speed-module", "item"),
            ("speed-module-3", "speed-module", "item"),
        ],
        [("efficiency-module", "item")],
        [
            ("efficiency-module", "item"),
            ("efficiency-module-2", "efficiency-module", "item"),
            ("efficiency-module-3", "efficiency-module", "item"),
        ],
        [("quality-module", "item")],
        [
            ("quality-module", "item"),
            ("quality-module-2", "quality-module", "item"),
            ("quality-module-3", "quality-module", "item"),
        ],
        [("productivity-module", "item")],
        [
            ("productivity-module", "item"),
            ("productivity-module-2", "productivity-module", "item"),
            ("productivity-module-3", "productivity-module", "item"),
        ],
        [
            ("speed-module", "item"),
            ("speed-module-2", "speed-module", "item"),
            ("speed-module-3", "speed-module", "item"),
            ("efficiency-module", "item"),
            ("efficiency-module-2", "efficiency-module", "item"),
            ("efficiency-module-3", "efficiency-module", "item"),
            ("quality-module", "item"),
            ("quality-module-2", "quality-module", "item"),
            ("quality-module-3", "quality-module", "item"),
            ("productivity-module", "item"),
            ("productivity-module-2", "productivity-module", "item"),
            ("productivity-module-3", "productivity-module", "item"),
        ],
    ],
    [
        [("speed-module-2", "item")],
        [
            ("speed-module", "speed-module-2", "item"),
            ("speed-module-2", "item"),
            ("speed-module-3", "speed-module-2", "item"),
        ],
        [("efficiency-module-2", "item")],
        [
            ("efficiency-module", "efficiency-module-2", "item"),
            ("efficiency-module-2", "item"),
            ("efficiency-module-3", "efficiency-module-2", "item"),
        ],
        [("quality-module-2", "item")],
        [
            ("quality-module", "quality-module-2", "item"),
            ("quality-module-2", "item"),
            ("quality-module-3", "quality-module-2", "item"),
        ],
        [("productivity-module-2", "item")],
        [
            ("productivity-module", "productivity-module-2", "item"),
            ("productivity-module-2", "item"),
            ("productivity-module-3", "productivity-module-2", "item"),
        ],
        [
            ("speed-module", "speed-module-2", "item"),
            ("speed-module-2", "item"),
            ("speed-module-3", "speed-module-2", "item"),
            ("efficiency-module", "efficiency-module-2", "item"),
            ("efficiency-module-2", "item"),
            ("efficiency-module-3", "efficiency-module-2", "item"),
            ("quality-module", "quality-module-2", "item"),
            ("quality-module-2", "item"),
            ("quality-module-3", "quality-module-2", "item"),
            ("productivity-module", "productivity-module-2", "item"),
            ("productivity-module-2", "item"),
            ("productivity-module-3", "productivity-module-2", "item"),
        ],
    ],
    [
        [("speed-module-3", "item")],
        [
            ("speed-module", "speed-module-3", "item"),
            ("speed-module-2", "speed-module-3", "item"),
            ("speed-module-3", "item"),
        ],
        [("efficiency-module-3", "item")],
        [
            ("efficiency-module", "efficiency-module-3", "item"),
            ("efficiency-module-2", "efficiency-module-3", "item"),
            ("efficiency-module-3", "item"),
        ],
        [("quality-module-3", "item")],
        [
            ("quality-module", "quality-module-3", "item"),
            ("quality-module-2", "quality-module-3", "item"),
            ("quality-module-3", "item"),
        ],
        [("productivity-module-3", "item")],
        [
            ("productivity-module", "productivity-module-3", "item"),
            ("productivity-module-2", "productivity-module-3", "item"),
            ("productivity-module-3", "item"),
        ],
        [
            ("speed-module", "speed-module-3", "item"),
            ("speed-module-2", "speed-module-3", "item"),
            ("speed-module-3", "item"),
            ("efficiency-module", "efficiency-module-3", "item"),
            ("efficiency-module-2", "efficiency-module-3", "item"),
            ("efficiency-module-3", "item"),
            ("quality-module", "quality-module-3", "item"),
            ("quality-module-2", "quality-module-3", "item"),
            ("quality-module-3", "item"),
            ("productivity-module", "productivity-module-3", "item"),
            ("productivity-module-2", "productivity-module-3", "item"),
            ("productivity-module-3", "item"),
        ],
    ],
]

all_items_3 = [
    [[("stone-wall", "entity")], [("gate", "entity")]],
    [[("radar", "entity")]],
    [
        [("land-mine", "entity")],
        [("gun-turret", "entity")],
        [("laser-turret", "entity")],
        [("flamethrower-turret", "entity")],
        [("artillery-turret", "entity")],
        [("rocket-turret", "entity")],
        [("tesla-turret", "entity")],
        [("railgun-turret", "entity")],
    ],
]

all_items_4 = [
    [
        [("rocket-silo", "entity")],
        [("crusher", "entity")],
        [("cargo-landing-pad", "entity")],
        [("thruster", "entity")],
        [("cargo-bay", "entity")],
        [("asteroid-collector", "entity")],
        [
            ("rocket-silo", "entity"),
            ("crusher", "entity"),
            ("cargo-landing-pad", "entity"),
            ("thruster", "entity"),
            ("cargo-bay", "entity"),
            ("asteroid-collector", "entity"),
        ],
    ],
]


all_items_5 = [
    [
        [
            ("burner-inserter", "entity"),
            ("inserter", "entity"),
            ("long-handed-inserter", "entity"),
            ("fast-inserter", "entity"),
            ("bulk-inserter", "entity"),
            ("stack-inserter", "entity"),
            ("pump", "entity"),
            ("offshore-pump", "entity"),
            ("pumpjack", "entity"),
            ("stone-furnace", "entity"),
            ("steel-furnace", "entity"),
            ("electric-furnace", "entity"),
            ("foundry", "entity"),
            ("recycler", "entity"),
            ("agricultural-tower", "entity"),
            ("biochamber", "entity"),
            ("captive-biter-spawner", "entity"),
            ("assembling-machine-1", "entity"),
            ("assembling-machine-2", "entity"),
            ("assembling-machine-3", "entity"),
            ("oil-refinery", "entity"),
            ("chemical-plant", "entity"),
            ("centrifuge", "entity"),
            ("electromagnetic-plant", "entity"),
            ("cryogenic-plant", "entity"),
            ("lab", "entity"),
            ("biolab", "entity"),
            ("beacon", "entity"),
            ("speed-module", "item"),
            ("speed-module-2", "item"),
            ("speed-module-3", "item"),
            ("efficiency-module", "item"),
            ("efficiency-module-2", "item"),
            ("efficiency-module-3", "item"),
            ("quality-module", "item"),
            ("quality-module-2", "item"),
            ("quality-module-3", "item"),
            ("productivity-module", "item"),
            ("productivity-module-2", "item"),
            ("productivity-module-3", "item"),
            ("radar", "entity"),
            ("roboport", "entity"),
        ],
        [
            ("wooden-chest", "entity"),
            ("iron-chest", "entity"),
            ("steel-chest", "entity"),
            ("active-provider-chest", "entity"),
            ("passive-provider-chest", "entity"),
            ("storage-chest", "entity"),
            ("buffer-chest", "entity"),
            ("requester-chest", "entity"),
        ],
        [
            ("burner-inserter", "entity"),
            ("inserter", "entity"),
            ("long-handed-inserter", "entity"),
            ("fast-inserter", "entity"),
            ("bulk-inserter", "entity"),
            ("stack-inserter", "entity"),
        ],
        [
            ("solar-panel", "entity"),
            ("accumulator", "entity"),
        ],
        [
            ("boiler", "entity"),
            ("steam-engine", "entity"),
            ("heating-tower", "entity"),
            ("nuclear-reactor", "entity"),
            ("heat-pipe", "entity"),
            ("heat-exchanger", "entity"),
            ("steam-turbine", "entity"),
        ],
        [
            ("fusion-reactor", "entity"),
            ("fusion-generator", "entity"),
        ],
        [
            #
            ("stone-wall", "entity"),
            ("gate", "entity"),
            ("land-mine", "entity"),
            ("gun-turret", "entity"),
            ("laser-turret", "entity"),
            ("flamethrower-turret", "entity"),
            ("artillery-turret", "entity"),
            ("rocket-turret", "entity"),
            ("tesla-turret", "entity"),
            ("railgun-turret", "entity"),
        ],
        [
            ("wooden-chest", "entity"),
            ("iron-chest", "entity"),
            ("steel-chest", "entity"),
            ("active-provider-chest", "entity"),
            ("passive-provider-chest", "entity"),
            ("storage-chest", "entity"),
            ("buffer-chest", "entity"),
            ("requester-chest", "entity"),
            ("storage-tank", "entity"),
            ("pump", "entity"),
            ("burner-inserter", "entity"),
            ("inserter", "entity"),
            ("long-handed-inserter", "entity"),
            ("fast-inserter", "entity"),
            ("bulk-inserter", "entity"),
            ("stack-inserter", "entity"),
            ("roboport", "entity"),
            #
            ("solar-panel", "entity"),
            ("accumulator", "entity"),
            ("boiler", "entity"),
            ("steam-engine", "entity"),
            ("heating-tower", "entity"),
            ("nuclear-reactor", "entity"),
            ("heat-pipe", "entity"),
            ("heat-exchanger", "entity"),
            ("steam-turbine", "entity"),
            ("fusion-reactor", "entity"),
            ("fusion-generator", "entity"),
            ("burner-mining-drill", "entity"),
            ("electric-mining-drill", "entity"),
            ("big-mining-drill", "entity"),
            ("offshore-pump", "entity"),
            ("pumpjack", "entity"),
            ("stone-furnace", "entity"),
            ("steel-furnace", "entity"),
            ("electric-furnace", "entity"),
            ("foundry", "entity"),
            ("recycler", "entity"),
            ("agricultural-tower", "entity"),
            ("biochamber", "entity"),
            ("captive-biter-spawner", "entity"),
            ("assembling-machine-1", "entity"),
            ("assembling-machine-2", "entity"),
            ("assembling-machine-3", "entity"),
            ("oil-refinery", "entity"),
            ("chemical-plant", "entity"),
            ("centrifuge", "entity"),
            ("electromagnetic-plant", "entity"),
            ("cryogenic-plant", "entity"),
            ("lab", "entity"),
            ("biolab", "entity"),
            ("lightning-rod", "entity"),
            ("lightning-collector", "entity"),
            ("beacon", "entity"),
            #
            ("speed-module", "item"),
            ("speed-module-2", "item"),
            ("speed-module-3", "item"),
            ("efficiency-module", "item"),
            ("efficiency-module-2", "item"),
            ("efficiency-module-3", "item"),
            ("quality-module", "item"),
            ("quality-module-2", "item"),
            ("quality-module-3", "item"),
            ("productivity-module", "item"),
            ("productivity-module-2", "item"),
            ("productivity-module-3", "item"),
            #
            ("stone-wall", "entity"),
            ("gate", "entity"),
            ("radar", "entity"),
            ("land-mine", "entity"),
            ("gun-turret", "entity"),
            ("laser-turret", "entity"),
            ("flamethrower-turret", "entity"),
            ("artillery-turret", "entity"),
            ("rocket-turret", "entity"),
            ("tesla-turret", "entity"),
            ("railgun-turret", "entity"),
        ],
    ]
]
######################################
# cl
# main
if __name__ == "__main__":
    # get all items
    # bp = blueprint.from_string(bp_text)
    # all_items = bp.get_all_items()
    # for item in all_items.keys():
    #     print('"{}": "entity",'.format(item))

    book = blueprint.new_blueprint_book(v2_0_34)

    def get_dict(name_from, name_to, item_type, quality, index):
        return {
            "from": {"type": item_type, "name": name_from},
            "to": {"type": item_type, "name": name_to, "quality": quality},
            "index": index,
        }

    def new_upgrade_planner(list_of_replacements, quality):
        bp = blueprint.from_string(upgrade_planner_text)
        mappers = []
        label_from = set()
        label_to = set()
        for index, replace in enumerate(list_of_replacements):
            if len(replace) == 2:
                name_from = name_to = replace[0]
                item_type = replace[1]
            elif len(replace) == 3:
                name_from, name_to, item_type = replace
            label_from.add("[{}={}]".format(item_type, name_from))
            label_to.add("[{}={},quality={}]".format(item_type, name_to, quality))
            mappers.append(get_dict(name_from, name_to, item_type, quality, index))
        bp.obj["settings"]["mappers"] = mappers
        # add label
        label = ""
        if len(label_from) < 6:
            for text in label_from:
                label += text
        label += "->"
        if len(label_to) < 6:
            for text in label_to:
                label += text
        bp.set_label(label)
        return bp

    def add_block(block, book):
        new_book = blueprint.new_blueprint_book(v2_0_34)
        for n, list_of_replacements in enumerate(block):  #
            for k, quality in enumerate(list_of_qualities):
                bp = new_upgrade_planner(list_of_replacements, quality)
                new_book.append_bp(bp, n * 6 + k)
        book.append_bp(new_book)

    def add_items(book, all_items, create_a_new_book=True):
        if create_a_new_book is True:
            new_book = blueprint.new_blueprint_book(v2_0_34)
        else:
            new_book = book
        for block in all_items:
            add_block(block, new_book)
        if create_a_new_book is True:
            book.append_bp(new_book)

    add_items(book, all_items_1)
    add_items(book, all_items_2)
    add_items(book, all_items_3)
    add_items(book, all_items_4, False)
    add_items(book, all_items_5, False)

    print()
    print("==================")
    print("book")
    print()
    print(book.to_str())
    print(book.to_file("out.txt"))
