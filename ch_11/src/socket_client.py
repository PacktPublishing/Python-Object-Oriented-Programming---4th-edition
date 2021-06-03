"""
Python 3 Object-Oriented Programming

Chapter 11. Common Design Patterns
"""
import gzip
import io
import socket


def main_zip() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 2401))
    count = input("How many rolls: ") or "1"
    pattern = input("Dice pattern nd6[dk+-]a: ") or "d6"
    command = f"Dice {count} {pattern}"
    server.send(command.encode("utf8"))
    zipped_response = io.BytesIO(server.recv(1024))
    with gzip.GzipFile(fileobj=zipped_response) as zipfile:
        response = zipfile.read()
    print(response.decode("utf-8"))
    server.close()


def main() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("localhost", 2401))
    count = input("How many rolls: ") or "1"
    pattern = input("Dice pattern nd6[dk+-]a: ") or "d6"
    command = f"Dice {count} {pattern}"
    server.send(command.encode("utf8"))
    response = server.recv(1024)
    print(response.decode("utf-8"))
    server.close()


if __name__ == "__main__":
    main_zip()
