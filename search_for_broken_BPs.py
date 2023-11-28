import argparse
from pathlib import Path
from bp_from_json import blueprint
import json
import collections
import re


assembling_machine = (
    "assembling-machine-1",
    "assembling-machine-2",
    "assembling-machine-3",
    "centrifuge",
    "chemical-plant",
    "oil-refinery",
)


# ====================================
def get_script_dir():
    return Path(__file__).parent.resolve()


# ====================================
def get_current_working_directory():
    return Path().resolve()


# ====================================
def get_index(filename):
    result = re.search(r"(\d+)-index (.*)", filename.name)
    if result:
        return int(result[1]), result[2]
    else:
        return None, None


# ====================================
def search_for_broken_bps_from_folder_parse(folder, f):
    # using recursion, we look through all directories
    for file in folder.iterdir():
        if file.is_file() and (file.suffix == ".bin" or file.suffix == ".txt"):
            check_the_BP(file, f)
        elif file.is_dir():
            search_for_broken_bps_from_folder_parse(folder / file, f)


# ====================================
def check_the_BP(filename, f):
    if filename.suffix == ".bin":
        bp = blueprint.from_file(filename)
    else:
        bp = blueprint.from_json_file(filename)
    # print(filename)
    if "entities" in bp.obj:
        for entity in bp.obj["entities"]:
            if entity["name"] in assembling_machine:
                if "recipe" not in entity:
                    print(filename)
                    print(filename, file=f, flush=True)
                    break


# ====================================
def search_for_broken_bps_from_folder(folder, f):
    # there should be one folder or one file in the root directory
    if len(tuple(folder.iterdir())) == 1:
        for file in folder.iterdir():
            if file.is_file() and file.suffix == ".bin":
                check_the_BP(file, f)
            elif file.is_dir():
                search_for_broken_bps_from_folder_parse(folder / file, f)
    else:
        raise RuntimeError(
            "ERROR!!! the number of files and directories in root is greater than 1"
        )
        return None


# ====================================
def init_parser():
    parser = argparse.ArgumentParser(
        description=(
            'Script "bps_from_folders.py" from the directory "bps_folder" creates a "bp_out.txt" '
            'For example: bps_from_folders.py -d="in_folder" -b="out-bp"'
        )
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default="",
        help=(
            '(IN) Directory with blueprints. Default = "working_directory/bps_folder"'
        ),
    )
    return parser


######################################
#
# main
if __name__ == "__main__":
    args = init_parser().parse_args()

    if args.directory:
        bps_folder = Path(args.directory)
    else:
        bps_folder = get_current_working_directory().joinpath("bps_folder")

    output_file = "broken_BPs.txt.ignore"

    with open(output_file, mode="w", encoding="utf8") as f:
        search_for_broken_bps_from_folder(bps_folder, f)
