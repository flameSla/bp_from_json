import argparse
from pathlib import Path
from bp_from_json import blueprint
import json
import collections
import re


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
def add_bp_from_folder_parse(bp, folder):
    # using recursion, we look through all directories
    for file in folder.iterdir():
        if file.is_file() and (file.suffix == ".txt" or file.suffix == ".bin"):
            index, blueprint_name = get_index(file)
            if file.suffix == ".bin":
                new_bp = blueprint.from_file(file)
            else:
                new_bp = blueprint.from_json_file(file)
            print(f"\tcreate blueprint '{new_bp.read_label()}'\tindex={index}")
            bp.append_bp(new_bp, index)
        elif file.is_dir():
            book = blueprint.new_blueprint_book()
            index, book_name = get_index(file)
            json_name = folder / file / (file.name + ".json")
            json_data = json.load(
                json_name.open(encoding="utf8"),
                object_pairs_hook=collections.OrderedDict,
            )
            if index != 0:
                book.data["index"] = index
            for key, value in json_data.items():
                book.obj[key] = value
            print(f"create book '{book.read_label()}'\tindex={index}")
            add_bp_from_folder_parse(book, folder / file)
            bp.append_bp(book, index)


# ====================================
def add_bp_from_folder(folder):
    # there should be one folder or one file in the root directory
    if len(tuple(folder.iterdir())) == 1:
        for file in folder.iterdir():
            if file.is_file() and (file.suffix == ".txt" or file.suffix == ".bin"):
                index, blueprint_name = get_index(file)
                if file.suffix == ".bin":
                    bp = blueprint.from_file(file)
                else:
                    bp = blueprint.from_json_file(file)
                print(f"\tcreate blueprint '{bp.read_label()}'\tindex={index}")
                return bp
            elif file.is_dir():
                book = blueprint.new_blueprint_book()
                index, book_name = get_index(file)
                json_name = folder / file / (file.name + ".json")
                json_data = json.load(
                    json_name.open(encoding="utf8"),
                    object_pairs_hook=collections.OrderedDict,
                )
                if index != 0:
                    book.data["index"] = index
                for key, value in json_data.items():
                    book.obj[key] = value
                print(f"create book '{book.read_label()}'\tindex={index}")
                add_bp_from_folder_parse(book, folder / file)
                return book
            else:
                return None
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
    parser.add_argument(
        "-b",
        "--blueprint",
        type=str,
        default="",
        help=('(OUT) Blueprint file. Default = "bp_out.txt"'),
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

    if args.blueprint:
        output_file = args.blueprint
    else:
        output_file = "bp_out.txt"

    bp = add_bp_from_folder(bps_folder)
    if bp:
        bp.to_file(output_file)
