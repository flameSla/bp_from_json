import json

######################################
#
# main
if __name__ == "__main__":

    print()
    print("==================")
    print("добавить предметы в постоянный комбинатоор")
    print()

    def get_filter(index, name, quality, count):
        return {
            "index": index,
            "name": name,
            "quality": quality,
            "comparator": "=",
            "count": count,
        }

    list_of_qualities = ("normal", "uncommon", "rare", "epic", "legendary")
    names = (
        "iron-plate",
        "electronic-circuit",
        "nutrients",
        "pentapod-egg",
        "landfill",
    )
    off = -100000
    counts = {
        "normal": -500,
        "uncommon": -500,
        "rare": -500,
        "epic": -500,
        "legendary": -500,
    }

    filters = []
    index = 1
    for name in names:
        for q in list_of_qualities:
            filters.append(get_filter(index, name, q, counts[q]))
            index += 1

    print(json.dumps(filters))
