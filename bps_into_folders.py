import argparse
from pathlib import Path
from bp_from_json import blueprint
import shutil
import json
import copy
from pathvalidate import sanitize_filename
import re


# ====================================
def get_script_dir():
    return Path(__file__).parent.resolve()


# ====================================
def get_current_working_directory():
    return Path().resolve()


# ====================================
def get_filename(bp):
    # convert the bp label to the file name
    if bp.is_blueprint_book():
        return sanitize_filename(
            "{:03d}-index {}".format(bp.data.get("index", 0), "book")
        )
    else:
        return sanitize_filename(
            "{:03d}-index {}".format(bp.data.get("index", 0), bp.read_label())
        )


# ====================================
def init_parser():
    parser = argparse.ArgumentParser(
        description=(
            'Script "bps_into_folders.py" creates separate files from the "bp.txt" in the "out_folder" directory.'
            " The contents of the directory are BEING DELETED! "
            'For example: bps_into_folders.py -d="out_folder" -b="bp-file"'
        )
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default="",
        help=(
            '(OUT) The directory for the result. The contents of the directory will be DESTROYED! Default = "working_directory/bps_folder"'
        ),
    )
    parser.add_argument(
        "-b",
        "--blueprint",
        type=str,
        default="",
        help=('(IN) Blueprint file. Default = "bp.txt"'),
    )
    return parser


# ====================================
#
# main
if __name__ == "__main__":
    args = init_parser().parse_args()

    if args.directory:
        bps_folder = Path(args.directory)
    else:
        bps_folder = get_current_working_directory().joinpath("bps_folder")

    # create folder
    if bps_folder.exists():
        shutil.rmtree(bps_folder)
    bps_folder.mkdir(exist_ok=True)

    print()
    print("==================")
    print()

    if args.blueprint:
        book = blueprint.from_file(args.blueprint)
    else:
        book = blueprint.from_file("bp.txt")

    def get_path(bps):
        path = Path(bps_folder)
        for bp in bps:
            if bp.is_blueprint_book():
                path = path.joinpath(get_filename(bp))
        return path

    bps = book.get_all_bp()
    for i in range(len(bps)):
        bp, path = bps[i]
        if not bp.is_blueprint_book():
            # "blueprint"
            # "upgrade_planner"
            # "deconstruction_planner"

            filename = get_path(path) / (get_filename(bp) + ".bin")
            print("blueprint: {}".format(get_filename(bp)))
            if len(str(filename)) < 200:
                bp.to_file(filename)
            else:
                # the length of the name is more than 200
                # we change the file name to "extended name.bin"
                # to the file "extended name.filename" saving a long name that can be restored
                result = re.search(r"(\d+-index )(.*)", filename.name)
                filename1 = result[1] + "extended name.bin"
                filename1 = filename.with_name(filename1)
                bp.to_file(filename1)
                with open(
                    filename1.with_suffix(".filename"), "w", encoding="utf8"
                ) as f:
                    print(filename, file=f, flush=True)
        else:
            # creating a directory
            # we save all the parameters of the book to a file "book name.json"
            print(f"blueprint book: {get_filename(bp)}")
            path = get_path(path)
            path.mkdir(parents=True, exist_ok=True)
            bp = copy.deepcopy(bp)
            if "blueprints" in bp.obj:
                del bp.obj["blueprints"]

            filename = path.joinpath(get_filename(bp)).with_suffix(".json")
            with filename.open(mode="w", encoding="utf8") as f:
                json.dump(bp.obj, f, indent=4, ensure_ascii=False)
