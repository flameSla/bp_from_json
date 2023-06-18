import base64
import zlib
import io
import sys
import os


def error(*args):
    print(*args, file=sys.stderr, flush=True)


################################################################
#
# main

if __name__ == "__main__":
    #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
    exchange_str = sys.stdin.read().strip()
    version_byte = exchange_str[0]

    if version_byte == "0":
        bin_data = zlib.decompress(base64.b64decode(exchange_str[1:]))
        #sys.stdout.buffer.write(bin_data)
        with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
            stdout.write(bin_data)
            stdout.flush()
        # print("bin_data = ", type(bin_data))

    else:
        error("Unsupported version: {0}".format(version_byte))
        exit(2)
