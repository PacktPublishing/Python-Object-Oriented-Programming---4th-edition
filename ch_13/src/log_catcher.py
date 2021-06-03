"""
Python 3 Object-Oriented Programming

Chapter 13.  Testing Object-Oriented Programs.
"""
import json
from pathlib import Path
import socketserver
from typing import TextIO
import pickle
import struct
import sys


class LogDataCatcher(socketserver.BaseRequestHandler):
    log_file: TextIO
    count: int = 0
    size_format = ">L"
    size_bytes = struct.calcsize(size_format)

    def handle(self) -> None:
        size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
        while size_header_bytes:
            payload_size = struct.unpack(LogDataCatcher.size_format, size_header_bytes)
            print(f"{size_header_bytes=} {payload_size=}", file=sys.stderr)
            payload_bytes = self.request.recv(payload_size[0])
            print(f"{len(payload_bytes)=}", file=sys.stderr)
            payload = pickle.loads(payload_bytes)
            LogDataCatcher.count += 1
            print(f"{self.client_address[0]} {LogDataCatcher.count} {payload!r}")
            self.log_file.write(json.dumps(payload) + "\n")
            try:
                size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
            except (ConnectionResetError, BrokenPipeError):
                break


def main(host: str, port: int, target: Path) -> None:
    with target.open("w") as unified_log:
        LogDataCatcher.log_file = unified_log
        with socketserver.TCPServer((host, port), LogDataCatcher) as server:
            server.serve_forever()


if __name__ == "__main__":
    HOST, PORT = "localhost", 18842
    main(HOST, PORT, Path("one.log"))
