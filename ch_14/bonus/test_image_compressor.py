"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from pathlib import Path
from PIL import Image
from pytest import *
from unittest.mock import AsyncMock, Mock, call
import image_compressor
import random

@fixture(params=[16, 32, 64, 128, 256, 384, 512])
def pattern(request):
    def diamond(width, height, h):
        if h < height//2:
            inset = int(((height//2-h) * (width//2))/(height//2))
        else:
            inset = int(((h-height//2) * (width//2))/(height//2))
        row = (
            [random.randint(0, int(i*255/inset)) for i in range(inset)]
            + [0xff for j in range(width-2*inset)]
            + [random.randint(0, int((inset-k)*255/inset)) for k in range(inset)]
        )
        return row
    width = height = request.param
    data = bytes(
        b
        for h in range(height)
        for b in diamond(width, height, h)
    )
    return width, height, data

def test_compress_decompress(pattern):
    width, height, data = pattern
    comp = b"".join(
        run.emit() for run in image_compressor.rle_compress(data)
    )
    decomp = image_compressor.rle_decompress(width, height, comp)
    assert decomp == data


def test_image_compress_decompress():
    bricks_path = Path.cwd() / "images" / "bricks.bmp"
    bricks_image = Image.open(bricks_path)
    width, height = bricks_image.size
    bricks_rle = image_compressor.image_to_rle(bricks_image)
    new_bricks_image = image_compressor.rle_to_image(width, height, bricks_rle)
    assert new_bricks_image.getdata() == new_bricks_image.getdata()
    assert len(bricks_rle) == 928
    assert len(bricks_image.getdata()) == 40_000
    assert len(new_bricks_image.getdata()) == 40_000
