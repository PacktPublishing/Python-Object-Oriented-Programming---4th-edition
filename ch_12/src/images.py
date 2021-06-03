"""
Python 3 Object-Oriented Programming

Chapter 12. Advanced Python Design Patterns
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import Iterator


class FindUML:
    def __init__(self, base: Path) -> None:
        self.base = base
        self.start_pattern = re.compile(r"@startuml *(.*)")

    def uml_file_iter(self) -> Iterator[tuple[Path, Path]]:
        for source in self.base.glob("**/*.uml"):
            if any(n.startswith(".") for n in source.parts):
                continue
            body = source.read_text()
            for output_name in self.start_pattern.findall(body):
                if output_name:
                    target = source.parent / output_name
                else:
                    target = source.with_suffix(".png")
                yield (source.relative_to(self.base), target.relative_to(self.base))


import subprocess


class PlantUML:
    """
    Default setup is this:

    1.  Download Java Runtime (JRE) for your platform.
        https://www.java.com/en/download/manual.jsp

    2.  Download the ``plantuml.jar`` and put into your conda environment ``share`` directory.
        https://plantuml.com/download

    3.  Use ``conda install graphiz`` to create the ``dot`` application in your conda environment.

    4.  If necessary, update this script with environment name and locations
    """

    conda_env_name = "CaseStudy"
    base_env = Path.home() / "miniconda3" / "envs" / conda_env_name

    def __init__(
        self,
        graphviz: Path = Path("bin") / "dot",
        plantjar: Path = Path("share") / "plantuml.jar",
    ) -> None:
        self.graphviz = self.base_env / graphviz
        self.plantjar = self.base_env / plantjar

    def process(self, source: Path) -> None:
        env = {
            "GRAPHVIZ_DOT": str(self.graphviz),
        }
        command = ["java", "-jar", str(self.plantjar), "-progress", str(source)]
        subprocess.run(command, env=env, check=True)
        print()


class GenerateImages:
    def __init__(self, base: Path, verbose: int = 0) -> None:
        self.finder = FindUML(base)
        self.painter = PlantUML()
        self.verbose = verbose

    def make_all_images(self) -> None:
        for source, target in self.finder.uml_file_iter():
            if not target.exists() or source.stat().st_mtime > target.stat().st_mtime:
                print(f"Processing {source} -> {target}")
                self.painter.process(source)
            else:
                if self.verbose > 0:
                    print(f"Skipping {source} -> {target}")


if __name__ == "__main__":
    g = GenerateImages(Path.cwd())
    g.make_all_images()
