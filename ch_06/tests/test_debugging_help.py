"""
Python 3 Object-Oriented Programming

Chapter 6, Abstract Base Classes and Operator Overloading
"""
from pytest import *  # type: ignore[import]
from debugging_help import DebuggingOnly

def test_happy_path(capfd):
    with DebuggingOnly():
        print("That worked")
        print("Quite well")

    print("Silence is golden")

    out, err = capfd.readouterr()
    assert out == "Silence is golden\n"

def test_exception_path(capfd):
    with raises(AssertionError) as ex:
        with DebuggingOnly():
            print("This is helpful")
            print("And this, too")
            assert False, "Because of this"

    out, err = capfd.readouterr()
    assert out == """--EX-->AssertionError('Because of this\\nassert False')
       This is helpful
       And this, too
"""
