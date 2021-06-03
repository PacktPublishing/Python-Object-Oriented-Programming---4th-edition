"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
import asyncio
import asyncio.exceptions
import json
from pathlib import Path
from typing import TextIO, Any
import pickle
import signal
import struct
import sys


TARGET: TextIO
LINE_COUNT = 0


def serialize(bytes_payload: bytes) -> str:
    object_payload = pickle.loads(bytes_payload)
    text_message = json.dumps(object_payload)
    TARGET.write(text_message)
    TARGET.write("\n")
    return text_message


if sys.version_info >= (3, 9):

    async def log_writer(bytes_payload: bytes) -> None:
        global LINE_COUNT
        LINE_COUNT += 1
        result = await asyncio.to_thread(serialize, bytes_payload)


else:

    async def log_writer(bytes_payload: bytes) -> None:
        """Python 3.8 version"""
        global LINE_COUNT
        LINE_COUNT += 1
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, serialize, bytes_payload)


SIZE_FORMAT = ">L"
SIZE_BYTES = struct.calcsize(SIZE_FORMAT)


async def log_catcher(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    count = 0
    client_socket = writer.get_extra_info("socket")
    size_header = await reader.read(SIZE_BYTES)
    while size_header:
        payload_size = struct.unpack(SIZE_FORMAT, size_header)
        bytes_payload = await reader.read(payload_size[0])
        await log_writer(bytes_payload)
        count += 1
        size_header = await reader.read(SIZE_BYTES)
    print(f"From {client_socket.getpeername()}: {count} lines")


server: asyncio.AbstractServer


async def main(host: str, port: int) -> None:
    global server
    server = await asyncio.start_server(
        log_catcher,
        host=host,
        port=port,
    )

    if sys.platform != "win32":
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)

    if server.sockets:
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")
    else:
        raise ValueError("Failed to create server")

    async with server:
        await server.serve_forever()


if sys.platform == "win32":
    from types import FrameType

    def close_server(signum: int, frame: FrameType) -> None:
        # print(f"Signal {signum}")
        server.close()

    signal.signal(signal.SIGINT, close_server)
    signal.signal(signal.SIGTERM, close_server)
    signal.signal(signal.SIGABRT, close_server)
    signal.signal(signal.SIGBREAK, close_server)


if __name__ == "__main__":
    # These often have command-line or environment overrides
    HOST, PORT = "localhost", 18842

    with Path("one.log").open("w") as TARGET:
        try:
            if sys.platform == "win32":
                # https://github.com/encode/httpx/issues/914
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main(HOST, PORT))
                loop.run_until_complete(asyncio.sleep(1))
                loop.close()
            else:
                asyncio.run(main(HOST, PORT))

        except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
            ending = {"lines_collected": LINE_COUNT}
            print(ending)
            TARGET.write(json.dumps(ending) + "\n")
