1. to create the foundation, run the "bps_decompiler_of_book.py" script once
    - **bps_decompiler_of_book.py -b="some_book.txt"**

1. files "bp_index_0 ... N.bin" contain bps for the corresponding indexes of the book

1. editing the file "makefile_bps.json"
    - edit the "summary_of_book" section, these are the properties of the book being created: title, description, etc.
    - edit the "indexes" section:
        - "filename" - the bp file that will be placed in the appropriate index
        - "label" - for information only, does not affect the book being created
        - "description" - for information only, does not affect the book being created

1. run the script "bps_decompiler_of_book.py"
    - **bps_decompiler_of_book.py -m="makefile_bps.json" -b="out_file"**