from bp_from_json import blueprint


######################################
#
# main
if __name__ == "__main__":
    exchange_str = """0eNqtl29z4iAQxr8Lr0PHRHP++SqdTocka2RKgFuIreP43W+JdzW2yUmsb0xw4AfsPvtAjqxQLViU2rPNkcnSaMc2z0fmZK2FCv/5gwW2YdJDwxKmRRNaoZ8X2vPSNIXUwhtkp4RJXcEH26Snl4SB9tJLOOO6xuFVt00BSB3+C0qYNY7GGh3mJx5P8/QpT9iBXpfp7CmnqWigR6NeC9iJvaRR1HUrlQeM2oBAL5UCPHDfIoJnHbINYch6+0huRwLbCriRiheCQKoHymefpGUEaavo6Xdo3gG/ryq9wFYRMOEcNIWSuuaNKHdSA5/3aZc9ziNozgJUvDFVq645iwtncXo5p0VDGXLnAi0NPwhVXwSSWhl1PoWJvwgjmyyM2YOFMaLsf9rIJ4lDoPQ7Sqosb+KyCFwFpaxIHLdYMSmFD4vgHPcotLMGPS9A+WH1LmIk0gilOEnYDq8ppgIo8OUbPyeLS+0A6WUk+jHxiiPNo1d2AxQTJmVq6To97MB57iiHoobhOk/z6UCE3y09r9bYR/6ajrTkJXIP3KLZB/mNkJfTyYKM4jZ4NcVY0p6phPZ8xGjmPzCa2foRRuPagubt5rjbXwpZc1AUFqSYWqPgfm9BU5hgA8NJiKkRBCskklzKtyvINB9Rwg0ffxdMHlWwho68d/KkEUiMXGvh4f4jGEUl+pq+5GM97ai8VvRiRNGLH9ypHqNoFHIs2mlUvOgS9bfP/TIOkHInpP6OmqjnLozYdhnioTz8/Xe7T+P7yultbxVVHbqijIzcMtcxu1Jyu+V0+isTXN0NCjSdRZDo5hCi7I0dvjzHpMtKC2OSWUeO597wGglQDUclm00pt/OBQd8v3USb3vdRwvZUCF0FZat0sVxny1U2T/M8O53+AEbFZmY="""

    bp = blueprint.from_string(exchange_str)

    req = []
    names = []
    for entity in bp.get_entities():
        parameters = entity.read("control_behavior")["filters"]
        print()
        for par in parameters:
            if par["signal"]["name"] in names:
                print(" ++ ", par["signal"]["name"], par["count"])
                for r in req:
                    if r["name"] == par["signal"]["name"]:
                        r["count"] = max(r["count"], par["count"])
            else:
                req.append(
                    {
                        "type": par["signal"]["type"],
                        "name": par["signal"]["name"],
                        "count": par["count"],
                    }
                )
                names.append(par["signal"]["name"])

    # print('req = ', type(req), req)
    count = 1
    for par in req:
        print(
            '{{signal = {{type = "{0:}", name = "{1:}"}}, count = {2:}, index = {3:} }},'.format(
                par["type"], par["name"], par["count"], count
            )
        )

        count += 1
        if count == 20:
            count = 1
            print()
