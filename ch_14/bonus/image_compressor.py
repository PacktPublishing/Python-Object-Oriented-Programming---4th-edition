"""
Python 3 Object-Oriented Programming

Chapter 14.  Concurrency
"""
from concurrent import futures
from PIL import Image  # type: ignore [import]
from pathlib import Path
import time
from typing import Iterator, List, Iterable, Tuple, Optional, Type


# State design with flyweight objects.


class RLERun:
    """
    Two subclasses of RLERun for Replicated
    bytes and Literal bytes.
    """

    def __init__(self, buffer: bytes, start: int) -> None:
        self.buffer = buffer
        self.start = start
        self.end = start + 1

    @property
    def count(self) -> int:
        return self.end - self.start

    def byte_state(self, index: int) -> "RLERun":
        raise NotImplementedError

    def emit(self) -> bytes:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.start}: {self.end})"


class Replicate(RLERun):
    """
    All bytes in self.buffer[self.start:self.end] are equal.

    >>> source = bytes([42, 42, 43])
    >>> s = Replicate(source, 0)
    >>> s.byte_state(1) == s
    True
    >>> s.start
    0
    >>> s.end
    2
    >>> s.byte_state(2) == s
    False
    >>> s.emit()
    b'\\x81*'

    >>> source = bytes(129*[42])
    >>> t = Replicate(source, 0)
    >>> t.byte_state(127) == t
    True
    >>> t.byte_state(128) == t
    False
    >>> t.emit()
    b'\\xff*'

    """

    flag = 0x80  # Identical Bytes

    def byte_state(self, index: int) -> RLERun:
        if self.buffer[index] == self.buffer[self.end - 1] and index - self.start < 128:
            self.end = index + 1
            return self
        else:
            self.end = index
            return Literal(self.buffer, index)

    def emit(self) -> bytes:
        data = [(self.count - 1) | self.flag, self.buffer[self.start]]
        return bytes(data)


class Literal(RLERun):
    """
    All bytes in self.buffer[self.start:self.end]
    serially unequal. self.buffer[self.start] != self.buffer[self.start+1]

    >>> source = bytes([42, 43, 44, 44])
    >>> s = Literal(source, 0)
    >>> s.byte_state(1) == s
    True
    >>> s.byte_state(2) == s
    True
    >>> s.byte_state(3) == s
    False
    >>> s.emit()
    b'\\x01*+'

    """

    flag = 0x00  # Unique Bytes

    def byte_state(self, index: int) -> RLERun:
        if self.buffer[index] != self.buffer[self.end - 1]:
            if index - self.start < 128:
                self.end = index + 1
                return self
            else:
                self.end = index
                return Literal(self.buffer, index)
        else:
            self.end = index - 1
            change = Replicate(self.buffer, self.end)
            change.byte_state(index)
            return change

    def emit(self) -> bytes:
        return (
            bytes([(self.count - 1) | self.flag]) + self.buffer[self.start : self.end]
        )


def rle_compress(image_bytes: bytes) -> Iterator[RLERun]:
    """
    >>> row = bytes([42, 42, 42, 42, 43, 44, 45, 45, 45])
    >>> [b.emit() for b in rle_compress(row)]
    [b'\\x83*', b'\\x01+,', b'\\x82-']
    """
    state: RLERun = Literal(image_bytes, 0)
    for index in range(1, len(image_bytes)):
        next_state = state.byte_state(index)
        if next_state != state:
            if state.count != 0:
                yield state
            state = next_state
    yield state


def rle_row_compress(row_bytes: bytes) -> bytes:
    return b"".join(run.emit() for run in rle_compress(row_bytes))


def image_to_rle(image: Image, workers: Optional[futures.Executor] = None) -> bytes:
    if workers is None:
        workers = futures.ProcessPoolExecutor()
    b_w = image.convert("L")
    width, height = b_w.size
    image_bytes: bytes = bytes(b_w.getdata())
    row_slices = (slice(r * width, (r + 1) * width) for r in range(height))
    row_compressors = [
        workers.submit(rle_row_compress, image_bytes[s]) for s in row_slices
    ]
    return b"".join(c.result() for c in row_compressors)


def compress(
    image_path: Path,
    executor_type: Optional[Type[futures.Executor]] = None,
) -> Tuple[str, float]:
    if executor_type is None:
        executor_type = futures.ProcessPoolExecutor
    start = time.perf_counter()
    source_image = Image.open(image_path)
    with executor_type() as workers:
        compressed_image = image_to_rle(source_image, workers)
    target = image_path.with_suffix(".rle")
    target.write_bytes(compressed_image)
    end = time.perf_counter()
    return target.name, end - start


def rle_decompress(width: int, height: int, compressed: bytes) -> bytes:
    """
    >>> rle_decompress(9, 1, bytes([0x83, 42, 0x01, 43, 44, 0x82, 45]))
    b'****+,---'
    """
    image_bytes = bytearray(width * height)
    index = 0
    iter_compressed = iter(compressed)
    for h in iter_compressed:
        if h & Replicate.flag:
            # Replicate
            span = (h ^ Replicate.flag) + 1
            r = bytes([next(iter_compressed)] * span)
        else:
            # Literal
            span = h + 1
            r = bytes(next(iter_compressed) for _ in range(span))
        image_bytes[index : index + span] = r
        index = index + span
    return bytes(image_bytes)


def rle_to_image(width: int, height: int, source: bytes) -> Image:
    image_bytes = rle_decompress(width, height, source)
    image = Image.new("L", (width, height))
    image.putdata(image_bytes)
    return image


def ascii_art(image: Image) -> None:
    grayscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    # "1" == 1-bit pixels, black and white, stored with one pixel per byte
    # "L" == 8-bit pixels, black and white
    b_w = image.convert("L")
    # b_w.show()
    width, height = b_w.size
    if width > 256:
        h_ratio = height / width
        scaled_b_w = b_w.resize((256, int(256 * h_ratio)))
    else:
        scaled_b_w = b_w

    bytes = list(scaled_b_w.getdata())
    for r in range(scaled_b_w.height):
        gray_char = lambda b: int(len(grayscale) * (b / 256))
        gray = map(
            gray_char, scaled_b_w[r * scaled_b_w.width : (r + 1) * scaled_b_w.width]
        )
        text = "".join(grayscale[g] for g in gray)
        print(text)


def display(image_path: Path = Path.cwd() / "images" / "bricks.bmp") -> None:
    with Image.open(image_path) as image:
        print(f"********** {image_path.name} {image.size} **********")
        ascii_art(image)


def benchmark() -> None:
    for conversion_type in (
        futures.ProcessPoolExecutor,
        futures.ThreadPoolExecutor,
    ):
        for compression_type in (
            futures.ProcessPoolExecutor,
            futures.ThreadPoolExecutor,
        ):
            print("per image, compression, workload, time")
            start = time.perf_counter()
            with conversion_type() as conversion_workers:
                images = [
                    conversion_workers.submit(compress, image_path, compression_type)
                    for image_path in (Path.cwd() / "images").glob("*.bmp")
                ]
                done, not_done = futures.wait(images, return_when=futures.ALL_COMPLETED)
                end = time.perf_counter()
                print(
                    f"{conversion_type.__name__}, {compression_type.__name__}, "
                    f"{len(done)}, {end-start:.3f}"
                )
                for d in done:
                    name, duration = d.result()
                    print(f", , {name}, {duration:.3f}")


if __name__ == "__main__":
    benchmark()
