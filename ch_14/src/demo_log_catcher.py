"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from __future__ import annotations
import argparse
import signal
import subprocess
import time
import sys


def main(clients: int = 10) -> None:
    if sys.platform == "win32":
        platform_flags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        platform_flags = 0
    server = subprocess.Popen(
        ["python", "src/log_catcher.py"], creationflags=platform_flags
    )
    # Give the server 100 ms to get started.
    time.sleep(0.100)
    # Make sure it didn't crash because of an earlier test
    assert server.poll() is None, f"Server didn't start."
    workers = [
        subprocess.Popen(["python", "src/remote_logging_app.py"])
        for i in range(clients)
    ]
    print(f"***{clients} WORKERS STARTED***")
    for w in workers:
        w.wait()
        print(f"worker {w.pid} finished {w.returncode}")
    print(f"***{clients} WORKERS FINISHED***")
    # Give the server 100 ms to finish processing
    time.sleep(0.100)

    if sys.platform == "win32":
        server.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        server.terminate()
    server.wait()
    print(f"server finished {server.returncode}")


def get_options(argv: list[str] = sys.argv[1:]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("workers", nargs="?", type=int, default=1)
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()
    main(options.workers)
