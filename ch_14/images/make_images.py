"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import abc
import asyncio
from math import hypot
from pathlib import Path
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageColor
import subprocess
from typing import Callable

# Three classes of images.
# XKCD comics, downloaded.
# Plantuml, built using the PlantUML and GraphViz components. (Optional)
# PIL, built here.

class BuildImage(abc.ABC):
    """Command design pattern."""
    def __init__(self, target: Path) -> None:
        self.target = target

    @property
    def exists(self) -> bool:
        return self.target.exists()

    @abc.abstractmethod
    async def make(self) -> None:
        ...

    async def convert(self, source: Path, target: Path) -> None:
        img = Image.open(source)
        img.save(target)


class GetXKCD(BuildImage):
    def __init__(self, target: Path, source: str) -> None:
        super().__init__(target)
        self.url = source
        url_path = Path(urllib.parse.urlparse(self.url).path)
        self.source_path = self.target.parent / url_path.name

    async def make(self) -> None:
        with urllib.request.urlopen(self.url) as source:
            self.source_path.write_bytes(source.read())
        await self.convert(self.source_path, self.target)


class RunPlantUML(BuildImage):
    """
    Requires plantuml.jar and graphviz package.
    """
    graphviz = "bin/dot"
    plantjar = "share/plantuml.jar"
    conda_env_name = "CaseStudy"

    def __init__(self, target: Path, source: Path) -> None:
        super().__init__(target)
        self.source = source
        self.intermediate = self.source.with_suffix(".png")

    async def make(self) -> None:
        base_env = Path.home() / "miniconda3" / "envs" / self.conda_env_name
        self.graphviz = base_env / self.graphviz
        self.plantjar = base_env / self.plantjar

        env = {
            "GRAPHVIZ_DOT": str(self.graphviz),
        }
        print(self.source)
        print(self.target)
        command = ["java", "-jar", str(self.plantjar), "-tpng", str(self.source)]
        subprocess.run(command, env=env, check=True)
        await self.convert(self.intermediate, self.target)


class DrawPIL(BuildImage):
    def __init__(self, target: Path, builder: Callable[[None], Image.Image]) -> None:
        super().__init__(target)
        self.builder = builder
    async def make(self) -> None:
        builder = self.builder
        image = builder()
        image.save(self.target)

def bricks() -> Image.Image:
    black = ImageColor.getcolor("black", "1")
    white = ImageColor.getcolor("white", "1")
    img = Image.new("1", (200, 200), color=white)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (100, 100)], fill=black)
    draw.rectangle([(136, 136), (200, 200)], fill=black)
    return img

def row() -> Image.Image:
    black = ImageColor.getcolor("black", "1")
    white = ImageColor.getcolor("white", "1")
    img = Image.new("1", (200, 2))
    draw = ImageDraw.Draw(img)
    draw.line([(0, 0), (100, 0)], fill=black, width=2)
    draw.line([(100, 0), (200, 0)], fill=white, width=2)
    return img

import random
def very_large() -> Image.Image:
    grays = [
        ImageColor.getcolor(f"#{g:02x}{g:02x}{g:02x}", "L")
        for g in range(0, 256, 16)
    ] + [
        ImageColor.getcolor(f"#ffffff", "L")
    ]
    img = Image.new("L", (7200, 5400))
    draw = ImageDraw.Draw(img)
    for c in range(256):
        r = random.randint(16, 32) + 1024-(c*4)
        x = random.randint(0+r, 7200-r)
        y = random.randint(0+r, 5400-r)
        neighborhood = int(hypot(x, y) / hypot(7200, 5400) * len(grays))
        color_slice = slice(max(neighborhood-2, 0), min(neighborhood+2, len(grays)))
        color = random.choice(grays[color_slice])
        draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=color, outline=color)
    return img

async def make(image: BuildImage) -> None:
    if not image.exists:
        print(f"Making {image.target.name}")
        await image.make()

async def main():
    base = Path.cwd()/"images"

    image_list = [
        GetXKCD(
            base / "python.bmp",
            "https://imgs.xkcd.com/comics/python.png"
        ),
        GetXKCD(
            base / "exploits_of_a_mom.bmp",
            "https://imgs.xkcd.com/comics/exploits_of_a_mom.png"
        ),
        GetXKCD(
            base / "compiling.bmp",
            "https://imgs.xkcd.com/comics/compiling.png"
        ),
        GetXKCD(
            base / "sandwich.bmp",
            "https://imgs.xkcd.com/comics/sandwich.png"
        ),
        RunPlantUML(
            base / "bricks_1.bmp", base / "bricks_1.uml"
        ),
        RunPlantUML(
            base / "bricks_2.bmp", base / "bricks_2.uml"
        ),
        DrawPIL(
            base / "bricks.bmp", bricks,
        ),
        DrawPIL(
            base / "row.bmp", row,
        ),
        DrawPIL(
            base / "large.bmp", very_large
        ),
    ]
    workers = [
        make(image) for image in image_list
    ]
    asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())


