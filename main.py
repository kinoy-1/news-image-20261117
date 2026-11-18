#!/usr/bin/env python3
"""Entry for make.fun news-image-20261117, round 2.

The image, entry.png, is a 1024x1024 infographic drawn by draw.py in
this session (pure PIL, no generated imagery). This program only places
its bytes at the path the grader reads, so every run writes exactly the
same file. Standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {os.path.getsize(dst)} bytes to {dst}")


if __name__ == "__main__":
    main()
