"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from __future__ import annotations
import abc
import argparse
import contextlib
from pathlib import Path
import sys
from typing import Union, Optional, cast


class Node(abc.ABC):
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.parent: Optional["Folder"] = None

    def move(self, new_place: "Folder") -> None:
        previous = self.parent
        new_place.add_child(self)
        if previous:
            del previous.children[self.name]

    @abc.abstractmethod
    def copy(self, new_folder: "Folder") -> None:
        ...

    @abc.abstractmethod
    def remove(self) -> None:
        ...

    @abc.abstractmethod
    def tree(self, indent: int = 0, last: bool = False, outer: bool = False) -> None:
        ...

    @abc.abstractmethod
    def dot(self) -> None:
        ...


class Folder(Node):
    def __init__(self, name: str, children: Optional[dict[str, "Node"]] = None) -> None:
        super().__init__(name)
        self.children = children or {}

    def __repr__(self) -> str:
        return f"Folder({self.name!r}, {self.children!r})"

    def add_child(self, node: "Node") -> "Node":
        node.parent = self
        return self.children.setdefault(node.name, node)

    def copy(self, new_folder: "Folder") -> None:
        target = cast(Folder, new_folder.add_child(Folder(self.name)))
        for c in self.children:
            self.children[c].copy(target)

    def remove(self) -> None:
        names = list(self.children)
        for c in names:
            self.children[c].remove()
        if self.parent:
            del self.parent.children[self.name]

    def tree(self, indent: int = 0, last: bool = False, outer: bool = False) -> None:
        indent_text = "     " if outer else " |   "
        print((indent * indent_text) + " +--", self.name)
        if self.children:
            *first, final = list(self.children)
            for c in first:
                self.children[c].tree(indent + 1, last=False, outer=outer)
            self.children[final].tree(indent + 1, last=True, outer=outer)

    def dot(self) -> None:
        for c in self.children:
            print(f"    n{id(self)} -> n{id(self.children[c])};")
            self.children[c].dot()
        print(f'    n{id(self)} [label = "{self.name}"];')


class File(Node):
    def __repr__(self) -> str:
        return f"File({self.name!r})"

    def copy(self, new_folder: "Folder") -> None:
        new_folder.add_child(File(self.name))

    def remove(self) -> None:
        if self.parent:
            del self.parent.children[self.name]

    def tree(self, indent: int = 0, last: bool = False, outer: bool = False) -> None:
        indent_text = "     " if outer else " |   "
        print((indent * indent_text) + " +--", self.name)

    def dot(self) -> None:
        print(f'    n{id(self)} [shape=box,label="{self.name}"];')


test_folder_file = """
>>> f = File("name.ex")
>>> f.tree()
 +-- name.ex

>>> d = Folder("Folder", {"name.ex": f})
>>> d.tree()
 +-- Folder
 |    +-- name.ex
 
>>> d.tree(outer=True)
 +-- Folder
      +-- name.ex

>>> d_p = Folder("Parent", {"Folder": d})
>>> d_p.tree()
 +-- Parent
 |    +-- Folder
 |    |    +-- name.ex

>>> tree = Folder("Tree")
>>> tree.add_child(Folder("src"))
Folder('src', {})
>>> tree.children["src"].add_child(File("ex1.py"))
File('ex1.py')
>>> tree.add_child(Folder("src"))
Folder('src', {'ex1.py': File('ex1.py')})
>>> tree.children["src"].add_child(File("test1.py"))
File('test1.py')
>>> tree
Folder('Tree', {'src': Folder('src', {'ex1.py': File('ex1.py'), 'test1.py': File('test1.py')})})

>>> tree.tree(outer=True)
 +-- Tree
      +-- src
           +-- ex1.py
           +-- test1.py


>>> test1 = tree.children["src"].children["test1.py"]
>>> test1
File('test1.py')
>>> tree.add_child(Folder("tests"))
Folder('tests', {})
>>> test1.move(tree.children["tests"])
>>> tree
Folder('Tree', {'src': Folder('src', {'ex1.py': File('ex1.py')}), 'tests': Folder('tests', {'test1.py': File('test1.py')})})
>>> tree.tree(outer=True)
 +-- Tree
      +-- src
           +-- ex1.py
      +-- tests
           +-- test1.py

>>> backup = tree.add_child(Folder("backup"))
>>> test1.copy(backup)
>>> tree.tree()
 +-- Tree
 |    +-- src
 |    |    +-- ex1.py
 |    +-- tests
 |    |    +-- test1.py
 |    +-- backup
 |    |    +-- test1.py

>>> backup.remove()
>>> tree.tree()
 +-- Tree
 |    +-- src
 |    |    +-- ex1.py
 |    +-- tests
 |    |    +-- test1.py

"""

test_folder_file_bad_move = """
>>> tree = Folder("Tree")
>>> tree.add_child(Folder("src"))
Folder('src', {})
>>> tree.children["src"].add_child(File("ex1.py"))
File('ex1.py')
>>> tree.add_child(Folder("src"))
Folder('src', {'ex1.py': File('ex1.py')})
>>> test1 = tree.children["src"].add_child(File("test1.py"))
>>> tree.add_child(File("tests"))
File('tests')
>>> test1.move(tree.children["tests"])
Traceback (most recent call last):
  File ...
    exec(compile(example.source, filename, "single",
  File "<doctest file_system.__test__.test_folder_file_bad_move[6]>", line 1, in <module>
    test1.move(tree.children["tests"])
  File "src/file_system.py", line 24, in move
    new_place.add_child(self)
AttributeError: 'File' object has no attribute 'add_child'

"""

test_folder_file_deep_copy = """
>>> tree = Folder("root", 
...     {
...         "src": Folder("src", 
...             {
...                 "__init__.py": File("__init__.py"), 
...                 "m1": Folder("m1",
...                     {"a.py": File("a.py"),}
...                 ),
...                 "m2": Folder("m2",
...                     {"b.py": File("b.py"),}
...                 ),
...             }
...         ),
...         "bkup": Folder("bkup"),
...     }
... )
>>> tree.tree()
 +-- root
 |    +-- src
 |    |    +-- __init__.py
 |    |    +-- m1
 |    |    |    +-- a.py
 |    |    +-- m2
 |    |    |    +-- b.py
 |    +-- bkup

>>> tree.children["src"].copy(tree.children["bkup"])
>>> tree.tree()
 +-- root
 |    +-- src
 |    |    +-- __init__.py
 |    |    +-- m1
 |    |    |    +-- a.py
 |    |    +-- m2
 |    |    |    +-- b.py
 |    +-- bkup
 |    |    +-- src
 |    |    |    +-- __init__.py
 |    |    |    +-- m1
 |    |    |    |    +-- a.py
 |    |    |    +-- m2
 |    |    |    |    +-- b.py

 
"""


def dump(tree: Folder) -> None:
    """Top-level dump with special "outer" rule."""
    print(tree.name)
    *first, final = list(tree.children)
    for c in first:
        tree.children[c].tree(outer=False)
    tree.children[final].tree(outer=True)


def dot(tree: Folder) -> None:
    print("digraph tree {")
    print("    rankdir=LR;")
    print("    ratio=auto;")
    print("    nodesep=.125;")
    tree.dot()
    print("}")


def populate(base: Path) -> Folder:
    tree = Folder(base.name)
    for item in base.glob("**/*"):
        if any(n.startswith(".") for n in item.parts):
            # Ignore directories like ".tox"
            continue
        if any(n.startswith("__") and n.endswith("__") for n in item.parts):
            # Ignore directories like "__pycache__"
            continue
        if item.is_file():
            here = tree
            for parent_name in item.relative_to(base).parts[:-1]:
                here = cast(Folder, here.add_child(Folder(parent_name)))
            here.add_child(File(item.name))
    return tree


def main(argv: list[str] = sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs=1, type=Path)
    options = parser.parse_args(argv)

    tree = populate(options.directory[0])
    # print(tree)
    dump(tree)
    with Path("tree.dot").open("w") as target:
        with contextlib.redirect_stdout(target):
            dot(tree)


__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}

if __name__ == "__main__":
    main()
