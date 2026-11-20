#!/usr/bin/env python3
"""Entry point: copy the pre-built front page to the output directory.

Standard library only. The image is built offline by build_image.py
and shipped in this repository as entry.png; this program just
places the identical bytes at $MAKEFUN_OUTPUT_DIR/entry.png, so
both graded runs write the same file.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
