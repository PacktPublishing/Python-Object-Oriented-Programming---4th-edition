"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from threading import Thread


class InputReader(Thread):
    def run(self) -> None:
        self.line_of_text = input()


if __name__ == "__main__":
    print("Enter some text and press enter: ")
    thread = InputReader()
    # thread.start()  # Concurrent
    thread.run()  # Sequential

    count = result = 1
    while thread.is_alive():
        result = count * count
        count += 1

    print(f"calculated squares up to {count} * {count} = {result}")
    print(f"while you typed {thread.line_of_text!r}")
