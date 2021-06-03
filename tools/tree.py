"""
Recursive directory tree display.
Uses asciitree.
"""
import argparse
from pathlib import Path
import sys
from asciitree import LeftAligned  # type: ignore[import]
from textwrap import indent
from typing import List, Dict, Any


def display(tree: Dict[str, Any], prefix: int = 0) -> None:
    for name in tree:
        if tree[name]:  # Non-empty: i.e., a directory
            print(indent(name, prefix * " "))
            display(tree[name], prefix + 4)
        else:
            print(indent(name, prefix * " "))


def build(root: Path) -> Dict[str, Any]:
    tree: Dict[str, Dict[str, Any]] = {}
    for path in root.glob("**/*"):
        if any(n.startswith(".") for n in path.parts):
            continue
        if any(n.startswith("__") and n.endswith("__") for n in path.parts):
            continue
        here = tree
        for name in path.parts[:-1]:
            here = here.setdefault(f"{name}/", {})
        if path.is_dir():
            here.setdefault(f"{path.parts[-1]}/", {})
        else:
            here.setdefault(path.parts[-1], {})
    return tree


def main(argv: List[str] = sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs=1, type=Path)
    options = parser.parse_args(argv)
    for directory in options.directory:
        tree = build(directory)
        tr = LeftAligned()
        print(tr(tree))
        # display(tree)


if __name__ == "__main__":
    main()
