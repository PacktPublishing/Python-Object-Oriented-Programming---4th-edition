"""
Python 3 Object-Oriented Programming Case Study

Chapter 5, When to Use Object-Oriented Programming
"""
from pathlib import Path
from pytest import *  # type: ignore [import]
import archive_tweaker
import zipfile

@fixture
def zip_data(tmp_path):
    test_file = tmp_path/"test.zip"
    with zipfile.ZipFile(test_file, "w") as output:
        for i in range(3):
            path_md = Path(f"ch_{i}")/"docs"/f"ch_{i}.md"
            path_other = Path(f"ch_{i}")/"docs"/f"ch_{i}.other"
            output.writestr(str(path_md), "sample data with xyzzy in it\n")
            output.writestr(str(path_other), "sample data with xyzzy in it\n")
        output.write(Path("docs") / "IMG_3421.png", Path("ch_05") / "docs" / "IMG_3421.png")
    return test_file

def test_zip_replace(zip_data):
    zr = archive_tweaker.ZipReplace(zip_data, "*.md", "xyzzy", "plover's egg")
    zr.find_and_replace()

    with zipfile.ZipFile(zip_data) as result:
        member_data = {
            item.filename: result.read(item).rstrip() for item in result.infolist() if Path(item.filename).suffix != ".png"
        }

    assert member_data == {
        'ch_0/docs/ch_0.md': b"sample data with plover's egg in it",
        'ch_0/docs/ch_0.other': b'sample data with xyzzy in it',
        'ch_1/docs/ch_1.md': b"sample data with plover's egg in it",
        'ch_1/docs/ch_1.other': b'sample data with xyzzy in it',
        'ch_2/docs/ch_2.md': b"sample data with plover's egg in it",
        'ch_2/docs/ch_2.other': b'sample data with xyzzy in it',
    }


def test_text_tweaker(zip_data):
    tt = archive_tweaker.TextTweaker(zip_data)
    tt.find_and_replace("xyzzy", "plover's egg").process_files("*.md")

    with zipfile.ZipFile(zip_data) as result:
        member_data = {
            item.filename: result.read(item).rstrip() for item in result.infolist() if Path(item.filename).suffix != ".png"
        }

    assert member_data == {
        'ch_0/docs/ch_0.md': b"sample data with plover's egg in it",
        'ch_0/docs/ch_0.other': b'sample data with xyzzy in it',
        'ch_1/docs/ch_1.md': b"sample data with plover's egg in it",
        'ch_1/docs/ch_1.other': b'sample data with xyzzy in it',
        'ch_2/docs/ch_2.md': b"sample data with plover's egg in it",
        'ch_2/docs/ch_2.other': b'sample data with xyzzy in it',
    }

from PIL import Image
from io import BytesIO

def test_image_tweaker(zip_data):
    it = archive_tweaker.ImgTweaker(zip_data)
    it.process_files("*.png")

    with zipfile.ZipFile(zip_data) as result:
        member_data = {
            item.filename: Image.open(BytesIO(result.read(item))).size
            for item in result.infolist() if Path(item.filename).suffix == ".png"
        }


    assert member_data == {'ch_05/docs/IMG_3421.png': (640, 960)}
