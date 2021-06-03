"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
from __future__ import annotations
import abc
from pathlib import Path
from PIL import Image  # type: ignore [import]
from typing import Tuple

Size = Tuple[int, int]


class FillAlgorithm(abc.ABC):
    @abc.abstractmethod
    def make_background(self, img_file: Path, desktop_size: Size) -> Image:
        pass


class TiledStrategy(FillAlgorithm):
    def make_background(self, img_file: Path, desktop_size: Size) -> Image:
        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        num_tiles = [o // i + 1 for o, i in zip(out_img.size, in_img.size)]
        for x in range(num_tiles[0]):
            for y in range(num_tiles[1]):
                out_img.paste(
                    in_img,
                    (
                        in_img.size[0] * x,
                        in_img.size[1] * y,
                        in_img.size[0] * (x + 1),
                        in_img.size[1] * (y + 1),
                    ),
                )
        return out_img


class CenteredStrategy(FillAlgorithm):
    def make_background(self, img_file: Path, desktop_size: Size) -> Image:
        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        left = (out_img.size[0] - in_img.size[0]) // 2
        top = (out_img.size[1] - in_img.size[1]) // 2
        out_img.paste(
            in_img,
            (left, top, left + in_img.size[0], top + in_img.size[1]),
        )
        return out_img


class ScaledStrategy(FillAlgorithm):
    def make_background(self, img_file: Path, desktop_size: Size) -> Image:
        in_img = Image.open(img_file)
        out_img = in_img.resize(desktop_size)
        return out_img


class Resizer:
    def __init__(self, algorithm: FillAlgorithm) -> None:
        self.algorithm = algorithm

    def resize(self, image_file: Path, size: Size) -> Image:
        result = self.algorithm.make_background(image_file, size)
        return result


def main() -> None:
    image_file = Path.cwd() / "boat.png"
    tiled_desktop = Resizer(TiledStrategy())
    tiled_image = tiled_desktop.resize(image_file, (1920, 1080))
    tiled_image.show()

    centered_desktop = Resizer(CenteredStrategy())
    centered_image = centered_desktop.resize(image_file, (1920, 1080))
    centered_image.show()

    scaled_desktop = Resizer(ScaledStrategy())
    scaled_image = scaled_desktop.resize(image_file, (1920, 1080))
    scaled_image.show()


if __name__ == "__main__":
    main()
