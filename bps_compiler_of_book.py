import argparse
from pathlib import Path
from bp_from_json import blueprint
import json


# ====================================
def get_script_dir():
    return Path(__file__).parent.resolve()


# ====================================
def get_current_working_directory():
    return Path().resolve()


# ====================================
def init_parser():
    parser = argparse.ArgumentParser(
        description=(
            "the compiler of the book"
            'For example: bps_compiler_of_book.py -m="makefile_bps" -b="out-bp"'
        )
    )
    parser.add_argument(
        "-m",
        "--makefile_bps",
        type=str,
        default="",
        help=('(IN) makefile for the book. Default = "makefile_bps.json"'),
    )
    parser.add_argument(
        "-b",
        "--blueprint",
        type=str,
        default="",
        help=('(OUT) Blueprint file. Default = "bp_compiler_out.txt"'),
    )
    return parser


######################################
#
# main
if __name__ == "__main__":
    args = init_parser().parse_args()

    if args.makefile_bps:
        makefile_bps = args.makefile_bps
    else:
        makefile_bps = "makefile_bps.json"

    if args.blueprint:
        output_file = args.blueprint
    else:
        output_file = "bp_compiler_out.txt"

    makefile_json = json.load(Path(makefile_bps).open(encoding="utf8"))

    # print(makefile_json["summary_of_book"])
    # print(makefile_json["indexes"])

    book = blueprint.new_blueprint_book()
    for key, value in makefile_json["summary_of_book"].items():
        book.obj[key] = value

    for index, val in makefile_json["indexes"].items():
        bp = blueprint.from_file(val["filename"])
        book.append_bp(bp, index)

    book.to_file(output_file)
