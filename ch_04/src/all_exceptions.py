"""
Python 3 Object-Oriented Programming Case Study

Chapter 4, Expecting the Unexpected
"""


def exception_demo() -> None:

    some_exceptions = [ValueError, TypeError, IndexError, None]

    for choice in some_exceptions:
        try:
            print(f"\nRaising {choice}")
            if choice:
                raise choice("An error")
            else:
                print("no exception raised")
        except ValueError:
            print("Caught a ValueError")
        except TypeError:
            print("Caught a TypeError")
        except Exception as e:
            print(f"Caught some other error: {e.__class__.__name__}")
        else:
            print("This code called if there is no exception")
        finally:
            print("This cleanup code is always called")


test_exception_demo = """
>>> exception_demo()
<BLANKLINE>
Raising <class 'ValueError'>
Caught a ValueError
This cleanup code is always called
<BLANKLINE>
Raising <class 'TypeError'>
Caught a TypeError
This cleanup code is always called
<BLANKLINE>
Raising <class 'IndexError'>
Caught some other error: IndexError
This cleanup code is always called
<BLANKLINE>
Raising None
no exception raised
This code called if there is no exception
This cleanup code is always called

"""

__test__ = {name: case for name, case in globals().items() if name.startswith("test_")}


if __name__ == "__main__":
    exception_demo()
