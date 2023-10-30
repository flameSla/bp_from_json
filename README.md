### bp_from_json

"bp_from_json" is a Python module for creating and editing blueprints for the game [Factorio](https://factorio.com/).
This is a simple wrapper for easier work with json.



* Script **"bps_into_folders.py"** creates separate files from the "bp.txt" in the "bps_folder" directory. The contents of the directory are **BEING DELETED**!

**bps_into_folders.py**:
```
options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        (OUT) The directory for the result. The contents of the directory will be DESTROYED! Default = "working_directory/bps_folder"
  -b BLUEPRINT, --blueprint BLUEPRINT
                        (IN) Blueprint file. Default = "bp.txt"
```


* Script **"bps_from_folders.py"** from the directory "bps_folder" creates a "bp_out.txt".

**bps_from_folders.py**:
```
options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        (IN) Directory with blueprints. Default = "working_directory/bps_folder"
  -b BLUEPRINT, --blueprint BLUEPRINT
                        (OUT) Blueprint file. Default = "bp_out.txt"
```
