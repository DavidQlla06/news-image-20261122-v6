#!/usr/bin/env python3
"""make.fun entrypoint: copy this repo's entry.png to the output dir.

The grader runs the program with no network; the image beside this file
is the entry. Outside the grader container, MAKEFUN_OUTPUT_DIR stands
in for /output.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
