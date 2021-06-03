"""
Check requirements.txt in each chapter
"""

import ast
import collections
from pathlib import Path
import re
import site
from textwrap import dedent
from typing import List, Tuple, Set, Iterator, Iterable, Dict, Sequence, cast, Union


class ImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        # print(ast.dump(node))
        for alias in node.names:
            self.imports.add(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # print(ast.dump(node))
        if node.module:
            self.imports.add(node.module)


def find_imports(path: Path) -> Set[str]:
    tree = ast.parse(path.read_text())
    iv = ImportVisitor()
    iv.visit(tree)
    return iv.imports


def all_source(path: Path) -> Iterator[Path]:
    for code_path in path.glob("**/*.py"):
        if any(n.startswith(".") for n in code_path.parts):
            continue
        if any(n.startswith("__") and n.endswith("__") for n in code_path.parts):
            continue
        yield code_path


def all_imports(all_source: Iterable[Path]) -> Iterator[Set[str]]:
    for code_path in all_source:
        import_names = find_imports(code_path)
        yield import_names


def find_requirements(path: Path) -> Iterator[Sequence[str]]:
    req_pat = re.compile(r"(.+?)([\>\<~=]+)(.*)")
    if not path.exists():
        return []
    lines = filter(None, (line.rstrip() for line in path.read_text().splitlines()))
    matches = [(req_pat.match(line), line) for line in lines]
    failures = [txt for m, txt in matches if m is None]
    assert len(failures) == 0, f"Unparseable {failures}"
    yield from (m.groups() for m, txt in matches if m)


def defined(*locations: Path) -> Iterator[str]:
    for site_packages_path in locations:
        for path in Path(site_packages_path).glob("*"):
            if any(n.startswith("__") and n.endswith("__") for n in path.parts):
                continue
            yield path.stem
        for path in Path(site_packages_path).glob("*.py"):
            yield path.stem


def scan(base: Path = Path.cwd()) -> None:
    std_locations = [Path(p).parent for p in site.getsitepackages()]
    standard_library = set(defined(*std_locations)) | {
        "collections.abc",
        "math",
        "sys",
        "itertools",
        "time",
        "urllib.parse",
        "urllib.request",
        "unittest.mock",
    }
    master_requirements: Dict[str, Set[Tuple[str, str, str]]] = collections.defaultdict(
        set
    )
    for chapter in base.glob("ch_*"):
        requirements = list(find_requirements(chapter / "requirements.txt"))
        for n, op, v in requirements:
            master_requirements[n].add((n, op, v))
        req_names = set(n for n, op, v in requirements)
        import_names = cast(Set[str], set()).union(*all_imports(all_source(chapter)))
        defined_names = set(defined(chapter / "src"))
        non_standard = import_names - standard_library - defined_names
        if non_standard:
            print(chapter.stem, "needs", non_standard)
    print("\nrequirements.txt")
    for references in master_requirements.values():
        exemplar, *others = list(references)
        print(f"{''.join(exemplar)}", end="")
        if others:
            print(" #", end="")
        for other in others:
            print(f" {''.join(other)}", end="")
        print()


master_requirements = dedent(
    """
    beautifulsoup4==4.9.1
    jsonschema==3.2.0
    pyyaml==5.3.1
    pillow==8.0.1
    """
)


def blast(base: Path = Path.cwd()) -> None:
    for chapter in base.glob("ch_*"):
        existing = chapter / "requirements.txt"
        if existing.exists():
            backup = existing.with_stem(f"(old) {existing.stem}")
            if backup.exists():
                backup.unlink()
            backup.write_text(existing.read_text())
            existing.write_text(master_requirements)
            print(f"Replaced {existing.relative_to(base)}")
    print("Fix Chapter 8 examples!")

if __name__ == "__main__":
    # scan()
    blast()
