#
# бесперспективный подход для нахождения сломанных BPs
#


import json
from bp_from_json import blueprint
from bp_from_json import dict_bp
from bp_from_json import entity
from bp_from_json import get_items


# ====================================
def json_to_file(filename, bp):
    with open(filename, "w") as f:
        print(json.dumps(bp.obj["entities"], indent=4), file=f, flush=True)


# ====================================
def get_entity_diff(a, b):
    if len(a) > len(b):
        return get_entity_diff(b, a)
    else:
        res = []
        for k in b.keys():
            temp = a.get(k, "None")
            if temp != b[k]:
                res.append(k)
                # print("[{}]: '{}' '{}'".format(k, temp, b[k]))
        return res


# ====================================
def compare(bp1, bp2):
    entities1 = bp1.obj["entities"]
    entities2 = bp2.obj["entities"]

    if len(entities1) == len(entities2):
        for i in range(len(entities1)):
            if entities1[i] != entities2[i]:
                # print(entities1[i].get("recipe", "None"))
                # print(entities2[i].get("recipe", "None"))
                res = get_entity_diff(entities1[i], entities2[i])
                lines = []
                if "recipe" in res:
                    lines.append("\t----------")
                    lines.append(
                        "\tentity_number = {}".format(entities1[i]["entity_number"])
                    )
                    lines.append("")
                    for k in res:
                        lines.append(
                            "\t[{}]: '{}' '{}'".format(
                                k,
                                entities1[i].get(k, "None"),
                                entities2[i].get(k, "None"),
                            )
                        )
                    return lines
                else:
                    return None


# ====================================


######################################
#
# main
if __name__ == "__main__":
    f1 = """0eNrNVsGOozAM/ZVVzmSWJFAYfmVVVQE8nWghIBJmt6r49zUwg7pT1CZtD71BnDzbL8+OjySvemg7pS3JjkQVjTYk+3UkRu21rMY1e2iBZERZqElAtKzHvxwkbiVDQJQu4S/J2BBcPSSNgTqvlN7TWhbvSgMVJxB82AYEtFVWwRzE9HPY6b7OoUMfC5KxsvhNlTbQWbQEpG0MHsOI0DdCUf4SB+SAH+IlRg+l6qCY7XwM9BswX4CVflMaTbR4B2NXgMX/wF/7dwasxcTMuK+DuvmAXY+2CsODcjfygCbb9TCs+BeXKTqPIvyKgs9RzPB4AS1ASeum7KvxIN7KirfImUbmxWLszCK/h8Q3WRkIyLw86+TT7R+JKzSXXQcVOi2aflR1HAYEGZnYtbQCOUW0yHa7RtFmSaVVLVDb0H2HaOUlpXEXjpIbJMxcgNMbJMweKOFXf1E55cVCf1WxJ1UVY9/75/nlRJ9JhJcLm6/i8+v47B58cRX/LvjoKvxd7MT+tedU02zjX3v8gaXHklufD3HD68FS70p3Y/Gkg/Q5Qk9bzxUwB74WGfdvFfxJOwVn/g+Q26TD/YsgcgIW/kUQPbAIuP9U45aX/1QTPYWotnNhj810mfADUskcYTLCWRr+ND8mcFz+QKczBSmLkleeJKlIhdiczPds+Af4BQ7f"""
    f2 = """0eNrNV9GOmzAQ/JXKz/Y1tiFw/EoVRQb2clbBIGyujSL+vQvkUJrQC05SKW9gm9nZ8ezaHEhatFA32jiSHIjOKmNJ8uNArN4ZVfRjbl8DSYh2UBJKjCr7txQULiUdJdrk8JskvKNXP1LWQpkW2uxYqbJ3bYDJEwjRbSgB47TTMJIYXvZb05YpNBhjQrJOZT+ZNhYahzOU1JXFz5ARxkYoJl5CSvb4IF9CjJDrBrJxXvREz4DFBKzNmzY4xbJ3sG4GWP4N/Ll+a8E5TMz26xooqw/YtjhXID3It70OOOWaFrqZ+PJriS5ZrD5ZiIv0KIbP9KA+lDVm8kshB5aqpoECoY5UcLNqgJyVVd4WfRDcwRlmwWLJuZfi4WLFxT2Cv6nCAiXj8OipY9gzVbKq7SsgXFGCigw74VgBamA0WXwzJ9F6SqVG2Zmr2K5BtPwrV4olGkU32J0vAY5vsDt/oN1f/U21KC++8ncVf1JXcX7eay83JzgmsRpz+Fdhi1l8cR2f34Mvr+LfBR9chb9LndC/9hbVNF/71554YOnx6NajRv7nk4bH3l1hmeIn3aZNEXpYeumWMck5ZsK/rYgn7SqC+x9Wy25Qwr9ggkXA0r9gggcWjPC/AS3Ly/8GFDyFqTZjYfeNd/pzoKRQKcIkRPB49d1+G8Bx+AODjhLEPIheRRTFMpZyffLfwLs/frktLQ=="""

    bp1 = blueprint.from_string(f1)
    bp2 = blueprint.from_string(f2)

    # json_to_file("parser_for_git_diff_bp1.ignore", bp1)
    # json_to_file("parser_for_git_diff_bp2.ignore", bp2)

    # compare(bp1, bp2)

    # print(bp1.obj["entities"][0])

    file = []
    files = []
    with open("good vs bad.txt.ignore", encoding="utf8") as f:
        for line in reversed(f.readlines()):
            line = line.rstrip()
            file.insert(0, line)
            if "diff --git" in line:
                files.insert(0, file)
                file = []

    print()
    print("==================")
    print("")
    print()
    count = 0
    for i, f in enumerate(files):
        if "index" in f[1] and f[4] == "@@ -1 +1 @@":
            bp1 = blueprint.from_string(f[5][1:])
            bp2 = blueprint.from_string(f[6][1:])
            lines = compare(bp1, bp2)
            if lines:
                count += 1
                print()
                print(i, "\t", f[0])
                print("\t", f[2][6:])
                for line in lines:
                    print(line)

    print()
    print(count)