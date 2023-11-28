import os
from bp_from_json import blueprint


################################################################
def input_def(text, default):
    str = input(text + "[" + default + "]:")
    return str if str else default


################################################################
def set_requests_for_roboports(book):
    for bp in book.get_all_bp(onedimensional=True, blueprint_only=True):
        for entity in bp.get_entities():
            if "roboport" in entity.read_name():
                entity.update_items({"construction-robot": 5}, name_verification=False)


################################################################
#
# main
if __name__ == "__main__":
    exchange_str = input_def("bp:(string or filename.txt)", "bp.txt")
    if os.path.exists(exchange_str):
        with open(exchange_str, "r") as f:
            exchange_str = f.read()

    bp = blueprint.from_string(exchange_str)
    set_requests_for_roboports(bp)
    # print(bp.to_str())
    bp.to_file("bp_out.ignore")

