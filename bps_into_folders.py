import argparse
from pathlib import Path
from bp_from_json import blueprint
import shutil
import json
from pathvalidate import sanitize_filename


# ====================================
def get_script_dir():
    return Path(__file__).parent.resolve()


# ====================================
def get_current_working_directory():
    return Path().resolve()


# ====================================
def get_filename(bp):
    # convert the bp label to the file name
    index = int(bp.data.get("index", 0))
    # print('index = ', type(index), index)
    if bp.is_blueprint_book():
        return sanitize_filename("{:03d}-index {}".format(index, "book"))
    elif bp.is_blueprint():
        return sanitize_filename("{:03d}-index {}".format(index, "bp"))
    elif bp.is_upgrade_planner():
        return sanitize_filename("{:03d}-index {}".format(index, "upg_planner"))
    elif bp.is_deconstruction_planner():
        return sanitize_filename("{:03d}-index {}".format(index, "dec_planner"))
    else:
        return sanitize_filename("{:03d}-index {}".format(index, "unknown"))


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
    ),
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="bin",
        help=('Format for storing BPs "bin" or "json". Default = "bin"'),
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
            print("blueprint: {}".format(get_filename(bp)))
            if args.mode == "bin":
                bp.to_file(get_path(path) / (get_filename(bp) + ".bin"))
            else:
                bp.to_json_file(get_path(path) / (get_filename(bp) + ".txt"))
            with open(
                get_path(path) / (get_filename(bp) + ".json"), "w", encoding="utf8"
            ) as f:
                json_str = json.dumps(
                    bp.summary_of_book().obj, indent=4, ensure_ascii=False
                )
                print(json_str, file=f)
        else:
            # creating a directory
            # we save all the parameters of the book to a file "book name.json"
            print(f"blueprint book: {get_filename(bp)}")
            path_for_dir = get_path(path)
            path_for_dir.mkdir(parents=True, exist_ok=True)
            with open(
                path_for_dir / (get_filename(bp) + ".json"),
                mode="w",
                encoding="utf8",
            ) as f:
                json_str = json.dumps(
                    bp.summary_of_book().obj, indent=4, ensure_ascii=False
                )
                print(json_str, file=f)
