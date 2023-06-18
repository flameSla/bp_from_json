py bp_to_json_bin.py < bp-1.txt > bp-1.json
py bp_to_json_bin.py < bp-2.txt > bp-2.json

jq -S  . bp-1.json > bp-1-sort.json
jq -S  . bp-2.json > bp-2-sort.json

pause