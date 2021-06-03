"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from time import sleep
from subprocess import Popen
from os import kill
from signal import SIGTERM, SIGINT
from sys import argv


def child() -> None:
    print("Child Started")
    try:
        sleep(600)
    except Exception as ex:
        print(f"Child {ex}")
        raise


def parent() -> None:
    child_process = Popen(
        ["python", "src/demo_signals.py", "child"],
        shell=False,
    )
    print(f"Child: {child_process.poll()}")
    print(f"Child: {child_process.pid}")
    sleep(2)
    print(f"Signaling Child...")
    kill(child_process.pid, SIGINT)


if __name__ == "__main__":
    if len(argv) > 1:
        option = argv[1]
    else:
        option = "parent"
    print(option)
    function = {"parent": parent, "child": child}[option]
    function()
